#!/usr/bin/env python3
"""
Test script for Asset Data Privacy system.
Demonstrates the functionality with sample financial data.
"""

import json
import tempfile
import os
from data_masking import DataMaskingEngine
from fund_obfuscator import FundNameObfuscator

def test_data_masking():
    """Test the data masking functionality."""
    print("🔒 Testing Data Masking Engine...")
    
    # Sample financial text
    sample_text = """
    Investment Portfolio Summary:
    - Total Assets: $15,750,000
    - Cash Position: $2,500,000 (15.9%)
    - Fixed Income: $8,250,000 (52.4%)
    - Equity Holdings: $5,000,000 (31.7%)
    - Number of Positions: 45
    - Average Position Size: $350,000
    """
    
    # Initialize masking engine
    masking_engine = DataMaskingEngine()
    
    # Mask numerical values
    masked_text, masking_info = masking_engine.mask_numerical_values(sample_text)
    
    print("Original Text:")
    print(sample_text)
    print("\nMasked Text:")
    print(masked_text)
    print(f"\nTotal masked values: {masking_info['total_masked']}")
    
    # Test decryption
    decrypted_text = masking_engine.decrypt_numerical_values(masked_text, masking_info)
    
    print("\nDecrypted Text:")
    print(decrypted_text)
    
    # Verify integrity
    assert decrypted_text.strip() == sample_text.strip(), "Data integrity check failed!"
    print("✅ Data masking test passed!")
    
    return masking_info

def test_fund_obfuscation():
    """Test the fund name obfuscation functionality."""
    print("\n🏦 Testing Fund Name Obfuscator...")
    
    # Sample text with fund names
    sample_text = """
    Fund Allocation Report:
    - MasterFund1: $5,000,000 (31.7%)
    - AlphaFund: $3,750,000 (23.8%)
    - StrategicFund: $2,500,000 (15.9%)
    - GrowthFund: $2,000,000 (12.7%)
    - ValueFund: $1,500,000 (9.5%)
    - Cash Reserve: $1,000,000 (6.3%)
    """
    
    # Initialize obfuscator
    obfuscator = FundNameObfuscator()
    
    # Obfuscate fund names
    obfuscated_text, obfuscation_info = obfuscator.obfuscate_fund_names(sample_text)
    
    print("Original Text:")
    print(sample_text)
    print("\nObfuscated Text:")
    print(obfuscated_text)
    print(f"\nTotal obfuscated funds: {obfuscation_info['total_obfuscated']}")
    
    # Test deobfuscation
    deobfuscated_text = obfuscator.deobfuscate_fund_names(obfuscated_text, obfuscation_info)
    
    print("\nDeobfuscated Text:")
    print(deobfuscated_text)
    
    # Verify integrity
    assert deobfuscated_text.strip() == sample_text.strip(), "Fund obfuscation integrity check failed!"
    print("✅ Fund obfuscation test passed!")
    
    return obfuscation_info

def test_integration():
    """Test the complete integration workflow."""
    print("\n🔄 Testing Complete Integration...")
    
    # Sample financial document
    document_text = """
    QUARTERLY INVESTMENT REPORT
    
    Portfolio Overview:
    - Total Portfolio Value: $25,000,000
    - Number of Holdings: 67
    - Average Position Size: $373,134
    
    Top Holdings:
    1. MasterFund1: $8,500,000 (34.0%)
    2. AlphaFund: $6,250,000 (25.0%)
    3. StrategicFund: $4,500,000 (18.0%)
    4. GrowthFund: $3,750,000 (15.0%)
    5. ValueFund: $2,000,000 (8.0%)
    
    Performance Metrics:
    - YTD Return: 12.5%
    - Volatility: 8.3%
    - Sharpe Ratio: 1.51
    - Maximum Drawdown: -4.2%
    """
    
    # Initialize components
    masking_engine = DataMaskingEngine()
    obfuscator = FundNameObfuscator()
    
    print("Original Document:")
    print(document_text)
    
    # Step 1: Mask numerical values
    print("\n--- Step 1: Masking Numerical Values ---")
    masked_text, masking_info = masking_engine.mask_numerical_values(document_text)
    print(f"Masked {masking_info['total_masked']} numerical values")
    
    # Step 2: Obfuscate fund names
    print("\n--- Step 2: Obfuscating Fund Names ---")
    obfuscated_text, obfuscation_info = obfuscator.obfuscate_fund_names(masked_text)
    print(f"Obfuscated {obfuscation_info['total_obfuscated']} fund names")
    
    print("\nFinal Masked Document (Ready for AI Processing):")
    print(obfuscated_text)
    
    # Step 3: Decrypt results (simulating AI processing completion)
    print("\n--- Step 3: Decrypting Results ---")
    
    # Deobfuscate fund names first
    deobfuscated_text = obfuscator.deobfuscate_fund_names(obfuscated_text, obfuscation_info)
    
    # Decrypt numerical values
    decrypted_text = masking_engine.decrypt_numerical_values(deobfuscated_text, masking_info)
    
    print("\nDecrypted Document:")
    print(decrypted_text)
    
    # Verify complete integrity
    assert decrypted_text.strip() == document_text.strip(), "Integration test failed - data integrity compromised!"
    print("✅ Complete integration test passed!")
    
    return {
        'masking_info': masking_info,
        'obfuscation_info': obfuscation_info,
        'masked_document': obfuscated_text
    }

def test_file_operations():
    """Test file saving and loading operations."""
    print("\n💾 Testing File Operations...")
    
    # Test masking info persistence
    masking_engine = DataMaskingEngine()
    sample_text = "Investment: $1,000,000 in Fund001"
    masked_text, masking_info = masking_engine.mask_numerical_values(sample_text)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        masking_engine.save_masking_info(temp_file)
    
    # Load from file
    new_masking_engine = DataMaskingEngine()
    new_masking_engine.load_masking_info(temp_file)
    
    # Test decryption with loaded info
    decrypted_text = new_masking_engine.decrypt_numerical_values(masked_text, masking_info)
    
    # Clean up
    os.unlink(temp_file)
    
    assert decrypted_text.strip() == sample_text.strip(), "File operations test failed!"
    print("✅ File operations test passed!")

def main():
    """Run all tests."""
    print("🚀 Asset Data Privacy System - Test Suite")
    print("=" * 50)
    
    try:
        # Run individual tests
        masking_info = test_data_masking()
        obfuscation_info = test_fund_obfuscation()
        integration_results = test_integration()
        test_file_operations()
        
        print("\n" + "=" * 50)
        print("🎉 All Tests Passed Successfully!")
        print("\nSystem Summary:")
        print(f"  - Data Masking: {masking_info['total_masked']} values processed")
        print(f"  - Fund Obfuscation: {obfuscation_info['total_obfuscated']} funds processed")
        print(f"  - Integration: Complete workflow verified")
        print(f"  - File Operations: Persistence verified")
        
        print("\nThe system is ready for production use!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise

if __name__ == "__main__":
    main()
