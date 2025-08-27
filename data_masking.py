import re
import json
from typing import Dict, Any, Tuple

class DataMaskingEngine:
    """
    Engine for masking sensitive numerical data using unique identifiers.
    Maintains data integrity while ensuring privacy.
    """
    
    def __init__(self):
        # Track masked values for decryption
        self.masked_values = {}
        self.mask_counter = 0
    
    def mask_numerical_values(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Mask all numerical values in the text using unique identifiers.
        
        Args:
            text: Input text containing numerical values
            
        Returns:
            Tuple of (masked_text, masking_info)
        """
        # Use a single comprehensive pattern to avoid overlaps
        pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?|\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d+%'
        
        masking_info = {
            'masked_values': {},
            'total_masked': 0
        }
        
        # Find all matches
        matches = list(re.finditer(pattern, text))
        
        # Create a list of replacements to apply
        replacements = []
        for match in matches:
            original_value = match.group()
            # Create a unique identifier for this value
            masked_value = f"NUM_{self.mask_counter:06d}"
            
            # Store mapping for decryption
            mask_id = f"MASK_{self.mask_counter:06d}"
            self.masked_values[mask_id] = {
                'original': original_value,
                'masked': masked_value,
                'position': match.span()
            }
            
            masking_info['masked_values'][mask_id] = {
                'original': original_value,
                'masked': masked_value,
                'position': match.span()
            }
            
            replacements.append((match.start(), match.end(), masked_value))
            self.mask_counter += 1
        
        # Apply replacements in reverse order to avoid position shifting
        masked_text = text
        for start, end, masked_value in reversed(replacements):
            masked_text = masked_text[:start] + masked_value + masked_text[end:]
        
        masking_info['total_masked'] = len(masking_info['masked_values'])
        return masked_text, masking_info
    
    def decrypt_numerical_values(self, masked_text: str, masking_info: Dict[str, Any]) -> str:
        """
        Decrypt masked numerical values back to original values.
        
        Args:
            masked_text: Text with masked numerical values
            masking_info: Information about the masking process
            
        Returns:
            Decrypted text with original numerical values
        """
        decrypted_text = masked_text
        
        # Process in reverse order to avoid conflicts
        mask_ids = list(masking_info['masked_values'].keys())
        mask_ids.reverse()
        for mask_id in mask_ids:
            info = masking_info['masked_values'][mask_id]
            original_value = info['original']
            masked_value = info['masked']
            
            # Replace all occurrences of masked value with original
            decrypted_text = decrypted_text.replace(masked_value, original_value)
        
        return decrypted_text
    
    def get_masking_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all masked values.
        
        Returns:
            Dictionary containing masking summary
        """
        return {
            'total_masked_values': len(self.masked_values),
            'masked_values': self.masked_values
        }
    
    def save_masking_info(self, filepath: str):
        """
        Save masking information to a JSON file for later decryption.
        
        Args:
            filepath: Path to save the masking information
        """
        with open(filepath, 'w') as f:
            json.dump(self.get_masking_summary(), f, indent=2)
    
    def load_masking_info(self, filepath: str):
        """
        Load masking information from a JSON file.
        
        Args:
            filepath: Path to the masking information file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.masked_values = data['masked_values']
            self.mask_counter = len(self.masked_values)
