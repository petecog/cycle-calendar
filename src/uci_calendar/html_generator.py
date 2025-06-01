#!/usr/bin/env python3
"""
HTML Calendar Generator
Creates an HTML page displaying UCI MTB calendar events for debugging and quick reference
"""

from datetime import datetime
import json
import logging
from typing import List, Dict
from .scraper import UCICalendarScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLGenerator:
    def __init__(self):
        self.template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UCI MTB Calendar - Debug View</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #0066cc;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .events-grid {
            display: grid;
            gap: 20px;
        }
        .event-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s;
        }
        .event-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        .event-header {
            background: linear-gradient(135deg, #0066cc, #004499);
            color: white;
            padding: 20px;
        }
        .event-title {
            font-size: 1.3em;
            font-weight: bold;
            margin: 0;
        }
        .event-date {
            font-size: 1.1em;
            margin-top: 8px;
            opacity: 0.9;
        }
        .event-body {
            padding: 20px;
        }
        .event-location {
            font-size: 1.1em;
            color: #666;
            margin-bottom: 10px;
        }
        .event-url {
            margin-top: 15px;
        }
        .event-url a {
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
        }
        .event-url a:hover {
            text-decoration: underline;
        }
        .no-events {
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 8px;
            color: #666;
        }
        .last-updated {
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
        }
        .debug-info {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .debug-title {
            font-weight: bold;
            color: #856404;
            margin-bottom: 10px;
        }
        .nav-links {
            text-align: center;
            margin-bottom: 20px;
        }
        .nav-links a {
            display: inline-block;
            margin: 0 10px;
            padding: 10px 20px;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
        }
        .nav-links a:hover {
            background: #0052a3;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚵‍♂️ UCI MTB Calendar - Debug View</h1>
        <p>Real-time view of scraped UCI Mountain Bike calendar events</p>
    </div>
    
    <div class="nav-links">
        <a href="index.html">← Back to Main</a>
        <a href="calendar.ics" download>📥 Download iCal</a>
    </div>
    
    <div class="debug-info">
        <div class="debug-title">🔧 Debug Information</div>
        <div><strong>Last Updated:</strong> {last_updated}</div>
        <div><strong>Source:</strong> <a href="https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB" target="_blank">UCI MTB Calendar</a></div>
        <div><strong>Calendar URL:</strong> <a href="calendar.ics">calendar.ics</a></div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_events}</div>
            <div class="stat-label">Total Events</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{upcoming_events}</div>
            <div class="stat-label">Upcoming Events</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{next_event_days}</div>
            <div class="stat-label">Days to Next Event</div>
        </div>
    </div>
    
    <div class="events-grid">
        {events_html}
    </div>
    
    <div class="last-updated">
        Generated: {generation_time}
    </div>
</body>
</html>"""

    def format_date(self, date_obj: datetime) -> str:
        """Format date for display"""
        if not date_obj:
            return "Date TBD"
        
        now = datetime.now()
        diff = (date_obj - now).days
        
        date_str = date_obj.strftime("%B %d, %Y")
        
        if diff == 0:
            return f"{date_str} (Today)"
        elif diff == 1:
            return f"{date_str} (Tomorrow)"
        elif diff > 0:
            return f"{date_str} (in {diff} days)"
        else:
            return f"{date_str} ({abs(diff)} days ago)"

    def generate_event_html(self, event: Dict) -> str:
        """Generate HTML for a single event"""
        title = event.get('title', 'Untitled Event')
        date_str = self.format_date(event.get('date'))
        location = event.get('location', 'Location TBD')
        url = event.get('url', '')
        
        url_html = ""
        if url:
            url_html = f'<div class="event-url"><a href="{url}" target="_blank">🔗 More Information</a></div>'
        
        return f"""
        <div class="event-card">
            <div class="event-header">
                <h3 class="event-title">{title}</h3>
                <div class="event-date">📅 {date_str}</div>
            </div>
            <div class="event-body">
                <div class="event-location">📍 {location}</div>
                {url_html}
            </div>
        </div>"""

    def calculate_stats(self, events: List[Dict]) -> Dict:
        """Calculate statistics for the events"""
        now = datetime.now()
        upcoming_events = [e for e in events if e.get('date') and e['date'] > now]
        
        next_event_days = "N/A"
        if upcoming_events:
            next_event = min(upcoming_events, key=lambda x: x['date'])
            next_event_days = (next_event['date'] - now).days
        
        return {
            'total_events': len(events),
            'upcoming_events': len(upcoming_events),
            'next_event_days': next_event_days
        }

    def generate_html_calendar(self, filename: str = 'debug.html') -> bool:
        """Generate HTML calendar view"""
        try:
            # Scrape events
            scraper = UCICalendarScraper()
            events = scraper.scrape_events()
            
            # Calculate stats
            stats = self.calculate_stats(events)
            
            # Generate events HTML
            if events:
                # Sort events by date
                events_sorted = sorted([e for e in events if e.get('date')], 
                                     key=lambda x: x['date'])
                events_html = '\n'.join([self.generate_event_html(event) for event in events_sorted])
            else:
                events_html = '''
                <div class="no-events">
                    <h3>🔍 No Events Found</h3>
                    <p>Either there are no upcoming events, or the scraper needs adjustment for the UCI website structure.</p>
                </div>'''
            
            # Fill template
            try:
                html_content = self.template.format(
                    last_updated=datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
                    total_events=stats['total_events'],
                    upcoming_events=stats['upcoming_events'],
                    next_event_days=stats['next_event_days'],
                    events_html=events_html,
                    generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                )
            except KeyError as e:
                logger.error(f"Template formatting error - missing key: {e}")
                return False
            except ValueError as e:
                logger.error(f"Template formatting error - value error: {e}")
                return False
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Successfully generated {filename} with {len(events)} events")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate HTML calendar: {e}")
            return False

def main():
    """Main function to generate HTML calendar"""
    generator = HTMLGenerator()
    success = generator.generate_html_calendar()
    
    if success:
        print("✅ HTML calendar generated successfully!")
        print("📄 File: debug.html")
    else:
        print("❌ Failed to generate HTML calendar")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())