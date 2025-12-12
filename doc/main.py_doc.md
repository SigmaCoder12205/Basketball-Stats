# main.py Documentation

## Overview

**FILE**: `main/main.py`  
**PURPOSE**: Application entry point for basketball statistics GUI

Minimal launcher script that configures Python path and initializes the PlayerReport GUI application.

---

## Full File Content

```python
import sys
sys.path.append("C:/Users/Drags Jrs/Drags")
from PyQt5.QtWidgets import QApplication
from main.player_report import PlayerReport
from utils.accessing_data import AccessData
```

---

## Code Breakdown

### Path Configuration

```python
import sys
sys.path.append("C:/Users/Drags Jrs/Drags")
```

**Purpose**: Add parent directory to Python module search path

**Details**:
- `sys.path`: List of directories Python searches for modules
- `.append()`: Adds directory to end of search path
- Path: `"C:/Users/Drags Jrs/Drags"` (absolute path to project root)

**Why Needed**:
- Enables imports from `main`, `utils`, `testing` modules
- Without this: `ModuleNotFoundError` for local packages
- Allows script to find project modules regardless of working directory

**Issue - Hardcoded Path**:
- **Problem**: Absolute path specific to one machine
- **Impact**: Won't work on other computers or users
- **Location**: `"C:/Users/Drags Jrs/Drags"` only valid on developer machine
- **Result**: Other developers get import errors

---

### Imports

```python
from PyQt5.QtWidgets import QApplication
from main.player_report import PlayerReport
from utils.accessing_data import AccessData
```

**QApplication** (`PyQt5.QtWidgets`):
- Main Qt application class
- Manages GUI event loop
- Required for all PyQt5 applications
- Handles windowing system integration

**PlayerReport** (`main.player_report`):
- Main GUI window class
- Player statistics report card interface
- Displays all analytics features
- Inherits from QWidget

**AccessData** (`utils.accessing_data`):
- Data access layer class
- Loads and caches game statistics
- Provides query methods
- Backend for GUI data

**Import Note**: Imports modules but doesn't use them (incomplete file)

---

## File Status

### Incomplete Implementation

**Current State**:
- Imports configured
- No execution code
- No `if __name__ == '__main__'` block
- No application instantiation
- No GUI launch

**Expected Code** (Missing):
```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayerReport("Player Name")
    window.show()
    sys.exit(app.exec_())
```

**Result**: Running this file does nothing (imports only)

---

### Legacy Status

**Indicators**:
1. Outdated import path (`main.player_report` vs `testing.player_report`)
2. Hardcoded absolute path
3. Incomplete implementation
4. Superseded by `testing/player_report.py`

**Current Entry Point**: `testing/player_report.py` (complete implementation)

---

## Issues and Problems

### Issue 1: Hardcoded Absolute Path

```python
sys.path.append("C:/Users/Drags Jrs/Drags")
```

**Problems**:
- Machine-specific path
- Won't work on other computers
- Breaks on different user accounts
- Not portable or shareable

**Solutions**:

**Option A - Relative Path**:
```python
import sys
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get project root (parent of main/)
project_root = os.path.dirname(script_dir)

# Add to path
sys.path.insert(0, project_root)
```

**Option B - Package Installation**:
```bash
# Install project as package
pip install -e .

# No path manipulation needed
from main.player_report import PlayerReport
```

**Option C - Working Directory**:
```bash
# Run from project root
cd "C:/Users/Drags Jrs/Drags"
python main/main.py

# Python automatically adds cwd to path
```

---

### Issue 2: Incorrect Import Path

```python
from main.player_report import PlayerReport
```

**Problem**: `player_report.py` not in `main/` folder

**Actual Location**: `testing/player_report.py`

**Result**: `ModuleNotFoundError: No module named 'main.player_report'`

**Fix**:
```python
from testing.player_report import PlayerReport
```

---

### Issue 3: Unused Import

```python
from utils.accessing_data import AccessData
```

**Issue**: Imported but never used

**Reason**: File incomplete, no code references AccessData

**Cleanup**:
```python
# Remove unused import
# AccessData imported automatically by PlayerReport
```

---

### Issue 4: No Execution Logic

**Problem**: File has no `if __name__ == '__main__'` block

**Result**: Nothing happens when run

**Fix**:
```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayerReport("Aston Sharp")
    window.show()
    sys.exit(app.exec_())
```

---

## Correct Implementation

### Fixed Version

```python
"""Basketball Statistics Application - Main Entry Point"""
import sys
import os

# Add project root to path (relative, not hardcoded)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from testing.player_report import PlayerReport  # Correct path


def main(player_name="Aston Sharp"):
    """Launch the player report GUI application.
    
    Args:
        player_name (str): Name of player to display
    """
    app = QApplication(sys.argv)
    window = PlayerReport(player_name)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Parse command line arguments for player name
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()  # Default player
```

---

### Enhanced Version with Error Handling

```python
"""Basketball Statistics Application - Main Entry Point"""
import sys
import os

# Configure path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from testing.player_report import PlayerReport
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Ensure PyQt5 is installed: pip install PyQt5")
    sys.exit(1)


def main(player_name="Aston Sharp"):
    """Launch the player report GUI application.
    
    Args:
        player_name (str): Name of player to display
        
    Returns:
        int: Application exit code
    """
    try:
        app = QApplication(sys.argv)
        window = PlayerReport(player_name)
        window.show()
        return app.exec_()
    except Exception as e:
        print(f"Error launching application: {e}")
        return 1


if __name__ == '__main__':
    # Parse command line arguments
    player = sys.argv[1] if len(sys.argv) > 1 else "Aston Sharp"
    
    exit_code = main(player)
    sys.exit(exit_code)
```

