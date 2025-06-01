# Web Scraping Experiments

**Status**: De-implemented (replaced by Excel parsing)  
**Reason**: UCI website uses dynamic content loading, yielding 0 events from static scraping

## Contents

### `working_scraper_reference.py`
- **Purpose**: Proven parsing logic that successfully extracted 158 events from saved HTML
- **Success**: Demonstrates correct parsing of UCI page structure when fully rendered
- **Methods**: `parse_competition_cards()` and `parse_calendar_items()`
- **Date parsing**: Handles UCI formats ("01 Jun 2025", "30 May - 01 Jun 2025")

### `debug_scraper_reference.py`
- **Purpose**: Comprehensive debugging tools for web scraping analysis
- **Features**: HTML structure analysis, network debugging, event validation
- **Tools**: Brace counting, format testing, output comparison

## Key Findings

### What Worked
- ✅ Parsing logic correctly extracts event data from fully rendered HTML
- ✅ Date parsing handles UCI's non-standard formats
- ✅ Both `competition-card` and `calendar-item` structures identified
- ✅ 158 events successfully parsed from saved HTML file

### What Failed
- ❌ Live scraping yields 0 events due to JavaScript/lazy loading
- ❌ Events only appear after scrolling or JavaScript execution
- ❌ Static HTML requests return empty event containers
- ❌ BeautifulSoup cannot access dynamically loaded content

## Future Re-implementation

If web scraping needs to be revived:

1. **Use existing parsing logic** from `working_scraper_reference.py`
2. **Add JavaScript rendering** with Selenium or Playwright
3. **Handle lazy loading** by scrolling or waiting for content
4. **Test with live UCI calendar** to verify event counts
5. **Add fallback to Excel parsing** if scraping fails

## Related Documentation

- `webscraping_approach_documentation.md` - Comprehensive implementation guide (in this folder)
- `../../decisions.md` - Decision to replace with Excel parsing
- `../../memory/20250106-*.md` - Session notes on scraping challenges

## API Alternative

UCI API discovered: `https://api.uci.ch/v1.2/ucibws/competitions/getreportxls`
- Requires Bearer token (Microsoft Azure AD, ~1 hour expiry)
- More reliable than scraping if authentication solved
- See download scripts for implementation details