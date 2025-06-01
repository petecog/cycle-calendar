"""
UCI MTB Calendar Scraper Package

A package for scraping UCI MTB calendar events and generating calendar files.
"""

# Scraper temporarily disabled - Excel parsing is primary data source
# from .scraper import UCICalendarScraper
from .calendar_generator import CalendarGenerator
from .html_generator import HTMLGenerator
from .excel_parser import UCIExcelParser
from .browser_downloader import UCIBrowserDownloader, download_uci_year, download_uci_bulk

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

async def download_uci_excel(year_or_years, output_dir=None, headless=True):
    """
    Convenience function to download UCI Excel files using browser automation
    
    Args:
        year_or_years: Single year string or list of years
        output_dir: Directory to save files
        headless: Whether to run browser in headless mode
        
    Returns:
        True/dict depending on single year or multiple years
    """
    if isinstance(year_or_years, str):
        return await download_uci_year(year_or_years, output_dir, headless)
    else:
        return await download_uci_bulk(year_or_years, output_dir, headless)

__all__ = [
    # 'UCICalendarScraper',  # Disabled - Excel parsing is primary
    'CalendarGenerator', 
    'HTMLGenerator',
    'UCIExcelParser',
    'UCIBrowserDownloader',
    'parse_excel_events',
    'generate_ical',
    'generate_html',
    'download_uci_excel',
    'download_uci_year',
    'download_uci_bulk'
]