#!/usr/bin/env python3
"""
Asset Data Privacy - Web Frontend
Flask application with OpenAI integration and tabular output display.
"""

import os
import json
import tempfile
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import openai
from data_masking import DataMaskingEngine
from fund_obfuscator import FundNameObfuscator
from pdf_processor import PDFProcessor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# OpenAI configuration
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Initialize components
data_masking_engine = DataMaskingEngine()
fund_obfuscator = FundNameObfuscator()
pdf_processor = PDFProcessor()

# Create upload and output directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Main page with file upload and configuration."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Process the document
        result = process_document(filepath)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_document(filepath):
    """Process a PDF document through the privacy system."""
    try:
        # Extract text from PDF
        extracted_text, pdf_metadata = pdf_processor.extract_text_from_pdf(filepath)
        
        # Mask numerical values
        masked_text, masking_info = data_masking_engine.mask_numerical_values(extracted_text)
        
        # Obfuscate fund names
        obfuscated_text, obfuscation_info = fund_obfuscator.obfuscate_fund_names(masked_text)
        
        # Create processing summary
        processing_summary = {
            'input_file': os.path.basename(filepath),
            'processing_timestamp': datetime.now().isoformat(),
            'pdf_metadata': pdf_metadata,
            'masking_info': masking_info,
            'obfuscation_info': obfuscation_info,
            'total_characters': len(extracted_text),
            'total_masked_values': masking_info['total_masked'],
            'total_obfuscated_funds': obfuscation_info['total_obfuscated'],
            'original_text': extracted_text,
            'masked_text': obfuscated_text
        }
        
        # Save processing information
        info_filename = f"processing_info_{uuid.uuid4().hex[:8]}.json"
        info_filepath = os.path.join(OUTPUT_FOLDER, info_filename)
        
        # Ensure all data is JSON serializable
        serializable_summary = json.loads(json.dumps(processing_summary, default=str))
        
        with open(info_filepath, 'w') as f:
            json.dump(serializable_summary, f, indent=2)
        
        serializable_summary['processing_info_file'] = info_filename
        
        return serializable_summary
        
    except Exception as e:
        raise Exception(f"Error processing document: {str(e)}")

