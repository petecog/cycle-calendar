#!/usr/bin/env python3
"""
Advanced UCI Calendar Scraper
Handles JavaScript-rendered content and lazy loading using Selenium
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
import re

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class AdvancedUCIScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.debug_dir = Path(__file__).parent / "debug"
        self.debug_dir.mkdir(exist_ok=True)
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not available. Install with: pip install selenium")
        
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            print("💡 Install ChromeDriver: https://chromedriver.chromium.org/")
            return None
    
    def scroll_and_load_content(self, driver, max_scrolls=10):
        """Scroll down to trigger lazy loading of calendar events"""
        print("📜 Scrolling to load dynamic content...")
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(2)
            
            # Check if new content was loaded
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            print(f"   Scroll {scroll_count + 1}: Height {last_height} → {new_height}")
            
            if new_height == last_height:
                print("   No new content loaded, stopping scroll")
                break
                
            last_height = new_height
            scroll_count += 1
        
        print(f"✅ Completed {scroll_count} scrolls")
        return scroll_count
    
    def wait_for_calendar_elements(self, driver, timeout=10):
        """Wait for calendar elements to appear"""
        print("⏳ Waiting for calendar elements to load...")
        
        # Common selectors for calendar events
        selectors_to_try = [
            '[class*="event"]',
            '[class*="calendar"]', 
            '[class*="race"]',
            '[class*="competition"]',
            'article',
            '.event-card',
            '.calendar-item',
            '[data-event]',
            '[data-date]'
        ]
        
        for selector in selectors_to_try:
            try:
                elements = WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    return selector, elements
            except TimeoutException:
                continue
        
        print("⚠️  No calendar elements found with common selectors")
        return None, []
    
    def extract_events_from_elements(self, elements):
        """Extract event data from found elements"""
        events = []
        
        for i, element in enumerate(elements):
            try:
                # Extract text content
                text = element.text.strip()
                if not text:
                    continue
                
                # Extract attributes that might contain data
                attrs = {
                    'class': element.get_attribute('class'),
                    'data-date': element.get_attribute('data-date'),
                    'data-event': element.get_attribute('data-event'),
                    'title': element.get_attribute('title'),
                    'href': element.get_attribute('href')
                }
                
                # Look for date patterns in text
                date_matches = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+\d{4}', text)
                
                event_data = {
                    'index': i,
                    'text': text[:200],  # Limit text length
                    'dates_found': date_matches,
                    'attributes': {k: v for k, v in attrs.items() if v},
                    'element_tag': element.tag_name
                }
                
                events.append(event_data)
                
            except Exception as e:
                print(f"   Error processing element {i}: {e}")
                continue
        
        return events
    
    def scrape_with_selenium(self):
        """Main scraping method using Selenium"""
        print("🚀 Starting advanced UCI calendar scraping with Selenium")
        print("=" * 60)
        
        driver = self.setup_driver()
        if not driver:
            return []
        
        try:
            url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB"
            print(f"🌐 Loading: {url}")
            
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Save initial page state
            initial_html = driver.page_source
            initial_file = self.debug_dir / 'selenium_initial.html'
            with open(initial_file, 'w', encoding='utf-8') as f:
                f.write(initial_html)
            print(f"💾 Saved initial page state: {initial_file}")
            
            # Scroll to trigger lazy loading
            scroll_count = self.scroll_and_load_content(driver)
            
            # Save final page state after scrolling
            final_html = driver.page_source
            final_file = self.debug_dir / 'selenium_final.html'
            with open(final_file, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"💾 Saved final page state: {final_file}")
            
            # Look for calendar elements
            selector, elements = self.wait_for_calendar_elements(driver)
            
            events = []
            if elements:
                print(f"📊 Processing {len(elements)} potential event elements...")
                events = self.extract_events_from_elements(elements)
                
                # Save events data
                events_file = self.debug_dir / 'selenium_events.json'
                with open(events_file, 'w') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'url': url,
                        'selector_used': selector,
                        'scroll_count': scroll_count,
                        'total_elements': len(elements),
                        'events': events
                    }, f, indent=2)
                print(f"📊 Saved events data: {events_file}")
            
            # Compare initial vs final HTML size
            size_initial = len(initial_html)
            size_final = len(final_html)
            print(f"📈 HTML size change: {size_initial} → {size_final} ({size_final - size_initial:+} chars)")
            
            return events
            
        except Exception as e:
            print(f"💥 Selenium scraping failed: {e}")
            import traceback
            traceback.print_exc()
            return []
            
        finally:
            driver.quit()
    
    def fallback_analysis(self):
        """Analyze static HTML for clues about dynamic loading"""
        print("\n🔍 Fallback: Analyzing static HTML for dynamic loading clues")
        print("=" * 60)
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get("https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for JavaScript that might load calendar data
            scripts = soup.find_all('script')
            api_clues = []
            
            for script in scripts:
                if script.string:
                    content = script.string
                    # Look for API endpoints, AJAX calls, or data loading
                    if any(keyword in content.lower() for keyword in ['api', 'ajax', 'fetch', 'calendar', 'event']):
                        api_clues.append(content[:200])
            
            print(f"🔍 Found {len(api_clues)} scripts with potential API/data loading:")
            for i, clue in enumerate(api_clues[:3]):
                print(f"   {i+1}: {clue}...")
            
            # Save analysis
            analysis_file = self.debug_dir / 'api_analysis.json'
            with open(analysis_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'api_clues_count': len(api_clues),
                    'api_clues': api_clues[:5]  # Limit size
                }, f, indent=2)
            print(f"📊 Saved API analysis: {analysis_file}")
            
        except Exception as e:
            print(f"❌ Fallback analysis failed: {e}")

def main():
    """Main function"""
    print("🚵‍♂️ Advanced UCI MTB Calendar Scraper")
    print("=" * 60)
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not available!")
        print("💡 Install with: pip install selenium")
        print("💡 Also install ChromeDriver: https://chromedriver.chromium.org/")
        print("\n🔄 Running fallback analysis instead...")
        
        scraper = AdvancedUCIScraper()
        scraper.fallback_analysis()
        return
    
    scraper = AdvancedUCIScraper(headless=True)
    
    # Try Selenium scraping
    events = scraper.scrape_with_selenium()
    
    print(f"\n🎯 Results: Found {len(events)} potential events")
    if events:
        print("📋 Sample events:")
        for event in events[:3]:
            print(f"   - {event.get('text', 'No text')[:60]}...")
    
    # Also run fallback analysis for comparison
    scraper.fallback_analysis()
    
    print(f"\n📁 Debug files saved to: {scraper.debug_dir}")

if __name__ == "__main__":
    main()