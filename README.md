# UCI MTB Calendar Sync

Automatically syncs UCI MTB calendar events to a Google Calendar-compatible format.

## Usage

Subscribe to the calendar in your calendar app:
```
https://petecog.github.io/cycle-calendar/calendar.ics
```

## How it works

1. GitHub Actions runs every 6 hours
2. Scrapes the UCI MTB calendar page
3. Generates an iCal (.ics) file
4. Hosts it on GitHub Pages

## Development

```bash
pip install -r requirements.txt
python scraper.py
```