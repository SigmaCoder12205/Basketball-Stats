# accessing_data.py Documentation

## Overview

**FILE**: `utils/accessing_data.py`  
**PURPOSE**: Data access layer for basketball statistics system  
**RATING**: 760/1000  
**LINES**: ~1000 (excluding comments/docstrings)

Core data management class providing comprehensive query methods, aggregation functions, and statistical calculations with extensive logging and error handling.

---

## Quick Reference

### File Statistics

```
TOTAL CLASSES:        1 (AccessData)
TOTAL METHODS:        18 (class methods + instance methods)
TOTAL FUNCTIONS:      2 (utility functions)
TOTAL METHODS+FUNCS:  20
CLASS METHODS:        14 (most query methods)
INSTANCE METHODS:     4 (initialization, save, repr, str)
```

---

### Method Categories

```python
# UTILITY FUNCTIONS (2)
get_public_ip()
create_log()

# INITIALIZATION (4)
__init__()
__repr__()
__str__()
initialize()

# DATA PERSISTENCE (1)
save()

# METADATA QUERIES (2)
get_details()
get_lineup()

# STATISTICS QUERIES (8)
get_quarter_stats()
get_specific_stats()
get_game_stats()
get_season_stats()
get_team_season_stats()
get_quarter_season_stats()
get_highest_stats_quarter()
get_highest_stats_game()

# ANALYSIS (2)
specific_players_best_stat()
check_player()
```

---

## Critical Issues

### Hardcoded Absolute Paths

**Multiple Locations**:
```python
sys.path.extend(r"C:/Users/Drags Jrs/Drags")
os.makedirs("C:/Users/Drags Jrs/Database/errors", exist_ok=True)
write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", ...)
```

**Problem**: Won't work on other machines

**Fix**: Use relative paths from `__file__`

---

### Class vs Instance Method Confusion

**Issue**: Mix of classmethods and instance methods accessing same data

```python
class AccessData:
    data: Dict = {}  # Shared class variable
    
    def __init__(self):  # Instance method
        self.initialize()
    
    @classmethod
    def get_season_stats(cls):  # Classmethod
        cls._ensure_initialized()
        return cls.data  # Uses class variable
```

**Problem**: 
- All instances share same data
- Thread-unsafe
- Breaks encapsulation

---

### Logging in Every Method

**Pattern** (repeated 20+ times):
```python
try:
    # Method logic
    log_entry = create_log(level="INFO", ...)
    write.write_to("C:/Users/.../log.json", log_entry)
except Exception as e:
    error = {"type": type(e).__name__, "message": str(e)}
    log_entry = create_log(level="ERROR", error=error, ...)
    write.write_to("C:/Users/.../log.json", log_entry)
    return log_entry
```

**Issues**:
- Code duplication (DRY violation)
- Performance overhead
- Hardcoded log path
- Sequential I/O blocking

---

## Key Components

### Utility Functions

#### `get_public_ip()`
```python
def get_public_ip() -> str:
    try:
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except Exception:
        return socket.gethostbyname(socket.gethostname())
```

**Purpose**: Get public IP with fallback  
**API**: `https://api.ipify.org`  
**Fallback**: Local hostname IP

---

#### `create_log()`
```python
def create_log(level, message, where, error=None, ...) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "log_level": level,
        "service_name": "access_data_service",
        "host": socket.gethostname(),
        "message": message,
        "where": where,
        "user_id": user_id,
        "source_ip": source_ip,
        "request_id": request_id,
        **( {"error": error} if error else {})
    }
```

**Purpose**: Structured logging  
**Format**: JSON-compatible dict  
**Tracking**: UUID per request

---

### AccessData Class

#### Class Variables
```python
data: Dict[str, Any] = {}          # Shared JSON data
file_path: str = ""                 # Path to Data.json
_initialized: bool = False          # Init flag
current_time: datetime              # Timestamp
error_message: dict                 # Error storage
user_id: str = "N/A"               # User tracking
source_ip: str = "N/A"             # IP tracking
request_id: str = "N/A"            # Request ID
```

**Note**: Class-level variables shared across all instances

---

#### Initialization Pattern

```python
def __init__(self, user_id="anonymous", source_ip=None):
    self.user_id = user_id
    self.source_ip = source_ip
    self.request_id = str(uuid.uuid4())
    self.current_time = datetime.now(timezone.utc)
    self.initialize()  # Load data

@classmethod
def _ensure_initialized(cls):
    if not cls._initialized:
        cls()  # Create instance
        cls._initialized = True
```

