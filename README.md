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

### Quick Setup (VSCode)
1. Install "Dev Containers" extension
2. Open project in VSCode
3. `F1` → "Dev Containers: Reopen in Container"
4. All dependencies auto-installed!

### Manual Setup
```bash
pip install -r requirements-dev.txt
python test_local.py          # Test scraping
python calendar_generator.py  # Generate calendar
python html_calendar_generator.py  # Generate debug view
```

### Available Tasks (VSCode)
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Generate Calendar, Test Local, Format Code, Lint Code

## 📁 Project Structure

```
├── scraper.py                 # UCI calendar scraper
├── calendar_generator.py      # iCal file generator  
├── html_calendar_generator.py # HTML debug viewer
├── .github/workflows/         # Auto-update workflow
├── .devcontainer/            # VSCode dev environment
└── docs/                     # GitHub Pages files
```

## 🚀 Deployment

See [SETUP.md](SETUP.md) for detailed deployment instructions.

## 🔧 Troubleshooting

- **No events showing?** Check the [debug view](https://petecog.github.io/cycle-calendar/debug.html)
- **Empty calendar?** UCI website may have changed structure
- **Local testing fails?** Ensure internet access to UCI site

## 📝 Contributing

1. Make changes in dev container
2. Test with `python test_local.py`
3. Format code with `black .`
4. Submit pull request

---

*Automatically updated every 6 hours via GitHub Actions*