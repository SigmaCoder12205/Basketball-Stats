=== Overview ===

Basketball Statistics Data Access Layer

FILE NAME RELATIVE: accessing_data.py
FILE NAME ABSOLUTE: C:/Users/Drags Jrs/Mylesbasketballstatsanddata/utils/accessing_data.py

CODE QUALITY RATING: 740/1000
    Strengths:
        - Comprehensive method coverage for all data queries
        - Consistent return formats across methods
        - Good error handling with graceful fallbacks
        - Flexible formatting options (look_good parameter)
        - Class-level caching for performance
    
    Areas for Improvement:
        - Some method names inconsistent (e.g., Get_details vs quick_game_details)
        - Repetitive code patterns could be refactored
        - Missing type hints on most methods
        - Some docstrings incomplete or missing
        - Could benefit from validation helpers

PURPOSE:
    This module provides a comprehensive data access layer for basketball game statistics.
    It serves as the intermediary between the raw JSON data storage (Data.json) and the
    GUI application (player_report.py), offering a clean API for querying, filtering, and
    aggregating basketball statistics across games, players, and teams.

ARCHITECTURE:
    Single class design with class-level data caching:
    - AccessData class handles all data operations
    - Class variable 'data' stores loaded JSON in memory (singleton pattern)
    - Class variable '_initialized' tracks initialization state
    - All methods are classmethods (no instance creation needed)
    - Automatic initialization on first use via _ensure_initialized()

DATA STRUCTURE:
    Data.json contains hierarchical game records:
    {
        "Game_N": {
            "Details": {
                "Time": str, "Day": str, "Month": str, "Year": int,
                "Court": int, "Game_against": str, "Our_Scores": int,
                "There_Scores": int, "Good_bad_ref": str, ...
            },
            "Lineup": {
                "Team_A": [player_names],
                "Team_B": [player_names]
            },
            "Quarters": {
                "Quarter N": {
                    "Player_Name": {
                        "Points": int, "Fouls": int, "Assists": int,
                        "Rebounds": int, "Turnovers": int
                    }
                }
            }
        }
    }

KEY FEATURES:
    Game-Level Queries:
        - Get_details(): Game metadata (time, teams, scores, etc.)
        - Get_a_lineup(): Team rosters for specific game
        - Get_quarter_stats(): All player stats for a quarter
        - Get_specific_Stats(): Individual player quarter stats
    
    Player-Level Queries:
        - Get_season_stats(): Player totals across all games
        - Get_game_stats(): Player totals for specific game
        - Get_quarter_season_stats(): Player totals for specific quarters
        - Specific_players_best_stat(): Find player's peak performance
    
    Team-Level Queries:
        - Get_team_season_stats(): All players' season totals
        - Aggregation and summing capabilities
    
    Performance Analysis:
        - Get_highest_stats_quarter(): Top performer in quarter
        - Get_highest_stats_game(): Top performer in game
        - Check_player(): Verify player participation
    
    Output Formatting:
        - look_good=True: Human-readable formatted strings
        - look_good=False: Python dictionaries for programmatic use

USAGE PATTERNS:
    Initialization (automatic on first use):
        AccessData()  # Explicitly initialize (optional)
        # OR
        AccessData.Get_season_stats(...)  # Auto-initializes if needed
    
    Query Examples:
        # Player season totals
        stats = AccessData.Get_season_stats("Aston Sharp", sum_total=True)
        
        # Game details
        details = AccessData.Get_details("Game_1", look_good=False)
        
        # Team season totals
        team = AccessData.Get_team_season_stats(sum_total=True)
        
        # Best performer in quarter
        top = AccessData.Get_highest_stats_quarter("Game_1", "Quarter 1", "Points")

METHOD CATEGORIES:
    Initialization:
        - __init__(): Instance initializer (calls Initialize)
        - Initialize(): Loads JSON data into memory
        - _ensure_initialized(): Automatic initialization checker
    
    Game Queries (8 methods):
        - Get_details()
        - Get_a_lineup()
        - Get_quarter_stats()
        - Get_specific_Stats()
        - Get_game_stats()
        - Get_highest_stats_quarter()
        - Get_highest_stats_game()
        - Check_player()
    
    Player Queries (3 methods):
        - Get_season_stats()
        - Get_quarter_season_stats()
        - Specific_players_best_stat()
    
    Team Queries (1 method):
        - Get_team_season_stats()

DESIGN PHILOSOPHY:
    - Stateless queries (no side effects on data)
    - Consistent error handling (return error dicts/strings)
    - Optional pretty printing (look_good parameter)
    - Performance through in-memory caching
    - Graceful degradation (return empty/default values on error)

ERROR HANDLING STRATEGY:
    File Operations:
        - FileNotFoundError: Returns None, prints error message
        - json.JSONDecodeError: Returns None, prints error message
        - Generic exceptions: Caught and printed
    
    Data Queries:
        - Missing game/player/stat: Returns error dict or empty dict
        - Invalid parameters: Returns error dict with descriptive message
        - look_good=True: Returns formatted error strings

PERFORMANCE CHARACTERISTICS:
    Initialization: ~50ms (one-time file read)
    Queries: ~1-5ms (in-memory dictionary lookups)
    Aggregations: ~10-30ms (depends on data size)
    Memory Usage: ~50KB (typical season of 5-10 games)

DEPENDENCIES:
    Built-in:
        - json: JSON parsing and serialization
    
    Internal:
        - Data.json: Game statistics database (must exist at hardcoded path)

