#!/usr/bin/env python3
"""
Convert UCI Excel download to iCal format
This gives us clean, structured event data from UCI's official download
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def parse_uci_excel():
    """Parse the UCI Excel file and convert to our standard format"""
    
    claude_dir = Path(__file__).parent.parent / '.claude'
    excel_file = claude_dir / 'UCICompetitions_MTB_2025.xls'
    
    if not excel_file.exists():
        print("❌ Excel file not found")
        return []
    
    print("📊 Parsing UCI Excel file...")
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # The headers are in row 3 (index 3)
        # First few rows contain title and spacing
        header_row = 3
        
        # Get the headers
        headers = df.iloc[header_row].tolist()
        print(f"📋 Headers: {headers}")
        
        # Create clean dataframe with proper headers
        clean_df = df.iloc[header_row + 1:].copy()  # Skip header row
        clean_df.columns = headers
        
        # Remove rows with no event name
        clean_df = clean_df.dropna(subset=['Name'])
        
        print(f"✅ Found {len(clean_df)} events")
        print()
        
        # Show sample data
        print("📖 Sample events:")
        for i, row in clean_df.head(3).iterrows():
            print(f"   {row['Name']} | {row['Date From']} | {row['Venue']}, {row['Country']}")
        print()
        
        # Convert to our standard format
        events = []
        
        for i, row in clean_df.iterrows():
            try:
                # Parse dates
                date_from = pd.to_datetime(row['Date From'], errors='coerce')
                date_to = pd.to_datetime(row['Date To'], errors='coerce')
                
                if pd.isna(date_from):
                    continue  # Skip events without valid start date
                
                # Build location string
                venue = str(row['Venue']) if pd.notna(row['Venue']) else ''
                country = str(row['Country']) if pd.notna(row['Country']) else ''
                location = f"{venue}, {country}" if venue and country else venue or country or 'Unknown location'
                
                # Build event
                event = {
                    'title': str(row['Name']),
                    'date': date_from,
                    'end_date': date_to if pd.notna(date_to) and date_to != date_from else None,
                    'location': location,
                    'venue': venue,
                    'country': country,
                    'category': str(row['Category']) if pd.notna(row['Category']) else 'MTB',
                    'calendar': str(row['Calendar']) if pd.notna(row['Calendar']) else '',
                    'class': str(row['Class']) if pd.notna(row['Class']) else '',
                    'email': str(row['EMail']) if pd.notna(row['EMail']) else '',
                    'url': str(row['Website']) if pd.notna(row['Website']) else '',
                    'source': 'uci_excel'
                }
                
                events.append(event)
                
            except Exception as e:
                print(f"⚠️  Error parsing row {i}: {e}")
                continue
        
        print(f"🎯 Successfully converted {len(events)} events")
        
        # Filter for upcoming events
        now = datetime.now()
        upcoming_events = [e for e in events if e['date'] >= now]
        
        print(f"📅 {len(upcoming_events)} upcoming events")
        
        # Save for analysis
        debug_dir = Path(__file__).parent / 'debug'
        debug_dir.mkdir(exist_ok=True)
        
        # Convert dates to strings for JSON
        events_json = []
        for event in events:
            event_json = event.copy()
            event_json['date'] = event['date'].strftime('%Y-%m-%d') if event['date'] else None
            event_json['end_date'] = event['end_date'].strftime('%Y-%m-%d') if event['end_date'] else None
            events_json.append(event_json)
        
        with open(debug_dir / 'uci_excel_events.json', 'w') as f:
            json.dump(events_json, f, indent=2)
        
        print(f"💾 Saved events to {debug_dir}/uci_excel_events.json")
        
        return events
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def create_ical_from_excel():
    """Create iCal file from Excel data"""
    
    events = parse_uci_excel()
    if not events:
        print("❌ No events to process")
        return False
    
    print(f"\n🔧 Creating iCal from {len(events)} events...")
    
    try:
        from uci_calendar import CalendarGenerator
        
        generator = CalendarGenerator()
        generator.events = events
        
        debug_dir = Path(__file__).parent / 'debug' / 'generated_calendars'
        debug_dir.mkdir(parents=True, exist_ok=True)
        output_file = debug_dir / 'uci_excel_calendar.ics'
        if generator.generate_ical_file(str(output_file)):
            print(f"✅ Generated {output_file}")
            
            # Show some stats
            upcoming = [e for e in events if e['date'] >= datetime.now()]
            print(f"📊 Statistics:")
            print(f"   Total events: {len(events)}")
            print(f"   Upcoming: {len(upcoming)}")
            
            # Show countries
            countries = set(e['country'] for e in events if e['country'])
            print(f"   Countries: {len(countries)} ({', '.join(sorted(list(countries))[:5])}...)")
            
            return True
        else:
            print("❌ Failed to generate iCal")
            return False
            
    except Exception as e:
        print(f"❌ Error creating iCal: {e}")
        return False

if __name__ == "__main__":
    print("🎯 UCI Excel to iCal Converter")
    print("=" * 40)
    
    success = create_ical_from_excel()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("✅ Excel data successfully converted to iCal format")
        print("💡 This approach bypasses all dynamic loading issues!")
    else:
        print("\n❌ Conversion failed")
        print("📝 Check error messages above")