"""
UCI MTB Calendar Scraper Package

A package for scraping UCI MTB calendar events and generating calendar files.
"""

from .scraper import UCICalendarScraper
from .calendar_generator import CalendarGenerator
from .html_generator import HTMLGenerator
from .excel_parser import UCIExcelParser

__version__ = "1.0.0"
__author__ = "UCI MTB Calendar Sync"

# Package-level convenience functions
def parse_excel_events(excel_file_path):
    """Convenience function to parse events from Excel file"""
    parser = UCIExcelParser()
    return parser.parse_excel_file(excel_file_path)

def generate_ical(events, filename='calendar.ics'):
    """Convenience function to generate iCal file from events"""
    generator = CalendarGenerator()
    generator.events = events
    return generator.generate_ical_file(filename)

def generate_html(filename='debug.html'):
    """Convenience function to generate HTML debug view"""
    generator = HTMLGenerator()
    return generator.generate_html_calendar(filename)

__all__ = [
    'UCICalendarScraper',
    'CalendarGenerator', 
    'HTMLGenerator',
    'UCIExcelParser',
    'parse_excel_events',
    'generate_ical',
    'generate_html'
]