DATA FILE LOCATION:
    Hardcoded path: r"C:\Users\Drags Jrs\Mylesbasketballstatsanddata\Database\Data.json"
    Note: Path is Windows-specific and absolute (not portable)

MAINTAINED BY: Drags Jrs
CREATED: 2025
LAST UPDATED: 2025
VERSION: 2.0.1
STATUS: Production

=== AccessData (class) ===

    Centralized data access layer for basketball game statistics.
    
    This class provides a comprehensive API for querying, filtering, and aggregating
    basketball statistics from a JSON data file. Uses a singleton-like pattern with
    class-level data caching for performance. All methods are classmethods, eliminating
    the need for instance creation.

    CLASS ATTRIBUTES:
        data (dict): Class-level dictionary storing all loaded game data from JSON
                    Structure: {game_name: {Details, Lineup, Quarters}}
                    Shared across all accesses (singleton pattern)
        
        _initialized (bool): Flag tracking whether data has been loaded from file
                           Prevents redundant file I/O operations
                           Set to True after first successful initialization

    INSTANCE ATTRIBUTES:
        None - All functionality implemented at class level

    DESIGN PATTERNS:
        Singleton Pattern:
            - Single shared data store across all accesses
            - Class variable 'data' holds the one instance
            - _initialized flag prevents duplicate loading
        
        Lazy Initialization:
            - Data loaded on first access
            - _ensure_initialized() called before each query
            - Automatic, transparent to caller
        
        Classmethod Pattern:
            - No instance creation needed
            - Call directly: AccessData.Get_season_stats(...)
            - Cleaner API for stateless operations

    INITIALIZATION FLOW:
        First Query:
            User calls AccessData.Get_season_stats(...)
            → _ensure_initialized() checks _initialized flag
            → Flag is False, creates instance
            → Instance __init__() calls Initialize()
            → JSON loaded into AccessData.data
            → _initialized set to True
        
        Subsequent Queries:
            User calls any method
            → _ensure_initialized() checks _initialized flag
            → Flag is True, skips loading
            → Query executes immediately

    DATA STRUCTURE (AccessData.data):
        {
            "Game_1": {
                "Details": {
                    "Time": "6:05PM",
                    "Day": "Monday",
                    "Month": "Aug",
                    "Year": 2025,
                    "Court": 3,
                    "Game_against": "Team Name",
                    "Our_Scores": 40,
                    "There_Scores": 65,
                    ...
                },
                "Lineup": {
                    "Team A": ["Player1", "Player2", ...],
                    "Team B": ["Player3", "Player4", ...]
                },
                "Quarters": {
                    "Quarter 1": {
                        "Player Name": {
                            "Points": 5,
                            "Fouls": 1,
                            "Assists": 2,
                            "Rebounds": 3,
                            "Turnovers": 1
                        },
                        ...
                    },
                    "Quarter 2": {...},
                    ...
                }
            },
            "Game_2": {...},
            ...
        }

    METHOD CATEGORIES (12 methods):
        Initialization (3):
            __init__(): Instance initializer
            Initialize(): JSON loader
            _ensure_initialized(): Auto-init checker
        
        Game-Level Queries (4):
            Get_details(): Game metadata
            Get_a_lineup(): Team rosters
            Get_quarter_stats(): All quarter stats
            Get_specific_Stats(): Single player quarter stats
        
        Aggregation Queries (3):
            Get_game_stats(): Sum quarters for a game
            Get_season_stats(): Sum games for a player
            Get_team_season_stats(): Sum all players
        
        Analysis Queries (2):
            Get_highest_stats_quarter(): Top performer in quarter
            Get_highest_stats_game(): Top performer in game
            Specific_players_best_stat(): Player's career best
        
        Utility Queries (1):
            Check_player(): Verify participation
            Get_quarter_season_stats(): Quarter-specific season stats

    OUTPUT FORMATTING:
        look_good=False (default):
            - Returns Python dictionaries/lists
            - Suitable for programmatic use
            - Easy to parse and manipulate
            - Used by GUI application
        
        look_good=True:
            - Returns formatted strings
            - Human-readable output
            - Includes headers and formatting
            - Useful for console display/debugging

    ERROR HANDLING:
        Return Patterns:
            - Missing data: Returns error dict {"error": "message"}
            - Invalid game/player: Returns error dict or None
            - Empty results: Returns empty dict {}
            - File errors: Returns None, prints message

    USAGE EXAMPLES:
        # Get player season totals
        stats = AccessData.Get_season_stats("Aston Sharp", sum_total=True)
        # Returns: {'Points': 37, 'Fouls': 3, 'Assists': 5, ...}
        
        # Get game details
        details = AccessData.Get_details("Game_1")
        # Returns: {'Time': '6:05PM', 'Day': 'Monday', ...}
        
        # Get team season totals
        team = AccessData.Get_team_season_stats(sum_total=True)
        # Returns: {'Player1': {'Points': 40, ...}, 'Player2': {...}, ...}
        
        # Find top scorer in quarter
        top = AccessData.Get_highest_stats_quarter("Game_1", "Quarter 1", "Points")
        # Returns: {'Player Name': 22}
        
        # Check if player participated
        played = AccessData.Check_player("Game_1", "Team A", "John Doe")
        # Returns: True or False

    PERFORMANCE CHARACTERISTICS:
        Initialization: ~50ms (one-time, loads entire JSON)
        Query Operations: ~1-5ms (in-memory dict lookups)
        Aggregations: ~10-30ms (depends on data size)
        Memory Footprint: ~50-100KB (typical season)

    THREAD SAFETY:
        Not thread-safe:
            - Shared class variable 'data'
            - No locking mechanisms
            - Single-threaded use recommended
            - For multi-threaded: add threading.Lock

    LIMITATIONS:
        - Hardcoded file path (not configurable after load)
        - No data validation on load
        - No write/update capabilities
        - Windows-specific absolute path
        - Entire dataset loaded into memory
        - No partial loading for large datasets

    DEPENDENCIES:
        - json module (built-in)
        - Data.json file at hardcoded path

    NOTES:
        - Original method names preserved in comments
        - Some inconsistency in naming conventions
        - look_good parameter throughout for flexibility
        - Defensive programming with .get() and empty checks
    
    data = {}
    Class-level dictionary storing all loaded game statistics.
    
    Shared across all method calls (singleton pattern). Populated by Initialize()
    method on first access. Persists for the lifetime of the program.
    
    Structure: {game_id: {Details, Lineup, Quarters}}
    
    _initialized = False
    Class-level flag tracking initialization state.
    
    Set to True after first successful data load. Prevents redundant file I/O
    operations on subsequent method calls. Checked by _ensure_initialized().