**Pattern**: Lazy initialization with singleton-like behavior

---

### Data Loading

#### `initialize()`
```python
def initialize(self, load=False, filename="Data.json"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "Database", filename)
    
    with open(data_file, 'r', encoding="utf-8") as file:
        data = json.load(file)
        AccessData.data = data  # Store in class variable
    
    return AccessData.data if load else None
```

**Process**:
1. Calculate relative path to Database/
2. Load and validate JSON
3. Store in class variable
4. Log success/failure

---

### Data Persistence

#### `save()`
```python
def save(self, filename=None, backup=True) -> bool:
    save_path = filename or self.file_path
    
    if backup and os.path.exists(save_path):
        shutil.copy2(save_path, f"{save_path}.bak")
    
    temp_path = f"{save_path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    os.replace(temp_path, save_path)  # Atomic
    return True
```

**Features**:
- Automatic backup (.bak file)
- Atomic write (temp file + replace)
- Error handling with logging

---

## Query Methods Overview

### Pattern: `look_good` Parameter

**All query methods have**:
```python
def method(..., look_good: bool = False):
    if look_good:
        return formatted_string  # Human-readable
    else:
        return raw_data          # Dict/list
```

**Purpose**: Single method for both data and display

**Issue**: Mixes data access with presentation logic

---

### Example: `get_season_stats()`

```python
@classmethod
def get_season_stats(cls, player, sum_total=False, look_good=False):
    cls._ensure_initialized()
    
    if sum_total:
        # Return aggregated stats across all games
        total = {}
        for game in cls.data.values():
            for quarter in game["Quarters"].values():
                if player in quarter:
                    for stat, value in quarter[player].items():
                        total[stat] = total.get(stat, 0) + value
        return total
    else:
        # Return per-game stats
        game_totals = {}
        for game_name, game in cls.data.items():
            # Aggregate quarters for this game
            ...
        return game_totals
```

**Parameters**:
- `player`: Player name
- `sum_total`: True = season total, False = per-game
- `look_good`: True = formatted string, False = dict

---

## Performance Concerns

### Issue 1: No Caching

**Current**:
```python
@classmethod
def get_season_stats(cls, player, ...):
    # Iterates entire dataset EVERY call
    for game in cls.data.values():
        for quarter in game["Quarters"].values():
            # Aggregate...
```

**Problem**: O(n) on every call, no memoization

**Solution**:
```python
from functools import lru_cache

@classmethod
@lru_cache(maxsize=128)
def get_season_stats_cached(cls, player, sum_total):
    # Expensive calculation
    ...
```

---

### Issue 2: Sequential I/O

**Current**:
```python
# Every method writes log synchronously
write.write_to("C:/Users/.../log.json", log_entry)
```

**Problem**: Blocks execution, scales poorly

**Solution**:
```python
import queue
import threading

log_queue = queue.Queue()

def log_worker():
    while True:
        log_entry = log_queue.get()
        write.write_to("...", log_entry)
        log_queue.task_done()

# In methods
log_queue.put(log_entry)  # Non-blocking
```

---

### Issue 3: String Formatting Overhead

**Current** (`look_good=True`):
```python
output = "-------------------- Header ---------------------\n"
for player, stats in data.items():
    stat_line = ", ".join(f"{k}: {v}" for k, v in stats.items())
    output += f"{player}: {stat_line}\n"
return output
```

**Problem**: String concatenation, repeated formatting

**Better**: Return data, format in presentation layer

---

## Design Patterns

### Singleton-Like Data Sharing

**Implementation**:
```python
class AccessData:
    data = {}  # Class variable, shared
    _initialized = False
    
    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            cls()
```

**Pros**: Single data load  
**Cons**: Thread-unsafe, breaks instance isolation

---

### Classmethod Query Pattern

**Why classmethods?**
- No instance creation needed
- Shared data access
- Convenient for GUI (`AccessData.get_season_stats(...)`)

**Trade-off**: All instances share state

---

## Method Reference

### Metadata Queries

| Method | Purpose | Returns |
|--------|---------|---------|
| `get_details(game)` | Game metadata | Dict of details |
| `get_lineup(game, team)` | Team roster | List of players |

---

### Statistics Queries

| Method | Purpose | Granularity |
|--------|---------|-------------|
| `get_quarter_stats` | Quarter stats | All players |
| `get_specific_stats` | Player quarter stats | Single player/quarter |
| `get_game_stats` | Game totals | All players or one |
| `get_season_stats` | Season totals | Single player |
| `get_team_season_stats` | Team season stats | All players |
| `get_quarter_season_stats` | Quarter across season | Single player/quarter |

