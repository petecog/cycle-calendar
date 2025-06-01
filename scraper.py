#!/usr/bin/env python3
"""
UCI MTB Calendar Scraper
Scrapes UCI MTB calendar events and converts them to iCal format
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import logging
from typing import List, Dict, Optional
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UCICalendarScraper:
    def __init__(self):
        self.base_url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_calendar_page(self) -> Optional[str]:
        """Fetch the UCI MTB calendar page"""
        try:
            params = {'discipline': 'MTB'}
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch calendar page: {e}")
            return None
    
    def parse_events(self, html_content: str) -> List[Dict]:
        """Parse events from the HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        events = []
        
        # Look for common calendar event patterns
        # This will need to be adjusted based on actual UCI page structure
        event_containers = soup.find_all(['div', 'tr', 'li'], class_=re.compile(r'event|calendar|race', re.I))
        
        for container in event_containers:
            event = self.extract_event_data(container)
            if event:
                events.append(event)
        
        logger.info(f"Found {len(events)} events")
        return events
    
    def extract_event_data(self, element) -> Optional[Dict]:
        """Extract event data from a DOM element"""
        try:
            # Look for date patterns
            date_text = self.find_text_with_pattern(element, r'\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}-\d{2}-\d{2}')
            
            # Look for event titles/names
            title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'], class_=re.compile(r'title|name|event', re.I))
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Look for location
            location_elem = element.find(text=re.compile(r'location|venue|city|country', re.I))
            location = location_elem.strip() if location_elem else None
            
            if date_text and title:
                return {
                    'title': title,
                    'date': self.parse_date(date_text),
                    'location': location,
                    'url': self.extract_url(element)
                }
        except Exception as e:
            logger.debug(f"Error extracting event data: {e}")
        
        return None
    
    def find_text_with_pattern(self, element, pattern: str) -> Optional[str]:
        """Find text matching a regex pattern within an element"""
        text = element.get_text()
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse date string into datetime object"""
        date_patterns = [
            r'%d/%m/%Y',
            r'%m/%d/%Y', 
            r'%Y-%m-%d',
            r'%d-%m-%Y'
        ]
        
        for pattern in date_patterns:
            try:
                return datetime.strptime(date_text, pattern)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_text}")
        return None
    
    def extract_url(self, element) -> Optional[str]:
        """Extract URL from element"""
        link = element.find('a')
        if link and link.get('href'):
            href = link['href']
            if href.startswith('http'):
                return href
            elif href.startswith('/'):
                return f"https://www.uci.org{href}"
        return None
    
    def scrape_events(self) -> List[Dict]:
        """Main method to scrape all events"""
        logger.info("Starting UCI MTB calendar scrape")
        
        html_content = self.fetch_calendar_page()
        if not html_content:
            return []
        
        events = self.parse_events(html_content)
        
        # Filter out events without dates or in the past
        valid_events = []
        cutoff_date = datetime.now() - timedelta(days=1)
        
        for event in events:
            if event.get('date') and event['date'] > cutoff_date:
                valid_events.append(event)
        
        logger.info(f"Returning {len(valid_events)} valid upcoming events")
        return valid_events

if __name__ == "__main__":
    scraper = UCICalendarScraper()
    events = scraper.scrape_events()
    
    print(f"Found {len(events)} events:")
    for event in events:
        print(f"- {event['title']} on {event['date']} at {event.get('location', 'TBD')}")