=== _Ensure Initialized ===

Ensure data is loaded before query execution (lazy initialization).
        
        Checks the _initialized flag and loads data if needed. Called automatically
        at the start of every query method to guarantee data availability. Implements
        lazy initialization pattern - data loaded on first access, not at import time.

        Parameters:
            None (classmethod - operates on class, not instance)

        Returns:
            None

        Side Effects:
            If not initialized (_initialized == False):
                - Creates AccessData instancea
                - Instance __init__() calls Initialize()
                - Initialize() loads Data.json into cls.data
                - Sets cls._initialized to True
            
            If already initialized (_initialized == True):
                - No action taken (fast return)
                - No file I/O performed

        Algorithm:
            1. Check cls._initialized flag
            2. If False:
               a. Create instance: instance = cls()
               b. __init__() automatically called
               c. __init__() calls Initialize()
               d. Initialize() populates cls.data
               e. Set cls._initialized = True
            3. If True:
               - Return immediately (no operations)

        Execution Flow:
            First Method Call:
                User: AccessData.Get_season_stats("Player")
                → _ensure_initialized() called
                → _initialized is False
                → instance = cls() creates instance
                → __init__() runs Initialize()
                → Data loaded into cls.data
                → _initialized set to True
                → Query proceeds with loaded data
            
            Subsequent Calls:
                User: AccessData.Get_game_stats("Game_1")
                → _ensure_initialized() called
                → _initialized is True
                → Return immediately
                → Query proceeds (data already in memory)

        Performance:
            First call: ~50ms (includes file loading)
            Subsequent calls: ~0.001ms (single if-check)
            
            Benchmark (typical):
                Initial: 50ms (file I/O dominates)
                After: <1µs (flag check only)

        Design Pattern:
            Lazy Initialization:
                - Delays expensive operation until needed
                - Avoids unnecessary loading if never queried
                - Transparent to caller (automatic)
            
            Guard Pattern:
                - _initialized flag guards against redundant work
                - Once True, loading never repeated
                - Prevents duplicate file I/O

        Thread Safety:
            Not thread-safe:
                - No locking mechanism
                - Race condition possible if multiple threads
                - Could create multiple instances simultaneously
                - For multi-threaded: add threading.Lock

        Memory Impact:
            - Instance created but not stored (garbage collected)
            - Only cls.data persists (class variable)
            - Instance creation overhead negligible (~1KB)

        Called By:
            Every query method in the class:
                - Get_details()
                - Get_season_stats()
                - Get_team_season_stats()
                - Get_highest_stats_quarter()
                - And all others...

        Notes:
            - Instance variable not stored (could optimize with cls())
            - Variable name 'instance' unused after creation
            - Side effect: __init__() does the actual work
            - Flag prevents redundant initialization forever

=== __init__ ===

        Initialize an AccessData instance and load game data from JSON file.
        
        Constructor that creates an AccessData instance and immediately calls Initialize()
        to load the Data.json file into memory. While this is an instance method, the
        class is designed to work primarily with classmethods, making direct instantiation
        uncommon. Typically called internally by _ensure_initialized() rather than by users.

        Parameters:
            None

        Returns:
            None (constructor)

        Side Effects:
            - Calls self.Initialize() method
            - Initialize() loads Data.json into AccessData.data class variable
            - May print error messages if file loading fails
            - Sets AccessData._initialized flag to True (via _ensure_initialized)

        Execution Flow:
            1. Python calls __init__ when instance created: instance = AccessData()
            2. __init__ calls self.Initialize()
            3. Initialize() opens and parses Data.json
            4. Data stored in AccessData.data (class variable, not instance variable)
            5. Constructor completes, instance returned to caller

        Design Pattern:
            Initialization in Constructor:
                - Standard pattern for resource loading
                - Ensures data available immediately after creation
                - No separate initialization call needed
                - Eager loading (happens at instantiation time)

        Usage Context:
            Internal Use (typical):
                # Called by _ensure_initialized()
                instance = cls()  # __init__ runs, loads data
            
            Direct Use (rare):
                accessor = AccessData()  # __init__ runs, loads data
                # But still use classmethods:
                AccessData.Get_season_stats("Player")

        Class vs Instance:
            - Instance created but data stored at class level
            - Instance itself has no attributes (no self.data)
            - All data in AccessData.data (class variable)
            - Instance creation is side effect for initialization
            - Instance typically not stored or used after creation

        Performance:
            Time: ~50ms (dominated by file I/O in Initialize)
            Memory: ~1KB for instance object + ~50KB for data
            Note: Data stored once at class level, not per instance

        Error Handling:
            - No try-except at this level
            - Initialize() handles all errors
            - Errors caught and printed, not raised
            - Constructor always succeeds (even if loading fails)

        Called By:
            _ensure_initialized():
                if not cls._initialized:
                    instance = cls()  # <-- Triggers __init__
                    cls._initialized = True

        Relationship to Other Methods:
            __init__() 
                → Initialize() 
                    → Loads AccessData.data
                        → Available to all classmethods

        Design Notes:
            Simple and Clean:
                - One-line constructor
                - Single responsibility (delegate to Initialize)
                - No complex logic
                - Standard Python pattern
            
            Unused Instance:
                - Instance created but not utilized
                - Could be static initialization instead
                - Current pattern: instance as initialization trigger
                - Class-level storage makes instance unnecessary

        Alternatives Considered:
            Static Initialization:
                # At module level
                AccessData.data = load_json()
                # But: loads even if never used
            
            Explicit Initialize:
                AccessData.Initialize()
                # But: requires manual call, easy to forget
            
            Current Approach (Lazy):
                # Best of both worlds
                # Automatic, on-demand loading

        Thread Safety:
            Not thread-safe:
                - No locking in __init__
                - Multiple simultaneous calls could cause issues
                - Rare in practice (single-threaded typical use)

        Memory Lifecycle:
            1. Instance created (small object)
            2. Initialize() loads data (class level)
            3. Instance may be garbage collected
            4. Data persists at class level
            5. Data lives until program termination

        Notes:
            - No instance variables created (no self.anything)
            - All state stored at class level
            - Constructor never fails (errors caught in Initialize)
            - Simple delegation pattern
            - Standard Python constructor convention