---

## Usage

### Current File (Broken)

```bash
# Attempt to run
cd "C:/Users/Drags Jrs/Drags"
python main/main.py

# Result: Nothing happens (no execution code)
```

---

### After Fixes

```bash
# Run with default player
python main/main.py

# Run with specific player
python main/main.py "Benjamin Berridge"

# Or from project root
cd basketball-stats
python main/main.py
```

---

## Relationship to Other Files

### Current Application Flow

```
testing/player_report.py (Actual Entry Point)
├── Contains if __name__ == '__main__' block
├── Launches GUI directly
└── Complete implementation

main/main.py (Legacy/Incomplete)
├── No execution code
├── Incorrect imports
└── Not used
```

---

### Intended Application Flow

```
main/main.py (Entry Point)
└── Imports and launches
    ├── testing/player_report.py (GUI)
    │   └── utils/accessing_data.py (Data Layer)
    │       └── Database/Data.json (Data Storage)
```

---

## Comparison with Active Entry Point

### main/main.py (This File)

```python
# Imports only
import sys
sys.path.append("C:/Users/Drags Jrs/Drags")
from PyQt5.QtWidgets import QApplication
from main.player_report import PlayerReport
from utils.accessing_data import AccessData

# Nothing else
```

**Status**: Incomplete, not functional

---

### testing/player_report.py (Active)

```python
# Path configuration
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from utils.accessing_data import AccessData
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# Full class implementation
class PlayerReport(QWidget):
    # ... 1000+ lines ...

# Execution block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    report = PlayerReport("Aston Sharp")
    report.show()
    sys.exit(app.exec_())
```

**Status**: Complete, functional, actively used

---

## Recommendations

### Option 1: Delete This File

**Rationale**:
- Incomplete implementation
- Superseded by testing/player_report.py
- Confusing for developers
- No unique functionality

**Action**:
```bash
git rm main/main.py
git commit -m "Remove legacy incomplete main.py"
```

---

### Option 2: Fix and Use This File

**Rationale**:
- Separation of concerns (launcher vs GUI)
- Clear entry point
- Easier command-line interface

**Action**:
1. Implement fixes from "Correct Implementation"
2. Keep testing/player_report.py as GUI module only
3. Remove execution block from testing/player_report.py
4. Update documentation and launch configs

---

### Option 3: Redirect to Active Entry Point

**Minimal Fix**:
```python
"""
Legacy entry point - redirects to active implementation.
Use testing/player_report.py directly instead.
"""
import sys
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

# Import and run active entry point
if __name__ == '__main__':
    print("Note: Using testing/player_report.py as entry point")
    print("Consider running that file directly")
    
    from testing.player_report import PlayerReport
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = PlayerReport("Aston Sharp")
    window.show()
    sys.exit(app.exec_())
```

---

## Integration with Project

### Launch Configurations

**VS Code launch.json** currently references:
```json
{
    "name": "▶ Run Main",
    "program": "${workspaceFolder}/Code/main.py"  // Wrong path
}
```

**Issues**:
1. Path points to `Code/main.py` (doesn't exist)
2. Should be `main/main.py` or `testing/player_report.py`
3. Configuration not aligned with actual structure

**Fix**:
```json
{
    "name": "▶ Run Main",
    "program": "${workspaceFolder}/testing/player_report.py"  // Actual entry point
}
```

---

### Import Dependencies

**Required Packages**:
```bash
pip install PyQt5
```

**Project Modules**:
- `utils.accessing_data` - Data layer
- `testing.player_report` - GUI (correct path)
- `main.player_report` - Doesn't exist (wrong path)

---

## Best Practices

### Path Manipulation

**Don't**:
```python
sys.path.append("C:/Users/Drags Jrs/Drags")  # Hardcoded
```

**Do**:
```python
# Relative to script location
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
```

---

### Entry Point Pattern

**Standard Structure**:
```python
"""Module docstring"""
import sys
import os

# Path configuration
# ...

# Imports
from PyQt5.QtWidgets import QApplication
from testing.player_report import PlayerReport


def main():
    """Application entry point"""
    # Setup
    # Launch
    # Return exit code


if __name__ == '__main__':
    sys.exit(main())
```

---

### Import Organization

```python
# Standard library
import sys
import os

# Third-party
from PyQt5.QtWidgets import QApplication

# Local modules
from testing.player_report import PlayerReport
from utils.accessing_data import AccessData
```

---

## Related Files

### Active Files
- `testing/player_report.py` - Actual GUI entry point
- `utils/accessing_data.py` - Data access layer
- `Database/Data.json` - Data storage

### Configuration
- `.vscode/launch.json` - Debug configurations (needs update)
- `requirements.txt` - Dependencies (if exists)

### Legacy
- `Old-basketball-stats/Code/main.py` - Original implementation
- This file (`main/main.py`) - Incomplete rewrite

---

## Summary

`main/main.py` is:

**Current State**:
- Incomplete implementation
- Hardcoded absolute path
- Incorrect import paths
- No execution code
- Legacy/unused file

**Issues**:
1. Path: `"C:/Users/Drags Jrs/Drags"` (machine-specific)
2. Import: `main.player_report` (doesn't exist)
3. Unused: AccessData import
4. Missing: Execution logic

**Recommendations**:
- **Delete**: Remove as redundant/incomplete
- **Fix**: Implement properly with corrections
- **Redirect**: Point to active entry point

**Active Entry Point**: `testing/player_report.py` (complete, functional)

**Action Required**: Decide to delete, fix, or redirect this file