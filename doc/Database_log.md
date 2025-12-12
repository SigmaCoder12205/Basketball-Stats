# Database Folder Documentation

## Overview

**FOLDER**: `Database/`  
**PURPOSE**: Data storage and documentation directory for basketball statistics system

Central repository containing game data, backup files, documentation, and operation logs for the basketball statistics tracking application.

---

## Folder Structure

```
Database/
├── Data.json                      # Primary game data storage
├── Data.json.bak                  # Backup copy of data file
├── doc/
│   └── data.json_doc.md          # Data structure documentation
└── log/
    ├── accessing_data_log.json   # Data access operation logs
    ├── player_report_log.json    # GUI operation logs
    └── testing_log.json          # Test execution logs
```

---

## Files Overview

### Data Files (Root Level)

#### `Data.json`
**Purpose**: Primary game statistics database

**Contents**:
- 3 games (Game_1, Game_2, Game_3)
- Game details and metadata
- Team lineups
- Quarter-by-quarter player statistics

**Structure**:
```json
{
    "Game_1": {
        "Details": { ... },
        "Lineup": { ... },
        "Quarters": { ... }
    }
}
```

**Size**: ~8 KB  
**Format**: JSON  
**Access**: Read by AccessData class  
**Modification**: Manual editing or future data entry tool

---

#### `Data.json.bak`
**Purpose**: Backup copy of primary data file

**Usage**:
- Recovery if Data.json corrupted
- Rollback to previous state
- Safety net for manual edits

**Maintenance**:
```bash
# Create backup before editing
cp Database/Data.json Database/Data.json.bak

# Restore from backup
cp Database/Data.json.bak Database/Data.json
```

**Update Frequency**: Manual (before significant changes)

---

### Documentation (doc/ Subdirectory)

#### `doc/data.json_doc.md`
**Purpose**: Comprehensive documentation for Data.json structure

**Contains**:
- Full file structure explanation
- Field definitions and data types
- Example data snippets
- Usage patterns in application
- Data validation rules
- Expansion guidelines

**Target Audience**: 
- Developers working with data layer
- Data entry personnel
- Future maintainers

**Format**: Markdown with code examples

---

### Logs (log/ Subdirectory)

#### `log/accessing_data_log.json`
**Purpose**: Tracks data access operations

**Logged Operations**:
- Data file reads
- Query executions
- Cache operations
- Error conditions

**Example Entry**:
```json
{
    "timestamp": "2025-08-15T18:30:45",
    "operation": "Get_season_stats",
    "player": "Aston Sharp",
    "success": true,
    "duration_ms": 15
}
```

**Usage**: Performance monitoring, debugging, audit trail

---

#### `log/player_report_log.json`
**Purpose**: Tracks GUI operations and user interactions

**Logged Operations**:
- Feature access (which statistics viewed)
- User navigation patterns
- Display updates
- GUI errors or crashes

**Example Entry**:
```json
{
    "timestamp": "2025-08-15T18:31:20",
    "feature": "Season_average",
    "player": "Aston Sharp",
    "stat_selected": "Points",
    "success": true
}
```

**Usage**: User behavior analysis, feature usage tracking, error diagnosis

---

#### `log/testing_log.json`
**Purpose**: Records test execution results

**Logged Operations**:
- Test runs (passed/failed)
- Test duration
- Coverage metrics
- Error details

**Example Entry**:
```json
{
    "timestamp": "2025-08-15T17:00:00",
    "test_file": "test_accessing_data.py",
    "tests_run": 15,
    "tests_passed": 14,
    "tests_failed": 1,
    "duration_ms": 250
}
```

**Usage**: Test history tracking, regression detection, quality metrics

---

## Directory Relationships

### Data Flow

```
Data.json
    ↓
    ├─ Read by: utils/accessing_data.py
    ↓          └─ Cached in memory
    ├─ Used by: testing/player_report.py
    ↓          └─ GUI displays statistics
    └─ Logged in: log/accessing_data_log.json
               └─ Performance tracking
```

### Backup Strategy

```
Data.json ────────→ Data.json.bak
    ↑                     ↓
    └─────────────────────┘
         (restore if needed)
```

