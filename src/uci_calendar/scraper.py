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
    
    def parse_competition_cards(self, soup):
        """Parse competition-card elements from carousel"""
        events = []
        competition_cards = soup.find_all('div', class_='competition-card')
        
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
                
                event = {
                    'title': name,
                    'dates': dates,
                    'venue': venue,
                    'race_hub_url': race_hub_link,
                    'source': 'competition_card'
                }
                
                events.append(event)
                
            except Exception as e:
                logger.debug(f"Error parsing competition card: {e}")
        
        return events
    
    def parse_calendar_items(self, soup):
        """Parse calendar-item elements from main list"""
        events = []
        calendar_items = soup.find_all('div', class_='calendar-item__title')
        
        for item in calendar_items:
            try:
                # Get the parent container
                container = item.parent
                
                # Extract event name and URL
                title_link = item.find('a')
                if not title_link:
                    continue
                    
                name = title_link.get_text(strip=True)
                detail_url = title_link.get('href')
                
                # Find location and dates in sibling elements
                location_elem = container.find('div', class_='calendar-item__location')
                location = location_elem.get_text(strip=True) if location_elem else "No location"
                
                dates_elem = container.find('div', class_='calendar-item__dates')
                dates = dates_elem.get_text(strip=True) if dates_elem else "No dates"
                
                # Parse location: "Venue | COUNTRY | REGION"
                venue = "Unknown venue"
                country = "Unknown country"
                if location:
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
                
            except Exception as e:
                logger.debug(f"Error parsing calendar item: {e}")
        
        return events
    
    def parse_uci_dates(self, date_string):
        """Parse UCI date format into datetime objects"""
        if not date_string or date_string == "No dates":
            return None, None
        
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
                
                # Extract year from end date and add to start if missing
                year_match = re.search(r'\d{4}', end_part)
                if year_match:
                    year = year_match.group()
                    if year not in start_part:
                        start_part += f' {year}'
                
                start_date = datetime.strptime(start_part, '%d %b %Y')
                end_date = datetime.strptime(end_part, '%d %b %Y')
                return start_date, end_date
            
            return None, None
            
        except Exception as e:
            logger.debug(f"Date parsing error for '{date_string}': {e}")
            return None, None
    
    def parse_events(self, html_content: str) -> List[Dict]:
        """Parse events from the HTML content using multiple strategies"""
        soup = BeautifulSoup(html_content, 'html.parser')
        all_events = []
        
        # Strategy 1: Parse competition cards (featured events in carousel)
        competition_events = self.parse_competition_cards(soup)
        all_events.extend(competition_events)
        logger.info(f"Found {len(competition_events)} competition card events")
        
        # Strategy 2: Parse calendar items (full calendar list)
        calendar_events = self.parse_calendar_items(soup)
        all_events.extend(calendar_events)
        logger.info(f"Found {len(calendar_events)} calendar item events")
        
        # Convert to standard format
        standard_events = []
        for event in all_events:
            try:
                start_date, end_date = self.parse_uci_dates(event['dates'])
                
                if start_date:
                    standard_event = {
                        'title': event['title'],
                        'date': start_date,
                        'end_date': end_date if end_date != start_date else None,
                        'location': event.get('venue', event.get('country', 'Unknown location')),
                        'url': event.get('detail_url') or event.get('race_hub_url'),
                        'country': event.get('country'),
                        'category': event.get('category', 'Mountain Bike')
                    }
                    standard_events.append(standard_event)
                    
            except Exception as e:
                logger.debug(f"Error converting event: {e}")
        
        logger.info(f"Converted {len(standard_events)} events with valid dates")
        return standard_events
    
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