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
from .scraper import UCICalendarScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalendarGenerator:
    def __init__(self):
        self.timezone = pytz.UTC
        
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
            
            # Optional fields
            if event_data.get('location'):
                event.add('location', event_data['location'])
            
            if event_data.get('url'):
                event.add('url', event_data['url'])
                event.add('description', f"More info: {event_data['url']}")
            
            # Add categories
            event.add('categories', ['MTB', 'Cycling', 'UCI'])
            
            return event
            
        except Exception as e:
            logger.error(f"Error creating event for {event_data.get('title', 'Unknown')}: {e}")
            return None
    
    def generate_ical_file(self, filename: str = 'calendar.ics') -> bool:
        """Generate complete iCal file from UCI events"""
        try:
            # Scrape events
            scraper = UCICalendarScraper()
            events = scraper.scrape_events()
            
            if not events:
                logger.warning("No events found, creating empty calendar")
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