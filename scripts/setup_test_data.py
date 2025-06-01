#!/usr/bin/env python3
"""
Setup test data by copying Excel file from claude-input to data directory
This is for testing until we have the download working
"""

import shutil
from pathlib import Path

def setup_test_data(year: str = "2025"):
    """Copy Excel file from claude-input to data directory for testing"""
    
    # Source file in claude-input (for our reference)
    source_file = Path(__file__).parent.parent / '.claude' / 'claude-input' / f'UCICompetitions_MTB_{year}.xls'
    
    # Destination in data directory (for application use)
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    dest_file = data_dir / f'{year}.xls'
    
    if source_file.exists():
        shutil.copy2(source_file, dest_file)
        print(f"✅ Copied test data: {dest_file}")
        print(f"   Source: {source_file}")
        print(f"   Size: {dest_file.stat().st_size} bytes")
        return True
    else:
        print(f"❌ Source file not found: {source_file}")
        return False

if __name__ == "__main__":
    success = setup_test_data()
    if not success:
        exit(1)