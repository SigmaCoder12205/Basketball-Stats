# UI Folder Documentation

## Overview

**FOLDER**: `UI/`  
**PURPOSE**: User interface design mockups and ASCII art layouts

Contains text-based UI design drafts and menu layouts for the basketball statistics application. Used for planning visual design before implementation.

---

## Folder Structure

```
UI/
├── designs.txt          # UI design mockups and ASCII art
└── doc/
    └── designs.txt_doc.md   # (This documentation)
```

---

## File Overview

### `designs.txt`

**Purpose**: Visual design mockups and menu layouts

**Format**: ASCII art text designs

**Status**: Design drafts, not production code

**Contents**: Two main menu designs with variations

---

## Design Mockups

### Design 1: Main Application Menu

```
======================================================= WELCOME TO DRAGONE =======================================================
             
             1.                                                  Get details on the game
             2.                                              Compare games, quarters and players
             3.                                      Get stats and analytics on games, quarters and players

             
             Make your choice (1-3):
```

**Characteristics**:
- Equals border (`=`)
- Centered title: "WELCOME TO DRAGONE"
- 3 menu options
- Numbered list with spacing
- Full-width layout (~120+ characters)
- Prompt: "Make your choice (1-3)"

**Purpose**: Main application entry point

**Features**:
1. Game details viewer
2. Comparison tools (games/quarters/players)
3. Statistics and analytics

---

### Design 1 (Variant 2): Dash Border

```
------------------------------------------------------- WELCOME TO DRAGONE -------------------------------------------------------
             
             1.                                                  Get details on the game
             2.                                              Compare games, quarters and players
             3.                                      Get stats and analytics on games, quarters and players

                    Make your choice (1-3):
```

**Changes from Variant 1**:
- Dash border (`-`) instead of equals
- Indented prompt (8 spaces)

---

### Design 1 (Variant 3): Asterisk Border

```
******************************************************* WELCOME TO DRAGONE *******************************************************
             
             1.                                                  Get details on the game
             2.                                              Compare games, quarters and players
             3.                                      Get stats and analytics on games, quarters and players

                    Make your choice (1-3):
```

**Changes from Variant 1**:
- Asterisk border (`*`)
- Indented prompt

**Visual Impact**: More prominent/attention-grabbing

---

### Design 2: Player Report Card Menu

```
======================================== Myles Dragone Report Card ======================================

1. Get quick stats 
2. Comapre all games
3. season grading
4. best worst game highlights               
5. Game rating
6. Season Game Rating
```

**Characteristics**:
- Equals border (shorter than Design 1)
- Player-specific title: "Myles Dragone Report Card"
- 6 menu options
- Compact formatting (no extra spacing)
- No prompt line
- Feature names only (no descriptions)

**Purpose**: Player-specific statistics menu

**Features**:
1. Quick stats (season averages)
2. Game comparison (typo: "Comapre")
3. Season grading (letter grades)
4. Best/worst game highlights
5. Individual game rating (0-100)
6. Season game rating overview

**Note**: This design matches actual PlayerReport GUI implementation

---

## Design Comparison

### Border Styles

| Style | Character | Visual Weight | Use Case |
|-------|-----------|---------------|----------|
| Equals | `=` | Heavy | Main title, emphasis |
| Dash | `-` | Light | Subtle separation |
| Asterisk | `*` | Very Heavy | Attention-grabbing |

### Layout Styles

| Design | Width | Options | Descriptions | Spacing |
|--------|-------|---------|--------------|---------|
| Design 1 | ~120 chars | 3 | Yes (detailed) | Generous |
| Design 2 | ~100 chars | 6 | No (brief) | Compact |

---

## Design Evolution

### Original Concept (Design 1)
```
Purpose: Main application menu
Audience: All users
Focus: Broad functionality
Style: Spacious, descriptive
```

### Implemented Design (Design 2)
```
Purpose: Player report menu
Audience: Specific player analysis
Focus: Statistics features
Style: Compact, feature-focused
```

**Transition**: From general-purpose to specialized player analysis

---

## Relationship to Implementation

### Design 2 → PlayerReport GUI

**Menu Text**:
```
designs.txt                        player_report.py
──────────────────────────────────────────────────────────
1. Get quick stats                 get_quick_stats_btn
2. Comapre all games               compare_all_games_btn
3. season grading                  season_grading_btn
4. best worst game highlights      best_worst_game_btn
5. Game rating                     game_rating_btn
6. Season Game Rating              season_game_rating_btn
```

