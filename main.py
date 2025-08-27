#!/usr/bin/env python3
"""
Asset Data Privacy - Main Application
Ensures privacy of sensitive financial data when processed by AI models.
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any, Tuple

from data_masking import DataMaskingEngine
from fund_obfuscator import FundNameObfuscator
from pdf_processor import PDFProcessor

class AssetDataPrivacy:
    """
    Main application for ensuring financial data privacy.
    Orchestrates data masking, fund obfuscation, and document processing.
    """
    
    def __init__(self, config_file: str = None):
        self.data_masking_engine = DataMaskingEngine()
        self.fund_obfuscator = FundNameObfuscator()
        self.pdf_processor = PDFProcessor()
        
        # Load configuration if provided
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        
        # Create output directory
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_document(self, pdf_path: str, save_masked: bool = True) -> Dict[str, Any]:
        """
        Process a PDF document: extract, mask, and prepare for AI processing.
        
        Args:
            pdf_path: Path to the PDF file
            save_masked: Whether to save masked text to file
            
        Returns:
            Dictionary containing processing results
        """
        print(f"Processing document: {pdf_path}")
        
        # Step 1: Extract text from PDF
        print("Extracting text from PDF...")
        extracted_text, pdf_metadata = self.pdf_processor.extract_text_from_pdf(pdf_path)
        
        # Step 2: Mask numerical values
        print("Masking numerical values...")
        masked_text, masking_info = self.data_masking_engine.mask_numerical_values(extracted_text)
        
        # Step 3: Obfuscate fund names
        print("Obfuscating fund names...")
        obfuscated_text, obfuscation_info = self.fund_obfuscator.obfuscate_fund_names(masked_text)
        
        # Step 4: Prepare processing summary
        processing_summary = {
            'input_file': pdf_path,
            'processing_timestamp': datetime.now().isoformat(),
            'pdf_metadata': pdf_metadata,
            'masking_info': masking_info,
            'obfuscation_info': obfuscation_info,
            'total_characters': len(extracted_text),
            'total_masked_values': masking_info['total_masked'],
            'total_obfuscated_funds': obfuscation_info['total_obfuscated']
        }
        
        # Step 5: Save masked text if requested
        if save_masked:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            masked_text_path = os.path.join(self.output_dir, f"{base_name}_masked.txt")
            self.pdf_processor.save_processed_text(obfuscated_text, masked_text_path)
            processing_summary['masked_text_file'] = masked_text_path
        
        # Step 6: Save processing information
        info_file_path = os.path.join(self.output_dir, f"{base_name}_processing_info.json")
        with open(info_file_path, 'w') as f:
            json.dump(processing_summary, f, indent=2)
        
        processing_summary['processing_info_file'] = info_file_path
        
        print(f"Document processed successfully!")
        print(f"  - Total masked values: {masking_info['total_masked']}")
        print(f"  - Total obfuscated funds: {obfuscation_info['total_obfuscated']}")
        print(f"  - Masked text saved to: {masked_text_path if save_masked else 'Not saved'}")
        print(f"  - Processing info saved to: {info_file_path}")
        
        return processing_summary
    
    def decrypt_results(self, masked_text: str, processing_info_file: str) -> str:
        """
        Decrypt masked results back to original sensitive data.
        
        Args:
            masked_text: Text with masked values
            processing_info_file: Path to the processing information file
            
        Returns:
            Decrypted text with original values
        """
        print("Decrypting results...")
        
        # Load processing information
        with open(processing_info_file, 'r') as f:
            processing_info = json.load(f)
        
        # Step 1: Deobfuscate fund names
        print("Deobfuscating fund names...")
        deobfuscated_text = self.fund_obfuscator.deobfuscate_fund_names(
            masked_text, 
            processing_info['obfuscation_info']
        )
        
        # Step 2: Decrypt numerical values
        print("Decrypting numerical values...")
        decrypted_text = self.data_masking_engine.decrypt_numerical_values(
            deobfuscated_text, 
            processing_info['masking_info']
        )
        
        print("Results decrypted successfully!")
        return decrypted_text
    
    def save_decrypted_results(self, decrypted_text: str, output_path: str):
        """
        Save decrypted results to a file.
        
        Args:
            decrypted_text: Decrypted text content
            output_path: Path to save the decrypted text
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
        
        print(f"Decrypted results saved to: {output_path}")
    
    def load_config(self, config_file: str):
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Load custom fund names if specified
            if 'fund_names_file' in config:
                self.fund_obfuscator.load_fund_names(config['fund_names_file'])
            
            print(f"Configuration loaded from: {config_file}")
            
        except Exception as e:
            print(f"Warning: Could not load configuration from {config_file}: {e}")
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current processing state.
        
        Returns:
            Dictionary containing processing summary
        """
        return {
            'data_masking_summary': self.data_masking_engine.get_masking_summary(),
            'fund_obfuscation_summary': self.fund_obfuscator.get_obfuscation_summary()
        }

def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Asset Data Privacy - Ensure financial data privacy for AI processing"
    )
    
    parser.add_argument(
        'input_pdf', 
        help='Path to the input PDF file'
    )
    
    parser.add_argument(
        '--output-dir', 
        default='output',
        help='Output directory for processed files (default: output)'
    )
    
    parser.add_argument(
        '--config', 
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--no-save-masked', 
        action='store_true',
        help='Do not save masked text to file'
    )
    
    parser.add_argument(
        '--decrypt', 
        help='Path to processing info file for decryption'
    )
    
    parser.add_argument(
        '--masked-text', 
        help='Path to masked text file for decryption'
    )
    
    args = parser.parse_args()
    
    # Initialize the application
    app = AssetDataPrivacy(config_file=args.config)
    
    if args.decrypt and args.masked_text:
        # Decryption mode
        print("Running in decryption mode...")
        
        # Read masked text
        with open(args.masked_text, 'r', encoding='utf-8') as f:
            masked_text = f.read()
        
        # Decrypt
        decrypted_text = app.decrypt_results(masked_text, args.decrypt)
        
        # Save decrypted results
        base_name = os.path.splitext(os.path.basename(args.masked_text))[0]
        decrypted_path = os.path.join(args.output_dir, f"{base_name}_decrypted.txt")
        app.save_decrypted_results(decrypted_text, decrypted_path)
        
    else:
        # Processing mode
        print("Running in processing mode...")
        
        # Process the document
        processing_summary = app.process_document(
            args.input_pdf, 
            save_masked=not args.no_save_masked
        )
        
        print("\nProcessing completed successfully!")
        print(f"Output directory: {args.output_dir}")

if __name__ == "__main__":
    main()
