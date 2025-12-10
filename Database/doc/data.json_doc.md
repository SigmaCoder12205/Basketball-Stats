# Data.json Documentation

## Overview

**FILE**: `Database/Data.json`  
**PURPOSE**: Primary data storage for basketball game statistics and metadata

Central JSON database storing comprehensive game information including scores, player statistics, lineups, game details, and quarter-by-quarter performance data for youth basketball league.

---

## File Structure

```json
{
    "Game_1": { ... },
    "Game_2": { ... },
    "Game_3": { ... }
}
```

**Root Level**: Dictionary of games indexed by game identifier
- Keys: Game identifiers (`"Game_1"`, `"Game_2"`, etc.)
- Values: Game objects containing complete game data

---

## Game Object Structure

Each game contains three main sections:

```json
{
    "Details": { ... },      // Game metadata and context
    "Lineup": { ... },        // Team rosters
    "Quarters": { ... }       // Statistical data by quarter
}
```

---

## Details Section

### Purpose
Stores game metadata, context, and non-statistical information.

### Structure

```json
"Details": {
    "Time": "6:05PM",
    "Day": "Monday",
    "Month": "Aug",
    "Year": 2025,
    "Court": 3,
    "Game_against": "Newport Raiders U16 Boys Paul",
    "Our_Scores": 40,
    "There_Scores": 65,
    "Good_bad_ref": "mid",
    "Who_was_the_ref": "white head old guy",
    "Player_Calm": "Benjamin",
    "Player_Angry": "Angus",
    "Intensity": "low",
    "Other_team_calm": "Daniel",
    "Other_team_angry": "no",
    "Amount_of_timeouts": 1,
    "Amount_of_refs": 2,
    "Amount_of_subs": 5,
    "Total_team_players": 7,
    "Other_team_players": 7,
    "Amount_of_fill_in": 1,
    "Clear_good_player": 1
}
```

### Field Definitions

#### Temporal Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Time` | String | Game start time | `"6:05PM"` |
| `Day` | String | Day of week | `"Monday"` |
| `Month` | String | Month abbreviation | `"Aug"` |
| `Year` | Integer | Year | `2025` |

#### Venue Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Court` | Integer | Court number | `3` |

#### Teams and Scores
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Game_against` | String | Opponent team name | `"Newport Raiders U16 Boys Paul"` |
| `Our_Scores` | Integer | Home team final score | `40` |
| `There_Scores` | Integer | Away team final score | `65` |

#### Officiating
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Good_bad_ref` | String | Referee quality rating | `"mid"`, `"good"`, `"bad"` |
| `Who_was_the_ref` | String | Referee description | `"white head old guy"` |
| `Amount_of_refs` | Integer | Number of referees | `2` |

#### Player Behavior
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Player_Calm` | String | Calmest home player | `"Benjamin"` |
| `Player_Angry` | String | Most emotional home player | `"Angus"` |
| `Other_team_calm` | String | Calmest opponent player | `"Daniel"` |
| `Other_team_angry` | String | Most emotional opponent | `"no"` (none) |

#### Game Characteristics
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Intensity` | String | Game intensity level | `"low"`, `"mid"`, `"mid-high"` |

#### Game Management
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Amount_of_timeouts` | Integer | Timeouts called | `1` |
| `Amount_of_subs` | Integer | Substitutions made | `5` |

#### Roster Information
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Total_team_players` | Integer | Home team roster size | `7` |
| `Other_team_players` | Integer | Opponent roster size | `7` |
| `Amount_of_fill_in` | Integer | Fill-in players used | `1` |
| `Clear_good_player` | Integer | Standout players identified | `1` |

---

## Lineup Section

### Purpose
Lists all players on both teams for the game.

### Structure

```json
"Lineup": {
    "Team_Name_1": [
        "Player 1",
        "Player 2",
        "Player 3"
    ],
    "Team_Name_2": [
        "Player 4",
        "Player 5",
        "Player 6"
    ]
}
```

### Example

