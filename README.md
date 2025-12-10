# Basketball Statistics System

## Overview

Comprehensive basketball game statistics tracking and analysis system with GUI interface. Tracks individual player performance, game details, and provides advanced analytics for youth basketball teams.

**Version:** 1.0  
**Python Version:** 3.13  
**Primary Framework:** PyQt5

---

## Project Structure

```
Drags/
├── .vscode/              # VSCode configuration
│   ├── launch.json       # Debug configurations
│   ├── settings.json     # Editor settings
│   └── doc/              # Configuration documentation
├── Database/             # Data storage
│   ├── Data.json         # Primary game/player data
│   ├── Data.json.bak     # Backup data file
│   ├── doc/              # Database documentation
│   └── log/              # System logs
├── git/                  # Git configuration
│   ├── .gitignore        # Git exclusions
│   ├── .gitmodules       # Submodule config
│   └── doc/              # Git documentation
├── main/                 # Core application
│   ├── main.py           # Application entry point
│   ├── player_report.py  # Player report GUI (1000+ lines)
│   ├── doc/              # Main module documentation
│   └── __pycache__/      # Python cache
├── Old-basketball-stats/ # Legacy code (submodule)
├── templates/            # Design templates and ideas
├── testing/              # Test files
│   ├── test_file.py      # Unit tests
│   ├── team_report.py    # Team report module
│   ├── doc/              # Testing documentation
│   └── __pycache__/      # Python cache
├── UI/                   # UI design files
│   ├── designs.txt       # UI mockups
│   └── doc/              # UI documentation
└── utils/                # Utility modules
    ├── accessing_data.py # Data access layer (1000+ lines)
    ├── write.py          # Error logging utility
    ├── doc/              # Utils documentation
    └── __pycache__/      # Python cache
```

---

## Features

### Data Management
- JSON-based game and player statistics storage
- Automatic backup system (Data.json.bak)
- Comprehensive error logging
- Multi-user access tracking with UUID system

### Player Analysis
- Individual player performance tracking
- Game-by-game statistics
- Quarter-level granularity
- Advanced metrics calculation
- Performance trend analysis

### GUI Interface
- PyQt5-based player report cards
- Real-time data visualization
- Interactive statistics display
- User-friendly navigation

### Analytics
- Game comparison tools
- Season grading system
- Best/worst game highlights
- Game rating system
- Quarter-by-quarter breakdowns

---

## Installation

### Prerequisites
```bash
Python 3.13+
PyQt5
```

### Setup
```bash
# Clone repository
git clone <repository-url>
cd Drags

# Install dependencies
pip install PyQt5

# Initialize submodules
git submodule update --init --recursive
```

---

## Usage

### Running the Application

**Option 1: Main Entry Point**
```bash
python main/main.py
```

**Option 2: Player Report GUI**
```bash
python main/player_report.py
```

**Option 3: VSCode Debug**
- Press F5
- Select configuration:
  - ▶ Run Current File
  - ▶ Run Player Report
  - ▶ Run Main
  - ▶ Run AccessData Module

### Testing
```bash
python testing/test_file.py
```

---

## Core Modules

### `main/main.py`
Application entry point. Initializes PyQt5 application, loads data access layer, and launches player report GUI.

### `main/player_report.py`
Massive 1000+ line GUI module with 27+ methods. Handles:
- Player report card generation
- Statistical visualization
- Game data display
- Interactive analytics

### `utils/accessing_data.py`
Data access layer (1000+ lines). Provides:
- JSON data reading/writing
- Data validation
- Query methods
- Error handling
- User tracking
- Backup management

### `utils/write.py`
Error logging utility. Appends error logs to JSON files with structured format.

---

## Data Structure

### Database/Data.json
```json
{
  "Game_1": {
    "Details": {
      "Time": "6:05PM",
      "Day": "Monday",
      "Month": "Aug",
      "Year": 2025,
      "Court": 3,
      "Game_against": "Newport Raiders U16 Boys Paul",
      "Our_Scores": 40,
      "There_Scores": 35
    },
    "Players": {
      "Player_Name": {
        "Q1": {...},
        "Q2": {...},
        "Q3": {...},
        "Q4": {...}
      }
    }
  }
}
```

---

## Configuration

### VSCode Launch Configurations
- **Run Current File**: Executes active file
- **Run Player Report**: Launches player report GUI
- **Run Main**: Starts main application
- **Run AccessData Module**: Tests data access layer

### Editor Settings
- Theme: Evondev Dracula Darker Contrast
- Icon Theme: Material Icon Theme
- Testing: pytest enabled
- Spell Check: Custom dictionary for basketball terms

---

## Logging

### Log Files (Database/log/)
- `accessing_data_log.json`: Data access operations
- `player_report_log.json`: GUI events and errors
- `testing_log.json`: Test execution logs

### Log Format
```json
[
  {
    "timestamp": "2025-12-09T17:52:00Z",
    "event": "data_access",
    "details": {...}
  }
]
```

---

## Development

### Adding New Features
1. Create feature branch
2. Update relevant module in `main/` or `utils/`
3. Add tests in `testing/`
4. Update documentation in `doc/` folders
5. Submit pull request

### Code Style
- Python 3.13+ syntax
- Type hints where applicable
- Comprehensive inline documentation
- Rating system (e.g., `# Rated 942/1000`)

### Documentation
Each module has corresponding documentation in `doc/` folders:
- File-level: `<filename>_doc.md`
- Folder-level: `<foldername>_doc.md`

---

## Known Issues

### Database
- Manual backup management required
- No automatic migration system
- Single JSON file (scalability concern)

### UI
- PyQt5 dependency (large package)
- No responsive design
- Limited theming options

### Testing
- Incomplete test coverage
- No automated CI/CD
- Manual test execution

---

## Future Improvements

### Planned Features
- Team comparison analytics
- Season summary reports
- Export to PDF/Excel
- Cloud data sync
- Mobile app interface

### Technical Debt
- Refactor 1000+ line files into smaller modules
- Implement proper database (SQLite/PostgreSQL)
- Add comprehensive unit tests
- Create automated deployment pipeline
- Implement proper error recovery

---

## Git Configuration

### Ignored Files (.gitignore)
- `__pycache__/` - Python bytecode
- `.vscode/` - Editor settings
- `Database/Data.json` - User data
- Build artifacts and OS files

### Submodules
- `Old-basketball-stats`: Legacy codebase (archived)

---

## License

[Specify License]

---

## Contact

**Project Lead:** Drags Jrs  
**System Path:** `C:/Users/Drags Jrs/Drags`

---

## Quick Start

```bash
# 1. Clone and setup
git clone <repo-url>
cd Drags
git submodule update --init

# 2. Install dependencies
pip install PyQt5

# 3. Run application
python main/main.py

# 4. View player reports
# GUI will launch automatically
```

---

## Documentation

Full documentation available in `doc/` folders:
- **Configuration**: `.vscode/doc/`
- **Database**: `Database/doc/`
- **Main Application**: `main/doc/`
- **Utilities**: `utils/doc/`
- **Testing**: `testing/doc/`
- **UI Design**: `UI/doc/`

---

**Last Updated:** December 9, 2025  
**Documentation Version:** 1.0