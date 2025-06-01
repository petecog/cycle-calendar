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
import asyncio

def _try_browser_download(year: str, output_dir: Path) -> bool:
    """
    Try to download using browser automation
    
    Args:
        year: Year to download
        output_dir: Output directory
        
    Returns:
        True if successful, False otherwise
    """
    
    try:
        # Import browser automation script
        browser_script = Path(__file__).parent / 'browser_download_uci.py'
        if not browser_script.exists():
            print("❌ Browser automation script not found")
            return False
        
        # Import the UCIBrowserDownloader class
        import sys
        sys.path.insert(0, str(browser_script.parent))
        from browser_download_uci import UCIBrowserDownloader
        
        # Run browser download
        async def run_download():
            downloader = UCIBrowserDownloader(output_dir)
            return await downloader.download_year(year, headless=True)
        
        # Execute the async function
        return asyncio.run(run_download())
        
    except ImportError as e:
        print(f"❌ Browser automation not available: {e}")
        print("💡 Install with: pip install playwright && playwright install chromium")
        return False
    except Exception as e:
        print(f"❌ Browser automation failed: {e}")
        return False

def download_uci_excel_for_year(year: str, output_dir: Path = None, try_browser: bool = True) -> bool:
    """
    Download UCI MTB Excel file for a specific year
    
    Args:
        year: Year to download (e.g. "2025")
        output_dir: Directory to save the file (defaults to data/)
        try_browser: Whether to try browser automation first (defaults to True)
        
    Returns:
        True if successful, False otherwise
    """
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'data'
    
    output_dir.mkdir(exist_ok=True)
    
    # Try browser automation first (if available and requested)
    if try_browser:
        try:
            print("🤖 Attempting browser automation download...")
            success = _try_browser_download(year, output_dir)
            if success:
                return True
            else:
                print("⚠️  Browser automation failed, falling back to direct API...")
        except Exception as e:
            print(f"⚠️  Browser automation error: {e}")
            print("🔄 Falling back to direct API approach...")
    
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
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "dnt": "1",
        "origin": "https://www.uci.org",
        "priority": "u=1, i",
        "referer": "https://www.uci.org/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    
    try:
        print("📡 Calling UCI API (no authentication required)...")
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        print(f"   Response content preview: {response.text[:500]}")
        
        if response.status_code == 200:
            # Check if we got Excel file
            content_type = response.headers.get('content-type', '').lower()
            
            if ('excel' in content_type or 
                'spreadsheet' in content_type or
                'application/vnd.ms-excel' in content_type or
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type):
                
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
    
    print("\n❌ API download failed")
    print("\n💡 Manual download instructions:")
    print("1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
    print("2. Click 'Download season' → 'xls'")
    print(f"3. Save as: {output_dir}/{year}.xls")
    print("\n🔧 API Details:")
    print(f"   Endpoint: {api_url}")
    print(f"   Method: POST")
    print(f"   Payload: {payload}")
    
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