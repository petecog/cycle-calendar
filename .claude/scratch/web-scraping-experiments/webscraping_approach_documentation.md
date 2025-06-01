# UCI MTB Calendar Web Scraping Approach - Documentation

**Status**: De-implemented (replaced by Excel parsing)  
**Reason for replacement**: Dynamic content loading made web scraping unreliable (0 events scraped vs 651 from Excel)

## Overview

This documents the web scraping approach that was developed and then de-implemented for the UCI MTB calendar sync application. The approach successfully parsed event data from saved HTML but failed with live scraping due to dynamic content loading.

## Technical Implementation

### Core Components

1. **UCICalendarScraper** (`src/uci_calendar/scraper.py`)
   - Main scraper class with requests/BeautifulSoup4
   - Filtered URL with specific event types and categories
   - Two parsing methods for different page structures

2. **Parsing Methods**
   ```python
   def parse_competition_cards(self, soup):
       """Parse competition-card elements from carousel"""
       # Extracts: name, dates, venue, race hub links
       # Found in carousel/featured events section
   
   def parse_calendar_items(self, soup):
       """Parse calendar-item elements from main list"""  
       # Extracts: titles, locations, countries, URLs
       # Found in main event listing
   ```

3. **Date Parsing**
   ```python
   def parse_uci_dates(self, date_string):
       """Parse UCI date formats: '01 Jun 2025' and '30 May - 01 Jun 2025'"""
       # Handles both single dates and date ranges
       # Returns start_date, end_date tuple
   ```

### URL Configuration

**Filtered URL**: `https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB`

**Filter Parameters**:
- Event Types: Enduro, Downhill, Cross-Country Olympic, Cross-Country Short Track, Cross-Country Marathon, Cross-Country Eliminator
- Categories: Men Elite, Women Elite, Men Masters, Women Masters, Mixed

## Key Findings

### Success with Saved HTML
- **Working prototype**: `dev/working_scraper.py` successfully parsed **158 events** from `Mountain Bike calendar _ UCI.html`
- Proved parsing logic was correct
- Demonstrated both `competition-card` and `calendar-item` structures existed

### Dynamic Loading Problem
- **Live scraping yielded 0 events** - UCI calendar uses JavaScript/lazy loading
- Events only appear after scrolling or JavaScript execution
- Static HTML requests return empty event containers
- Beautiful Soup could not access dynamically loaded content

### Page Structure Analysis
```html
<!-- Competition cards (carousel) -->
<div class="competition-card">
  <div class="competition-card__name">Event Name</div>
  <div class="competition-card__date">01 Jun 2025</div>
  <div class="competition-card__venue">Location</div>
  <a href="/race-hub/..." class="competition-card__race-hub-link">
</div>

<!-- Calendar items (main list) -->
<div class="calendar-item__title">
  <a href="...">Event Title</a>
</div>
<div class="calendar-item__location">City, Country</div>
```

## Development Files (Preserved for Reference)

### Core Implementation
- `src/uci_calendar/scraper.py` - Main scraper class (kept but removed from imports)
- `dev/working_scraper.py` - Successful prototype that parsed 158 events from saved HTML
- `dev/debug_scraper.py` - Comprehensive debugging and analysis tools

### Debugging Tools
- `dev/find_brace_issue.py` - HTML template brace analysis
- `dev/fix_template_braces.py` - Automatic CSS brace fixing
- `dev/test_html_template.py` - HTML generation testing

### Test Data
- `Mountain Bike calendar _ UCI.html` - Fully rendered page with 158+ events (user-provided)
- Shows complete page structure after JavaScript execution

## Potential Future Solutions

### 1. JavaScript Rendering
```python
# Using Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url)
# Scroll to trigger lazy loading
html = driver.page_source
```

### 2. Playwright Alternative
```python
# More modern than Selenium
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state('networkidle')
    html = page.content()
```

### 3. API Discovery
- Look for UCI internal APIs used by the calendar page
- Network tab analysis during page load
- May require reverse engineering

## Why Excel Parsing Was Chosen

1. **Reliability**: 651 structured events vs 0 from scraping
2. **Data Quality**: Complete metadata, standardized format
3. **UCI Official**: Direct from UCI's own export functionality
4. **Maintenance**: No dependency on web page structure changes
5. **Performance**: No browser automation overhead

## Integration Points

The scraper was designed to integrate with:
- `CalendarGenerator` - Accepts events from any source
- `HTMLGenerator` - Display scraped events
- Event filtering by type and category
- iCal generation pipeline

## Lessons Learned

1. **Always test with live data** - Saved HTML can mislead about actual scraping success
2. **Modern websites use dynamic loading** - Static scraping often insufficient
3. **Official data exports are preferable** - More reliable than scraping when available
4. **Keep working prototypes** - `dev/working_scraper.py` preserved the successful parsing logic

## Re-implementation Checklist

If web scraping needs to be re-implemented:

1. ✅ Use existing parsing logic from `.claude/working_scraper_reference.py`
2. ✅ Implement JavaScript rendering (Selenium/Playwright)
3. ✅ Test with live UCI calendar page
4. ✅ Verify event counts match expected numbers
5. ✅ Handle lazy loading/infinite scroll
6. ✅ Add fallback to Excel parsing if scraping fails
7. ✅ Update dependencies (add selenium/playwright to requirements)

## File Locations

**Core Files**:
- `src/uci_calendar/scraper.py` - Main implementation (preserved)
- `.claude/working_scraper_reference.py` - Working prototype (moved from dev/)
- `.claude/debug_scraper_reference.py` - Comprehensive debug tools (recovered from git)

**Test Data**:
- `.claude/claude-input/Mountain Bike calendar _ UCI.html` - Reference HTML with full event data

**Documentation**:
- This file: `.claude/webscraping_approach_documentation.md`