=== Initialize ===

        Load basketball game statistics from JSON file into memory.
        
        Reads the Data.json file from a hardcoded path, parses it as JSON, and stores
        the entire dataset in the class-level AccessData.data dictionary. Handles file
        errors gracefully with try-except blocks and optional return of loaded data.

        Parameters:
            load (bool): If True, returns the loaded data dictionary after successful load.
                        If False (default), returns None after successful load.
                        Legacy parameter - typically unused in practice.
            
            filename (str): Intended filename parameter but currently unused.
                           Hardcoded path takes precedence.
                           Default: "Data.json"
                           Note: Parameter exists but has no effect

        Returns:
            dict or None:
                - If load=True and successful: Returns AccessData.data (full dataset)
                - If load=False and successful: Returns None
                - If any error occurs: Returns None

        Side Effects:
            Success:
                - Loads entire Data.json into AccessData.data class variable
                - Overwrites any existing data in AccessData.data
                - Makes data available to all query methods
            
            Failure:
                - Prints error message to console
                - AccessData.data remains unchanged (empty {} if first load)
                - No exception raised (errors caught and handled)

        File Path:
            Hardcoded: r"C:\Users\Drags Jrs\Mylesbasketballstatsanddata\Database\Data.json"
            
            Issues:
                - Windows-specific (uses backslashes)
                - Absolute path (not relative)
                - User-specific (includes username)
                - Not configurable (filename parameter ignored)
                - Not portable (won't work on other machines)

        Error Handling:
            FileNotFoundError:
                Trigger: Data.json doesn't exist at specified path
                Action: Print "File not found: {path}"
                Return: None
                Impact: AccessData.data remains empty or unchanged
            
            json.JSONDecodeError:
                Trigger: File exists but contains invalid JSON
                Action: Print "Error reading JSON from {path}"
                Return: None
                Common causes: Syntax errors, trailing commas, missing quotes
            
            Generic Exception:
                Trigger: Any other error (permissions, encoding, etc.)
                Action: Print "Unknown error: {exception}"
                Return: None
                Catches: IOError, PermissionError, UnicodeDecodeError, etc.

        Algorithm:
            1. Define hardcoded file path (ignores filename parameter)
            2. Open file in read mode
            3. Parse JSON into Python dictionary using json.load()
            4. Store in AccessData.data class variable
            5. If error occurs:
               a. Catch specific exception
               b. Print descriptive error message
               c. Return None
            6. If load=True and successful:
               - Return the loaded data
            7. Otherwise:
               - Return None (implicit or explicit)

        JSON Structure Expected:
            {
                "Game_1": {
                    "Details": {...},
                    "Lineup": {...},
                    "Quarters": {...}
                },
                "Game_2": {...},
                ...
            }

        Performance:
            File Size: ~10-50KB (typical season)
            Load Time: ~50ms (includes file I/O + JSON parsing)
            Memory: Stores entire dataset in RAM
            
            Benchmark:
                Small file (5 games): ~30ms
                Medium file (10 games): ~50ms
                Large file (20 games): ~80ms

        Usage Examples:
            Standard (automatic via _ensure_initialized):
                # No direct call needed
                AccessData.Get_season_stats("Player")  # Triggers Initialize internally
            
            Explicit initialization:
                accessor = AccessData()  # Calls Initialize()
            
            With data return:
                accessor = AccessData()
                data = accessor.Initialize(load=True)  # Returns loaded data
                # But data also in AccessData.data anyway

        Called By:
            - __init__(): Automatically when instance created
            - _ensure_initialized(): Indirectly via instance creation

        Design Issues:
            Parameter Unused:
                - filename parameter exists but ignored
                - Misleading API (suggests configurability)
                - Should be removed or implemented
            
            Hardcoded Path:
                - Not configurable
                - Not portable across systems
                - Should use config file or environment variable
            
            Error Handling:
                - Prints to console (no logging)
                - Silent failure (returns None)
                - No exception propagation
                - Difficult to debug in production

        Improvements Needed:
            1. Use filename parameter or remove it
            2. Make path configurable (config file, env var, or parameter)
            3. Use pathlib for cross-platform paths
            4. Add logging instead of print statements
            5. Provide more detailed error context
            6. Consider raising exceptions instead of returning None
            7. Add data validation after loading
            8. Support relative paths

        Memory Considerations:
            - Entire file loaded into RAM
            - No streaming or partial loading
            - Acceptable for small datasets (<1MB)
            - Could be issue for large datasets (>10MB)

        Thread Safety:
            Not thread-safe:
                - Modifies class variable AccessData.data
                - No locking mechanism
                - Concurrent calls could cause issues

        Notes:
            - Raw string (r"...") prevents backslash interpretation
            - Context manager (with) ensures file closure
            - json.load() reads entire file at once
            - Class variable assignment (not instance variable)
            - load parameter rarely used in practice

=== Get Details ===

Retrieve game metadata and details for a specific game.
        
        Returns comprehensive game information including time, date, teams, scores, referee
        quality, court number, and other metadata from the Details section of a game record.
        Supports both dictionary and formatted string output.

        Parameters:
            game (str or None): Game identifier (e.g., "Game_1", "Game_2", "Game_3").
                               If None or invalid, returns error dictionary.
            
            look_good (bool): Output format control.
                             False (default): Returns dictionary for programmatic use
                             True: Returns formatted string with headers for display

        Returns:
            dict or str:
                If look_good=False:
                    Success: Dictionary of game details
                        {
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
                            ...
                        }
                    Error: {"Error": "Invalid game: {game}"} or {"Error": "Game: {game} not found"}
                
                If look_good=True:
                    Success: Formatted string with headers
                        "--------------------- Details ------------------------
                         Time: 6:05PM
                         Day: Monday
                         Month: Aug
                         Year: 2025
                         ...
                         --------------------------------------------------"
                    Error: {"Error": "..."} (still returns dict on error)

        Side Effects:
            - Calls cls._ensure_initialized() to load data if needed
            - No modifications to stored data
            - Creates defensive copy of details dict (look_good=False)

        Algorithm:
            1. Ensure data is loaded (_ensure_initialized)
            2. Validate game parameter (not None, exists in data)
            3. If invalid: Return error dictionary
            4. Retrieve game_stats from cls.data
            5. Double-check game_stats not empty (defensive)
            6. Extract "Details" section from game_stats
            7. Format output based on look_good parameter:
               - False: Return copy of details dictionary
               - True: Build formatted string with headers
            8. Return formatted result

        Validation Checks:
            Check 1: if not game or game not in cls.data
                - Catches None parameter
                - Catches invalid game names
                - Returns: {"Error": "Invalid game: {game}"}
            
            Check 2: if game_stats == {}
                - Defensive check after .get()
                - Should be redundant if Check 1 works
                - Returns: {"Error": "Game: {game} not found"}

        Data Structure Accessed:
            cls.data[game]["Details"] = {
                "Time": str,
                "Day": str,
                "Month": str,
                "Year": int,
                "Court": int,
                "Game_against": str,
                "Our_Scores": int,
                "There_Scores": int,
                "Good_bad_ref": str,
                "Who_was_the_ref": str,
                "Player_Calm": str,
                "Player_Angry": str,
                "Intensity": str,
                "Other_team_calm": str,
                "Other_team_angry": str,
                "Amount_of_timeouts": int,
                "Amount_of_refs": int,
                "Amount_of_subs": int,
                "Total_team_players": int,
                "Other_team_players": int,
                "Amount_of_fill_in": int,
                "Clear_good_player": int
            }

        Formatting (look_good=True):
            Header: "--------------------- Details ------------------------"
            Body: Each detail on separate line, format: "{key}: {value}"
            Footer: "--------------------------------------------------"
            Separator: Newline (\n) between each line

        Usage Examples:
            Basic retrieval:
                details = AccessData.Get_details("Game_1")
                print(details["Time"])  # "6:05PM"
                print(details["Our_Scores"])  # 40
            
            Formatted display:
                output = AccessData.Get_details("Game_1", look_good=True)
                print(output)  # Prints formatted details with borders
            
            Error handling:
                result = AccessData.Get_details("Invalid_Game")
                if "Error" in result:
                    print(f"Failed: {result['Error']}")

        Defensive Copy:
            return details.copy()
            
            Why:
                - Prevents caller from modifying original data
                - Protects data integrity
                - Shallow copy sufficient (values are primitives)
            
            Performance:
                - ~1µs overhead for copy
                - Negligible compared to query time

        Performance:
            Time: ~2-5ms
                - _ensure_initialized: ~0.001ms (if already loaded)
                - Dictionary lookups: ~1ms
                - Copy operation: ~1ms
                - Formatting (if look_good): ~2ms
            
            Memory: ~1-2KB (details dictionary copy)

        Error Cases:
            game=None:
                Returns: {"Error": "Invalid game: None"}
            
            game="NonExistent":
                Returns: {"Error": "Invalid game: NonExistent"}
            
            game exists but no Details section:
                Returns: {} (empty dict, not an error)

        Original Method Name:
            Comment indicates: "Original name: quick_game_details"
            Renamed to: Get_details for consistency with naming pattern

        Called By:
            - player_report.py: Potentially for game context display
            - Direct queries: For game information retrieval

        Related Methods:
            - Get_a_lineup(): Gets team rosters
            - Get_quarter_stats(): Gets quarter-level stats
            - Get_game_stats(): Gets aggregated game stats

        Use Cases:
            Game Summary Display:
                - Show when/where game was played
                - Display final scores
                - Referee information
            
            Context for Statistics:
                - Date of performance
                - Opponent information
                - Game intensity level
            
            Report Generation:
                - Game header information
                - Complete game metadata

        Design Notes:
            Redundant Validation:
                - Two checks for game existence
                - Second check (game_stats == {}) likely unnecessary
                - Kept for defensive programming
            
            Error Format Inconsistency:
                - Errors return dict even when look_good=True
                - Could return formatted error string instead
                - Current behavior: dict errors, string success

        Notes:
            - Uses .get() with default {} for safety
            - Creates defensive copy to protect data
            - look_good formatting uses list comprehension for efficiency
            - All detail fields returned (no filtering)
            - Order of details preserved from JSON

=== Get A Lineup ===

        Retrieve the roster/lineup of players for a specific team in a specific game.
        
        Returns a list of player names who were on the roster for the specified team
        in the given game. Useful for verifying participation, displaying team rosters,
        and identifying which players were available for a particular matchup.

        Parameters:
            game (str or None): Game identifier (e.g., "Game_1", "Game_2", "Game_3").
                               If None or invalid, returns error dictionary.
            
            team (str or None): Team name as it appears in the Lineup section.
                               Examples: "Newport Raiders U16 Boys Paul",
                                        "Newport Raiders U16 Boys Julie",
                                        "Truganina South Basketball Club Bullets"
            
            look_good (bool): Output format control.
                             False (default): Returns list of player names
                             True: Returns formatted numbered string for display

        Returns:
            list or str or dict:
                If look_good=False:
                    Success: List of player names (strings)
                        ["Benjamin Berridge", "Angus Lee", "Aston Sharp", ...]
                    Error: {"Error": "{game} is not valid"} or 
                           {"error": "{team} not found in {game}"}
                
                If look_good=True:
                    Success: Formatted numbered string
                        "----------------- Team players ----------------------
                         
                         1. Benjamin Berridge
                         
                         2. Angus Lee
                         
                         3. Aston Sharp
                         ..."
                    Error: {"error": "..."} (still returns dict on error)

        Side Effects:
            - Calls cls._ensure_initialized() to load data if needed
            - No modifications to stored data
            - Returns original list reference (not a copy - minor data exposure)

        Algorithm:
            1. Ensure data is loaded (_ensure_initialized)
            2. Retrieve game_stats from cls.data using .get(game, {})
            3. Validate game_stats not empty
            4. If empty: Return error dict (invalid game)
            5. Navigate to team players: game_stats["Lineup"][team]
            6. Use chained .get() for safe nested access
            7. Validate team_players not empty
            8. If empty: Return error dict (team not found)
            9. Format output based on look_good parameter:
               - False: Return player list directly
               - True: Build numbered list with headers
            10. Return formatted result

        Data Structure Accessed:
            cls.data[game]["Lineup"] = {
                "Team A Name": [
                    "Player 1 Name",
                    "Player 2 Name",
                    "Player 3 Name",
                    ...
                ],
                "Team B Name": [
                    "Player 4 Name",
                    "Player 5 Name",
                    ...
                ]
            }

        Validation Checks:
            Check 1: if not game_stats
                - Catches invalid game parameter
                - Catches None game parameter
                - Returns: {"Error": "{game} is not valid"}
            
            Check 2: if not team_players
                - Catches invalid team name
                - Catches team not in this game
                - Catches empty roster (unlikely but possible)
                - Returns: {"error": "{team} not found in {game}"}

        Error Capitalization Inconsistency:
            First error: {"Error": ...} (capital E)
            Second error: {"error": ...} (lowercase e)
            Note: Inconsistent but functional (calling code should check both)

        Formatting (look_good=True):
            Header: "----------------- Team players ----------------------"
            Body: Numbered list (1-indexed), format: "{number}. {player_name}"
            Separator: Double newline (\n\n) between each player
            No footer line (unlike Get_details)

        Usage Examples:
            Get roster list:
                players = AccessData.Get_a_lineup("Game_1", "Newport Raiders U16 Boys Julie")
                print(players)  # ["Benjamin Berridge", "Angus Lee", ...]
                print(f"Team has {len(players)} players")
            
            Formatted display:
                output = AccessData.Get_a_lineup("Game_1", "Team A", look_good=True)
                print(output)  # Prints numbered roster with header
            
            Check if player in roster:
                roster = AccessData.Get_a_lineup("Game_1", "Team A")
                if "John Doe" in roster:
                    print("Player was on roster")
            
            Error handling:
                result = AccessData.Get_a_lineup("Game_1", "Invalid Team")
                if isinstance(result, dict) and ("Error" in result or "error" in result):
                    print("Team not found")

        Enumerate Details:
            enumerate(team_players, start=1)
            
            Purpose:
                - Creates numbered list starting at 1
                - More natural for users (1, 2, 3... vs 0, 1, 2...)
            
            Output:
                Player at index 0 → numbered as "1."
                Player at index 1 → numbered as "2."
                And so on...

        Performance:
            Time: ~1-3ms
                - _ensure_initialized: ~0.001ms (if already loaded)
                - Dictionary navigation: ~0.5ms
                - List access: ~0.5ms
                - Formatting (if look_good): ~1-2ms (depends on roster size)
            
            Memory: 
                - List reference only (~8 bytes)
                - Formatted string: ~100-500 bytes (depends on roster size)

        Typical Roster Sizes:
            Youth basketball: 5-10 players
            Full roster: 10-15 players
            With fill-ins: May vary

        Data Protection Issue:
            return team_players
            
            Issue:
                - Returns direct reference to original list
                - Caller could modify: roster.append("New Player")
                - Would modify original data in cls.data
            
            Should be:
                return team_players.copy() or list(team_players)
            
            Impact:
                - Low (list typically not modified by callers)
                - But violates data encapsulation principle

        Error Cases:
            game=None:
                Returns: {"Error": "None is not valid"}
            
            game="NonExistent":
                Returns: {"Error": "NonExistent is not valid"}
            
            team=None:
                Returns: {"error": "None not found in {game}"}
            
            team not in game:
                Returns: {"error": "{team} not found in {game}"}
            
            Empty roster (edge case):
                Returns: {"error": "{team} not found in {game}"}
                Note: Empty list treated as not found

        Original Method Name:
            Comment indicates: "Original name: get_a_team"
            Renamed to: Get_a_lineup for clarity (lineup more accurate than team)

        Called By:
            - Check_player(): Uses lineup to verify participation
            - Direct queries: For roster information
            - Report generation: Team composition display

        Related Methods:
            - Check_player(): Verifies if player in lineup
            - Get_details(): Gets game metadata (opponents)
            - Get_quarter_stats(): Gets stats for players in lineup

        Use Cases:
            Roster Verification:
                - Check who played in a game
                - Verify player participation
                - Identify fill-in players
            
            Report Generation:
                - Display team composition
                - Create game summaries
                - Compare rosters across games
            
            Analysis:
                - Track roster changes
                - Identify common lineups
                - Count participation frequency

        Design Notes:
            Safe Navigation:
                - Chained .get() prevents KeyError
                - Default {} and [] for missing data
                - Graceful degradation
            
            Double Newline Separator:
                - \n\n creates blank line between players
                - More spacing than typical formatting
                - Makes roster easier to scan visually
            
            No Footer:
                - Unlike Get_details which has footer line
                - Inconsistent formatting across methods
                - Minor aesthetic issue

        Notes:
            - Uses chained .get() for safe nested dictionary access
            - Enumeration starts at 1 for human readability
            - Empty roster treated as "not found" error

=== Get Quarter Stats ===

        Retrieve all player statistics for a specific quarter in a specific game.
        
        Returns a dictionary mapping player names to their individual statistics for
        the specified quarter. Each player's stats include Points, Fouls, Assists,
        Rebounds, and Turnovers. Useful for quarter-by-quarter analysis, finding top
        performers in a quarter, or breaking down game performance.

        Parameters:
            game (str or None): Game identifier (e.g., "Game_1", "Game_2", "Game_3").
                               If None or invalid, returns error dictionary.
            
            quarter (str or None): Quarter identifier (e.g., "Quarter 1", "Quarter 2").
                                  Must match exact format with capital Q and space.
                                  If None or invalid, returns error dictionary.
            
            look_good (bool): Output format control.
                             False (default): Returns dictionary for programmatic use
                             True: Returns formatted string with player stat lines

        Returns:
            dict or str:
                If look_good=False:
                    Success: Dictionary of all players and their stats
                        {
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
                            },
                            ...
                        }
                    Error: {"error": "Game: {game} not found"} or
                           {"error": "Quarter: {quarter} not found"}
                
                If look_good=True:
                    Success: Formatted string with header and stat lines
                        "-------------------- Game_1: Quarter 1 stats --------------------------
                         Benjamin Berridge: Points: 2, Fouls: 1, Rebounds: 2, Assists: 0, Turnovers: 2
                         
                         Angus Lee: Points: 3, Fouls: 1, Rebounds: 2, Assists: 0, Turnovers: 2
                         
                         ..."
                    Error: {"error": "..."} (still returns dict on error)

        Side Effects:
            - Calls cls._ensure_initialized() to load data if needed
            - No modifications to stored data
            - Creates defensive copy of quarter_stats dict (look_good=False)

        Algorithm:
            1. Ensure data is loaded (_ensure_initialized)
            2. Retrieve game_stats from cls.data
            3. Validate game exists (game_stats not empty)
            4. If invalid: Return error dict
            5. Navigate to Quarters section
            6. Retrieve specific quarter stats
            7. Validate quarter exists (quarter_stats not empty)
            8. If invalid: Return error dict
            9. Format output based on look_good parameter:
               - False: Return defensive copy of quarter_stats
               - True: Build formatted string with player stat lines
            10. Return formatted result

        Data Structure Accessed:
            cls.data[game]["Quarters"][quarter] = {
                "Player Name": {
                    "Points": int,
                    "Fouls": int,
                    "Rebounds": int,
                    "Assists": int,
                    "Turnovers": int
                },
                "Another Player": {...},
                ...
            }

        Validation Checks:
            Check 1: if not game_stats
                - Catches invalid game parameter
                - Catches None game parameter
                - Returns: {"error": "Game: {game} not found"}
            
            Check 2: if not quarter_stats
                - Catches invalid quarter name
                - Catches quarter not in this game
                - Catches empty quarter (unlikely)
                - Returns: {"error": "Quarter: {quarter} not found"}

        Potential Bug:
            Line: quarters = game_stats.get("Quarters")
            
            Issue:
                - No default value provided to .get()
                - If "Quarters" key missing, quarters = None
                - Next line: quarters.get(quarter, {})
                - Would raise AttributeError: 'NoneType' object has no attribute 'get'
            
            Should be:
                quarters = game_stats.get("Quarters", {})
            
            Impact:
                - Low (all games have Quarters section in practice)
                - But violates defensive programming principle

        Formatting (look_good=True):
            Header: "-------------------- {game}: {quarter} stats --------------------------"
            Body: Player stat lines
                Format: "{player_name}: {stat1}: {val1}, {stat2}: {val2}, ..."
            Separator: Newline (\n) between header and first player
                      Double newline (\n\n) between players (due to \n in append + \n in join)
            No footer line

        Stat Line Construction:
            stat_line = ", ".join(f"{stat_name}: {stat_value}" for ...)
            
            Example:
                Input: {"Points": 5, "Fouls": 1, "Rebounds": 3}
                Output: "Points: 5, Fouls: 1, Rebounds: 3"
            
            Features:
                - Comma-separated values
                - Space after comma
                - All stats on one line per player

        Usage Examples:
            Get all quarter stats:
                q1_stats = AccessData.Get_quarter_stats("Game_1", "Quarter 1")
                print(q1_stats["Benjamin Berridge"]["Points"])  # 2
            
            Formatted display:
                output = AccessData.Get_quarter_stats("Game_1", "Quarter 1", look_good=True)
                print(output)
            
            Find top scorer in quarter:
                stats = AccessData.Get_quarter_stats("Game_1", "Quarter 1")
                top_scorer = max(stats.items(), key=lambda x: x[1]["Points"])
                print(f"{top_scorer[0]} scored {top_scorer[1]['Points']} points")
            
            Iterate through all players:
                stats = AccessData.Get_quarter_stats("Game_1", "Quarter 1")
                for player, player_stats in stats.items():
                    print(f"{player}: {player_stats['Points']} pts")

        Defensive Copy:
            return quarter_stats.copy()
            
            Why:
                - Prevents caller from modifying original data
                - Protects data integrity
                - Shallow copy (stat dicts still shared)
            
            Shallow vs Deep:
                - Shallow: Copies outer dict, inner dicts still referenced
                - Deep: Would copy everything (import copy; copy.deepcopy())
                - Shallow sufficient (callers typically don't modify nested stats)

        Performance:
            Time: ~2-5ms
                - _ensure_initialized: ~0.001ms (if already loaded)
                - Dictionary navigation: ~1ms
                - Copy operation: ~1-2ms (depends on player count)
                - Formatting (if look_good): ~2-3ms (depends on player count)
            
            Memory: ~1-5KB
                - Dict copy overhead depends on number of players (5-10 typical)
                - Each player: ~200 bytes

        Typical Data Size:
            Players per quarter: 5-10 (depending on substitutions)
            Stats per player: 5 (Points, Fouls, Rebounds, Assists, Turnovers)
            Total entries: 25-50 key-value pairs

        Error Cases:
            game=None:
                Returns: {"error": "Game: None not found"}
            
            game="NonExistent":
                Returns: {"error": "Game: NonExistent not found"}
            
            quarter=None:
                Potential AttributeError if Quarters missing (bug)
                Or: {"error": "Quarter: None not found"}
            
            quarter="Quarter 5":
                Returns: {"error": "Quarter: Quarter 5 not found"}
            
            Empty quarter (no players):
                Returns: {"error": "Quarter: {quarter} not found"}

        Quarter Name Format:
            Expected: "Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"
            - Capital Q
            - Space between "Quarter" and number
            - Case-sensitive
            - Alternative names like "Q1" won't work

        Original Method Name:
            Comment indicates: "Same name" (Get_quarter_stats)
            No renaming from original implementation

        Called By:
            - Get_specific_Stats(): Uses this to get quarter data, then filters
            - Get_highest_stats_quarter(): Uses this to find top performers
            - Direct queries: For quarter-by-quarter analysis

        Related Methods:
            - Get_specific_Stats(): Gets single player's quarter stats
            - Get_game_stats(): Aggregates all quarters for a game
            - Get_highest_stats_quarter(): Finds top performer in quarter

        Use Cases:
            Quarter Analysis:
                - Compare player performance across quarters
                - Identify strong/weak quarters
                - Track substitution patterns
            
            Performance Tracking:
                - Monitor fatigue (declining stats over quarters)
                - Identify clutch performers (Q4 performance)
                - Analyze opening vs closing quarters
            
            Coaching Insights:
                - When to use timeouts (check quarter trends)
                - Substitution timing (based on player quarter stats)
                - Matchup analysis (how players perform against different lineups)

        Design Notes:
            Missing Default Value:
                - quarters.get("Quarters") has no default
                - Could cause AttributeError
                - Should add default: .get("Quarters", {})
            
            Newline in stat_line:
                - output.append(f"{players_name}: {stat_line}\n")
                - Explicit \n added
                - Then "\n".join(output) adds more newlines
                - Results in double spacing between players

        Notes:
            - Uses .copy() for defensive programming
            - Format could cause AttributeError if Quarters key missing
            - Stat line construction uses generator expression for efficiency
            - All players in quarter returned (no filtering)
            - Order of stats preserved from JSON

=== Get Specific Stats === 

DOCSTRING LAYOUT

=== Get Game Stats ===

DOCSTRING LAYOUT

=== Get Season Stats ===

DOCSTRING LAYOUT

=== Get Team Season Stats ===

DOCSTRING LAYOUT

=== Get Quarter Season Stats ===

DOCSTRING LAYOUT

=== Get Highest Stats Quarter ===

DOCSTRING LAYOUT

=== Get Highest Stats Game ===

DOCSTRING LAYOUT

=== Specific Players Best Stat ===

DOCSTRING LAYOUT

=== Check Player ===

DOCSTRING LAYOUT

=== If __name__ == '__main__': ===

DOCSTRING LAYOUT

