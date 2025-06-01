#!/usr/bin/env python3
"""
Extract API configuration from UCI calendar page
Looks for webSettings and other API endpoint configurations
"""

import sys
import json
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def extract_web_settings():
    """Extract the webSettings JavaScript object from UCI page"""
    print("🔍 Extracting API configuration from UCI calendar page")
    print("=" * 60)
    
    try:
        url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all script tags
        scripts = soup.find_all('script')
        
        web_settings = None
        api_endpoints = []
        
        for script in scripts:
            if script.string:
                content = script.string
                
                # Look for webSettings object
                if 'webSettings' in content:
                    print("✅ Found webSettings in script!")
                    
                    # Try to extract the complete webSettings object
                    match = re.search(r'const webSettings = ({.*?});', content, re.DOTALL)
                    if match:
                        try:
                            settings_json = match.group(1)
                            web_settings = json.loads(settings_json)
                            print(f"📊 Successfully parsed webSettings with {len(web_settings)} keys")
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON parse error: {e}")
                            print("📝 Raw webSettings string (first 500 chars):")
                            print(settings_json[:500])
                
                # Look for API endpoint patterns
                api_patterns = [
                    r'["\']https?://[^"\']*api[^"\']*["\']',
                    r'["\']https?://[^"\']*calendar[^"\']*["\']',
                    r'["\']https?://[^"\']*event[^"\']*["\']',
                    r'["\']\/api\/[^"\']*["\']',
                    r'["\']\/calendar\/[^"\']*["\']'
                ]
                
                for pattern in api_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Clean up quotes
                        endpoint = match.strip('\'"')
                        if endpoint not in api_endpoints:
                            api_endpoints.append(endpoint)
        
        # Save debug files
        debug_dir = Path(__file__).parent / "debug"
        debug_dir.mkdir(exist_ok=True)
        
        if web_settings:
            settings_file = debug_dir / 'web_settings.json'
            with open(settings_file, 'w') as f:
                json.dump(web_settings, f, indent=2)
            print(f"💾 Saved webSettings to: {settings_file}")
            
            # Print interesting keys
            print(f"\n🔑 webSettings keys:")
            for key in web_settings.keys():
                print(f"   - {key}")
        
        if api_endpoints:
            endpoints_file = debug_dir / 'api_endpoints.json'
            with open(endpoints_file, 'w') as f:
                json.dump({
                    'timestamp': str(datetime.now()),
                    'endpoints': api_endpoints
                }, f, indent=2)
            print(f"💾 Saved {len(api_endpoints)} API endpoints to: {endpoints_file}")
            
            print(f"\n🌐 Found API endpoints:")
            for endpoint in api_endpoints:
                print(f"   - {endpoint}")
        
        return web_settings, api_endpoints
        
    except Exception as e:
        print(f"💥 Error extracting configuration: {e}")
        import traceback
        traceback.print_exc()
        return None, []

def test_api_endpoints(endpoints, web_settings):
    """Test discovered API endpoints"""
    print(f"\n🧪 Testing {len(endpoints)} API endpoints")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    base_url = web_settings.get('baseUrl', 'https://www.uci.org/') if web_settings else 'https://www.uci.org/'
    
    results = []
    
    for endpoint in endpoints[:5]:  # Test first 5 endpoints
        try:
            # Make endpoint absolute if relative
            if endpoint.startswith('/'):
                full_url = base_url.rstrip('/') + endpoint
            else:
                full_url = endpoint
            
            print(f"🔗 Testing: {full_url}")
            
            response = requests.get(full_url, headers=headers, timeout=10)
            
            result = {
                'endpoint': endpoint,
                'full_url': full_url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', 'unknown'),
                'size': len(response.text),
                'success': response.status_code == 200
            }
            
            if response.status_code == 200:
                print(f"   ✅ {response.status_code} - {result['content_type']} - {result['size']} bytes")
                
                # Check if response looks like calendar data
                if any(keyword in response.text.lower() for keyword in ['event', 'calendar', 'date', 'race']):
                    result['likely_calendar_data'] = True
                    print("   🎯 Response contains calendar-related content!")
            else:
                print(f"   ❌ {response.status_code}")
            
            results.append(result)
            
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    # Save test results
    debug_dir = Path(__file__).parent / "debug"
    results_file = debug_dir / 'endpoint_test_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Saved test results to: {results_file}")
    
    return results

def main():
    """Main function"""
    from datetime import datetime
    
    print("🚵‍♂️ UCI API Configuration Extractor")
    print("=" * 60)
    
    # Extract configuration
    web_settings, endpoints = extract_web_settings()
    
    if endpoints:
        # Test the endpoints
        results = test_api_endpoints(endpoints, web_settings)
        
        # Summarize findings
        successful_endpoints = [r for r in results if r.get('success')]
        calendar_endpoints = [r for r in results if r.get('likely_calendar_data')]
        
        print(f"\n🎯 Summary:")
        print(f"   - Found {len(endpoints)} potential API endpoints")
        print(f"   - {len(successful_endpoints)} endpoints responded successfully")
        print(f"   - {len(calendar_endpoints)} endpoints contain calendar-related data")
        
        if calendar_endpoints:
            print(f"\n🏆 Promising calendar endpoints:")
            for result in calendar_endpoints:
                print(f"   - {result['full_url']}")
    else:
        print("❌ No API endpoints found")
    
    debug_dir = Path(__file__).parent / "debug"
    print(f"\n📁 Debug files saved to: {debug_dir}")

if __name__ == "__main__":
    main()