**Implementation**:
- Text-based menu → PyQt5 GUI buttons
- ASCII art → Dark theme with gradients
- Terminal interface → Windowed application
- Static text → Interactive widgets

---

### Design 1 → Not Implemented

**Status**: Conceptual design only

**Possible Uses**:
- Future CLI version
- Terminal-based interface
- Alternative entry point
- Admin tools

---

## Design Intent

### Design 1: Application Shell

**Goals**:
- Welcome user
- Present main categories
- Guide user choice
- Professional appearance

**User Flow**:
```
Launch app
    ↓
Display welcome menu
    ↓
User selects category (1-3)
    ↓
Navigate to sub-menu
    ↓
Perform analysis
```

---

### Design 2: Feature Menu

**Goals**:
- Quick feature access
- Player-focused
- Comprehensive analytics
- Efficient navigation

**User Flow**:
```
Select player
    ↓
Display report card menu
    ↓
User selects feature (1-6)
    ↓
View statistics
    ↓
Return to menu
```

---

## ASCII Art Considerations

### Width Constraints

**Terminal Standard**: 80 characters

**Design 1**: ~120 characters (requires wide terminal or wraps)

**Design 2**: ~100 characters (wraps on standard terminal)

**Recommendation**: Max 80 chars for compatibility

---

### Character Sets

**ASCII-Safe Characters**:
```
Border: = - * + # | _
Spacing: (space) (tab)
Numbers: 0-9
Letters: A-Z a-z
```

**Unicode (Risky)**:
```
Box drawing: ─ │ ┌ ┐ └ ┘
Bullets: • ‣ ◦
Arrows: → ← ↑ ↓
```

**Used in designs**: ASCII-safe only (good portability)

---

## Design Patterns

### Centered Title Pattern

```
[border] TITLE [border]
```

**Examples**:
```
======= WELCOME TO DRAGONE =======
------- PLAYER REPORT CARD -------
******* GAME STATISTICS *********
```

---

### Numbered List Pattern

```
1. Option text
2. Option text
3. Option text
```

**Spacing Variations**:
```
Compact:  No blank lines between
Spacious: Blank line between each
```

---

### Prompt Pattern

```
Make your choice (1-3):
```

**Variations**:
- Aligned left
- Indented (8 spaces)
- With/without blank line above

---

## Typography Issues

### Typo in Design 2

**Line 2**: "Comapre all games"

**Should Be**: "Compare all games"

**Impact**: 
- Text design only (not in code)
- Would need fixing before CLI implementation
- GUI buttons have correct spelling

---

### Capitalization Inconsistency

**Design 2**:
```
1. Get quick stats           (Sentence case)
2. Comapre all games        (Sentence case)
3. season grading           (lowercase)
4. best worst game highlights (lowercase)
5. Game rating              (Title case)
6. Season Game Rating       (Title Case)
```

**Inconsistent**: Mix of sentence case, lowercase, Title Case

**Should Be** (consistent):
```
Option 1: Title Case
1. Get Quick Stats
2. Compare All Games
3. Season Grading
4. Best Worst Game Highlights
5. Game Rating
6. Season Game Rating

Option 2: Sentence case
1. Get quick stats
2. Compare all games
3. Season grading
4. Best worst game highlights
5. Game rating
6. Season game rating
```

---

## Usage Context

### Planning Phase
- Visual design before coding
- Menu structure planning
- Feature organization
- User flow mapping

### Reference Material
- Implementation guide
- Feature list
- Menu structure
- Text content

### Documentation
- Design history
- UI evolution
- Feature additions
- Layout changes

---

## Implementation Notes

### If Building CLI from These Designs

**Design 1 Implementation**:
```python
def display_main_menu():
    print("=" * 120)
    print("WELCOME TO DRAGONE".center(120))
    print("=" * 120)
    print()
    print("1.".ljust(15) + "Get details on the game".center(90))
    print("2.".ljust(15) + "Compare games, quarters and players".center(90))
    print("3.".ljust(15) + "Get stats and analytics on games, quarters and players".center(90))
    print()
    choice = input("Make your choice (1-3): ")
    return choice
```

---

**Design 2 Implementation**:
```python
def display_player_menu(player_name):
    border = "=" * 100
    title = f"{player_name} Report Card".center(100)
    
    print(border)
    print(title)
    print(border)
    print()
    print("1. Get quick stats")
    print("2. Compare all games")  # Fixed typo
    print("3. Season grading")
    print("4. Best worst game highlights")
    print("5. Game rating")
    print("6. Season Game Rating")
    print()
    choice = input("Select option (1-6): ")
    return choice
```

