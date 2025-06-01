# UCI Calendar Scraping Analysis

## Problem Identified
The current scraper finds 0 events because the UCI calendar uses **dynamic content loading** (lazy loading/infinite scroll) rather than static HTML.

## Investigation Results

### 1. Static HTML Analysis ✅
- **Page loads**: 79k characters successfully fetched
- **Content**: No `<table>` rows, no divs with "event" class
- **JavaScript**: Found `webSettings` object with calendar-related localizations
- **Conclusion**: Calendar data is NOT in initial HTML

### 2. API Endpoint Discovery ❌
**Manual endpoint testing** - All return 404:
- `/api/calendar`, `/api/events`, `/api/competitions`
- `/calendar/api/*`, `/data/*`, `/umbraco/api/*`
- **Conclusion**: UCI doesn't use standard REST API patterns

### 3. JavaScript Configuration ✅
**Found webSettings object** with calendar localizations:
- `"calendar.viewMoreLabel": "View more"`
- `"calendar.noResults": "No results found"`
- `"calendar.searchLabel": "Search"`
- **Conclusion**: Confirms dynamic loading with "View more" functionality

## Recommended Solutions

### Option 1: Selenium with Network Monitoring 🎯
**Best approach** - Install Selenium to:
1. Load page in real browser
2. Scroll to trigger lazy loading
3. Monitor network requests to find actual API calls
4. Extract real API endpoints used by the site

```bash
pip install selenium
# Download ChromeDriver
python dev/network_analyzer.py
```

### Option 2: Browser Developer Tools Investigation 🔍
**Manual approach**:
1. Open UCI calendar in browser
2. Open DevTools → Network tab
3. Scroll down to load more events
4. Look for XHR/Fetch requests
5. Copy working API endpoints

### Option 3: Alternative Data Sources 🔄
**If APIs prove difficult**:
- Look for UCI RSS feeds
- Check if UCI provides official calendar exports
- Consider using UCI's mobile app API (if available)

## Tools Created

### Debug Tools 🛠️
- `dev/debug_scraper.py` - Comprehensive static analysis
- `dev/extract_api_config.py` - JavaScript configuration extraction
- `dev/network_analyzer.py` - Network traffic monitoring (requires Selenium)
- `dev/advanced_scraper.py` - Selenium-based scraping with scroll simulation

### Debug Output 📁
All tools save results to `dev/debug/` (git-ignored):
- `uci_raw.html` - Raw page HTML
- `uci_parsed.html` - Structured HTML
- `analysis.json` - Statistical summary
- `web_settings.json` - JavaScript configuration

## Current Status
- ✅ **Package structure**: Clean, professional organization
- ✅ **Debug infrastructure**: Comprehensive analysis tools
- ✅ **Problem identified**: Dynamic loading confirmed
- ❌ **Working scraper**: Needs Selenium or API discovery
- ❌ **Event extraction**: 0 events found with current approach

## Next Steps
1. **Install Selenium** + ChromeDriver
2. **Run network analyzer** to find real API endpoints
3. **Update scraper** to use discovered APIs
4. **Test with real data** from UCI calendar