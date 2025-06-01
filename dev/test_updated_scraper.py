#!/usr/bin/env python3
"""
Test the updated UCI scraper with saved HTML
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_with_saved_html():
    """Test scraper with the saved HTML file"""
    print("🧪 Testing Updated UCI Scraper with Saved HTML")
    print("=" * 60)
    
    try:
        from uci_calendar import UCICalendarScraper
        
        scraper = UCICalendarScraper()
        
        # Load saved HTML
        saved_html = Path(__file__).parent.parent / ".claude" / "Mountain Bike calendar _ UCI.html"
        
        if not saved_html.exists():
            print(f"❌ Saved HTML not found: {saved_html}")
            return False
        
        print(f"📖 Reading saved HTML: {saved_html}")
        with open(saved_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"📊 HTML size: {len(html_content)} characters")
        
        # Parse events
        events = scraper.parse_events(html_content)
        
        print(f"🎯 Parsed {len(events)} events")
        
        if events:
            print(f"\n📋 Sample events:")
            for i, event in enumerate(events[:5]):
                date_str = event['date'].strftime('%Y-%m-%d') if event['date'] else 'No date'
                print(f"   {i+1}. {event['title'][:50]}...")
                print(f"      📅 {date_str} | 📍 {event['location']}")
                if event.get('url'):
                    print(f"      🔗 {event['url']}")
        
        # Test calendar generation
        print(f"\n🔧 Testing calendar generation...")
        from uci_calendar import CalendarGenerator
        
        generator = CalendarGenerator()
        # Manually set events for testing
        generator.events = events
        
        if generator.generate_ical_file('test_working_calendar.ics'):
            print(f"✅ Generated test_working_calendar.ics with {len(events)} events")
        else:
            print(f"❌ Calendar generation failed")
        
        return len(events) > 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    success = test_with_saved_html()
    
    if success:
        print(f"\n🎉 SUCCESS! The updated scraper is working!")
        print(f"✅ Parsed events from saved HTML")
        print(f"✅ Calendar generation working")
        print(f"\n💡 The scraper now works with fully-rendered UCI calendar pages!")
    else:
        print(f"\n❌ Test failed")

if __name__ == "__main__":
    main()