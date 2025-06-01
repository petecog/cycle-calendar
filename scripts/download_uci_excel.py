#!/usr/bin/env python3
"""
Download UCI MTB Excel file

Attempts to download the UCI MTB calendar Excel file by reverse engineering
the download mechanism from the UCI website.
"""

import requests
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import time

def download_uci_excel_for_year(year: str, output_dir: Path = None) -> bool:
    """
    Download UCI MTB Excel file for a specific year
    
    Args:
        year: Year to download (e.g. "2025")
        output_dir: Directory to save the file (defaults to data/)
        
    Returns:
        True if successful, False otherwise
    """
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'data'
    
    output_dir.mkdir(exist_ok=True)
    
    print("🔍 Using discovered UCI API endpoint...")
    
    # The actual UCI API endpoint (discovered via Chrome Dev Tools)
    api_url = "https://api.uci.ch/v1.2/ucibws/competitions/getreportxls"
    
    # Request payload
    payload = {
        "IsGrouped": True,
        "Language": "En", 
        "Query": {
            "discipline": "MTB",
            "year": year
        },
        "ReportTitle": f"MTB - {year}"
    }
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors", 
        "sec-fetch-site": "cross-site",
        "referrer": "https://www.uci.org/",
        "referrerPolicy": "strict-origin-when-cross-origin"
        # Note: Authorization header needs to be obtained dynamically
    }
    
    print("⚠️  WARNING: This API requires authentication")
    print("   The discovered request included a Bearer token that expires")
    print("   We need to either:")
    print("   1. Reverse engineer the authentication flow, or")
    print("   2. Use manual download for now")
    print()
    
    try:
        print("🧪 Attempting API call without authentication...")
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ❌ Authentication required (401 Unauthorized)")
            return False
        elif response.status_code == 200:
            # Check if we got Excel file
            content_type = response.headers.get('content-type', '').lower()
            
            if ('excel' in content_type or 
                'spreadsheet' in content_type or
                'application/vnd.ms-excel' in content_type):
                
                filename = f"{year}.xls"
                output_file = output_dir / filename
                
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ SUCCESS! Downloaded: {output_file}")
                print(f"   File size: {len(response.content)} bytes")
                return True
            else:
                print(f"   ⚠️  Unexpected content type: {content_type}")
                print(f"   Response preview: {response.text[:200]}...")
        else:
            print(f"   ❌ API error: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    print("\n❌ API download failed - authentication required")
    print("\n💡 Manual download instructions:")
    print("1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
    print("2. Click 'Download season' → 'xls'")
    print(f"3. Save as: {output_dir}/{year}.xls")
    print("\n🔧 API Details for future automation:")
    print(f"   Endpoint: {api_url}")
    print(f"   Method: POST")
    print(f"   Payload: {payload}")
    print("   Auth: Bearer token required (expires ~1 hour)")
    
    return False

def discover_available_years() -> list:
    """
    Discover available years from UCI calendar
    
    Returns:
        List of available years as strings
    """
    
    # For now, we'll try common years around current time
    # In the future, this could be enhanced to scrape the UCI website
    # to dynamically discover available seasons
    
    from datetime import datetime
    current_year = datetime.now().year
    
    # Try current year and next 2 years (UCI often has future seasons)
    potential_years = [
        str(current_year),
        str(current_year + 1), 
        str(current_year + 2)
    ]
    
    print(f"🔍 Checking for available seasons: {', '.join(potential_years)}")
    return potential_years

def download_all_available_seasons(output_dir: Path = None) -> dict:
    """
    Download all available UCI MTB seasons
    
    Args:
        output_dir: Directory to save files (defaults to data/)
        
    Returns:
        Dictionary with year -> success status
    """
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'data'
    
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting dynamic UCI MTB season download...")
    
    # Discover available years
    years_to_try = discover_available_years()
    
    results = {}
    successful_downloads = 0
    
    for year in years_to_try:
        print(f"\n📅 Attempting to download {year} season...")
        
        try:
            success = download_uci_excel_for_year(year, output_dir)
            results[year] = success
            
            if success:
                successful_downloads += 1
                print(f"✅ Successfully downloaded {year}.xls")
            else:
                print(f"❌ Failed to download {year} season")
                
        except Exception as e:
            print(f"❌ Error downloading {year}: {e}")
            results[year] = False
    
    print(f"\n📊 Download Summary:")
    print(f"   Attempted: {len(years_to_try)} seasons")
    print(f"   Successful: {successful_downloads} downloads")
    print(f"   Failed: {len(years_to_try) - successful_downloads}")
    
    if successful_downloads > 0:
        print(f"\n💾 Downloaded files saved to: {output_dir}")
        # List downloaded files
        excel_files = list(output_dir.glob("*.xls")) + list(output_dir.glob("*.xlsx"))
        for file in sorted(excel_files):
            size_kb = file.stat().st_size // 1024
            print(f"   📄 {file.name} ({size_kb} KB)")
    
    if successful_downloads == 0:
        print(f"\n⚠️  No seasons downloaded successfully")
        print(f"💡 Manual download instructions:")
        print(f"1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
        print(f"2. Click 'Download season' → 'xls'")
        print(f"3. Save files as: {output_dir}/YYYY.xls (e.g. 2025.xls)")
        
    return results

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['all', 'auto', 'dynamic']:
            # Download all available seasons
            print("🔄 Dynamic mode: Downloading all available seasons...")
            results = download_all_available_seasons()
            
            # Exit with error if no downloads succeeded
            if not any(results.values()):
                exit(1)
        else:
            # Download specific year
            year = sys.argv[1]
            print(f"📅 Single year mode: Downloading {year} season...")
            success = download_uci_excel_for_year(year)
            if not success:
                exit(1)
    else:
        # Default: try dynamic download
        print("🔄 No arguments provided - trying dynamic download...")
        print("💡 Use 'python download_uci_excel.py YYYY' for specific year")
        print("💡 Use 'python download_uci_excel.py all' for all seasons")
        print()
        
        results = download_all_available_seasons()
        
        # Exit with error if no downloads succeeded
        if not any(results.values()):
            exit(1)