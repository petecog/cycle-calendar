#!/usr/bin/env python3
"""
HTML Calendar Generator
Creates an HTML page displaying UCI MTB calendar events for debugging and quick reference
"""

from datetime import datetime
import json
import logging
from typing import List, Dict
# Excel parser is the primary data source

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLGenerator:
    def __init__(self):
        self.events = []  # Allow setting events directly
        self.template = self._load_template()
    
    def _load_template(self):
        """Load HTML template from file"""
        from pathlib import Path
        
        template_file = Path(__file__).parent / 'templates' / 'debug_calendar.html'
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template = f.read()
            logger.info(f"Loaded HTML template from {template_file}")
            return template
        except Exception as e:
            logger.error(f"Failed to load template from {template_file}: {e}")
            # Fallback to a minimal template
            return """<!DOCTYPE html>
<html>
<head><title>UCI MTB Calendar</title></head>
<body>
<h1>Template Loading Error</h1>
<p>Could not load template file: {template_error}</p>
<div>{events_html}</div>
</body>
</html>"""

    def format_date(self, date_obj: datetime) -> str:
        """Format date for display"""
        if not date_obj:
            return "Date TBD"
        
        now = datetime.now()
        diff = (date_obj - now).days
        
        # Use unambiguous format: "10 Jan 2025" (day month year)
        date_str = date_obj.strftime("%d %b %Y")
        
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
            # Use pre-set events (must be provided externally)
            events = self.events
            
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