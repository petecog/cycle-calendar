#!/usr/bin/env python3
"""
Debug Scraper - REFERENCE IMPLEMENTATION
=======================================

⚠️  SPECULATIVE CODE - MAY BE NEEDED IN FUTURE ⚠️

This is a preserved reference implementation of comprehensive debugging tools
for the web scraping approach that was ultimately replaced by Excel parsing.

STATUS: De-implemented (replaced by Excel parsing approach)
REASON: UCI calendar uses JavaScript/lazy loading - live scraping yields 0 events

This debug scraper provided detailed analysis capabilities:
- Comprehensive HTML structure analysis
- Network request debugging
- Event parsing validation
- Output comparison between different parsing methods

See .claude/webscraping_approach_documentation.md for full context.
"""

import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def debug_fetch():
    """Test fetching the UCI calendar page with detailed output"""
    url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0"
    params = {
        'discipline': 'MTB',
        'seasonId': '1002',
        'raceCategory': 'ME,ME,WE,MM,WM,XE',
        'raceType': 'END,DHI,XCR,XCE,XCC,XCM,XCO'
    }
    
    # Ensure debug directory exists
    debug_dir = Path(__file__).parent / "debug"
    debug_dir.mkdir(exist_ok=True)
    
    print("🌐 Testing UCI Calendar Fetch")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Params: {params}")
    print(f"📁 Debug folder: {debug_dir}")
    print()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"📡 Making request...")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"📊 Content Length: {len(response.text)} characters")
        print(f"🎯 Content Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"🔗 Final URL: {response.url}")
        print()
        
        if response.status_code == 200:
            # Save raw HTML for inspection
            raw_file = debug_dir / 'uci_raw.html'
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"💾 Saved raw HTML to: {raw_file}")
            
            # Show first few lines
            lines = response.text.split('\n')[:20]
            print(f"📄 First 20 lines of HTML:")
            for i, line in enumerate(lines, 1):
                print(f"   {i:2d}: {line[:100]}")
            print()
            
            return response.text
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"💥 Request error: {e}")
        return None

def debug_parsing(html_content):
    """Test parsing the HTML with detailed output"""
    debug_dir = Path(__file__).parent / "debug"
    
    print("🔍 Testing HTML Parsing")
    print("=" * 50)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Show basic page structure
    title = soup.find('title')
    print(f"📰 Page Title: {title.get_text() if title else 'Not found'}")
    
    # Look for various calendar-related elements
    search_patterns = [
        {'name': 'Events by class', 'pattern': re.compile(r'event', re.I)},
        {'name': 'Calendar by class', 'pattern': re.compile(r'calendar', re.I)},
        {'name': 'MTB by text', 'pattern': re.compile(r'mtb', re.I)},
        {'name': 'Date patterns', 'pattern': re.compile(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2}')},
        {'name': 'Race by text', 'pattern': re.compile(r'race|competition|championship', re.I)},
    ]
    
    print("\n🎯 Searching for calendar indicators:")
    for search in search_patterns:
        elements = soup.find_all(text=search['pattern'])
        print(f"   {search['name']}: {len(elements)} matches")
        if elements and len(elements) <= 5:
            for elem in elements[:3]:
                print(f"      - {elem.strip()[:60]}...")
    
    print("\n📋 Looking for common calendar HTML structures:")
    
    # Check for various HTML patterns
    structures = [
        ('div with event class', soup.find_all('div', class_=re.compile(r'event', re.I))),
        ('table rows', soup.find_all('tr')),
        ('list items', soup.find_all('li')),
        ('divs with calendar class', soup.find_all('div', class_=re.compile(r'calendar', re.I))),
        ('spans with date-like content', soup.find_all('span')),
        ('links (a tags)', soup.find_all('a')),
    ]
    
    for name, elements in structures:
        print(f"   {name}: {len(elements)} found")
        if elements:
            for elem in elements[:3]:
                text = elem.get_text(strip=True)[:80]
                classes = elem.get('class', [])
                print(f"      - {text}... (classes: {classes})")
    
    # Look for JavaScript/JSON data
    scripts = soup.find_all('script')
    print(f"\n💻 JavaScript blocks: {len(scripts)} found")
    for i, script in enumerate(scripts[:5]):
        if script.string:
            content = script.string.strip()[:100]
            print(f"   Script {i+1}: {content}...")
    
    # Save structured data for inspection
    structure_file = debug_dir / 'uci_parsed.html'
    with open(structure_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print(f"\n💾 Saved prettified HTML to: {structure_file}")
    
    # Save analysis summary
    analysis_file = debug_dir / 'analysis.json'
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'page_title': title.get_text() if title else None,
        'total_elements': {
            'scripts': len(scripts),
            'links': len(soup.find_all('a')),
            'divs': len(soup.find_all('div')),
            'spans': len(soup.find_all('span')),
            'list_items': len(soup.find_all('li'))
        },
        'search_results': {}
    }
    
    # Add search pattern results
    for search in search_patterns:
        elements = soup.find_all(string=search['pattern'])
        analysis['search_results'][search['name']] = len(elements)
    
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"📊 Saved analysis summary to: {analysis_file}")

def test_scraper_logic():
    """Test the actual scraper logic"""
    print("\n🔧 Testing Current Scraper Logic")
    print("=" * 50)
    
    try:
        from uci_calendar import UCICalendarScraper
        
        scraper = UCICalendarScraper()
        
        # Test individual methods
        print("🌐 Testing fetch_calendar_page()...")
        html_content = scraper.fetch_calendar_page()
        
        if html_content:
            print(f"✅ Successfully fetched {len(html_content)} characters")
            
            print("\n🔍 Testing parse_events()...")
            events = scraper.parse_events(html_content)
            print(f"📊 Found {len(events)} raw events")
            
            if events:
                print("📋 Event details:")
                for i, event in enumerate(events[:5]):
                    print(f"   Event {i+1}: {event}")
            
            print("\n🚀 Testing full scrape_events()...")
            final_events = scraper.scrape_events()
            print(f"✅ Final result: {len(final_events)} valid events")
            
            if final_events:
                for event in final_events:
                    print(f"   - {event}")
        else:
            print("❌ Failed to fetch calendar page")
            
    except Exception as e:
        print(f"💥 Scraper error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run complete scraper debugging"""
    debug_dir = Path(__file__).parent / "debug"
    
    print("🚵‍♂️ UCI MTB Calendar Scraper Debug Tool")
    print("=" * 60)
    print()
    
    # Step 1: Test fetching
    html_content = debug_fetch()
    
    if html_content:
        # Step 2: Test parsing
        debug_parsing(html_content)
        
        # Step 3: Test scraper logic
        test_scraper_logic()
    
    print("\n" + "=" * 60)
    print("🎯 Debug complete! Check generated files:")
    print(f"   📁 Debug folder: {debug_dir}")
    print(f"   - uci_raw.html (raw UCI page)")
    print(f"   - uci_parsed.html (parsed structure)")
    print(f"   - analysis.json (summary data)")
    print()
    print("💡 Next steps:")
    print("   1. Open uci_raw.html in browser")
    print("   2. Inspect the page structure")
    print("   3. Look for calendar events manually")
    print("   4. Check analysis.json for patterns")
    print("   5. Update scraper.py logic if needed")

if __name__ == "__main__":
    main()