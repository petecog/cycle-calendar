#!/usr/bin/env python3
"""
Simple debug HTML generator without CSS formatting conflicts
"""

from datetime import datetime
from scraper import UCICalendarScraper

def generate_simple_debug():
    """Generate a simple debug HTML file"""
    
    # Get events
    scraper = UCICalendarScraper()
    events = scraper.scrape_events()
    
    # Simple HTML template
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>UCI MTB Calendar Debug</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .event {{ border: 1px solid #ccc; margin: 10px 0; padding: 15px; }}
        .title {{ font-weight: bold; font-size: 1.2em; }}
        .date {{ color: #666; }}
        .location {{ color: #0066cc; }}
    </style>
</head>
<body>
    <h1>🚵‍♂️ UCI MTB Calendar Debug</h1>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Found {len(events)} events</p>
    
    <div>
        <a href="index.html">← Back to Main</a> | 
        <a href="calendar.ics">Download Calendar</a>
    </div>
    
    <h2>Events</h2>
"""
    
    if events:
        for event in events:
            title = event.get('title', 'Unknown Event')
            date_str = event.get('date', 'No date').strftime('%Y-%m-%d') if event.get('date') else 'No date'
            location = event.get('location', 'No location')
            url = event.get('url', '')
            
            html += f"""
    <div class="event">
        <div class="title">{title}</div>
        <div class="date">📅 {date_str}</div>
        <div class="location">📍 {location}</div>
        {f'<div><a href="{url}" target="_blank">🔗 More info</a></div>' if url else ''}
    </div>"""
    else:
        html += """
    <div class="event">
        <div class="title">No events found</div>
        <div>Either no upcoming events exist, or the UCI website structure has changed.</div>
    </div>"""
    
    html += """
</body>
</html>"""
    
    # Write file
    with open('debug.html', 'w') as f:
        f.write(html)
    
    print(f"✅ Generated debug.html with {len(events)} events")

if __name__ == "__main__":
    generate_simple_debug()