# settings.json Documentation

## Overview

**FILE**: `.vscode/settings.json`  
**PURPOSE**: VS Code workspace-specific configuration for basketball statistics project

Defines workspace preferences for appearance, spell checking, and Python testing framework configuration.

---

## Full File Content

```json
{
    "workbench.iconTheme": "material-icon-theme",
    "workbench.colorTheme": "Evondev Dracula Darker Contrast",
    "cSpell.words": [
        "Dragone",
        "Mylesbasketballstatsanddata",
        "qlineargradient"
    ],
    "python.testing.pytestArgs": [
        "Code"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

---

## Settings Breakdown

### Workbench Configuration

#### Icon Theme
```json
"workbench.iconTheme": "material-icon-theme"
```

**Purpose**: Sets file/folder icons in VS Code explorer

**Theme**: Material Icon Theme
- Modern, colorful file type icons
- Enhanced visual file navigation
- Distinct icons for Python, JSON, Markdown files

**Installation**: 
```bash
# Via VS Code Extensions
# Search: "Material Icon Theme" by Philipp Kief
```

---

#### Color Theme
```json
"workbench.colorTheme": "Evondev Dracula Darker Contrast"
```

**Purpose**: Sets editor color scheme

**Theme**: Evondev Dracula Darker Contrast
- Dark theme variant
- High contrast for reduced eye strain
- Enhanced readability

**Characteristics**:
- Background: Very dark (near black)
- Syntax highlighting: Vibrant colors
- UI elements: High contrast borders

**Installation**:
```bash
# Via VS Code Extensions
# Search: "Evondev Dracula" by Evondev
```

---

### Spell Checker Configuration

#### Custom Dictionary
```json
"cSpell.words": [
    "Dragone",
    "Mylesbasketballstatsanddata",
    "qlineargradient"
]
```

**Purpose**: Whitelist custom words to prevent false spelling errors

**Extension**: Code Spell Checker (cSpell)

**Whitelisted Words**:

| Word | Type | Context |
|------|------|---------|
| `Dragone` | Proper Noun | Developer/team name |
| `Mylesbasketballstatsanddata` | Identifier | Repository/project name |
| `qlineargradient` | Technical | PyQt5 CSS gradient property |

**Why Needed**:
- `Dragone`: Personal/team identifier (not in standard dictionary)
- `Mylesbasketballstatsanddata`: Project-specific compound name
- `qlineargradient`: Qt-specific CSS property (camelCase, no spaces)

**Extension Installation**:
```bash
# Via VS Code Extensions
# Search: "Code Spell Checker" by Street Side Software
```

---

### Python Testing Configuration

#### Pytest Arguments
```json
"python.testing.pytestArgs": [
    "Code"
]
```

**Purpose**: Specify directory for pytest test discovery

**Configuration**:
- Test discovery path: `Code/` directory
- Pytest will search `Code/` for test files
- Pattern: Files matching `test_*.py` or `*_test.py`

**Note**: Path may be incorrect
- Current: `Code/` directory
- Actual structure: `testing/` directory contains tests
- May need update to: `"testing"` or `"."` (project root)

**Usage**:
```bash
# Equivalent command line
pytest Code/
```

---

#### Unit Test Framework
```json
"python.testing.unittestEnabled": false
```

**Purpose**: Disable Python's built-in unittest framework

**Reason**: Project uses pytest instead of unittest
- Prevents conflicting test discovery
- Avoids duplicate test runs
- Simplifies testing interface

---

#### Pytest Framework
```json
"python.testing.pytestEnabled": true
```

**Purpose**: Enable pytest as primary testing framework

**Features**:
- Test discovery in VS Code sidebar
- Run individual tests via CodeLens
- Integrated test results display
- Debug tests directly from editor

**Test Discovery**:
- Searches `Code/` directory (per `pytestArgs`)
- Finds files: `test_*.py`, `*_test.py`
- Identifies functions: `test_*()`

**VS Code Integration**:
1. Testing icon in sidebar shows all discovered tests
2. CodeLens "Run Test" appears above test functions
3. Test results shown inline with pass/fail indicators

---

## Setting Scope

### Workspace vs User Settings

**Workspace Settings** (this file):
- Apply only to this project
- Stored in `.vscode/settings.json`
- Project-specific customization
- Shared via version control

**User Settings** (global):
- Apply to all VS Code projects
- Stored in user config directory
- Personal preferences
- Not shared

**Precedence**: Workspace settings override user settings

---

## Dependencies

### Required VS Code Extensions

1. **Material Icon Theme**
   - Publisher: Philipp Kief
   - Required for: `workbench.iconTheme`

2. **Evondev Dracula Darker Contrast**
   - Publisher: Evondev
   - Required for: `workbench.colorTheme`

3. **Code Spell Checker**
   - Publisher: Street Side Software
   - Required for: `cSpell.words`

4. **Python Extension**
   - Publisher: Microsoft
   - Required for: All `python.testing.*` settings
   - Includes pytest integration

### Python Packages

```bash
# Install pytest for testing features
pip install pytest
```

---

## Testing Workflow

### Test Discovery
1. Open Testing sidebar (flask icon or Ctrl+Shift+T)
2. VS Code discovers tests in `Code/` directory
3. Tests appear in hierarchical tree view

### Running Tests
```python
# Example test file: Code/test_accessing_data.py
def test_get_season_stats():
    from utils.accessing_data import AccessData
    stats = AccessData.Get_season_stats("Aston Sharp")
    assert stats is not None
