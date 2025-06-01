#!/usr/bin/env python3
"""
UCI Excel Parser Module
Parses UCI MTB calendar data from Excel downloads
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class UCIExcelParser:
    """Parser for UCI MTB calendar Excel files"""
    
    def __init__(self):
        self.events = []
    
    def parse_excel_file(self, file_path: str) -> List[Dict]:
        """
        Parse UCI Excel file and return list of events
        
        Args:
            file_path: Path to the UCI Excel file
            
        Returns:
            List of event dictionaries
        """
        
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"Excel file not found: {file_path}")
            return []
        
        logger.info(f"Parsing UCI Excel file: {file_path}")
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # The headers are in row 3 (index 3)
            # First few rows contain title and spacing
            header_row = 3
            
            # Get the headers
            headers = df.iloc[header_row].tolist()
            logger.debug(f"Headers: {headers}")
            
            # Create clean dataframe with proper headers
            clean_df = df.iloc[header_row + 1:].copy()  # Skip header row
            clean_df.columns = headers
            
            # Remove rows with no event name
            clean_df = clean_df.dropna(subset=['Name'])
            
            logger.info(f"Found {len(clean_df)} events in Excel file")
            
            # Convert to our standard format
            events = []
            
            for i, row in clean_df.iterrows():
                try:
                    event = self._parse_event_row(row)
                    if event:
                        events.append(event)
                        
                except Exception as e:
                    logger.warning(f"Error parsing row {i}: {e}")
                    continue
            
            logger.info(f"Successfully converted {len(events)} events")
            self.events = events
            return events
            
        except Exception as e:
            logger.error(f"Error parsing Excel file: {e}")
            return []
    
    def _parse_event_row(self, row) -> Optional[Dict]:
        """Parse a single event row from the Excel data"""
        
        try:
            # Parse dates - UCI Excel uses US format (MM/DD/YYYY)
            # Force US format parsing to avoid ambiguity with dayfirst=False
            # This ensures 01/06/2025 is parsed as January 6th, not June 1st
            date_from = pd.to_datetime(row['Date From'], format='mixed', dayfirst=False, errors='coerce')
            date_to = pd.to_datetime(row['Date To'], format='mixed', dayfirst=False, errors='coerce')
            
            if pd.isna(date_from):
                return None  # Skip events without valid start date
            
            # Build location string
            venue = str(row['Venue']) if pd.notna(row['Venue']) else ''
            country = str(row['Country']) if pd.notna(row['Country']) else ''
            location = f"{venue}, {country}" if venue and country else venue or country or 'Unknown location'
            
            # Clean up fields
            def clean_field(field):
                """Clean field value, handling NaN and 'nan' strings"""
                if pd.isna(field) or str(field).lower() == 'nan':
                    return ''
                return str(field).strip()
            
            # Build event
            event = {
                'title': clean_field(row['Name']),
                'date': date_from,
                'end_date': date_to if pd.notna(date_to) and date_to != date_from else None,
                'location': location,
                'venue': clean_field(row['Venue']),
                'country': clean_field(row['Country']),
                'category': clean_field(row['Category']) or 'MTB',
                'calendar': clean_field(row['Calendar']),
                'class': clean_field(row['Class']),
                'email': clean_field(row['EMail']),
                'url': clean_field(row['Website']),
                'source': 'uci_excel'
            }
            
            return event
            
        except Exception as e:
            logger.debug(f"Error parsing event row: {e}")
            return None
    
    def get_upcoming_events(self, from_date: Optional[datetime] = None) -> List[Dict]:
        """
        Get upcoming events from the parsed data
        
        Args:
            from_date: Start date filter (defaults to today)
            
        Returns:
            List of upcoming events
        """
        
        if from_date is None:
            from_date = datetime.now()
        
        upcoming = [e for e in self.events if e['date'] >= from_date]
        
        logger.info(f"Found {len(upcoming)} upcoming events from {from_date.date()}")
        return upcoming
    
    def filter_events(self, **criteria) -> List[Dict]:
        """
        Filter events by criteria
        
        Args:
            **criteria: Filter criteria (country, class, calendar, etc.)
            
        Returns:
            Filtered list of events
        """
        
        filtered = self.events.copy()
        
        for key, value in criteria.items():
            if key in ['country', 'class', 'calendar', 'category']:
                filtered = [e for e in filtered if e.get(key, '').upper() == str(value).upper()]
        
        logger.info(f"Filtered to {len(filtered)} events with criteria: {criteria}")
        return filtered
    
    def get_event_stats(self) -> Dict:
        """Get statistics about the parsed events"""
        
        if not self.events:
            return {}
        
        stats = {
            'total_events': len(self.events),
            'upcoming_events': len(self.get_upcoming_events()),
            'countries': len(set(e['country'] for e in self.events if e['country'])),
            'classes': list(set(e['class'] for e in self.events if e['class'])),
            'calendars': list(set(e['calendar'] for e in self.events if e['calendar'])),
            'date_range': {
                'earliest': min(e['date'] for e in self.events).date(),
                'latest': max(e['date'] for e in self.events).date()
            }
        }
        
        return stats