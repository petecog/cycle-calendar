#!/usr/bin/env python3
"""
Test the new filtered UCI URL to see if it changes the page structure
"""

import sys
from pathlib import Path
import requests

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_filtered_url():
    """Test the filtered URL and save response for analysis"""
    
    # Original URL
    original_url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0"
    original_params = {'discipline': 'MTB'}
    
    # New filtered URL  
    filtered_params = {
        'discipline': 'MTB',
        'seasonId': '1002', 
        'raceCategory': 'ME,ME,WE,MM,WM,XE',
        'raceType': 'END,DHI,XCR,XCE,XCC,XCM,XCO'
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print("🔍 Testing URL filtering effects...")
    
    try:
        # Fetch original
        print("📥 Fetching original URL...")
        orig_response = session.get(original_url, params=original_params, timeout=30)
        orig_response.raise_for_status()
        
        # Fetch filtered  
        print("📥 Fetching filtered URL...")
        filtered_response = session.get(original_url, params=filtered_params, timeout=30)
        filtered_response.raise_for_status()
        
        print(f"📊 Original response: {len(orig_response.text)} characters")
        print(f"📊 Filtered response: {len(filtered_response.text)} characters")
        
        # Save for comparison
        debug_dir = Path(__file__).parent / 'debug'
        debug_dir.mkdir(exist_ok=True)
        
        with open(debug_dir / 'uci_original.html', 'w', encoding='utf-8') as f:
            f.write(orig_response.text)
            
        with open(debug_dir / 'uci_filtered.html', 'w', encoding='utf-8') as f:
            f.write(filtered_response.text)
            
        print(f"💾 Saved responses to {debug_dir}/")
        
        # Check for differences in key content
        from bs4 import BeautifulSoup
        
        orig_soup = BeautifulSoup(orig_response.text, 'html.parser')
        filtered_soup = BeautifulSoup(filtered_response.text, 'html.parser')
        
        orig_cards = orig_soup.find_all('div', class_='competition-card')
        filtered_cards = filtered_soup.find_all('div', class_='competition-card')
        
        orig_items = orig_soup.find_all('div', class_='calendar-item__title')
        filtered_items = filtered_soup.find_all('div', class_='calendar-item__title')
        
        print(f"🎴 Competition cards - Original: {len(orig_cards)}, Filtered: {len(filtered_cards)}")
        print(f"📅 Calendar items - Original: {len(orig_items)}, Filtered: {len(filtered_items)}")
        
        # Show the actual filtered URL for reference
        filtered_url = filtered_response.url
        print(f"🔗 Actual filtered URL: {filtered_url}")
        
        return len(filtered_cards) > 0 or len(filtered_items) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_filtered_url()
    if success:
        print("✅ Found some content with filtered URL")
    else:
        print("❌ No events found even with filtered URL (dynamic loading still an issue)")