```

**Run Options**:
- Click "Run Test" CodeLens above function
- Right-click test in sidebar → Run Test
- Run all tests via sidebar toolbar

### Debugging Tests
- Click "Debug Test" CodeLens
- Set breakpoints in test code
- Step through test execution

---

## Customization Examples

### Add More Spell Check Words
```json
"cSpell.words": [
    "Dragone",
    "Mylesbasketballstatsanddata",
    "qlineargradient",
    "AccessData",    // Add class names
    "PyQt",          // Add framework names
    "pyplot"         // Add library names
]
```

### Change Test Directory
```json
"python.testing.pytestArgs": [
    "testing",           // Correct directory
    "-v",               // Verbose output
    "--tb=short"        // Short traceback
]
```

### Enable Both Test Frameworks
```json
"python.testing.unittestEnabled": true,
"python.testing.pytestEnabled": true,
"python.testing.unittestArgs": [
    "-v",
    "-s",
    "."
]
```

---

## Theme Appearance

### Material Icon Theme Examples
```
📁 .vscode/          (Folder icon - purple)
📄 settings.json     (JSON icon - yellow)
🐍 main.py           (Python icon - blue/yellow)
📊 Data.json         (Database icon - orange)
📝 README.md         (Markdown icon - blue)
```

### Evondev Dracula Colors
```python
# Syntax highlighting examples
def function():              # Purple keyword
    variable = "string"      # Orange identifier, green string
    number = 42              # Purple number
    # Comment                # Gray italic
    return True              # Pink keyword, purple boolean
```

---

## Common Issues

### Icons Not Showing
```json
// Verify extension installed
"workbench.iconTheme": "material-icon-theme"

// Reload VS Code: Ctrl+Shift+P → "Reload Window"
```

### Theme Not Applied
```json
// Check theme name spelling
"workbench.colorTheme": "Evondev Dracula Darker Contrast"

// Install extension if missing
// View → Extensions → Search "Evondev Dracula"
```

### Spell Check Flagging Code
```json
// Add technical terms to dictionary
"cSpell.words": [
    "pyplot",
    "numpy",
    "pandas"
]

// Or disable for specific files
"cSpell.ignorePaths": [
    "**/*.json"
]
```

### Tests Not Discovered
```json
// Check pytest installed
// Terminal: pip install pytest

// Verify test directory path
"python.testing.pytestArgs": ["testing"]  // Not "Code"

// Refresh tests: Testing sidebar → Refresh icon
```

---

## Best Practices

### Workspace Settings
- Keep project-specific settings here
- Commit to version control
- Document unusual configurations
- Use relative paths

### Custom Dictionary
- Add project-specific terms only
- Include technical identifiers (CSS properties, frameworks)
- Don't add common misspellings
- Keep alphabetically sorted

### Testing Configuration
- Use one framework (pytest recommended)
- Specify test directory explicitly
- Add verbose flags for debugging
- Configure coverage if needed

---

## Integration with Project

### Python Testing Structure
```
project/
├── .vscode/
│   └── settings.json          # Testing config here
├── testing/
│   ├── test_file.py          # Should be discovered
│   └── __init__.py
└── utils/
    └── accessing_data.py     # Code under test
```

**Issue**: `pytestArgs` points to `Code/` but tests are in `testing/`

**Fix**:
```json
"python.testing.pytestArgs": [
    "testing"  // Correct directory
]
```

---

## Related Files

- `launch.json`: Debugger configurations (complements testing)
- `.gitignore`: Excludes `.vscode/` if needed
- `pytest.ini`: Additional pytest configuration (optional)
- `requirements.txt`: Specify pytest version

---

## Notes

- Settings are workspace-specific (project-level)
- Extensions must be installed for themes to work
- Testing path appears misaligned with actual structure
- Custom dictionary prevents annoying red squiggles
- Dark theme matches PyQt5 GUI color scheme