import re
import json
from typing import Dict, List, Tuple, Any

class FundNameObfuscator:
    """
    Obfuscator for master fund names to ensure privacy.
    Maintains a list of known fund names and replaces them with placeholders.
    """
    
    def __init__(self, fund_names_file: str = None):
        # Default list of master fund names
        self.default_fund_names = [
            "MasterFund1", "MasterFund2", "MasterFund3", "MasterFund4", "MasterFund5",
            "AlphaFund", "BetaFund", "GammaFund", "DeltaFund", "OmegaFund",
            "StrategicFund", "GrowthFund", "ValueFund", "IncomeFund", "BalancedFund",
            "GlobalFund", "RegionalFund", "SectorFund", "IndexFund", "HedgeFund"
        ]
        
        # Load custom fund names if provided
        self.master_fund_names = self.default_fund_names.copy()
        if fund_names_file:
            self.load_fund_names(fund_names_file)
        
        # Generate placeholder mapping
        self.placeholder_mapping = {}
        self._generate_placeholders()
        
        # Track obfuscated names for decryption
        self.obfuscated_funds = {}
        self.obfuscation_counter = 0
    
    def _generate_placeholders(self):
        """Generate placeholder names for each master fund."""
        for i, fund_name in enumerate(self.master_fund_names):
            placeholder = f"Fund{i+1:03d}"
            self.placeholder_mapping[fund_name] = placeholder
    
    def add_fund_name(self, fund_name: str):
        """
        Add a new master fund name to the list.
        
        Args:
            fund_name: Name of the fund to add
        """
        if fund_name not in self.master_fund_names:
            self.master_fund_names.append(fund_name)
            placeholder = f"Fund{len(self.master_fund_names):03d}"
            self.placeholder_mapping[fund_name] = placeholder
    
    def remove_fund_name(self, fund_name: str):
        """
        Remove a master fund name from the list.
        
        Args:
            fund_name: Name of the fund to remove
        """
        if fund_name in self.master_fund_names:
            self.master_fund_names.remove(fund_name)
            del self.placeholder_mapping[fund_name]
            # Regenerate placeholders to maintain consistency
            self._generate_placeholders()
    
    def obfuscate_fund_names(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Obfuscate all master fund names in the text.
        
        Args:
            text: Input text containing fund names
            
        Returns:
            Tuple of (obfuscated_text, obfuscation_info)
        """
        obfuscated_text = text
        obfuscation_info = {
            'master_fund_names': self.master_fund_names,
            'placeholder_mapping': self.placeholder_mapping,
            'obfuscated_funds': {},
            'total_obfuscated': 0
        }
        
        # Create regex pattern for all fund names
        fund_pattern = r'\b(' + '|'.join(re.escape(name) for name in self.master_fund_names) + r')\b'
        
        matches = re.finditer(fund_pattern, text, re.IGNORECASE)
        for match in matches:
            original_name = match.group()
            placeholder = self.placeholder_mapping[original_name]
            
            # Store mapping for decryption
            obfuscation_id = f"FUND_{self.obfuscation_counter:06d}"
            self.obfuscated_funds[obfuscation_id] = {
                'original': original_name,
                'placeholder': placeholder,
                'position': match.span()
            }
            
            obfuscation_info['obfuscated_funds'][obfuscation_id] = {
                'original': original_name,
                'placeholder': placeholder,
                'position': match.span()
            }
            
            # Replace in text (case-insensitive)
            obfuscated_text = re.sub(
                re.escape(original_name), 
                placeholder, 
                obfuscated_text, 
                flags=re.IGNORECASE,
                count=1
            )
            
            self.obfuscation_counter += 1
        
        obfuscation_info['total_obfuscated'] = len(obfuscation_info['obfuscated_funds'])
        return obfuscated_text, obfuscation_info
    
    def deobfuscate_fund_names(self, obfuscated_text: str, obfuscation_info: Dict[str, Any]) -> str:
        """
        Deobfuscate fund names back to original names.
        
        Args:
            obfuscated_text: Text with obfuscated fund names
            obfuscation_info: Information about the obfuscation process
            
        Returns:
            Deobfuscated text with original fund names
        """
        deobfuscated_text = obfuscated_text
        
        for obfuscation_id, info in obfuscation_info['obfuscated_funds'].items():
            original_name = info['original']
            placeholder = info['placeholder']
            
            # Replace placeholder with original name
            deobfuscated_text = deobfuscated_text.replace(placeholder, original_name)
        
        return deobfuscated_text
    
    def get_obfuscation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all obfuscated fund names.
        
        Returns:
            Dictionary containing obfuscation summary
        """
        return {
            'total_obfuscated_funds': len(self.obfuscated_funds),
            'master_fund_names': self.master_fund_names,
            'placeholder_mapping': self.placeholder_mapping,
            'obfuscated_funds': self.obfuscated_funds
        }
    
    def save_fund_names(self, filepath: str):
        """
        Save the list of master fund names to a JSON file.
        
        Args:
            filepath: Path to save the fund names
        """
        data = {
            'master_fund_names': self.master_fund_names,
            'placeholder_mapping': self.placeholder_mapping
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_fund_names(self, filepath: str):
        """
        Load master fund names from a JSON file.
        
        Args:
            filepath: Path to the fund names file
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.master_fund_names = data.get('master_fund_names', self.default_fund_names)
                self.placeholder_mapping = data.get('placeholder_mapping', {})
                # Regenerate placeholders if not present
                if not self.placeholder_mapping:
                    self._generate_placeholders()
        except FileNotFoundError:
            print(f"Fund names file {filepath} not found. Using default names.")
        except json.JSONDecodeError:
            print(f"Invalid JSON in fund names file {filepath}. Using default names.")
    
    def save_obfuscation_info(self, filepath: str):
        """
        Save obfuscation information to a JSON file for later deobfuscation.
        
        Args:
            filepath: Path to save the obfuscation information
        """
        with open(filepath, 'w') as f:
            json.dump(self.get_obfuscation_summary(), f, indent=2)
    
    def load_obfuscation_info(self, filepath: str):
        """
        Load obfuscation information from a JSON file.
        
        Args:
            filepath: Path to the obfuscation information file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.obfuscated_funds = data['obfuscated_funds']
            self.obfuscation_counter = len(self.obfuscated_funds)
