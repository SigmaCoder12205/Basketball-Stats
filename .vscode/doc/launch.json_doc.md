# launch.json Documentation

## Overview

**FILE**: `.vscode/launch.json`  
**PURPOSE**: VS Code debugger configuration for Python basketball statistics application

Defines launch configurations for running and debugging different entry points of the application through VS Code's integrated debugger.

---

## Full File Content

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "▶ Run Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "▶ Run Player Report",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/testing/player_report.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "▶ Run Main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/Code/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "▶ Run AccessData Module",
            "type": "python",
            "request": "launch",
            "module": "utils.accessing_data",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

---

## Structure

JSON configuration file with four launch configurations:
1. **Run Current File** - Generic Python file execution
2. **Run Player Report** - GUI application entry point
3. **Run Main** - Legacy main application entry point
4. **Run AccessData Module** - Data layer module execution

---

## Configuration Details

### Global Settings

```json
"version": "0.2.0"
```

VS Code debug configuration schema version.

---

### Configuration 1: Run Current File

```json
{
    "name": "▶ Run Current File",
    "type": "python",
    "request": "launch",
    "program": "${file}",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

**Purpose**: Execute any Python file currently open in the editor

**Properties**:
- `name`: Display name in debug dropdown (▶ prefix indicates run action)
- `type`: Language runtime (Python)
- `request`: Launch mode (creates new debug session)
- `program`: Target file (`${file}` = currently active file)
- `console`: Output destination (integrated terminal in VS Code)
- `cwd`: Working directory (`${workspaceFolder}` = project root)

**Usage**: 
- Open any `.py` file
- Press F5 or select from debug dropdown
- Executes file in integrated terminal

**Use Cases**:
- Quick testing of individual modules
- Running utility scripts
- Testing isolated functions

---

### Configuration 2: Run Player Report

```json
{
    "name": "▶ Run Player Report",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/testing/player_report.py",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

**Purpose**: Launch the Player Report Card GUI application

**Properties**:
- `program`: Fixed path to `testing/player_report.py`
- All other properties same as Configuration 1

**Usage**:
- Select from debug dropdown
- Launches PyQt5 GUI for player statistics
- Default player: "Aston Sharp" (hardcoded in file)

**What Happens**:
1. Initializes PyQt5 QApplication
2. Creates PlayerReport window
3. Displays GUI with 6 main menu features
4. Enters Qt event loop

**Primary Interface**: Main user-facing application for viewing player analytics

---

### Configuration 3: Run Main

```json
{
    "name": "▶ Run Main",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/Code/main.py",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

**Purpose**: Execute legacy main application entry point

**Properties**:
- `program`: Fixed path to `Code/main.py`
- All other properties same as Configuration 1

**Note**: Path appears incorrect based on folder structure
- Expected: `${workspaceFolder}/main/main.py`
- Current: `${workspaceFolder}/Code/main.py`
- May require path correction

**Status**: Legacy configuration (old codebase structure)

---

### Configuration 4: Run AccessData Module

```json
{
    "name": "▶ Run AccessData Module",
    "type": "python",
    "request": "launch",
    "module": "utils.accessing_data",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

**Purpose**: Execute data access layer module directly

**Properties**:
- `module`: Python module path (not file path)
- Uses module execution instead of file execution
- Equivalent to: `python -m utils.accessing_data`

**Usage**:
- Testing AccessData class functionality
- Running module-level code (if any `if __name__ == '__main__'` blocks)
- Debugging data retrieval operations

**Data Layer**: Core module for JSON data operations

---

## VS Code Variables

### `${file}`
- Path to currently active file in editor
- Dynamic - changes based on which file has focus
- Example: `/path/to/project/testing/player_report.py`

### `${workspaceFolder}`
- Root directory of the opened workspace/project
- Static - remains constant for project
- Example: `/path/to/basketball-stats`

---

## Console Options

### `integratedTerminal`
- Runs program in VS Code's integrated terminal pane
- Allows input/output interaction
- Preserves terminal after execution
- Best for GUI applications and interactive programs

### Alternative (not used):
- `internalConsole`: VS Code Debug Console (output only)
- `externalTerminal`: System terminal window

---

## Execution Methods

### Via F5 Key
1. Open desired file or use dropdown
2. Press F5
3. Executes currently selected configuration

### Via Debug Dropdown
1. Click debug icon in sidebar (or Ctrl+Shift+D)
2. Select configuration from dropdown
3. Click green play button

### Via Command Palette
1. Ctrl+Shift+P (Cmd+Shift+P on Mac)
2. Type "Debug: Select and Start Debugging"
3. Choose configuration

---

## Working Directory Behavior

All configurations set `cwd` to `${workspaceFolder}`:

**Impact**:
- Relative imports resolved from project root
- File operations use paths relative to root
- Example: `utils.accessing_data` import works correctly

**Without Correct CWD**:
- `ModuleNotFoundError` for local imports
- File paths would fail (e.g., `Database/Data.json`)

---

## Configuration Usage Matrix

| Configuration | When to Use | Target Audience |
|--------------|-------------|-----------------|
| Run Current File | Testing individual modules | Developers |
| Run Player Report | Launch main GUI application | End users, Testing |
| Run Main | Legacy application execution | Deprecated |
| Run AccessData | Test data layer | Developers, Debugging |

---

## Common Workflows

### Development
1. Edit code in any module
2. Use "Run Current File" to test changes
3. Use "Run Player Report" to verify GUI integration

### Debugging
1. Set breakpoints in code
2. Select appropriate configuration
3. Press F5 to start debugging
4. Use debug toolbar (step over/into/out)

### Testing Features
1. Select "Run Player Report"
2. Interact with GUI
3. Check console for errors/logs

---

## Integration with Project

### Python Path Resolution
Working directory set to root ensures:
```python
from utils.accessing_data import AccessData  # Works
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # Not needed
```

### Data File Access
```python
with open('Database/Data.json') as f:  # Works from project root
```

---

## Troubleshooting

### "No module named 'utils'"
- Check `cwd` is set to `${workspaceFolder}`
- Verify project folder structure
- Ensure Python interpreter is correct

### "Run Main" Configuration Fails
- Path may be incorrect (`Code/main.py` vs `main/main.py`)
- Update `program` path based on actual structure

### GUI Doesn't Launch
- Verify PyQt5 installed: `pip install PyQt5`
- Check Python interpreter in VS Code
- Look for errors in integrated terminal

---

## Best Practices

### Configuration Naming
- Use ▶ prefix for visual clarity
- Descriptive names indicate purpose
- Keep consistent naming convention

### Console Selection
- Use `integratedTerminal` for GUI apps
- Allows proper Qt event loop execution
- Enables user interaction

### CWD Management
- Always set to `${workspaceFolder}` for consistency
- Ensures predictable import behavior
- Maintains relative path integrity

---

## Future Enhancements

### Potential Additions
1. Debug configurations with arguments
2. Test runner configurations
3. Production vs development modes
4. Multiple player configurations

### Example - Parameterized Player
```json
{
    "name": "▶ Run Player Report (Custom)",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/testing/player_report.py",
    "args": ["Benjamin Berridge"],
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}"
}
```

---

## Related Files

- `settings.json`: VS Code workspace settings
- `player_report.py`: Main GUI entry point
- `accessing_data.py`: Data layer module
- `main.py`: Legacy main application

---

## Notes

- All configurations use `launch` request type (not `attach`)
- No environment variables specified (uses default Python env)
- No pre-launch tasks configured
- Debugger attaches automatically on exceptions