---

### GUI Implementation (Actual)

**PlayerReport Class**:
- Title in QLabel: `"{player_name}'s Report Card"`
- Menu items as QPushButtons (not numbered)
- Dark theme with gradients (not ASCII borders)
- Click interactions (not keyboard input)
- Visual feedback (hover, press states)

---

## Design Principles

### Consistency
- Border style consistent within design
- Number format consistent (1-6)
- Spacing consistent per design

### Clarity
- Clear option descriptions
- Obvious menu structure
- Simple numbering
- Direct prompts

### Accessibility
- High contrast (text on background)
- Simple characters (no complex Unicode)
- Clear hierarchy
- Readable spacing

---

## Alternative Design Concepts

### Minimalist Menu

```
DRAGONE - Basketball Stats

[1] Game Details
[2] Comparisons
[3] Analytics

Choice:
```

**Pros**: Compact, fast, simple  
**Cons**: Less welcoming, minimal branding

---

### Box-Style Menu

```
┌─────────────────────────────────────┐
│     DRAGONE BASKETBALL STATS        │
├─────────────────────────────────────┤
│  1. Game Details                    │
│  2. Comparison Tools                │
│  3. Statistics & Analytics          │
└─────────────────────────────────────┘

Select:
```

**Pros**: Professional, contained, clear  
**Cons**: Unicode box chars (compatibility issues)

---

### Banner-Style Menu

```
╔═══════════════════════════════════════╗
║        WELCOME TO DRAGONE             ║
║   Basketball Statistics System        ║
╠═══════════════════════════════════════╣
║  [1] Game Details                     ║
║  [2] Game Comparisons                 ║
║  [3] Statistical Analysis             ║
╚═══════════════════════════════════════╝
```

**Pros**: Very professional, structured  
**Cons**: Unicode, complex, may not render everywhere

---

## Best Practices

### Terminal UI Design

**Do**:
- Use ASCII-safe characters
- Respect 80-column limit
- Consistent alignment
- Clear spacing
- Simple navigation

**Don't**:
- Rely on Unicode
- Exceed standard width
- Mix alignment styles
- Overcomplicate layout
- Use color codes (portability)

---

### Menu Design

**Do**:
- Number options clearly
- Keep descriptions concise
- Group related items
- Provide clear prompts
- Show valid range

**Don't**:
- Use ambiguous labels
- Mix numbering systems
- Overwhelm with options
- Hide navigation hints
- Leave user guessing

---

## File Purpose

### What This File Is
- Design mockup collection
- UI planning document
- Visual reference
- Text-based prototype

### What This File Isn't
- Production code
- Executable script
- Configuration file
- User documentation

---

## Related Files

### Implementation
- `main/player_report.py` - GUI implementation of Design 2
- `testing/player_report.py` - Possible duplicate

### Documentation
- `doc/player_report_doc.md` - GUI documentation
- Project README - Feature overview

### Design Assets
- None (text-only designs)
- Future: Mockup images, wireframes

---

## Future Enhancements

### Design Documentation
- Add screenshots of implemented GUI
- Create side-by-side comparison (design vs implementation)
- Document design decisions
- Include user feedback

### Additional Designs
- Settings menu design
- Error message formats
- Loading screens
- Help text layouts

### Interactive Prototypes
- CLI prototype from Design 1
- Terminal-based version
- Fallback for no-GUI environments

---

## Summary

`UI/designs.txt` contains:

**Contents**:
- ASCII art menu mockups
- Two main design concepts
- Multiple border style variations
- Feature list for player reports

**Design 1**: Main application menu (3 options, wide layout, not implemented)

**Design 2**: Player report menu (6 options, compact, implemented as GUI)

**Issues**:
- Typo: "Comapre" should be "Compare"
- Inconsistent capitalization
- Width exceeds standard terminal (80 cols)
- No implementation code

**Purpose**: 
- Planning and reference
- Visual design before coding
- Feature organization

**Status**: 
- Design 2 implemented as PyQt5 GUI
- Design 1 conceptual only

**Value**: 
- Historical record of UI planning
- Reference for future CLI version
- Documentation of feature list
- Design evolution tracking

**Related**: 
- PlayerReport GUI uses Design 2 structure
- Buttons replace numbered menu
- Dark theme replaces ASCII art
- Interactive widgets replace text input

**Recommendation**: 
- Fix typo if implementing CLI
- Standardize capitalization
- Consider 80-column version
- Add design documentation notes