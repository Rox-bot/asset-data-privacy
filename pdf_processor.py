import PyPDF2
import fitz  # PyMuPDF
from typing import Dict, Any, Tuple, Optional
import os

class PDFProcessor:
    """
    Processor for handling PDF documents.
    Extracts text and maintains document structure for AI processing.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        try:
            # Try PyMuPDF first (better text extraction)
            text, metadata = self._extract_with_pymupdf(pdf_path)
        except ImportError:
            # Fallback to PyPDF2
            text, metadata = self._extract_with_pypdf2(pdf_path)
        
        return text, metadata
    
    def _extract_with_pymupdf(self, pdf_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text using PyMuPDF (fitz).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            pages_info = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                text += page_text + "\n\n"
                
                pages_info.append({
                    'page_number': page_num + 1,
                    'text_length': len(page_text),
                    'bbox': {
                        'x0': page.rect.x0,
                        'y0': page.rect.y0,
                        'x1': page.rect.x1,
                        'y1': page.rect.y1,
                        'width': page.rect.width,
                        'height': page.rect.height
                    }
                })
            
            metadata = {
                'extraction_method': 'PyMuPDF',
                'total_pages': len(doc),
                'pages_info': pages_info,
                'file_size': os.path.getsize(pdf_path),
                'file_path': pdf_path
            }
            
            doc.close()
            return text.strip(), metadata
            
        except ImportError:
            raise ImportError("PyMuPDF not available. Install with: pip install PyMuPDF")
    
    def _extract_with_pypdf2(self, pdf_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text using PyPDF2 (fallback method).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                text = ""
                pages_info = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += page_text + "\n\n"
                    
                    pages_info.append({
                        'page_number': page_num + 1,
                        'text_length': len(page_text)
                    })
                
                metadata = {
                    'extraction_method': 'PyPDF2',
                    'total_pages': len(pdf_reader.pages),
                    'pages_info': pages_info,
                    'file_size': os.path.getsize(pdf_path),
                    'file_path': pdf_path
                }
                
                return text.strip(), metadata
                
        except ImportError:
            raise ImportError("PyPDF2 not available. Install with: pip install PyPDF2")
    
    def save_processed_text(self, text: str, output_path: str):
        """
        Save processed text to a file.
        
        Args:
            text: Text content to save
            output_path: Path to save the text file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def get_document_summary(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get a summary of the PDF document without extracting full text.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing document summary
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            summary = {
                'file_path': pdf_path,
                'file_size': os.path.getsize(pdf_path),
                'total_pages': len(doc),
                'file_type': 'PDF'
            }
            doc.close()
            return summary
        except ImportError:
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    summary = {
                        'file_path': pdf_path,
                        'file_size': os.path.getsize(pdf_path),
                        'total_pages': len(pdf_reader.pages),
                        'file_type': 'PDF'
                    }
                    return summary
            except ImportError:
                raise ImportError("Neither PyMuPDF nor PyPDF2 available")
    
    def validate_pdf(self, pdf_path: str) -> bool:
        """
        Validate that a file is a valid PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if valid PDF, False otherwise
        """
        if not os.path.exists(pdf_path):
            return False
        
        if not pdf_path.lower().endswith('.pdf'):
            return False
        
        try:
            # Try to open with PyMuPDF
            doc = fitz.open(pdf_path)
            doc.close()
            return True
        except:
            try:
                # Try to open with PyPDF2
                with open(pdf_path, 'rb') as file:
                    PyPDF2.PdfReader(file)
                return True
            except:
                return False
