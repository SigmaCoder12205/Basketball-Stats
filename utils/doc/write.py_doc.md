# write.py Documentation

## Overview

**FILE**: `utils/write.py`  
**PURPOSE**: Append-only JSON logging utility  
**LINES**: ~15

Simple utility function for appending log entries to JSON array files.

---

## Full File Content

```python
# Writes to a given file for errors 
import json
import os

def write_to(filename, what_to_write):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = [data]
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    data.append(what_to_write)
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
```

---

## Function Details

### `write_to(filename, what_to_write)`

**Purpose**: Append log entry to JSON array file

**Parameters**:
- `filename` (str): Path to JSON log file
- `what_to_write` (Any): Data to append (typically dict)

**Returns**: None

---

## How It Works

### Algorithm

```python
1. Try to read existing file as JSON
2. If not list, convert to list
3. If file missing or invalid, start with empty list
4. Append new entry to list
5. Write entire list back to file
```

---

## Usage Examples

### Basic Logging

```python
from utils.write import write_to

# Log entry
log_entry = {
    "timestamp": "2025-12-08T10:30:00",
    "level": "INFO",
    "message": "Operation successful"
}

write_to("Database/log/app_log.json", log_entry)
```

**Result** (`app_log.json`):
```json
[
  {
    "timestamp": "2025-12-08T10:30:00",
    "level": "INFO",
    "message": "Operation successful"
  }
]
```

---

### Multiple Entries

```python
# First call
write_to("log.json", {"id": 1, "status": "start"})

# Second call
write_to("log.json", {"id": 2, "status": "end"})
```

**Result** (`log.json`):
```json
[
  {"id": 1, "status": "start"},
  {"id": 2, "status": "end"}
]
```

---

## Issues and Limitations

### Issue 1: Race Condition

**Problem**: Not thread-safe or process-safe

```python
# Process A reads file
# Process B reads file
# Process A writes (entry 1)
# Process B writes (overwrites, loses entry 1)
```

**Impact**: Lost log entries under concurrent access

**Fix**:
```python
import fcntl  # Unix
# Or use file locking library

def write_to(filename, what_to_write):
    with open(filename, 'a+') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        # Read, append, write
        fcntl.flock(file, fcntl.LOCK_UN)
```

---

### Issue 2: Performance

**Problem**: Read entire file, append one entry, write entire file

```python
# For large log files (1000+ entries)
data = json.load(file)  # Load all
data.append(new_entry)  # Add one
json.dump(data, file)   # Write all
```

**Impact**: O(n) time, O(n) memory, slow for large logs

**Better**:
```python
# Append-only mode (but not valid JSON array)
with open(filename, 'a') as file:
    file.write(json.dumps(what_to_write) + '\n')
```

---

### Issue 3: No Error Handling

**Problem**: Write failures silent

```python
with open(filename, 'w') as file:
    json.dump(data, file, indent=2)
# No try-except for disk full, permissions, etc.
```

**Fix**:
```python
try:
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
except IOError as e:
    print(f"Failed to write log: {e}")
    raise
```

---

### Issue 4: Corruption Risk

**Problem**: Interruption during write corrupts file

```python
# Power loss here:
with open(filename, 'w') as file:
    json.dump(data, file)  # ← Incomplete write = corrupted JSON
```

**Fix**: Atomic write
```python
import os
import tempfile

# Write to temp file
with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
    json.dump(data, tmp, indent=2)
    tmp_name = tmp.name

# Atomic rename
os.replace(tmp_name, filename)
```

---

## Design Analysis

### What It Does Well

✓ Simple API (one function, two parameters)  
✓ Creates file if missing  
✓ Handles corrupt JSON  
✓ Maintains JSON array format  
✓ Pretty-prints with indent

---

### What Needs Improvement

❌ Not thread/process-safe  
❌ Poor performance for large files  
❌ No error handling on write  
❌ File corruption risk  
❌ No rotation/size limits  
❌ Loads entire file into memory

---

## Recommended Improvements

### Production-Ready Version

```python
import json
import os
import fcntl
import tempfile
from pathlib import Path

def write_to(filename: str, what_to_write: dict) -> bool:
    """Safely append log entry to JSON array file.
    
    Args:
        filename: Path to log file
        what_to_write: Dict to append
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        # Lock file for exclusive access
        with open(filename, 'a+') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            
            # Read existing data
            file.seek(0)
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = [data]
            except (ValueError, json.JSONDecodeError):
                data = []
            
            # Append new entry
            data.append(what_to_write)
            
            # Write atomically via temp file
            with tempfile.NamedTemporaryFile('w', dir=os.path.dirname(filename), 
                                            delete=False) as tmp:
                json.dump(data, tmp, indent=2)
                tmp_name = tmp.name
            
            os.replace(tmp_name, filename)
            fcntl.flock(file, fcntl.LOCK_UN)
            
        return True
        
    except Exception as e:
        print(f"Log write failed: {e}")
        return False
```

---

## Alternative: Append-Only Format

### JSONL (JSON Lines)

```python
def write_to_jsonl(filename: str, what_to_write: dict):
    """Append JSON object as new line (JSONL format)."""
    with open(filename, 'a') as file:
        file.write(json.dumps(what_to_write) + '\n')
```

**Pros**:
- Fast (no read, just append)
- Memory efficient
- Concurrent-safe (append-only)

**Cons**:
- Not valid JSON array
- Need special parser

---

## Usage in Project

### Called By

`accessing_data.py` (20+ times):
```python
from utils import write

log_entry = create_log(...)
write.write_to("C:/Users/.../log.json", log_entry)
```

`player_report.py` (27+ times):
```python
from utils.write import write_to

log_entry = create_log(...)
write_to("C:/Users/.../log.json", log_entry)
```

---

### Log Files Written

```
Database/log/
├── accessing_data_log.json    # Data layer logs
└── player_report_log.json     # GUI logs
```

---

## Summary

`utils/write.py` provides:

**Purpose**: Simple JSON log appending

**Strengths**:
- Simple API
- Handles missing files
- Creates arrays automatically
- Pretty-prints output

**Weaknesses**:
- Not thread-safe (race conditions)
- Poor performance (read all, write all)
- No write error handling
- File corruption risk
- No log rotation

**Status**: Functional for single-threaded, low-volume use

**Recommendations**:
- Add file locking for concurrency
- Implement atomic writes
- Add error handling
- Consider JSONL format for performance
- Add log rotation/size limits

**Critical**: Used by all logging throughout application