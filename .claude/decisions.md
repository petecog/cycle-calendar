# UCI MTB Calendar Project - Key Decisions

## Design & Implementation Decisions

### 1. Data Source Strategy
**Decision**: Replace web scraping with Excel parsing as primary data source  
**Date**: January 2025  
**Rationale**: 
- Web scraping yielded 0 events due to JavaScript/lazy loading
- UCI Excel exports provide 651 structured events vs 0 from scraping
- Official UCI data source more reliable than page structure scraping
- Excel format includes comprehensive metadata not available via scraping

**Impact**: 
- ✅ 651 total events vs 0 from web scraping
- ✅ Structured data with full event details
- ✅ No dependency on UCI website structure changes
- ❌ Requires manual download step (API authentication needed)

### 2. Date Format Handling
**Decision**: Parse UCI Excel dates as US format (MM/DD/YYYY) with UK display format  
**Date**: January 6, 2025  
**Rationale**:
- UCI Excel files confirmed to use US date format
- User comparison of XLS vs website revealed format discrepancy
- Ambiguous dates like 01/06/2025 need explicit interpretation
- UK users prefer unambiguous display format

**Implementation**:
```python
# Input parsing (US format)
date_from = pd.to_datetime(row['Date From'], dayfirst=False, errors='coerce')

# Output display (UK format, unambiguous)
date_str = date_obj.strftime("%d %b %Y")  # "06 Jan 2025"
```

**Impact**: Prevents date misinterpretation (Jan 6th vs June 1st)

### 3. HTML Template Architecture
**Decision**: Extract HTML template to separate file with dynamic loading  
**Date**: January 6, 2025  
**Rationale**:
- Embedded HTML string in Python prevents proper tooling support
- Separate file enables HTML/CSS editors, syntax highlighting, linting
- Version control friendly for template changes
- Easier maintenance and debugging

**Implementation**:
- Template: `src/uci_calendar/templates/debug_calendar.html`
- Loader: `HTMLGenerator._load_template()` with fallback handling
- CSS braces escaped for Python string formatting compatibility

**Impact**: 
- ✅ Proper HTML/CSS development experience
- ✅ Template can be edited independently
- ✅ Normal browser preview capabilities

### 4. Filename Convention
**Decision**: Simplify Excel filenames to `YYYY.xls` format  
**Date**: January 6, 2025  
**Rationale**:
- `UCICompetitions_MTB_2025.xls` too verbose for multi-year management
- `2025.xls` format enables easy year identification
- Consistent naming pattern for multiple seasons
- Simpler manual workflow for users

**Impact**:
- ✅ Clean data directory: `2025.xls`, `2026.xls`, etc.
- ✅ Easier multi-season support
- ✅ Clearer user instructions

### 5. Fallback Strategy
**Decision**: Implement intelligent Excel file detection with most-recent fallback  
**Date**: January 6, 2025  
**Rationale**:
- Users may add Excel files with different naming conventions
- Exact year match not always possible (early season downloads)
- Graceful degradation improves user experience
- Enables manual repository file addition

**Implementation**:
1. Look for exact year match (`2025.xls`)
2. Auto-detect any `.xls`/`.xlsx` files in data folder
3. Use most recent file by modification time
4. Attempt dynamic download if no files found
5. Provide manual instructions as final fallback

**Impact**: Robust operation regardless of file naming or availability

### 6. Multi-Season Download Strategy
**Decision**: Dynamic year discovery with batch download capabilities  
**Date**: January 6, 2025  
**Rationale**:
- UCI often releases future season calendars early
- Users benefit from having multiple years available
- Automated discovery reduces manual coordination
- Batch processing more efficient than single-year requests

**Implementation**:
- Year range: Current year + 2 future years
- Command modes: single year, all seasons, default (all)
- Per-season status reporting
- Comprehensive error handling

**Impact**: 
- ✅ Future-proof calendar data availability
- ✅ Reduced manual download coordination
- ✅ Clear feedback on success/failure per season

### 7. Repository Structure
**Decision**: Commit all .claude directory contents including reference code  
**Date**: January 6, 2025  
**Rationale**:
- Documentation valuable for team and future reference
- Reference implementations preserve institutional knowledge
- Web scraping approach may be needed if Excel source fails
- Session summaries provide project history context

**Implementation**:
- Organized .claude structure: `/input`, `/memory`, `/scratch`, `decisions.md`
- Git tracking enabled for all .claude contents
- Reference code marked as "speculative" for future use

**Impact**: Complete knowledge preservation and team collaboration support

### 8. Error Handling Philosophy
**Decision**: Graceful degradation with comprehensive user guidance  
**Date**: January 6, 2025  
**Rationale**:
- UCI API requires authentication (Bearer token, 1-hour expiry)
- Manual workflow must remain viable long-term
- Users need clear instructions when automation fails
- System should never fail completely if any data available

**Implementation**:
- Multiple fallback levels (exact file → any file → download → manual)
- Detailed error messages with specific file paths
- Manual download instructions with proper naming guidance
- API details preserved for future automation improvements

**Impact**: Reliable operation regardless of UCI API availability

## Technology Choices

### Core Libraries
- **pandas + openpyxl**: Excel file processing (vs xlrd deprecation)
- **icalendar**: RFC-compliant calendar generation
- **pathlib**: Modern Python file path handling
- **requests**: HTTP client for future API automation

### Template Engine
**Decision**: Python string formatting vs templating engine  
**Rationale**: Simple variable substitution sufficient, no complex logic needed

### Date Handling
**Decision**: pandas datetime vs built-in datetime  
**Rationale**: pandas provides robust Excel date parsing with format control

## Architecture Principles

1. **Graceful Degradation**: Multiple fallback levels ensure operation
2. **User-Friendly**: Clear error messages and manual alternatives
3. **Future-Proof**: Framework ready for authentication solution
4. **Knowledge Preservation**: Document decisions and preserve working code
5. **Clean Separation**: Templates, logic, and data properly separated

## Future Decision Points

### Authentication Strategy
**Pending**: How to handle UCI Bearer token acquisition
**Options**: 
- Browser automation (Selenium/Playwright)
- Microsoft Azure AD authentication flow reverse engineering
- Accept manual workflow as primary method

### Multi-Year Data Strategy
**Pending**: How to handle historical data and multi-season calendars
**Considerations**: 
- Storage of multiple years in repository
- Calendar merging vs separate files
- Historical event preservation