#!/usr/bin/env python3
"""
Direct iCal generator for UCI Excel data
Creates iCal calendar directly from the Excel events
"""

import sys
from pathlib import Path
import json
from datetime import datetime
from icalendar import Calendar, Event, vText

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def create_ical_from_json():
    """Create iCal directly from the parsed JSON events"""
    
    debug_dir = Path(__file__).parent / 'debug'
    json_file = debug_dir / 'uci_excel_events.json'
    
    if not json_file.exists():
        print("❌ JSON events file not found")
        print("💡 Run excel_to_ical.py first to parse the Excel file")
        return False
    
    print("📋 Loading events from JSON...")
    
    with open(json_file, 'r') as f:
        events_data = json.load(f)
    
    print(f"✅ Loaded {len(events_data)} events")
    
    # Filter for upcoming events only
    now = datetime.now()
    upcoming_events = []
    
    for event in events_data:
        try:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if event_date >= now:
                upcoming_events.append(event)
        except:
            continue
    
    print(f"📅 {len(upcoming_events)} upcoming events")
    
    # Create calendar
    cal = Calendar()
    cal.add('prodid', '-//UCI MTB Calendar//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'UCI MTB Calendar 2025')
    cal.add('x-wr-caldesc', 'UCI Mountain Bike Events from Excel Download')
    
    added_events = 0
    
    for event_data in upcoming_events:
        try:
            event = Event()
            
            # Basic event info
            event.add('summary', event_data['title'])
            
            # Build comprehensive description with all UCI fields
            description_parts = []
            description_parts.append(f"Venue: {event_data['venue']}")
            description_parts.append(f"Country: {event_data['country']}")
            description_parts.append(f"Calendar: {event_data['calendar']}")
            description_parts.append(f"Class: {event_data['class']}")
            
            if event_data['email'] and event_data['email'] != 'nan':
                description_parts.append(f"Email: {event_data['email']}")
            
            if event_data['url'] and event_data['url'] != 'nan':
                description_parts.append(f"Website: {event_data['url']}")
            
            description_parts.append("\\nSource: UCI Excel Download")
            
            event.add('description', "\\n".join(description_parts))
            
            # Date handling
            start_date = datetime.strptime(event_data['date'], '%Y-%m-%d').date()
            event.add('dtstart', start_date)
            
            if event_data['end_date']:
                end_date = datetime.strptime(event_data['end_date'], '%Y-%m-%d').date()
                event.add('dtend', end_date)
            else:
                event.add('dtend', start_date)
            
            # Location
            event.add('location', event_data['location'])
            
            # URL if available
            if event_data['url'] and event_data['url'] != 'nan':
                event.add('url', event_data['url'])
            
            # Unique ID
            event.add('uid', f"uci-mtb-{event_data['date']}-{hash(event_data['title'])}")
            
            # Add to calendar
            cal.add_component(event)
            added_events += 1
            
        except Exception as e:
            print(f"⚠️  Error adding event '{event_data.get('title', 'Unknown')}': {e}")
            continue
    
    print(f"✅ Added {added_events} events to calendar")
    
    # Save calendar to debug folder
    debug_dir = Path(__file__).parent / 'debug' / 'generated_calendars'
    debug_dir.mkdir(parents=True, exist_ok=True)
    output_file = debug_dir / 'uci_mtb_2025.ics'
    
    try:
        with open(output_file, 'wb') as f:
            f.write(cal.to_ical())
        
        # Check file size
        file_size = Path(output_file).stat().st_size
        print(f"💾 Saved to {output_file} ({file_size:,} bytes)")
        
        # Show sample events
        print("\\n📋 Sample upcoming events:")
        for i, event in enumerate(upcoming_events[:5], 1):
            print(f"   {i}. {event['title']}")
            print(f"      📅 {event['date']} | 📍 {event['location']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving calendar: {e}")
        return False

def analyze_event_types():
    """Analyze the types of events in our dataset"""
    
    debug_dir = Path(__file__).parent / 'debug'
    json_file = debug_dir / 'uci_excel_events.json'
    
    with open(json_file, 'r') as f:
        events_data = json.load(f)
    
    print("\\n📊 Event Analysis:")
    print("=" * 30)
    
    # Analyze by class
    classes = {}
    for event in events_data:
        cls = event.get('class', 'Unknown')
        classes[cls] = classes.get(cls, 0) + 1
    
    print("🏆 Event Classes:")
    for cls, count in sorted(classes.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cls}: {count} events")
    
    # Analyze by calendar type
    calendars = {}
    for event in events_data:
        cal = event.get('calendar', 'Unknown')
        calendars[cal] = calendars.get(cal, 0) + 1
    
    print("\\n📅 Calendar Types:")
    for cal, count in sorted(calendars.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cal}: {count} events")
    
    # Look for your preferred event types
    preferred_types = ['DHI', 'END', 'XCO', 'XCC', 'XCM', 'XCE']
    matching_events = []
    
    for event in events_data:
        title = event['title'].upper()
        if any(ptype in title for ptype in preferred_types):
            matching_events.append(event)
    
    print(f"\\n🎯 Events matching preferred types: {len(matching_events)}")
    if matching_events:
        print("Sample matches:")
        for event in matching_events[:5]:
            print(f"   • {event['title']} | {event['date']}")

if __name__ == "__main__":
    print("🏆 UCI MTB Calendar Generator (Direct)")
    print("=" * 50)
    
    success = create_ical_from_json()
    
    if success:
        analyze_event_types()
        print("\\n🎉 SUCCESS!")
        print("✅ UCI MTB calendar created from Excel data")
        print("🔗 Subscribe to uci_mtb_2025.ics in your calendar app")
    else:
        print("\\n❌ Failed to create calendar")