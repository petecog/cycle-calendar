#!/usr/bin/env python3
"""
Test the UCI Calendar package structure
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_package_imports():
    """Test that all package imports work"""
    print("🧪 Testing UCI Calendar Package")
    print("=" * 40)
    
    try:
        # Test main package import
        import uci_calendar
        print(f"✅ Package import: uci_calendar v{uci_calendar.__version__}")
        
        # Test individual imports
        from uci_calendar import UCICalendarScraper, CalendarGenerator, HTMLGenerator
        print("✅ Individual imports: UCICalendarScraper, CalendarGenerator, HTMLGenerator")
        
        # Test convenience functions
        from uci_calendar import scrape_events, generate_ical, generate_html
        print("✅ Convenience functions: scrape_events, generate_ical, generate_html")
        
        # Test instantiation
        scraper = UCICalendarScraper()
        cal_gen = CalendarGenerator()
        html_gen = HTMLGenerator()
        print("✅ Object instantiation successful")
        
        print("\n🎯 Package structure verified!")
        return True
        
    except Exception as e:
        print(f"❌ Package test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quick_scrape():
    """Test a quick scrape operation"""
    print("\n🔍 Testing Quick Scrape")
    print("=" * 40)
    
    try:
        from uci_calendar import scrape_events
        
        print("🌐 Attempting to scrape events...")
        events = scrape_events()
        print(f"📊 Found {len(events)} events")
        
        if events:
            print("📋 Sample events:")
            for event in events[:3]:
                print(f"   - {event}")
        else:
            print("ℹ️  No events found (may be expected)")
        
        return True
        
    except Exception as e:
        print(f"❌ Scrape test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚵‍♂️ UCI MTB Calendar Package Test")
    print("=" * 50)
    
    success = True
    success &= test_package_imports()
    success &= test_quick_scrape()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All package tests passed!")
    else:
        print("❌ Some tests failed")
    
    print("\n💡 To run detailed scraper debugging:")
    print("   python dev/debug_scraper.py")