### Documentation Relationship

```
Data.json ←────── doc/data.json_doc.md
  (actual data)    (explains structure)
       ↓
  AccessData.py ←── Uses schema knowledge
       ↓
  PlayerReport.py ← Displays formatted data
```

---

## Purpose and Benefits

### Data Storage
**Primary Function**: 
- Centralized game statistics storage
- Single source of truth
- Structured, queryable format

**Benefits**:
- Consistent data access patterns
- Easy backup and recovery
- Version control friendly (JSON text format)

---

### Data Safety
**Backup System**:
- `Data.json.bak` provides rollback capability
- Manual backup before edits prevents data loss
- Future: Automated versioned backups

**Integrity**:
- JSON validation ensures structure
- AccessData class enforces schema
- Documentation defines standards

---

### Observability
**Logging System**:
- Tracks data access patterns
- Monitors performance metrics
- Records user behavior
- Captures errors for debugging

**Benefits**:
- Performance optimization insights
- User experience improvements
- Error diagnosis and prevention
- Usage analytics

---

### Documentation
**Knowledge Base**:
- `data.json_doc.md` preserves schema knowledge
- Examples aid understanding
- Guidelines ensure consistency
- Reference for future development

---

## Usage Patterns

### Application Startup

```python
# 1. AccessData loads Data.json
from utils.accessing_data import AccessData

# 2. Data cached in memory
AccessData._ensure_initialized()

# 3. Operations logged
# log/accessing_data_log.json updated
```

---

### User Interaction

```python
# 1. User opens PlayerReport GUI
app = PlayerReport("Aston Sharp")

# 2. GUI requests data
stats = AccessData.Get_season_stats("Aston Sharp")

# 3. Data retrieved from cache
# No disk I/O after initial load

# 4. Interaction logged
# log/player_report_log.json updated
```

---

### Data Updates

```bash
# 1. Create backup
cp Database/Data.json Database/Data.json.bak

# 2. Edit Data.json
# Add new game, update stats

# 3. Validate JSON
python -m json.tool Database/Data.json

# 4. Test application
python testing/player_report.py

# 5. Commit changes
git add Database/Data.json
git commit -m "Add Game_4 data"
```

---

## Maintenance Procedures

### Regular Backups

**Manual Backup**:
```bash
# Before editing
cp Database/Data.json Database/Data.json.bak

# Versioned backup
cp Database/Data.json Database/Data.json.$(date +%Y%m%d_%H%M%S)
```

**Automated Backup** (future):
```bash
# Cron job or script
0 0 * * * cp /path/to/Database/Data.json /path/to/backups/Data.json.$(date +\%Y\%m\%d)
```

---

### Log Management

**Log Rotation** (recommended):
```bash
# Archive old logs
mv Database/log/accessing_data_log.json Database/log/accessing_data_log.json.old

# Start fresh log
echo "[]" > Database/log/accessing_data_log.json
```

**Log Analysis**:
```python
import json

with open('Database/log/accessing_data_log.json') as f:
    logs = json.load(f)

# Analyze performance
avg_duration = sum(log['duration_ms'] for log in logs) / len(logs)
print(f"Average query time: {avg_duration}ms")
```

---

### Data Validation

**Structure Check**:
```python
import json

def validate_data_json():
    with open('Database/Data.json') as f:
        data = json.load(f)
    
    for game_id, game in data.items():
        # Check sections exist
        assert 'Details' in game
        assert 'Lineup' in game
        assert 'Quarters' in game
        
        # Check stats structure
        for quarter in game['Quarters'].values():
            for player_stats in quarter.values():
                assert 'Points' in player_stats
                assert 'Fouls' in player_stats
                assert 'Rebounds' in player_stats
                assert 'Assists' in player_stats
                assert 'Turnovers' in player_stats
    
    print("Data validation passed")

validate_data_json()
```

---

## File Size and Growth

### Current State
- **Data.json**: ~8 KB (3 games)
- **Data.json.bak**: ~8 KB (backup)
- **Logs**: <1 KB each (minimal entries)
- **Total**: ~20 KB

### Projected Growth

