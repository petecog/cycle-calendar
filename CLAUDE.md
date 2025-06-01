# UCI MTB Calendar Sync - Project Memory

## Project Overview
Automated service that scrapes the UCI MTB calendar and publishes it as a Google Calendar-compatible iCal feed hosted on GitHub Pages.

## Architecture
- **Source**: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB
- **Output**: iCal (.ics) file hosted at https://petecog.github.io/cycle-calendar/calendar.ics
- **Automation**: GitHub Actions runs every 6 hours
- **Hosting**: GitHub Pages

## Key Components

### Core Files
- `scraper.py` - UCI calendar scraper with BeautifulSoup
- `calendar_generator.py` - iCal file generator using icalendar library
- `calendar.ics` - Generated iCal file (auto-created by workflow)
- `index.html` - GitHub Pages landing page with subscription instructions

### Automation
- `.github/workflows/update-calendar.yml` - Scheduled GitHub Actions workflow
  - Runs every 6 hours (`0 */6 * * *`)
  - Scrapes UCI calendar, generates iCal, commits changes
  - Deploys to GitHub Pages

### Development Environment
- `.devcontainer/devcontainer.json` - VSCode dev container (Python 3.11)
- `requirements.txt` - Production dependencies (requests, beautifulsoup4, icalendar, pytz)
- `requirements-dev.txt` - Development dependencies (pytest, requests-mock, black, flake8)
- `.vscode/` - VSCode tasks and launch configurations

### Testing & Utilities
- `test_local.py` - Local testing script
- `SETUP.md` - Deployment instructions
- `README.md` - User-facing documentation

## Dependencies
### Production
- requests==2.31.0 - HTTP requests
- beautifulsoup4==4.12.2 - HTML parsing
- icalendar==5.0.11 - iCal file generation
- pytz==2023.3 - Timezone handling

### Development
- pytest - Testing framework
- requests-mock - HTTP mocking for tests
- black - Code formatting
- flake8 - Code linting
- ipython - Interactive Python

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
1. Use VSCode dev container for consistent environment
2. Run `python test_local.py` to test locally
3. Use VSCode tasks for formatting, linting, testing
4. GitHub Actions handles automated deployment

## Future Enhancements
- Add error handling for UCI site changes
- Implement event duration detection
- Add timezone support for different regions
- Create unit tests with mocked UCI responses
- Add health check endpoint