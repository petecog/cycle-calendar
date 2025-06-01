# 🚵‍♂️ UCI MTB Calendar Sync

Automatically syncs [UCI MTB calendar](https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB) events to a Google Calendar-compatible format.

## 📅 Quick Start

**Subscribe to the calendar:**
```
https://petecog.github.io/cycle-calendar/calendar.ics
```

**View events online:**
- [Main Page](https://petecog.github.io/cycle-calendar/) - Subscription instructions
- [Debug View](https://petecog.github.io/cycle-calendar/debug.html) - Live event listing

## 🔄 How it works

1. **GitHub Actions** runs every 6 hours
2. **Scrapes** the UCI MTB calendar page
3. **Generates** an iCal (.ics) file + HTML debug view
4. **Deploys** to GitHub Pages automatically

## 📱 Calendar Apps

| App | Instructions |
|-----|-------------|
| **Google Calendar** | Settings → Add calendar → From URL |
| **Apple Calendar** | File → New Calendar Subscription |
| **Outlook** | Add calendar → Subscribe from web |

## 🛠️ Development

### Quick Setup (VSCode Dev Container)
1. Install "Dev Containers" extension
2. Open project in VSCode
3. `F1` → "Dev Containers: Reopen in Container"
4. All dependencies auto-installed!

### Local Setup (Python venv)
```bash
# One-time setup
./scripts/setup_dev.sh

# Daily usage
source venv/bin/activate
python dev/serve_simple.py --port 3000  # Start local server
python dev/test_local.py                # Test scraping  
python scripts/generate_calendar.py     # Generate all files
```

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### Available Tasks (VSCode)
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Generate Calendar, Test Local, Format Code, Lint Code

## 📁 Project Structure

```
├── src/                      # Core application code
│   └── uci_calendar/        # Main package
│       ├── __init__.py      # Package interface
│       ├── scraper.py       # UCI calendar scraper
│       ├── calendar_generator.py # iCal file generator
│       └── html_generator.py # HTML debug viewer
├── scripts/                  # Executable utilities
│   ├── generate_calendar.py # Main generation script
│   └── setup_dev.sh        # Development setup
├── dev/                     # Development tools
│   ├── serve_simple.py     # Local development server
│   ├── test_local.py       # Testing utilities
│   ├── debug_scraper.py    # Detailed scraper debugging
│   ├── debug_simple.py     # Simple debug generator
│   └── test_package.py     # Package structure testing
├── docs/                    # Documentation
├── index.html              # GitHub Pages main page
├── .github/workflows/       # CI/CD automation
└── .devcontainer/          # VSCode dev environment
```

## 🚀 Deployment

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

## 🔧 Troubleshooting

- **No events showing?** Check the [debug view](https://petecog.github.io/cycle-calendar/debug.html)
- **Empty calendar?** UCI website may have changed structure
- **Local testing fails?** Ensure internet access to UCI site

## 📝 Contributing

1. Make changes in dev container or local venv
2. Test with `python dev/test_local.py`
3. Format code with `black .`
4. Generate files with `python scripts/generate_calendar.py`
5. Submit pull request

---

*Automatically updated every 6 hours via GitHub Actions*