**Per Season (20 games)**:
- Data.json: ~50 KB
- Logs: ~5 KB each
- Total: ~65 KB

**Multi-Season (5 years, 100 games)**:
- Data.json: ~250 KB
- Logs: ~25 KB each
- Total: ~325 KB

**Conclusion**: Negligible storage impact, no performance concerns

---

## Security Considerations

### Data Sensitivity

**Personal Information**:
- Player names (youth athletes)
- Team affiliations
- Performance data

**Recommendations**:
- Restrict file system access
- .gitignore for private deployments
- Consider anonymization for public sharing

---

### Backup Security

**Backup Location**:
```bash
# Keep backups outside repo for privacy
cp Database/Data.json ~/basketball-backups/Data.json.$(date +%Y%m%d)

# Or encrypted backup
tar czf - Database/ | gpg -c > basketball-backup.tar.gz.gpg
```

---

### Log Privacy

**Log Sanitization**:
```python
# Remove sensitive info from logs before sharing
import json

def sanitize_logs(log_file):
    with open(log_file) as f:
        logs = json.load(f)
    
    # Replace player names with IDs
    for log in logs:
        if 'player' in log:
            log['player'] = hash(log['player']) % 1000
    
    with open(log_file.replace('.json', '_sanitized.json'), 'w') as f:
        json.dump(logs, f, indent=2)
```

---

## Integration with Application

### AccessData Class

```python
# utils/accessing_data.py
class AccessData:
    data = {}  # Loaded from Database/Data.json
    
    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            # Load Database/Data.json
            with open('Database/Data.json') as f:
                cls.data = json.load(f)
```

**Dependency**: Application requires `Database/Data.json` to exist

---

### PlayerReport GUI

```python
# testing/player_report.py
from utils.accessing_data import AccessData

class PlayerReport:
    def __init__(self, players_name):
        # Implicitly loads Database/Data.json
        self.stats = AccessData.Get_season_stats(players_name)
```

**Dependency**: GUI functionality depends on Database folder structure

---

### Testing Suite

```python
# testing/test_file.py
import pytest
from utils.accessing_data import AccessData

def test_data_loading():
    # Tests Database/Data.json loading
    stats = AccessData.Get_season_stats("Aston Sharp")
    assert stats is not None
```

**Dependency**: Tests verify Database/Data.json integrity

---

## Common Workflows

### Add New Game Data

1. **Backup Current Data**
```bash
cp Database/Data.json Database/Data.json.bak
```

2. **Edit Data.json**
```json
"Game_4": {
    "Details": { ... },
    "Lineup": { ... },
    "Quarters": { ... }
}
```

3. **Validate JSON**
```bash
python -m json.tool Database/Data.json
```

4. **Test Application**
```bash
python testing/player_report.py
```

5. **Update Documentation**
```bash
# Edit doc/data.json_doc.md if schema changed
```

---

### Analyze Logs

```python
import json

# Load accessing_data logs
with open('Database/log/accessing_data_log.json') as f:
    access_logs = json.load(f)

# Find slow queries
slow_queries = [log for log in access_logs if log['duration_ms'] > 50]
print(f"Found {len(slow_queries)} slow queries")

# Most accessed players
from collections import Counter
players = [log['player'] for log in access_logs if 'player' in log]
popular = Counter(players).most_common(5)
print(f"Most viewed players: {popular}")
```

---

### Recover from Corruption

```bash
# If Data.json corrupted
cp Database/Data.json Database/Data.json.corrupted
cp Database/Data.json.bak Database/Data.json

# Verify restoration
python -m json.tool Database/Data.json
python testing/player_report.py
```

---

## Best Practices

### Data Management
- **Always backup before editing**
- Validate JSON after changes
- Test application after data updates
- Document schema modifications

### Log Management
- **Rotate logs periodically**
- Archive old logs for history
- Monitor log sizes
- Analyze for optimization opportunities

### Documentation
- **Keep docs in sync with data**
- Update doc/data.json_doc.md when schema changes
- Include examples for new fields
- Document breaking changes

### Version Control
- **Commit Data.json changes with messages**
- Don't commit logs (add to .gitignore)
- Commit documentation updates
- Tag releases with data versions

