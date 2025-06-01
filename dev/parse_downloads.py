#!/usr/bin/env python3
"""
Parse UCI calendar download files (PDF/XLS)
This should give us clean, structured event data
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def parse_excel_file():
    """Parse the UCI Excel file for event data"""
    
    claude_dir = Path(__file__).parent.parent / '.claude'
    excel_file = claude_dir / 'UCICompetitions_MTB_2025.xls'
    
    if not excel_file.exists():
        print("❌ Excel file not found")
        return None
    
    print("📊 Parsing UCI Excel file...")
    print(f"📄 File: {excel_file}")
    print(f"📏 Size: {excel_file.stat().st_size:,} bytes")
    print()
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        print(f"✅ Successfully loaded Excel file")
        print(f"📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print()
        
        # Show column names
        print("📋 Columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        print()
        
        # Show first few rows
        print("📖 First 5 rows:")
        print(df.head().to_string())
        print()
        
        # Show data types
        print("🔢 Data types:")
        for col, dtype in df.dtypes.items():
            print(f"   {col}: {dtype}")
        print()
        
        # Look for date columns
        date_columns = []
        for col in df.columns:
            if any(term in col.lower() for term in ['date', 'start', 'end', 'from', 'to']):
                date_columns.append(col)
        
        if date_columns:
            print(f"📅 Potential date columns: {date_columns}")
            for col in date_columns:
                sample_values = df[col].dropna().head(3).tolist()
                print(f"   {col}: {sample_values}")
        
        print()
        
        # Look for location/venue columns
        location_columns = []
        for col in df.columns:
            if any(term in col.lower() for term in ['location', 'venue', 'city', 'country', 'place']):
                location_columns.append(col)
        
        if location_columns:
            print(f"🌍 Potential location columns: {location_columns}")
            for col in location_columns:
                sample_values = df[col].dropna().head(3).tolist()
                print(f"   {col}: {sample_values}")
        
        print()
        
        # Look for event name/title columns
        name_columns = []
        for col in df.columns:
            if any(term in col.lower() for term in ['name', 'title', 'event', 'competition']):
                name_columns.append(col)
        
        if name_columns:
            print(f"🏆 Potential event name columns: {name_columns}")
            for col in name_columns:
                sample_values = df[col].dropna().head(3).tolist()
                print(f"   {col}: {sample_values}")
        
        # Save as JSON for analysis
        debug_dir = Path(__file__).parent / 'debug'
        debug_dir.mkdir(exist_ok=True)
        
        # Convert to JSON (handle dates)
        df_json = df.copy()
        for col in df_json.columns:
            if df_json[col].dtype == 'datetime64[ns]':
                df_json[col] = df_json[col].dt.strftime('%Y-%m-%d')
        
        json_file = debug_dir / 'uci_excel_data.json'
        df_json.to_json(json_file, orient='records', indent=2)
        print(f"💾 Saved data to {json_file}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error parsing Excel file: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_pdf_structure():
    """Analyze the PDF files to understand their structure"""
    
    claude_dir = Path(__file__).parent.parent / '.claude'
    
    pdf_files = [
        'Mountain Bike calendar _ UCI.pdf',
        'UCICompetitions_MTB_2025.pdf'
    ]
    
    print("📄 PDF File Analysis:")
    print("=" * 30)
    
    for pdf_name in pdf_files:
        pdf_file = claude_dir / pdf_name
        if pdf_file.exists():
            size = pdf_file.stat().st_size
            print(f"✅ {pdf_name}")
            print(f"   📏 Size: {size:,} bytes")
            print(f"   💡 Type: {'Rendered page' if 'calendar _' in pdf_name else 'Structured data'}")
            print()
        else:
            print(f"❌ {pdf_name} not found")
    
    print("💡 PDF parsing would require additional libraries (PyPDF2, pdfplumber)")
    print("   The Excel file is likely more suitable for structured data extraction")

def convert_to_ical_format(df):
    """Convert Excel data to our standard iCal format"""
    
    if df is None:
        return []
    
    print("\n🔄 Converting to iCal format...")
    
    events = []
    
    # This will depend on the actual column structure
    # We'll implement once we see the Excel structure
    print("💡 Need to analyze Excel structure first to implement conversion")
    
    return events

if __name__ == "__main__":
    print("🎯 UCI Download File Parser")
    print("=" * 40)
    
    # Parse Excel file first (most promising)
    df = parse_excel_file()
    
    # Analyze PDFs
    analyze_pdf_structure()
    
    if df is not None:
        print("\n🎉 Excel parsing successful!")
        print("📝 Next step: Implement conversion to iCal format based on column structure")
    else:
        print("\n❌ Excel parsing failed")
        print("📝 May need to try PDF parsing or manual inspection")