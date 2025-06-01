#!/usr/bin/env python3
"""
Network Traffic Analyzer for UCI Calendar
Monitors network requests to find API endpoints for calendar data
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import requests

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class UCINetworkAnalyzer:
    def __init__(self):
        self.debug_dir = Path(__file__).parent / "debug"
        self.debug_dir.mkdir(exist_ok=True)
        self.captured_requests = []
    
    def setup_driver_with_logging(self):
        """Set up Chrome with network logging enabled"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Enable logging for network requests
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            return None
    
    def capture_network_traffic(self):
        """Capture network requests while loading the calendar page"""
        print("📡 Capturing network traffic from UCI calendar page")
        print("=" * 60)
        
        driver = self.setup_driver_with_logging()
        if not driver:
            return []
        
        try:
            url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB"
            print(f"🌐 Loading: {url}")
            
            # Load the page
            driver.get(url)
            time.sleep(3)
            
            # Get performance logs (network requests)
            logs = driver.get_log('performance')
            
            # Scroll to trigger more loading
            print("📜 Scrolling to trigger additional requests...")
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Get additional logs after scrolling
                new_logs = driver.get_log('performance')
                logs.extend(new_logs)
            
            # Look for "View more" or similar buttons
            try:
                view_more_buttons = driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'View more') or contains(text(), 'Load more') or contains(text(), 'Show more')]")
                
                if view_more_buttons:
                    print(f"🔍 Found {len(view_more_buttons)} 'view more' type buttons")
                    for i, button in enumerate(view_more_buttons[:2]):  # Click first 2
                        try:
                            print(f"   Clicking button {i+1}: {button.text}")
                            button.click()
                            time.sleep(3)
                            
                            # Capture logs after clicking
                            click_logs = driver.get_log('performance')
                            logs.extend(click_logs)
                        except Exception as e:
                            print(f"   Failed to click button {i+1}: {e}")
            except Exception as e:
                print(f"⚠️  Error looking for buttons: {e}")
            
            print(f"📊 Captured {len(logs)} network events")
            return self.parse_network_logs(logs)
            
        finally:
            driver.quit()
    
    def parse_network_logs(self, logs):
        """Parse Chrome performance logs to extract network requests"""
        print("🔍 Analyzing network requests...")
        
        api_requests = []
        
        for log in logs:
            try:
                message = json.loads(log['message'])
                
                if message['message']['method'] == 'Network.responseReceived':
                    response = message['message']['params']['response']
                    url = response['url']
                    
                    # Filter for potentially interesting requests
                    if any(keyword in url.lower() for keyword in ['api', 'calendar', 'event', 'json', 'ajax']):
                        request_info = {
                            'url': url,
                            'method': response.get('method', 'GET'),
                            'status': response['status'],
                            'mimeType': response.get('mimeType', ''),
                            'timestamp': message['message']['params']['timestamp']
                        }
                        api_requests.append(request_info)
                
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Remove duplicates
        unique_requests = []
        seen_urls = set()
        for req in api_requests:
            if req['url'] not in seen_urls:
                unique_requests.append(req)
                seen_urls.add(req['url'])
        
        print(f"🎯 Found {len(unique_requests)} unique API-like requests")
        
        # Save captured requests
        requests_file = self.debug_dir / 'network_requests.json'
        with open(requests_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_logs': len(logs),
                'api_requests': unique_requests
            }, f, indent=2)
        print(f"💾 Saved network analysis to: {requests_file}")
        
        return unique_requests
    
    def test_discovered_apis(self, api_requests):
        """Test the discovered API endpoints"""
        print(f"\n🧪 Testing {len(api_requests)} discovered API endpoints")
        print("=" * 60)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, */*',
            'Referer': 'https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB'
        }
        
        successful_apis = []
        
        for req in api_requests:
            try:
                print(f"🔗 Testing: {req['url']}")
                
                response = requests.get(req['url'], headers=headers, timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Check if it contains calendar/event data
                    calendar_indicators = ['event', 'race', 'date', 'calendar', 'competition', 'mtb']
                    contains_calendar_data = any(indicator in content.lower() for indicator in calendar_indicators)
                    
                    result = {
                        'url': req['url'],
                        'status': response.status_code,
                        'content_type': response.headers.get('content-type', ''),
                        'size': len(content),
                        'contains_calendar_data': contains_calendar_data,
                        'sample_content': content[:200] if contains_calendar_data else ''
                    }
                    
                    if contains_calendar_data:
                        print(f"   ✅ {response.status_code} - Contains calendar data! ({len(content)} bytes)")
                        successful_apis.append(result)
                        
                        # Save the full response
                        filename = f"api_response_{len(successful_apis)}.json"
                        api_file = self.debug_dir / filename
                        with open(api_file, 'w') as f:
                            f.write(content)
                        print(f"   💾 Saved response to: {api_file}")
                    else:
                        print(f"   ℹ️  {response.status_code} - No calendar data detected")
                else:
                    print(f"   ❌ {response.status_code}")
                    
            except Exception as e:
                print(f"   💥 Error: {e}")
        
        return successful_apis
    
    def manual_api_discovery(self):
        """Try common UCI API endpoint patterns manually"""
        print("\n🔍 Manual API endpoint discovery")
        print("=" * 60)
        
        base_url = "https://www.uci.org"
        test_endpoints = [
            "/api/calendar",
            "/api/calendar/mtb",
            "/api/calendar/events",
            "/api/events",
            "/api/competitions",
            "/calendar/api",
            "/calendar/api/events",
            "/calendar/api/mtb",
            "/calendar/data",
            "/data/calendar",
            "/data/events",
            "/umbraco/api/calendar",
            "/umbraco/api/events",
            "/_api/calendar",
            "/_api/events"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, */*',
            'Referer': 'https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB'
        }
        
        found_endpoints = []
        
        for endpoint in test_endpoints:
            try:
                url = base_url + endpoint
                print(f"🔗 Testing: {url}")
                
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200 and response.headers.get('content-type', '').startswith('application/json'):
                    print(f"   ✅ Found JSON API! ({len(response.text)} bytes)")
                    found_endpoints.append(url)
                    
                    # Save response
                    filename = f"manual_api_{len(found_endpoints)}.json"
                    api_file = self.debug_dir / filename
                    with open(api_file, 'w') as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {api_file}")
                else:
                    print(f"   ❌ {response.status_code}")
                    
            except Exception as e:
                print(f"   💥 Error: {e}")
        
        return found_endpoints

def main():
    """Main function"""
    print("🚵‍♂️ UCI Calendar Network Analyzer")
    print("=" * 60)
    
    analyzer = UCINetworkAnalyzer()
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not available - skipping traffic capture")
        print("💡 Install with: pip install selenium")
        api_requests = []
    else:
        # Capture network traffic
        api_requests = analyzer.capture_network_traffic()
        
        if api_requests:
            # Test discovered APIs
            successful_apis = analyzer.test_discovered_apis(api_requests)
            
            if successful_apis:
                print(f"\n🏆 Found {len(successful_apis)} working calendar APIs!")
                for api in successful_apis:
                    print(f"   - {api['url']}")
    
    # Try manual discovery regardless
    manual_endpoints = analyzer.manual_api_discovery()
    
    print(f"\n🎯 Summary:")
    print(f"   - Network capture: {len(api_requests)} API-like requests found")
    print(f"   - Manual discovery: {len(manual_endpoints)} working endpoints found")
    
    debug_dir = analyzer.debug_dir
    print(f"\n📁 All results saved to: {debug_dir}")

if __name__ == "__main__":
    main()