---

## Troubleshooting

### Data.json Not Found

**Error**: `FileNotFoundError: Database/Data.json`

**Causes**:
- File deleted or moved
- Wrong working directory
- Incorrect path in code

**Solutions**:
```bash
# Check file exists
ls -l Database/Data.json

# Check current directory
pwd

# Verify path in code
grep -r "Database/Data.json" utils/
```

---

### Invalid JSON Format

**Error**: `json.JSONDecodeError`

**Causes**:
- Syntax error (missing comma, bracket)
- Manual edit mistake
- Corrupted file

**Solutions**:
```bash
# Validate JSON
python -m json.tool Database/Data.json

# Restore from backup
cp Database/Data.json.bak Database/Data.json

# Use JSON linter
jsonlint Database/Data.json
```

---

### Missing Required Fields

**Error**: `KeyError` when accessing data

**Causes**:
- Incomplete game data
- Schema mismatch
- Player not in game

**Solutions**:
```python
# Safe access with defaults
stats = quarter_data.get(player_name, {})
points = stats.get('Points', 0)

# Validate before access
if player_name in quarter_data:
    points = quarter_data[player_name]['Points']
```

---

### Log Files Growing Large

**Issue**: Log files consuming disk space

**Solutions**:
```bash
# Check log sizes
du -sh Database/log/*.json

# Archive old logs
mkdir -p Database/log/archive
mv Database/log/*_log.json Database/log/archive/

# Start fresh
echo "[]" > Database/log/accessing_data_log.json
```

---

## Future Enhancements

### Automated Backups
```python
# Scheduled backup script
import shutil
from datetime import datetime

def auto_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'Database/backups/Data.json.{timestamp}'
    shutil.copy('Database/Data.json', backup_path)
    print(f"Backup created: {backup_path}")
```

---

### Database Migration
```python
# Migrate to SQLite for better querying
import json
import sqlite3

def migrate_to_sqlite():
    # Load JSON data
    with open('Database/Data.json') as f:
        data = json.load(f)
    
    # Create SQLite database
    conn = sqlite3.connect('Database/basketball.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE games (
            game_id TEXT PRIMARY KEY,
            date TEXT,
            opponent TEXT,
            our_score INTEGER,
            their_score INTEGER
        )
    ''')
    
    # Migrate data
    for game_id, game in data.items():
        cursor.execute('''
            INSERT INTO games VALUES (?, ?, ?, ?, ?)
        ''', (
            game_id,
            f"{game['Details']['Day']} {game['Details']['Month']} {game['Details']['Year']}",
            game['Details']['Game_against'],
            game['Details']['Our_Scores'],
            game['Details']['There_Scores']
        ))
    
    conn.commit()
    conn.close()
```

---

### Structured Logging
```python
# Enhanced logging with levels
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_data)

# Setup
logger = logging.getLogger('basketball_stats')
handler = logging.FileHandler('Database/log/application.log')
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

---

## Related Files and Folders

### Project Files
- `utils/accessing_data.py` - Reads Database/Data.json
- `testing/player_report.py` - Displays data from Database
- `.vscode/launch.json` - Sets cwd for Database access

### External Dependencies
- Python `json` module - Parses Data.json
- File system - Stores all Database files
- Version control - Tracks Data.json changes

---

## Summary

The `Database/` folder provides:

1. **Data Storage**
   - Primary game statistics (Data.json)
   - Backup safety net (Data.json.bak)

2. **Documentation**
   - Schema reference (doc/data.json_doc.md)
   - Usage guidelines

3. **Observability**
   - Access logs (log/accessing_data_log.json)
   - GUI logs (log/player_report_log.json)
   - Test logs (log/testing_log.json)

**Key Benefits**:
- Centralized data management
- Backup and recovery capability
- Comprehensive documentation
- Operation tracking and debugging
- Performance monitoring

**Critical Files**:
- `Data.json` - Primary data (required)
- `Data.json.bak` - Backup (safety)
- `doc/data.json_doc.md` - Schema reference

**Maintenance**: Regular backups, log rotation, validation checks