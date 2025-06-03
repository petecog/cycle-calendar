#!/usr/bin/env python3
"""
iCal Calendar Generator
Converts UCI MTB events to iCal format
"""

from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import uuid
import logging
from typing import List, Dict
# Excel parser is the primary data source

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalendarGenerator:
    def __init__(self):
        self.timezone = pytz.UTC
        self.events = []  # Allow setting events directly
        
    def create_calendar(self, events: List[Dict]) -> Calendar:
        """Create an iCal calendar from event data"""
        cal = Calendar()
        
        # Calendar metadata
        cal.add('prodid', '-//UCI MTB Calendar Sync//uci-mtb-sync//EN')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', 'UCI MTB Calendar')
        cal.add('x-wr-caldesc', 'UCI Mountain Bike Calendar Events')
        cal.add('x-wr-timezone', 'UTC')
        
        # Add events
        for event_data in events:
            event = self.create_event(event_data)
            if event:
                cal.add_component(event)
        
        logger.info(f"Created calendar with {len(events)} events")
        return cal
    
    def create_event(self, event_data: Dict) -> Event:
        """Create an iCal event from event data"""
        try:
            event = Event()
            
            # Required fields
            event.add('uid', str(uuid.uuid4()))
            event.add('dtstamp', datetime.now(self.timezone))
            
            # Event details
            event.add('summary', event_data['title'])
            
            # Handle date - assume all-day event if no time specified
            event_date = event_data['date']
            if isinstance(event_date, datetime):
                if event_date.time() == event_date.time().min:
                    # All-day event
                    event.add('dtstart', event_date.date())
                    event.add('dtend', (event_date + timedelta(days=1)).date())
                else:
                    # Timed event
                    event_date = self.timezone.localize(event_date) if event_date.tzinfo is None else event_date
                    event.add('dtstart', event_date)
                    event.add('dtend', event_date + timedelta(hours=3))  # Default 3-hour duration
            
            # Handle end date for multi-day events
            if event_data.get('end_date'):
                end_date = event_data['end_date']
                if isinstance(end_date, datetime):
                    if end_date.time() == end_date.time().min:
                        # For all-day events, iCal DTEND should be one day after the last day (exclusive)
                        event.add('dtend', (end_date + timedelta(days=1)).date())
                    else:
                        end_date = self.timezone.localize(end_date) if end_date.tzinfo is None else end_date
                        event.add('dtend', end_date)
            
            # Optional fields
            if event_data.get('location'):
                event.add('location', event_data['location'])
            
            if event_data.get('url'):
                event.add('url', event_data['url'])
            
            # Build comprehensive description for Excel-sourced events
            description_parts = []
            
            # Basic info
            if event_data.get('venue') and event_data['venue'] != event_data.get('location', ''):
                description_parts.append(f"Venue: {event_data['venue']}")
            
            if event_data.get('country'):
                description_parts.append(f"Country: {event_data['country']}")
            
            # UCI-specific fields
            if event_data.get('calendar'):
                description_parts.append(f"Calendar: {event_data['calendar']}")
            
            if event_data.get('class'):
                description_parts.append(f"Class: {event_data['class']}")
            
            if event_data.get('email'):
                description_parts.append(f"Email: {event_data['email']}")
            
            if event_data.get('url'):
                description_parts.append(f"Website: {event_data['url']}")
            
            # Add source info
            if event_data.get('source'):
                description_parts.append(f"\nSource: {event_data['source']}")
            
            if description_parts:
                event.add('description', "\n".join(description_parts))
            elif event_data.get('url'):
                event.add('description', f"More info: {event_data['url']}")
            
            # Add categories
            categories = ['MTB', 'Cycling', 'UCI']
            if event_data.get('category'):
                categories.append(event_data['category'])
            event.add('categories', categories)
            
            return event
            
        except Exception as e:
            logger.error(f"Error creating event for {event_data.get('title', 'Unknown')}: {e}")
            return None
    
    def generate_ical_file(self, filename: str = 'calendar.ics') -> bool:
        """Generate complete iCal file from UCI events"""
        try:
            # Use pre-set events (must be provided externally)
            events = self.events
            
            if not events:
                logger.warning("No events provided, creating empty calendar")
                events = []
            
            # Create calendar
            calendar = self.create_calendar(events)
            
            # Write to file
            with open(filename, 'wb') as f:
                f.write(calendar.to_ical())
            
            logger.info(f"Successfully generated {filename} with {len(events)} events")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate calendar file: {e}")
            return False

def main():
    """Main function to generate calendar"""
    generator = CalendarGenerator()
    success = generator.generate_ical_file()
    
    if success:
        print("✅ Calendar generated successfully!")
        print("📅 File: calendar.ics")
    else:
        print("❌ Failed to generate calendar")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())