```json
"Lineup": {
    "Newport Raiders U16 Boys Paul": [
        "William McGirr",
        "Bailey McPherson",
        "Seamus Martins",
        "Hudson Mann",
        "Xavier Zagame",
        "Ethan Burgess",
        "Fill-in",
        "Dainiel Ugiagbe"
    ],
    "Newport Raiders U16 Boys Julie": [
        "Benjamin Berridge",
        "Angus Lee",
        "Fill-in",
        "Aston Sharp",
        "Leon Baronti",
        "Ryder Sotiroudis",
        "Myles Dragone"
    ]
}
```

### Notes
- Keys are team names (full team names with divisions)
- Values are arrays of player full names
- `"Fill-in"` indicates substitute/guest players
- Order in array has no significance
- Roster sizes vary by game (5-9 players typical)

---

## Quarters Section

### Purpose
Stores player statistics broken down by quarter.

### Structure

```json
"Quarters": {
    "Quarter 1": {
        "Player_Name": {
            "Points": 0,
            "Fouls": 0,
            "Rebounds": 0,
            "Assists": 0,
            "Turnovers": 0
        }
    },
    "Quarter 2": { ... }
}
```

### Stat Categories

| Stat | Description | Range |
|------|-------------|-------|
| `Points` | Points scored | 0-30+ per quarter |
| `Fouls` | Personal fouls committed | 0-5 (5 = foul out) |
| `Rebounds` | Ball recoveries | 0-15+ per quarter |
| `Assists` | Passes leading to scores | 0-10+ per quarter |
| `Turnovers` | Ball possession losses | 0-10+ per quarter |

### Example - Quarter 1

```json
"Quarter 1": {
    "Benjamin Berridge": {
        "Points": 2,
        "Fouls": 1,
        "Rebounds": 2,
        "Assists": 0,
        "Turnovers": 2
    },
    "Angus Lee": {
        "Points": 3,
        "Fouls": 1,
        "Rebounds": 2,
        "Assists": 0,
        "Turnovers": 2
    }
}
```

### Notes
- Only players who participated in quarter are listed
- All five stats always present (0 if no activity)
- Player names must match exactly with Lineup section
- Data structure consistent across all quarters and games

---

## Complete Game Example

### Game_1 Full Structure

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
            "There_Scores": 65,
            "Good_bad_ref": "mid",
            "Who_was_the_ref": "white head old guy",
            "Player_Calm": "Benjamin",
            "Player_Angry": "Angus",
            "Intensity": "low",
            "Other_team_calm": "Daniel",
            "Other_team_angry": "no",
            "Amount_of_timeouts": 1,
            "Amount_of_refs": 2,
            "Amount_of_subs": 5,
            "Total_team_players": 7,
            "Other_team_players": 7,
            "Amount_of_fill_in": 1,
            "Clear_good_player": 1
        },
        "Lineup": {
            "Newport Raiders U16 Boys Paul": [
                "William McGirr",
                "Bailey McPherson",
                "Seamus Martins",
                "Hudson Mann",
                "Xavier Zagame",
                "Ethan Burgess",
                "Fill-in",
                "Dainiel Ugiagbe"
            ],
            "Newport Raiders U16 Boys Julie": [
                "Benjamin Berridge",
                "Angus Lee",
                "Fill-in",
                "Aston Sharp",
                "Leon Baronti",
                "Ryder Sotiroudis",
                "Myles Dragone"
            ]
        },
        "Quarters": {
            "Quarter 1": {
                "Benjamin Berridge": {
                    "Points": 2,
                    "Fouls": 1,
                    "Rebounds": 2,
                    "Assists": 0,
                    "Turnovers": 2
                },
                "Angus Lee": {
                    "Points": 3,
                    "Fouls": 1,
                    "Rebounds": 2,
                    "Assists": 0,
                    "Turnovers": 2
                }
            },
            "Quarter 2": {
                "Benjamin Berridge": {
                    "Points": 8,
                    "Fouls": 0,
                    "Rebounds": 6,
                    "Assists": 0,
                    "Turnovers": 0
                }
            }
        }
    }
}
```

---

## Data Analysis Examples

### Season Totals Calculation

```python
# Calculate player's season points
player_name = "Aston Sharp"
total_points = 0

