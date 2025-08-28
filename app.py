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

**COMPREHENSIVE FINANCIAL DOCUMENT ANALYSIS:**

Document Content:
{masked_text}

**ANALYSIS REQUIREMENTS:**
1. **Portfolio Overview**: Extract comprehensive asset allocation and fund composition
2. **Performance Analysis**: Identify all performance metrics, returns, and benchmarks  
3. **Risk Assessment**: Analyze risk measures, volatility, and correlation data
4. **Strategic Insights**: Provide actionable insights based on the full document context
5. **Data Completeness**: Ensure no significant information is overlooked

**REQUIRED OUTPUT FORMAT:**

**1. EXECUTIVE SUMMARY TABLE:**
| Metric | Value | Details |
|--------|-------|---------|
| Total Portfolio Value | [Value] | [Context] |
| Number of Assets | [Count] | [Breakdown] |
| Risk Profile | [Level] | [Justification] |

**2. ASSET ALLOCATION TABLE:**
| Asset/Fund Name | Allocation % | Current Value | Performance | Risk Level | Key Details |
|-----------------|--------------|---------------|-------------|------------|-------------|
| [Asset1] | [%] | [$] | [%] | [Level] | [Details] |
| [Asset2] | [%] | [$] | [%] | [Level] | [Details] |

**3. PERFORMANCE ANALYSIS:**
| Time Period | Portfolio Return | Benchmark | Outperformance | Key Drivers |
|-------------|------------------|-----------|----------------|-------------|
| [Period] | [%] | [%] | [%] | [Factors] |

**IMPORTANT INSTRUCTIONS:**
- Use the ENTIRE document context for comprehensive analysis
- Extract ALL numerical values, percentages, and financial metrics
- Provide professional-grade insights suitable for senior management
- Ensure data accuracy and completeness across all sections
- Present findings in clear, actionable format

Please provide a thorough, professional analysis using the complete document context.
"""
        
        # Call OpenAI API
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior financial analyst with expertise in portfolio management and risk analysis. Your task is to extract comprehensive investment portfolio data and present it in professional, structured tabular format. Analyze the entire document context to provide thorough insights."},
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
