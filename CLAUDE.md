# UCI MTB Calendar Sync - Project Memory

## Project Overview
Automated service that downloads UCI MTB calendar data from Excel files and publishes it as a Google Calendar-compatible iCal feed with a responsive web interface.

## Architecture
- **Source**: UCI Excel files (2025.xls, 2026.xls, 2027.xls) from UCI calendar downloads
- **Output**: iCal (.ics) file and responsive HTML interface
- **Automation**: GitHub Actions (configurable schedule)
- **Hosting**: GitHub Pages with custom Help page

## Key Components

### Core Files
- `src/uci_calendar/excel_parser.py` - UCI Excel file parser with pandas/openpyxl
- `src/uci_calendar/calendar_generator.py` - iCal file generator using icalendar library
- `src/uci_calendar/html_generator.py` - HTML debug view generator
- `src/uci_calendar/templates/` - Web interface templates (index.html, help.html, styles.css)
- `calendar.ics` - Generated iCal file (auto-created by workflow)

### Web Interface
- `index.html` - Main landing page with calendar subscription
- `help.html` - Dedicated help page with subscription instructions and troubleshooting
- `styles.css` - Shared stylesheet for consistent styling
- `debug.html` - Generated debug view of calendar events

### Automation & Scripts
- `scripts/generate_calendar.py` - Main calendar generation script
- `scripts/setup_dev.sh` - Environment setup with --dev/--deploy flags
- `scripts/download_uci_excel.py` - UCI data download utility
- `.github/workflows/update-calendar.yml` - Scheduled GitHub Actions workflow

### Development Environment
- **Dual Environment Setup**:
  - `venv-dev/` - Full development environment (testing, linting, browser automation)
  - `venv-deploy/` - Minimal production environment (runtime only)
- `requirements.txt` - Production dependencies (requests, beautifulsoup4, icalendar, pytz, pandas, openpyxl)
- `requirements-dev.txt` - Development dependencies (pytest, requests-mock, black, flake8, pre-commit, playwright, selenium)
- `.vscode/settings.json` - VS Code configuration pointing to venv-dev
- `activate_dev.sh` / `activate_deploy.sh` - Auto-generated activation scripts

### Testing & Documentation
- `docs/SETUP.md` - Deployment and development setup instructions
- `README.md` - User-facing documentation
- `.github/ISSUE_TEMPLATE/` - Structured bug reports and feature requests

## Dependencies
### Production (requirements.txt)
- requests==2.31.0 - HTTP requests
- beautifulsoup4==4.12.2 - HTML parsing  
- icalendar==5.0.11 - iCal file generation
- pytz==2023.3 - Timezone handling
- pandas>=2.0.0 - Excel file processing
- openpyxl>=3.0.0 - Excel file reading

### Development (requirements-dev.txt)
- pytest==7.4.3 - Testing framework
- requests-mock==1.11.0 - HTTP mocking for tests
- ipython==8.17.2 - Interactive Python
- black==23.11.0 - Code formatting
- flake8==6.1.0 - Code linting
- pre-commit==3.5.0 - Git hooks
- playwright>=1.40.0 - Browser automation
- selenium==4.15.2 - Web automation
- Plus all production dependencies

## Deployment Status
- Repository: Created at petecog/cycle-calendar
- GitHub Pages: Configured to deploy from gh-pages branch
- URLs updated: All references use petecog.github.io domain
- Calendar URL: https://petecog.github.io/cycle-calendar/calendar.ics

## Known Limitations
- Scraping logic may need adjustment if UCI changes their page structure
- Assumes events are all-day unless time is explicitly specified
- Default 3-hour duration for timed events
- UTC timezone for all events

## Development Workflow

### Environment Setup
```bash
# Set up both environments
./scripts/setup_dev.sh

# Or set up specific environment
./scripts/setup_dev.sh --dev      # Development only
./scripts/setup_dev.sh --deploy   # Production only
```

### Daily Development
```bash
# Activate development environment
source activate_dev.sh

# Generate calendar files
python scripts/generate_calendar.py

# Run tests and linting
pytest
black .
flake8 .

# Start local web server
cd src/uci_calendar/templates
python -m http.server 8000
```

### VS Code Integration
- Automatically uses `venv-dev/bin/python` as interpreter
- Configured for black formatting, flake8 linting, pytest testing
- Virtual environment directories hidden from explorer

## Project Structure Evolution
- **Original**: Single environment, HTML scraping from UCI website
- **Current**: Dual environments, Excel file processing, responsive web interface
- **Web Interface**: Reorganized with dedicated Help page and shared CSS
- **Development**: Separate dev/deploy environments for different use cases

## Future Enhancements
- Add automated UCI Excel file downloading
- Implement event filtering by discipline/category  
- Add timezone support for different regions
- Enhanced error handling and logging
- Performance monitoring and health checks