for game_id, game_data in data.items():
    for quarter_id, quarter_data in game_data["Quarters"].items():
        if player_name in quarter_data:
            total_points += quarter_data[player_name]["Points"]

# Result: Aston Sharp season points
```

### Team Performance

```python
# Game_1 team performance
game = data["Game_1"]

home_team = "Newport Raiders U16 Boys Julie"
away_team = "Newport Raiders U16 Boys Paul"

home_score = game["Details"]["Our_Scores"]      # 40
away_score = game["Details"]["There_Scores"]    # 65

result = "Loss" if home_score < away_score else "Win"
```

### Player Efficiency

```python
# Calculate player efficiency for Game_2
game = data["Game_2"]
player = "Aston Sharp"

points = 0
turnovers = 0

for quarter in game["Quarters"].values():
    if player in quarter:
        points += quarter[player]["Points"]
        turnovers += quarter[player]["Turnovers"]

efficiency = points - turnovers  # Simple efficiency metric
```

---

## Data Patterns

### Games in Dataset
- **Game_1**: Loss (40-65) vs Newport Raiders Paul
- **Game_2**: Loss (50-84) vs Truganina Bullets  
- **Game_3**: Close Loss (37-39) vs Willy Cannons JAZZ

### Common Players (Core Team)
Appear in multiple games:
- Benjamin Berridge (Games 1, 3)
- Angus Lee (Games 1, 2, 3)
- Aston Sharp (Games 1, 2, 3)
- Leon Baronti (Games 1, 2, 3)
- Ryder Sotiroudis (Games 1, 2, 3)
- Myles Dragone (Games 1, 2, 3)

### Quarter Coverage
- Game_1: 2 quarters recorded
- Game_2: 2 quarters recorded
- Game_3: 2 quarters recorded

**Note**: Only half-game data (likely halves, not traditional 4 quarters)

---

## Data Quality Notes

### Consistent Elements
✓ All games have Details, Lineup, Quarters sections  
✓ All player stats have 5 categories (Points, Fouls, Rebounds, Assists, Turnovers)  
✓ Player names consistent across Lineup and Quarters  
✓ Numeric fields use appropriate types (integers for counts)

### Inconsistencies
- `Other_team_angry` field name varies (`Other_team_Angry` in Game_3)
- Referee descriptions informal ("white head old guy")
- "None" vs "no" for indicating absence
- Player behavior fields sometimes use first names only

### Missing Data
- Only 2 quarters per game (incomplete games or halftime-only tracking)
- No individual quarter scores (only final scores in Details)
- No time-on-court data
- No plus/minus statistics

---

## Usage in Application

### AccessData Class Integration

```python
from utils.accessing_data import AccessData

# Get season stats for player
stats = AccessData.Get_season_stats("Aston Sharp", sum_total=True)
# Returns: {'Points': 15, 'Fouls': 1, 'Rebounds': 8, ...}

# Get specific game details
details = AccessData.Get_details("Game_2")
# Returns: {'Time': '6:05PM', 'Day': 'Monday', ...}

# Get team season stats
team_stats = AccessData.Get_team_season_stats(sum_total=True)
# Returns: {'Player1': {...}, 'Player2': {...}, ...}
```

### PlayerReport GUI Integration

Application reads this file to:
1. Calculate season averages (mean, median, range)
2. Generate game-to-game comparisons
3. Compute letter grades based on team contribution
4. Identify best/worst game performances
5. Calculate 0-100 game ratings

---

## File Management

### Location
```
Database/
├── Data.json          # Main data file
└── Data.json.bak      # Backup copy
```

### Backup Strategy
- `Data.json.bak` maintains previous version
- Manual backup before edits recommended
- Version control (Git) provides history

### Editing Safely

**Before Editing**:
```bash
# Create backup
cp Database/Data.json Database/Data.json.backup

