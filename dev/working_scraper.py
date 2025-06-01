#!/usr/bin/env python3
"""
Working UCI MTB Calendar Scraper
Parses the actual rendered HTML structure found in the saved page
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def parse_saved_html():
    """Parse the saved UCI HTML to understand the structure"""
    saved_html = Path(__file__).parent.parent / ".claude" / "Mountain Bike calendar _ UCI.html"
    
    if not saved_html.exists():
        print(f"❌ Saved HTML not found at: {saved_html}")
        return []
    
    print(f"📖 Reading saved HTML from: {saved_html}")
    
    with open(saved_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Look for the calendar structure we found
    events = []
    
    # Method 1: Look for competition-card elements (carousel at top)
    competition_cards = soup.find_all('div', class_='competition-card')
    print(f"🎯 Found {len(competition_cards)} competition cards")
    
    for card in competition_cards:
        try:
            # Extract event name
            name_elem = card.find('div', class_='competition-card__name')
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Event"
            
            # Extract dates
            dates_elem = card.find('div', class_='competition-card__dates')
            dates = dates_elem.get_text(strip=True) if dates_elem else "No dates"
            
            # Extract venue
            venue_elem = card.find('div', class_='competition-card__venue')
            venue = venue_elem.get_text(strip=True) if venue_elem else "No venue"
            
            # Extract race hub link
            race_hub_link = None
            hub_link = card.find('a', string=re.compile(r'Race Hub'))
            if hub_link:
                race_hub_link = hub_link.get('href')
            
            # Extract category/discipline
            category_elem = card.find('div', class_='date-and-category__category')
            category = category_elem.get_text(strip=True) if category_elem else "Mountain Bike"
            
            event = {
                'title': name,
                'dates': dates,
                'venue': venue,
                'category': category,
                'race_hub_url': race_hub_link,
                'source': 'competition_card'
            }
            
            events.append(event)
            print(f"   📋 {name[:50]}... | {dates} | {venue}")
            
        except Exception as e:
            print(f"   ❌ Error parsing competition card: {e}")
    
    # Method 2: Look for calendar-item elements (main calendar list)
    calendar_items = soup.find_all('div', class_='calendar-item__title')
    print(f"\n🗓️  Found {len(calendar_items)} calendar items")
    
    for item in calendar_items:
        try:
            # Get the parent container to find related elements
            container = item.parent
            
            # Extract event name
            title_link = item.find('a')
            if title_link:
                name = title_link.get_text(strip=True)
                detail_url = title_link.get('href')
            else:
                continue
            
            # Find location and dates in sibling elements
            location_elem = container.find('div', class_='calendar-item__location')
            location = location_elem.get_text(strip=True) if location_elem else "No location"
            
            dates_elem = container.find('div', class_='calendar-item__dates')
            dates = dates_elem.get_text(strip=True) if dates_elem else "No dates"
            
            # Parse location to extract venue and country
            venue = "Unknown venue"
            country = "Unknown country"
            if location:
                # Location format: "Venue | COUNTRY | REGION"
                parts = [p.strip() for p in location.split('|')]
                if len(parts) >= 2:
                    venue = parts[0]
                    country = parts[1]
            
            event = {
                'title': name,
                'dates': dates,
                'venue': venue,
                'country': country,
                'detail_url': detail_url,
                'source': 'calendar_item'
            }
            
            events.append(event)
            print(f"   📋 {name[:50]}... | {dates} | {venue}")
            
        except Exception as e:
            print(f"   ❌ Error parsing calendar item: {e}")
    
    return events

def parse_dates(date_string):
    """Parse UCI date format into datetime objects"""
    if not date_string or date_string == "No dates":
        return None, None
    
    # Common UCI date patterns:
    # "01 Jun 2025"
    # "30 May - 01 Jun 2025" 
    # "05 Jun - 08 Jun 2025"
    
    try:
        # Single date: "01 Jun 2025"
        single_date_match = re.match(r'(\d{1,2}\s+\w+\s+\d{4})$', date_string.strip())
        if single_date_match:
            date_str = single_date_match.group(1)
            parsed_date = datetime.strptime(date_str, '%d %b %Y')
            return parsed_date, parsed_date
        
        # Date range: "30 May - 01 Jun 2025"
        range_match = re.match(r'(\d{1,2}\s+\w+)\s*-\s*(\d{1,2}\s+\w+\s+\d{4})', date_string.strip())
        if range_match:
            start_part = range_match.group(1)
            end_part = range_match.group(2)
            
            # Extract year from end date
            year_match = re.search(r'\d{4}', end_part)
            if year_match:
                year = year_match.group()
                # Add year to start date if missing
                if year not in start_part:
                    start_part += f' {year}'
            
            start_date = datetime.strptime(start_part, '%d %b %Y')
            end_date = datetime.strptime(end_part, '%d %b %Y')
            return start_date, end_date
        
        print(f"⚠️  Could not parse date: {date_string}")
        return None, None
        
    except Exception as e:
        print(f"❌ Date parsing error for '{date_string}': {e}")
        return None, None

def convert_to_standard_format(events):
    """Convert parsed events to standard format for calendar generation"""
    standard_events = []
    
    for event in events:
        try:
            # Parse dates
            start_date, end_date = parse_dates(event['dates'])
            
            if start_date:
                standard_event = {
                    'title': event['title'],
                    'date': start_date,
                    'end_date': end_date if end_date != start_date else None,
                    'location': event.get('venue', event.get('country', 'Unknown location')),
                    'url': event.get('detail_url') or event.get('race_hub_url'),
                    'country': event.get('country'),
                    'category': event.get('category', 'Mountain Bike'),
                    'source': event['source']
                }
                standard_events.append(standard_event)
            
        except Exception as e:
            print(f"❌ Error converting event: {e}")
    
    return standard_events

def main():
    """Test the working scraper with saved HTML"""
    print("🚵‍♂️ Working UCI MTB Calendar Scraper")
    print("=" * 60)
    
    # Parse the saved HTML
    events = parse_saved_html()
    
    if not events:
        print("❌ No events found in saved HTML")
        return
    
    print(f"\n📊 Total events parsed: {len(events)}")
    
    # Convert to standard format
    standard_events = convert_to_standard_format(events)
    
    print(f"📅 Events with valid dates: {len(standard_events)}")
    
    # Save results
    debug_dir = Path(__file__).parent / "debug"
    debug_dir.mkdir(exist_ok=True)
    
    # Save raw parsed events
    raw_file = debug_dir / 'parsed_events_raw.json'
    with open(raw_file, 'w') as f:
        json.dump(events, f, indent=2, default=str)
    print(f"💾 Saved raw events to: {raw_file}")
    
    # Save standard format events
    standard_file = debug_dir / 'parsed_events_standard.json'
    with open(standard_file, 'w') as f:
        json.dump(standard_events, f, indent=2, default=str)
    print(f"💾 Saved standard events to: {standard_file}")
    
    # Show sample events
    print(f"\n📋 Sample events:")
    for i, event in enumerate(standard_events[:5]):
        date_str = event['date'].strftime('%Y-%m-%d') if event['date'] else 'No date'
        print(f"   {i+1}. {event['title'][:40]}... | {date_str} | {event['location']}")
    
    print(f"\n🎯 Success! Found {len(standard_events)} events with valid dates")
    return standard_events

if __name__ == "__main__":
    main()