# Asset Data Privacy

A comprehensive solution for ensuring the privacy of sensitive financial data when it is processed by AI models. This system provides data masking, fund name obfuscation, and secure decryption capabilities.

## Features

### 🔒 Data Masking for Numerical Values
- **Fixed Digit Mapping**: Replaces each digit with another fixed digit (e.g., 1→5, 2→7, etc.)
- **Multiple Formats**: Handles currency amounts, percentages, integers, and comma-separated numbers
- **Data Integrity**: Preserves data structure while ensuring privacy

### 🏦 Master Fund Name Obfuscation
- **Configurable Fund List**: Maintains a list of known master fund names
- **Placeholder Replacement**: Replaces fund names with generic placeholders (e.g., Fund001, Fund002)
- **Case-Insensitive**: Handles variations in fund name formatting

### 📄 PDF Document Processing
- **Text Extraction**: Extracts text from PDF documents using PyMuPDF (with PyPDF2 fallback)
- **Metadata Preservation**: Maintains document structure and metadata
- **Format Validation**: Ensures input files are valid PDFs

### 🔓 Secure Decryption
- **Reversible Process**: All masking and obfuscation can be reversed
- **Processing Information**: Stores encryption keys and mappings securely
- **Result Recovery**: Provides original sensitive data after AI processing

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Asset-Data-Privacy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python3 main.py --help
   ```

## Usage

### Basic Document Processing

Process a PDF document to mask sensitive data:

```bash
python3 main.py input_document.pdf
```

This will:
- Extract text from the PDF
- Mask all numerical values using fixed digit mapping
- Obfuscate fund names with placeholders
- Save masked text and processing information to the `output/` directory

### Advanced Processing

```bash
python3 main.py input_document.pdf \
    --output-dir custom_output \
    --config config.json \
    --no-save-masked
```

### Decryption

After AI processing, decrypt the results:

```bash
python3 main.py \
    --decrypt output/document_processing_info.json \
    --masked-text output/document_masked.txt
```

## Configuration

### Custom Fund Names

Create a custom fund names file (`custom_fund_names.json`):

```json
{
  "master_fund_names": [
    "Your Fund Name 1",
    "Your Fund Name 2",
    "Another Fund Name"
  ]
}
```

### Configuration File

Create a configuration file (`config.json`):

```json
{
  "fund_names_file": "custom_fund_names.json",
  "output_directory": "output",
  "save_intermediate_files": true,
  "log_level": "INFO"
}
```

## File Structure

```
Asset-Data-Privacy/
├── main.py                      # Main application
├── data_masking.py             # Numerical value masking engine
├── fund_obfuscator.py          # Fund name obfuscation
├── pdf_processor.py            # PDF document processing
├── requirements.txt             # Python dependencies
├── config_example.json         # Example configuration
├── custom_fund_names_example.json  # Example fund names
├── README.md                   # This file
└── output/                     # Output directory (created automatically)
```

## How It Works

### 1. Document Processing
```
PDF Input → Text Extraction → Numerical Masking → Fund Obfuscation → AI-Ready Output
```

### 2. Data Masking
- **Original**: $1,250,000 invested in MasterFund1
- **Masked**: $5,750,000 invested in Fund001

### 3. AI Processing
The masked document is sent to the AI model, which processes it without exposure to sensitive data.

### 4. Decryption
```
AI Output → Fund Deobfuscation → Numerical Decryption → Original Data
```

## Security Features

- **Fixed Mapping**: Consistent digit replacement ensures data integrity
- **No Encryption Keys**: Uses deterministic mapping for reliable decryption
- **Audit Trail**: Complete processing information stored for verification
- **Isolated Processing**: Sensitive data never leaves the local system

## Examples

### Input Document
```
Investment Summary:
- Total Capital: $5,000,000
- MasterFund1 Allocation: $2,500,000 (50%)
- MasterFund2 Allocation: $1,500,000 (30%)
- Cash Reserve: $1,000,000 (20%)
```

### Masked Output
```
Investment Summary:
- Total Capital: $1,000,000
- Fund001 Allocation: $7,500,000 (50%)
- Fund002 Allocation: $5,500,000 (30%)
- Cash Reserve: $5,000,000 (20%)
```

### Decrypted Results
```
Investment Summary:
- Total Capital: $5,000,000
- MasterFund1 Allocation: $2,500,000 (50%)
- MasterFund2 Allocation: $1,500,000 (30%)
- Cash Reserve: $1,000,000 (20%)
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `input_pdf` | Path to the input PDF file |
| `--output-dir` | Output directory (default: output) |
| `--config` | Path to configuration file |
| `--no-save-masked` | Do not save masked text to file |
| `--decrypt` | Path to processing info file for decryption |
| `--masked-text` | Path to masked text file for decryption |

## Dependencies

- **PyMuPDF**: Primary PDF processing (recommended)
- **PyPDF2**: Fallback PDF processing
- **typing-extensions**: Type hinting support

## Troubleshooting

### Common Issues

1. **PDF Extraction Errors**: Ensure the PDF is not password-protected or corrupted
2. **Import Errors**: Install dependencies with `pip install -r requirements.txt`
3. **Permission Errors**: Check file permissions and output directory access

### Performance Tips

- Use PyMuPDF for better text extraction quality
- Process large documents in batches
- Monitor output directory size for large-scale processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Open an issue on GitHub

---

**Note**: This system is designed for local processing to ensure data privacy. Sensitive financial data should never be transmitted over unsecured networks or stored in unsecured locations.