# Or use versioned backup
cp Database/Data.json Database/Data.json.$(date +%Y%m%d)
```

**After Editing**:
```bash
# Validate JSON syntax
python -m json.tool Database/Data.json
```

---

## Data Schema Validation

### Required Fields Per Game

**Details Section** (22 fields):
- Temporal: Time, Day, Month, Year
- Venue: Court
- Teams: Game_against, Our_Scores, There_Scores
- Officiating: Good_bad_ref, Who_was_the_ref, Amount_of_refs
- Behavior: Player_Calm, Player_Angry, Other_team_calm, Other_team_angry
- Characteristics: Intensity
- Management: Amount_of_timeouts, Amount_of_subs
- Roster: Total_team_players, Other_team_players, Amount_of_fill_in, Clear_good_player

**Lineup Section** (2 arrays):
- Two team names as keys
- Array of player names as values

**Quarters Section** (2+ quarters):
- Quarter identifiers ("Quarter 1", "Quarter 2")
- Player names matching Lineup
- 5 stat categories per player

### Validation Script Concept

```python
def validate_game(game_data):
    """Validate game data structure."""
    required_sections = ["Details", "Lineup", "Quarters"]
    
    for section in required_sections:
        if section not in game_data:
            return False, f"Missing {section}"
    
    # Validate stat structure
    for quarter_data in game_data["Quarters"].values():
        for player_stats in quarter_data.values():
            required_stats = ["Points", "Fouls", "Rebounds", "Assists", "Turnovers"]
            for stat in required_stats:
                if stat not in player_stats:
                    return False, f"Missing {stat}"
    
    return True, "Valid"
```

---

## Expansion Considerations

### Adding New Games

```json
"Game_4": {
    "Details": { ... },
    "Lineup": { ... },
    "Quarters": {
        "Quarter 1": { ... },
        "Quarter 2": { ... },
        "Quarter 3": { ... },  // Add more quarters
        "Quarter 4": { ... }
    }
}
```

### Adding New Stats

```json
"Player_Name": {
    "Points": 10,
    "Fouls": 2,
    "Rebounds": 5,
    "Assists": 3,
    "Turnovers": 1,
    "Steals": 2,        // New stat
    "Blocks": 1,        // New stat
    "Minutes": 15       // New stat
}
```

**Impact**: Requires updating AccessData class to handle new fields

---

## File Size and Performance

### Current Stats
- **Games**: 3
- **Players**: ~12 unique
- **File Size**: ~8 KB
- **Load Time**: <10ms

### Projected Growth
- **1 Season (20 games)**: ~50 KB
- **5 Seasons (100 games)**: ~250 KB
- **Load Time**: Still <50ms

**Conclusion**: JSON format suitable for expected scale

---

## Security and Privacy

### Sensitive Information
- Player full names (youth athletes)
- Referee descriptions (potentially identifiable)
- Team names and opponent information

### Recommendations
- Anonymize for public sharing
- Restrict file access to authorized users
- Consider data retention policies
- GDPR/privacy compliance for youth data

---

## Related Files

- `Database/Data.json.bak` - Backup copy
- `utils/accessing_data.py` - Data access layer
- `testing/player_report.py` - Main data consumer
- `Database/log/` - Operation logs (if any)

---

## Future Enhancements

### Potential Additions
1. **Advanced Stats**: Steals, blocks, field goal percentage
2. **Time Tracking**: Minutes played per quarter
3. **Play-by-Play**: Detailed action log
4. **Video Links**: Game footage references
5. **Coach Notes**: Strategy and performance notes
6. **Opponent Stats**: Track opponent player performance
7. **Season Metadata**: League info, standings, schedules

### Schema Evolution
```json
{
    "metadata": {
        "version": "2.0",
        "season": "2024-2025",
        "league": "U16 Boys"
    },
    "games": {
        "Game_1": { ... },
        "Game_2": { ... }
    }
}
```

---

## Summary

`Data.json` serves as:
- **Central Data Repository** for all game information
- **Structured Format** enabling programmatic access
- **Comprehensive Storage** of stats, metadata, context
- **Foundation** for analytics and reporting features

**Key Characteristics**:
- JSON format for easy parsing
- Three-section structure (Details, Lineup, Quarters)
- Consistent stat categories across all games
- Human-readable and machine-processable

**Usage**: Read by AccessData class, consumed by PlayerReport GUI, analyzed for player performance insights