@app.route('/decrypt', methods=['POST'])
def decrypt_results():
    """Decrypt masked results back to original data."""
    try:
        data = request.get_json()
        masked_text = data.get('masked_text')
        processing_info = data.get('processing_info')
        
        if not masked_text or not processing_info:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Deobfuscate fund names first
        deobfuscated_text = fund_obfuscator.deobfuscate_fund_names(
            masked_text, 
            processing_info['obfuscation_info']
        )
        
        # Decrypt numerical values
        decrypted_text = data_masking_engine.decrypt_numerical_values(
            deobfuscated_text, 
            processing_info['masking_info']
        )
        
        return jsonify({
            'decrypted_text': decrypted_text,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/openai_process', methods=['POST'])
def openai_process():
    """Process masked text with OpenAI API."""
    try:
        if not OPENAI_API_KEY:
            return jsonify({'error': 'OpenAI API key not configured'}), 400
        
        data = request.get_json()
        masked_text = data.get('masked_text')
        prompt = data.get('prompt', 'Please analyze this financial document and provide insights.')
        
        if not masked_text:
            return jsonify({'error': 'Missing masked text'}), 400
        
        # Prepare the prompt for OpenAI
        full_prompt = f"""
{prompt}

## Objective
Extract comprehensive asset-level investment data from PDF documents (such as investment reports, portfolio statements, fund documents, or financial statements) and organize into a standardized tabular format.

## Output Format Requirements
- **Single table format** with each asset as a separate row
- **Exact column headers** (maintain spelling and order):
  1. Name
  2. Invested Capital
  3. Current Cost
  4. Fair Market Value
  5. Date of Investment
  6. Gross IRR
  7. Net IRR
  8. Gross MOIC
  9. Net MOIC
  10. EBITDA
  11. Net Debt
  12. Total Debt
  13. City
  14. State
  15. Country
  16. Continent
  17. Business Description
  18. GICS Sector

## Data Extraction Guidelines

### 1. Asset Identification
- Each investment, holding, portfolio company, or asset mentioned should be a separate row
- Include all types of investments: equity, debt, real estate, funds, securities, etc.
- Do NOT aggregate or combine multiple assets into single rows

### 2. Field-Specific Instructions

#### **Name**
- Use the most complete company/asset name available
- Include legal entity suffixes (LLC, Inc., Ltd., etc.) if present
- If multiple names exist, use the primary/most formal version
- Examples: "ABC Manufacturing LLC", "XYZ Technology Inc."

#### **Financial Metrics** (Invested Capital, Current Cost, Fair Market Value)
- Extract exact numerical values with currency if specified
- Look for terms like: "Investment Cost", "Book Value", "Market Value", "NAV", "Valuation"
- Include currency symbol/code (USD, EUR, GBP, etc.)
- Format: "$10,500,000" or "€5.2M" or "10.5 (millions)"

#### **Date of Investment**
- Look for: "Investment Date", "Acquisition Date", "Initial Investment", "Purchase Date"
- Format as MM/DD/YYYY, DD/MM/YYYY, or YYYY-MM-DD based on source format
- If only year/quarter available, use that format

#### **Performance Metrics** (IRR and MOIC)
- **IRR**: Look for "Internal Rate of Return", "IRR", percentage returns
- **MOIC**: Look for "Multiple of Invested Capital", "Money Multiple", "Cash Multiple"
- Specify Gross vs Net when clearly indicated
- Format IRR as percentages: "15.2%" or "0.152"
- Format MOIC as multiples: "2.3x" or "2.30"

#### **Financial Position** (EBITDA, Debt)
- **EBITDA**: "Earnings Before Interest, Tax, Depreciation, Amortization"
- **Net Debt**: Total debt minus cash/cash equivalents
- **Total Debt**: All interest-bearing obligations
- Include trailing twelve months (TTM) or latest available period

#### **Location Fields**
- **City**: Headquarters or primary operating location
- **State/Province**: Include for US, Canada, Australia, etc.
- **Country**: Full country name (not abbreviations)
- **Continent**: North America, South America, Europe, Asia, Africa, Oceania
- Research/infer continent from country if not explicitly stated

#### **Business Description**
- Extract complete business descriptions, operations summary, or industry focus
- Include key products/services, market position, business model
- Maximum 2-3 sentences, maintain original language when possible

#### **GICS Sector**
- Look for Global Industry Classification Standard sectors
- Common sectors: Technology, Healthcare, Financials, Consumer Discretionary, etc.
- If not explicitly stated, leave blank (do not infer)

### 3. Data Quality Standards

#### **Missing Data Protocol**
- Use **blank cells** (not "N/A", "NULL", or "-") for missing information
- Do not estimate or calculate missing values
- Do not combine related fields to fill missing data

#### **Data Consistency**
- Maintain consistent formatting within each column
- Preserve original units and currency notations
- Use consistent date formats throughout

#### **Validation Rules**
- Each asset must have at minimum a Name
- Financial figures should maintain original precision
- Dates should be chronologically reasonable
- Location data should be geographically accurate

## Special Extraction Scenarios

### Portfolio Summary Tables
- Extract individual assets, not portfolio totals
- Skip aggregate rows, subtotals, or summary statistics

### Multi-Page Documents
- Scan entire document for asset information
- Assets may be split across multiple sections/pages
- Check appendices, footnotes, and detailed schedules

### Different Document Types
- **Fund Reports**: Focus on underlying investments
- **Financial Statements**: Look for investment schedules, fair value tables
- **Pitch Books**: Extract portfolio company details
- **Quarterly Reports**: Prioritize most recent asset values

### Currency and Units
- Preserve original currency designations
- Note if figures are in thousands/millions (maintain original notation)
- Include any footnotes about currency conversion dates

## Quality Assurance Checklist

Before finalizing the table, verify:
- [ ] Each row represents a unique asset/investment
- [ ] No duplicate entries for the same asset
- [ ] All 18 columns are present with exact headers
- [ ] Blank cells used for missing data (not placeholder text)
- [ ] Financial figures include appropriate units/currency
- [ ] Dates are in consistent format
- [ ] Geographic data is accurate and complete where available
- [ ] Business descriptions are concise but informative

## Example Output Structure

| Name | Invested Capital | Current Cost | Fair Market Value | Date of Investment | Gross IRR | Net IRR | Gross MOIC | Net MOIC | EBITDA | Net Debt | Total Debt | City | State | Country | Continent | Business Description | GICS Sector |
|------|-----------------|--------------|-------------------|-------------------|-----------|---------|------------|----------|---------|----------|------------|------|-------|---------|-----------|---------------------|-------------|
| TechCorp Inc. | $50,000,000 | $52,000,000 | $75,000,000 | 03/15/2020 | 18.5% | 15.2% | 1.5x | 1.44x | $12,500,000 | $25,000,000 | $30,000,000 | Austin | Texas | United States | North America | Leading software solutions provider for enterprise customers | Information Technology |
| MedDevice LLC | €25,000,000 | | €35,000,000 | 2019-Q2 | | 22.1% | | 1.4x | | | | Berlin | | Germany | Europe | Medical device manufacturer specializing in diagnostic equipment | Health Care |

Remember: Accuracy and completeness are paramount. When in doubt, leave fields blank rather than making assumptions.

**Document Content to Analyze:**
{masked_text}
"""
        
        # Call OpenAI API
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",  # Upgraded to GPT-4o for 30K TPM limit
            messages=[
                {"role": "system", "content": "You are a senior financial data extraction specialist with expertise in portfolio analysis, corporate finance, and investment research. Your task is to extract comprehensive asset-level investment data from financial documents and present it in a standardized tabular format with exactly 18 columns. Follow the detailed extraction guidelines precisely, ensuring data quality and accuracy. Present only the data table with no additional commentary."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=4000,  # Increased for comprehensive analysis
            temperature=0.2    # More focused and consistent
        )
        
        # Get the AI response from the correct structure
        if response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            ai_response = choice.message.content
        else:
            raise Exception("No response choices from OpenAI")
        
        return jsonify({
            'ai_response': ai_response,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download processing information files."""
    try:
        return send_file(
            os.path.join(OUTPUT_FOLDER, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration status."""
    return jsonify({
        'openai_configured': bool(OPENAI_API_KEY),
        'server_port': 5001,
        'max_file_size': '16MB'
    })

@app.route('/api/fund_names', methods=['GET', 'POST', 'DELETE'])
def manage_fund_names():
    """Manage fund names for obfuscation."""
    try:
        if request.method == 'GET':
            return jsonify({
                'fund_names': fund_obfuscator.master_fund_names,
                'placeholder_mapping': fund_obfuscator.placeholder_mapping
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            fund_name = data.get('fund_name')
            if fund_name:
                fund_obfuscator.add_fund_name(fund_name)
                return jsonify({'success': True, 'message': f'Added fund: {fund_name}'})
            return jsonify({'error': 'Fund name required'}), 400
        
        elif request.method == 'DELETE':
            data = request.get_json()
            fund_name = data.get('fund_name')
            if fund_name:
                fund_obfuscator.remove_fund_name(fund_name)
                return jsonify({'success': True, 'message': f'Removed fund: {fund_name}'})
            return jsonify({'error': 'Fund name required'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

# For Render deployment
app.config['SERVER_NAME'] = None
