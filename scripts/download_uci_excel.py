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

def download_uci_excel(output_dir: Path = None) -> bool:
    """
    Download UCI MTB Excel file using discovered API endpoint
    
    Args:
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
            "year": "2025"
        },
        "ReportTitle": "MTB - 2025"
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
                
                filename = "UCICompetitions_MTB_2025.xls"
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
    print(f"3. Save as: {output_dir}/UCICompetitions_MTB_2025.xls")
    print("\n🔧 API Details for future automation:")
    print(f"   Endpoint: {api_url}")
    print(f"   Method: POST")
    print(f"   Payload: {payload}")
    print("   Auth: Bearer token required (expires ~1 hour)")
    
    return False

if __name__ == "__main__":
    success = download_uci_excel()
    if not success:
        exit(1)