---

### Analysis Methods

| Method | Purpose | Use Case |
|--------|---------|----------|
| `get_highest_stats_quarter` | Leader in quarter | Find top scorer |
| `get_highest_stats_game` | Leader in game | Game MVP |
| `specific_players_best_stat` | Player's peak | Career high |
| `check_player` | Verify participation | Roster validation |

---

## Error Handling Pattern

**Every method**:
```python
try:
    # Validation
    if not isinstance(param, expected_type):
        raise TypeError(f"param must be {expected_type}")
    
    # Business logic
    result = ...
    
    # Log success
    log_entry = create_log(level="INFO", ...)
    write.write_to("...", log_entry)
    
    return result

except Exception as e:
    # Log error
    error = {"type": type(e).__name__, "message": str(e)}
    log_entry = create_log(level="ERROR", error=error, ...)
    write.write_to("...", log_entry)
    return log_entry  # Or raise
```

**Issues**:
- Inconsistent: Some return error dict, some raise
- Code duplication (20+ copies)
- Mixes error handling with business logic

---

## Dependencies

### External Libraries
```python
import json          # Data serialization
import os            # File operations
import shutil        # Backup operations
import socket        # Network info
import uuid          # Request IDs
import urllib.request # IP lookup
from typing import Optional, Dict, Any
from datetime import datetime, timezone
```

### Internal Modules
```python
from utils import write  # Logging
# OR
import write             # Fallback
```

**Circular Dependency Risk**: write module may import this

---

## Usage Examples

### Basic Usage

```python
# Create instance
asd = AccessData(user_id="owner")

# Get season totals
stats = AccessData.get_season_stats(
    player="Aston Sharp",
    sum_total=True
)
# Returns: {'Points': 37, 'Fouls': 3, ...}

# Get formatted output
output = AccessData.get_season_stats(
    player="Aston Sharp",
    sum_total=True,
    look_good=True
)
# Returns: "Season stats for Aston Sharp\n    - Points: 37\n..."
```

---

### Advanced Queries

```python
# Find best performer in quarter
leader = AccessData.get_highest_stats_quarter(
    game="Game_1",
    quarter="Quarter 1",
    what_to_look_for="Points"
)
# Returns: {'Player Name': 22}

# Get player's career high
best = AccessData.specific_players_best_stat(
    player="Aston Sharp",
    what_to_look_for="Points",
    look_good=True
)
# Returns: "Aston Sharp got the most Points (22) in Quarter 2 of Game_2"
```

---

## Recommendations

### Immediate Fixes

1. **Remove hardcoded paths**
```python
# Use relative paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(base_dir, "Database", "log", "accessing_data_log.json")
```

2. **Extract logging decorator**
```python
def log_method(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            log_success()
            return result
        except Exception as e:
            log_error(e)
            raise
    return wrapper
```

3. **Separate presentation**
```python
# Remove look_good parameter
# Create separate Formatter class
```

---

### Medium-Term Improvements

1. **Add caching layer**
2. **Async logging**
3. **Type validation with Pydantic**
4. **Separate concerns (data vs presentation)**
5. **Add indices for fast lookups**

---

### Long-Term Migration

**Move to database**:
```python
# Replace JSON with SQLite
import sqlite3

class AccessDataDB:
    def get_season_stats(self, player):
        with sqlite3.connect('basketball.db') as conn:
            return conn.execute(
                "SELECT SUM(points), SUM(rebounds) FROM stats WHERE player=?",
                (player,)
            ).fetchone()
```

**Benefits**: Efficient queries, transactions, scalability

---

## Summary

`utils/accessing_data.py` provides:

**Functionality**: Comprehensive data access layer with 18 methods

**Strengths**:
- Complete feature set
- Extensive error handling
- Detailed logging
- Type hints
- Atomic save operations

**Issues**:
- Hardcoded absolute paths (won't work on other machines)
- No caching (O(n) every query)
- Class/instance confusion (shared data)
- Logging overhead (synchronous I/O)
- Presentation mixed with data (look_good parameter)
- Code duplication (20+ identical try-except blocks)

**Rating**: 760/1000 (functional but needs refactoring)

**Dependencies**: write module, Database/Data.json

**Primary Users**: PlayerReport GUI, analysis tools

**Critical for**: All statistics features in application