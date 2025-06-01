#!/usr/bin/env python3
"""
Analyze UCI calendar download options (PDF/XLS)
This could bypass the dynamic loading issue entirely
"""

import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def analyze_download_options():
    """Analyze the download options on the UCI calendar page"""
    
    print("📄 UCI Calendar Download Analysis")
    print("=" * 50)
    
    # Use our filtered URL
    url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0"
    params = {
        'discipline': 'MTB',
        'seasonId': '1002',
        'raceCategory': 'ME,ME,WE,MM,WM,XE',
        'raceType': 'END,DHI,XCR,XCE,XCC,XCM,XCO'
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        print(f"🌐 Fetching page...")
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"✅ Page loaded: {len(response.text)} characters")
        print(f"🔗 URL: {response.url}")
        print()
        
        # Look for the download section you found
        print("🔍 Searching for download elements...")
        
        # Find the floating filters div
        floating_filters = soup.find('div', class_='calendar__floating-filters')
        if floating_filters:
            print("✅ Found calendar__floating-filters div")
            
            # Look for download filter
            download_filter = floating_filters.find('div', class_='calendar__download-filter')
            if download_filter:
                print("✅ Found calendar__download-filter div")
                
                # Find all download links
                links = download_filter.find_all('a')
                print(f"📎 Found {len(links)} download links:")
                
                for i, link in enumerate(links, 1):
                    href = link.get('href', 'No href')
                    text = link.get_text(strip=True)
                    print(f"   {i}. Text: '{text}' | Href: '{href}'")
                    
            else:
                print("❌ No calendar__download-filter found")
        else:
            print("❌ No calendar__floating-filters found")
        
        print()
        
        # Search for any PDF/XLS related links more broadly
        print("🔍 Searching for PDF/XLS links across entire page...")
        
        # Look for any links with pdf or xls in them
        all_links = soup.find_all('a')
        download_links = []
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True).lower()
            
            if any(term in href.lower() for term in ['pdf', 'xls', 'excel', 'download']) or \
               any(term in text for term in ['pdf', 'xls', 'excel', 'download']):
                download_links.append({
                    'text': link.get_text(strip=True),
                    'href': href,
                    'onclick': link.get('onclick', ''),
                    'data_attrs': {k:v for k,v in link.attrs.items() if k.startswith('data-')}
                })
        
        if download_links:
            print(f"📋 Found {len(download_links)} potential download links:")
            for i, link in enumerate(download_links, 1):
                print(f"   {i}. '{link['text']}'")
                print(f"      Href: {link['href']}")
                if link['onclick']:
                    print(f"      OnClick: {link['onclick']}")
                if link['data_attrs']:
                    print(f"      Data attrs: {link['data_attrs']}")
                print()
        else:
            print("❌ No obvious download links found")
        
        # Look for JavaScript that might handle downloads
        print("🔍 Searching for download-related JavaScript...")
        scripts = soup.find_all('script')
        download_js = []
        
        for script in scripts:
            content = script.get_text()
            if any(term in content.lower() for term in ['download', 'pdf', 'xls', 'excel']):
                # Extract relevant lines
                lines = content.split('\n')
                relevant_lines = [line.strip() for line in lines 
                                if any(term in line.lower() for term in ['download', 'pdf', 'xls', 'excel'])]
                if relevant_lines:
                    download_js.extend(relevant_lines)
        
        if download_js:
            print(f"📜 Found {len(download_js)} JavaScript lines mentioning downloads:")
            for i, line in enumerate(download_js[:10], 1):  # Show first 10
                print(f"   {i}. {line[:100]}...")
        else:
            print("❌ No download-related JavaScript found")
        
        # Save the HTML for manual inspection
        debug_dir = Path(__file__).parent / 'debug'
        debug_dir.mkdir(exist_ok=True)
        
        output_file = debug_dir / 'uci_download_analysis.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"\n💾 Saved page to {output_file} for manual inspection")
        
        return download_links
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def check_claude_folder():
    """Check if user has placed any downloaded files in .claude folder"""
    
    print("\n📂 Checking .claude folder for downloaded files...")
    
    claude_dir = Path(__file__).parent.parent / '.claude'
    if not claude_dir.exists():
        print("❌ .claude folder not found")
        return []
    
    # Look for PDF and XLS files
    download_files = []
    for pattern in ['*.pdf', '*.xls', '*.xlsx']:
        files = list(claude_dir.glob(pattern))
        download_files.extend(files)
    
    if download_files:
        print(f"✅ Found {len(download_files)} downloaded files:")
        for file in download_files:
            size = file.stat().st_size
            print(f"   📄 {file.name} ({size:,} bytes)")
        return download_files
    else:
        print("📝 No download files found yet")
        print("💡 If you download PDF/XLS files, place them in .claude/ folder")
        return []

if __name__ == "__main__":
    download_links = analyze_download_options()
    downloaded_files = check_claude_folder()
    
    print("\n" + "="*50)
    if download_links:
        print("🎯 Next steps:")
        print("1. Manually navigate to the UCI calendar page")
        print("2. Use the download buttons to get PDF/XLS files") 
        print("3. Place files in .claude/ folder")
        print("4. We can then parse the structured data directly!")
    else:
        print("💡 The download links might be JavaScript-powered")
        print("   Manual download from the browser may be the best approach")