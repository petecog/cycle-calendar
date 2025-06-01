"""
UCI MTB Calendar Scraper Package

A package for scraping UCI MTB calendar events and generating calendar files.
"""

from .scraper import UCICalendarScraper
from .calendar_generator import CalendarGenerator
from .html_generator import HTMLGenerator

__version__ = "1.0.0"
__author__ = "UCI MTB Calendar Sync"

# Package-level convenience functions
def scrape_events():
    """Convenience function to scrape events using default scraper"""
    scraper = UCICalendarScraper()
    return scraper.scrape_events()

def generate_ical(filename='calendar.ics'):
    """Convenience function to generate iCal file"""
    generator = CalendarGenerator()
    return generator.generate_ical_file(filename)

def generate_html(filename='debug.html'):
    """Convenience function to generate HTML debug view"""
    generator = HTMLGenerator()
    return generator.generate_html_calendar(filename)

__all__ = [
    'UCICalendarScraper',
    'CalendarGenerator', 
    'HTMLGenerator',
    'scrape_events',
    'generate_ical',
    'generate_html'
]