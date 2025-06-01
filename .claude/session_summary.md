# UCI MTB Calendar Project - Session Summary

**Date**: January 6, 2025  
**Status**: ✅ Production Ready  

## Overview

Completed transformation from unreliable web scraping to robust Excel-based UCI MTB calendar sync application. The system now successfully processes 651 UCI events and generates both iCal and HTML outputs with proper date handling.

## Major Achievements

### 1. ✅ Excel Parser Implementation
- **Fixed US date format parsing**: Added `dayfirst=False` to handle UCI's MM/DD/YYYY format correctly
- **Robust data processing**: Handles 651 total events, filters to 381 upcoming events
- **Comprehensive event data**: Extracts titles, dates, locations, countries, categories, URLs

### 2. ✅ Date Format Improvements  
- **Input parsing**: Correctly interprets US format (01/06/2025 = January 6th, not June 1st)
- **Human-readable output**: Changed to unambiguous "06 Jan 2025" format for HTML display
- **Technical formats**: ISO dates for iCal and internal processing

### 3. ✅ HTML Template Refactoring
- **Extracted to separate file**: `src/uci_calendar/templates/debug_calendar.html`
- **Normal HTML/CSS syntax**: No more escaped braces, proper tooling support
- **Template loading system**: Dynamic loading with fallback error handling
- **Fixed CSS brace escaping issues**: All formatting errors resolved

### 4. ✅ Repository Organization
- **Cleaned up development files**: Removed 10+ obsolete scripts from `/dev`
- **Preserved working code**: Moved web scraping implementations to `.claude` memory
- **Git configuration**: Proper `.claude` directory tracking with selective ignoring
- **Data directory structure**: `/data` for Excel files with git.keep preservation

### 5. ✅ Download Infrastructure
- **API endpoint discovery**: Found actual UCI API at `https://api.uci.ch/v1.2/ucibws/competitions/getreportxls`
- **Authentication analysis**: Identified Bearer token requirement (expires ~1 hour)
- **Fallback system**: Manual download instructions when automation fails
- **Test data setup**: Scripts to copy files for development testing

### 6. ✅ Documentation & Preservation
- **Web scraping documentation**: Comprehensive guide in `.claude/webscraping_approach_documentation.md`
- **Reference implementations**: Preserved working scraper code as `.claude/working_scraper_reference.py`
- **Debug tools**: Saved debugging utilities as `.claude/debug_scraper_reference.py`
- **API details**: Complete download automation research for future use

## Current System Architecture

```
UCI Excel File (Manual Download)
       ↓
UCIExcelParser (US date format)
       ↓
CalendarGenerator → calendar.ics (381 events)
       ↓
HTMLGenerator → debug.html (with template)
```

## File Structure

**Core Application**:
- `src/uci_calendar/excel_parser.py` - Primary data source (651 events)
- `src/uci_calendar/calendar_generator.py` - iCal generation
- `src/uci_calendar/html_generator.py` - HTML generation with template loading
- `src/uci_calendar/templates/debug_calendar.html` - Clean HTML template

**Scripts**:
- `scripts/generate_calendar.py` - Main entry point with dynamic year detection and fallback
- `scripts/download_uci_excel.py` - Dynamic multi-season UCI download (auth required)
- `scripts/setup_test_data.py` - Copy test data for development

**Data & Output**:
- `data/2025.xls` - UCI Excel file (ignored by git, simplified naming)
- `calendar.ics` - Generated iCal with 381 upcoming events
- `debug.html` - HTML view with unambiguous date format

**Documentation**:
- `.claude/webscraping_approach_documentation.md` - Complete web scraping reference
- `.claude/working_scraper_reference.py` - Working prototype (158 events from saved HTML)
- `.claude/debug_scraper_reference.py` - Comprehensive debugging tools

## Key Technical Solutions

### Date Parsing Fix
```python
# Excel parser - Force US format interpretation
date_from = pd.to_datetime(row['Date From'], format='mixed', dayfirst=False, errors='coerce')

# HTML generator - Unambiguous display format  
date_str = date_obj.strftime("%d %b %Y")  # "06 Jan 2025"
```

### Template Loading System
```python
def _load_template(self):
    template_file = Path(__file__).parent / 'templates' / 'debug_calendar.html'
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()
```

### UCI API Endpoint (Future Automation)
```python
# POST https://api.uci.ch/v1.2/ucibws/competitions/getreportxls
payload = {
    "IsGrouped": True,
    "Language": "En",
    "Query": {"discipline": "MTB", "year": "2025"},
    "ReportTitle": "MTB - 2025"
}
# Requires: Bearer token (Microsoft Azure AD, ~1 hour expiry)
```

## Testing Results

**Excel Processing**: ✅  
- 651 total events loaded successfully
- 381 upcoming events filtered correctly
- US date format parsing working (01/06/2025 = January 6th)

**iCal Generation**: ✅  
- calendar.ics created with 381 events
- Compatible with Google Calendar, Apple Calendar, Outlook

**HTML Generation**: ✅  
- debug.html created with clean template
- Unambiguous date format ("06 Jan 2025")
- Proper CSS rendering without escape issues

## Usage Instructions

**Manual Download** (Current):
1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB
2. Click "Download season" → "xls"
3. Save as `data/2025.xls` (or any .xls/.xlsx file in data/ folder)
4. Run: `python scripts/generate_calendar.py`

**Fallback Workflow**:
- Script will auto-detect any .xls/.xlsx files in data/ folder
- Uses most recent file if no exact year match found
- Enables manual file addition to repository

**Development Setup**:
```bash
source venv/bin/activate
pip install -r requirements.txt
python scripts/setup_test_data.py  # Copy test data
python scripts/generate_calendar.py
```

**Download Script Usage**:
```bash
# Download all available seasons (2025, 2026, 2027)
python scripts/download_uci_excel.py all

# Download specific year
python scripts/download_uci_excel.py 2025

# Default behavior (tries all seasons)
python scripts/download_uci_excel.py
```

## Future Enhancements

1. **Authentication Automation**: Reverse engineer UCI Bearer token acquisition
2. **Multi-season Support**: Process 2025, 2026 Excel files automatically  
3. **Browser Automation**: Selenium/Playwright for click-based download
4. **Error Calendar**: Fallback calendar when UCI data unavailable
5. **GitHub Actions**: Automated daily updates with Excel download

## Preserved Knowledge

- **Web scraping approach**: Fully documented with working 158-event prototype
- **UCI page structure**: Competition cards and calendar items parsing
- **API research**: Complete endpoint analysis for future automation
- **Date parsing solutions**: US vs UK format handling strategies

## Success Metrics

- ✅ **651 total events** parsed from UCI Excel
- ✅ **381 upcoming events** in generated calendar
- ✅ **0 date parsing errors** with US format handling
- ✅ **100% template rendering** success after brace fixes
- ✅ **Clean codebase** with proper separation of concerns

The system is now production-ready for manual UCI Excel file updates and automatic calendar generation.