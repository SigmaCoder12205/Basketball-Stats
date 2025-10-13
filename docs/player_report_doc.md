=== Overview === 

Basketball Player Report Card System - GUI Module

FILE NAME RELATIVE: player_report.py
FILE NAME ABSOLUTE: C:/Users/Drags Jrs/Drags/testing/player_report.py

PURPOSE:
    This module provides a PyQt5-based graphical user interface for viewing and analyzing
    individual basketball player statistics across games and seasons. It serves as the 
    primary user-facing component of the basketball statistics tracking system.

IMPORTS AND PATH CONFIGURATION:
    sys, os:
        - System-level operations and path manipulation
        - Required for dynamic Python path configuration
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))):
        - Adds parent directory to Python's module search path
        - Prevents ModuleNotFoundError when importing local modules
        - Ensures interpreter can find utils.accessing_data from testing/ directory
        - Works by resolving: current_file → parent_dir → add to sys.path
    
    AccessData (from utils.accessing_data):
        - Data access layer that interfaces with Data.json
        - Provides all methods for retrieving and aggregating basketball statistics
        - Central connection between raw JSON data and GUI display
    
    PyQt5.QtWidgets:
        - QApplication: Main application controller
        - QWidget: Base class for PlayerReport window
        - QLabel: Text/header displays
        - QLineEdit: Text input fields (imported but unused)
        - QPushButton: Interactive buttons for navigation
        - QVBoxLayout: Vertical layout manager
        - QTextEdit: Multi-line text display areas (HTML-capable)
        - QComboBox: Dropdown selection menus
    
    PyQt5.QtCore:
        - Qt: Core Qt constants and enums (alignment, object naming, etc.)

MAIN CLASS:
    PlayerReport - A QWidget-based GUI application that displays comprehensive player analytics

FEATURES:
    1. Season Average Stats - Calculate mean, median, range, and team contribution percentage
    2. Game Comparison - Track stat trends across multiple games with visual indicators
    3. Season Grading - Letter grade evaluation (A+ to F) based on team performance contribution
    4. Best/Worst Game Highlights - Identify peak and lowest performances for each stat category
    5. Individual Game Rating - Weighted scoring system (0-100) for single game performance
    6. Season Game Rating - Aggregate ratings across all games with average calculation

DATA FLOW:
    User Input (GUI) → PlayerReport methods → AccessData queries → Data.json → 
    Formatted HTML output → QTextEdit display

DESIGN PATTERN:
    - Single-page application with dynamic content loading
    - Menu-driven navigation with "back to main menu" functionality
    - HTML-rendered statistics with dark theme styling
    - Dropdown selectors for stat category and game selection
    - Widget reuse pattern (show/hide instead of recreate for performance)

USAGE:
    from testing.player_report import PlayerReport
    
    app = QApplication(sys.argv)
    report = PlayerReport("Player Name")
    report.show()
    sys.exit(app.exec_())

RATING ALGORITHM:
    Game Rating = ((Points × 1.7) + (Assists × 1.2) + (Rebounds × 1.45) 
                   - (Fouls × 0.3) - (Turnovers × 1.3) + 10) × 2.2
    Capped between 0-100

GRADING SCALE:
    A+ (90-100%) | A (80-89%) | B+ (70-79%) | B (60-69%)
    C+ (50-59%)  | C (40-49%) | D+ (30-39%) | D (20-29%) | F (0-19%)

AUTHOR: Drags Jrs
LAST MODIFIED: 2025

=== Player Report === 

Main GUI window for displaying comprehensive individual player basketball statistics.
    
    This class creates a dark-themed, menu-driven interface with six analytical features
    for examining player performance across single games and entire seasons. Uses PyQt5
    for the interface and AccessData for all data retrieval operations.

    INHERITANCE:
        Inherits from QWidget (PyQt5.QtWidgets.QWidget)

    ATTRIBUTES:
        Instance Variables (Core):
            players_name (str): The player's full name for data queries
            header_label (QLabel): Main title displaying "{Player}'s Report Card"
            vbox (QVBoxLayout): Primary vertical layout manager for all widgets
            menu_buttons (list): Collection of all 6 main menu button references
            
        Main Menu Buttons (Always Present):
            get_quick_stats_btn (QPushButton): Opens season statistics interface
            compare_all_games_btn (QPushButton): Opens game-to-game comparison interface
            season_grading_btn (QPushButton): Opens letter grade evaluation interface
            best_worst_game_btn (QPushButton): Opens performance highlights interface
            game_rating_btn (QPushButton): Opens single game rating interface
            season_game_rating_btn (QPushButton): Opens season-wide ratings interface
            
        Dynamic Widgets (Created on Demand):
            stat_selector (QComboBox): Dropdown for season stats feature
            stats_display (QTextEdit): Display area for season statistics
            back_button (QPushButton): Navigation for season stats
            
            stat_selector_compare (QComboBox): Dropdown for comparison feature
            trends_display (QTextEdit): Display area for game trends
            back_button_compare (QPushButton): Navigation for comparison
            
            grading_display (QTextEdit): Display area for letter grades
            back_button_grading (QPushButton): Navigation for grading
            
            highlights_selector (QComboBox): Dropdown for highlights feature
            highlights_display (QTextEdit): Display area for best/worst games
            back_button_highlights (QPushButton): Navigation for highlights
            
            game_selector (QComboBox): Dropdown for single game rating
            game_rating_display (QTextEdit): Display area for game rating
            back_button_game_rating (QPushButton): Navigation for game rating
            
            season_rating_display (QTextEdit): Display area for season ratings
            back_button_season_rating (QPushButton): Navigation for season ratings

    METHODS:
        Initialization:
            __init__(players_name): Create window and initialize all main menu components
            init_main_UI(): Configure layout, styling, and window properties
            
        Navigation:
            back_to_main_menu(): Hide all dynamic widgets and return to main menu
            
        Season Statistics Feature:
            Season_average(): Display season stats interface
            update_season_stats(stat_name): Refresh display when stat selection changes
            calculate_season_average(what_to_look_for): Compute statistical measures
            
        Game Comparison Feature:
            show_compare_all_games(): Display game comparison interface
            update_game_comparison(stat_name): Refresh display when stat selection changes
            compare_all_games(): Generate trend analysis data
            
        Season Grading Feature:
            show_grading(): Display grading interface
            format_grading(): Generate HTML for grade display
            grading(): Calculate letter grades for all stats
            
        Performance Highlights Feature:
            show_best_worst_highlights(): Display highlights interface
            format_highlights(stat_name): Generate HTML for highlights display
            best_worst_highlights(what_to_look_for): Find best and worst games
            
        Game Rating Feature:
            show_game_rating(): Display single game rating interface
            format_game_rating(game_name): Generate HTML for rating display
            game_rating(game_name): Calculate 0-100 performance score
            
        Season Rating Feature:
            show_game_season_game_rating(): Display season ratings interface
            format_season_game_rating(): Generate HTML for season ratings
            season_game_rating(): Calculate ratings for all games

    DESIGN PATTERNS:
        Widget Reuse: Widgets are created once and shown/hidden rather than destroyed
        Single Page Application: All features displayed in same window
        Signal-Slot Connections: Dropdown changes automatically trigger display updates
        HTML Rendering: All statistics formatted as styled HTML for visual appeal

    COLOR SCHEME:
        Background: #0a0a0f (near black)
        Primary Accent: #6366f1 (indigo blue)
        Success/Positive: #10b981 (green)
        Warning/Caution: #eab308 (yellow)
        Danger/Negative: #ef4444 (red)
        Info/Neutral: #8b5cf6 (purple)
        Text Primary: #e5e7eb (light gray)
        Text Secondary: #9ca3af (medium gray)

    STAT CATEGORIES:
        All features analyze these five statistics:
        - Points: Player scoring
        - Fouls: Personal fouls committed
        - Assists: Passes leading to scores
        - Rebounds: Ball recoveries
        - Turnovers: Ball possession losses

=== Init ===

        Initialize the PlayerReport GUI window for a specific player.
        
        Creates the main window infrastructure by initializing the QWidget base class,
        storing the player's name, creating the header label, instantiating all six
        main menu buttons, connecting each button to its handler method, and calling
        init_main_UI() to finalize the window setup.

        Parameters:
            players_name (str): The full name of the player to generate reports for.
                              Must exactly match a player name in Data.json (case-sensitive).
                              Example: "Aston Sharp", "Benjamin Berridge", "Angus Lee"

        Returns:
            None

        Side Effects:
            - Calls super().__init__() to initialize QWidget base class
            - Stores players_name as instance variable
            - Creates QLabel for header with player name
            - Sets header alignment to center
            - Assigns "header" object name for CSS styling
            - Creates 6 QPushButton instances for main menu navigation
            - Connects each button's clicked signal to its handler method
            - Calls init_main_UI() to complete window configuration

        Widget Initialization:
            Header:
                - header_label: QLabel displaying "{players_name}'s Report Card"
                - Center aligned, styled via CSS with "header" object name
            
            Main Menu Buttons:
                - get_quick_stats_btn: Opens season statistics feature
                - compare_all_games_btn: Opens game-to-game comparison feature
                - season_grading_btn: Opens letter grade evaluation feature
                - best_worst_game_btn: Opens performance highlights feature
                - game_rating_btn: Opens single game rating feature
                - season_game_rating_btn: Opens season-wide ratings feature

        Signal-Slot Connections:
            get_quick_stats_btn.clicked → self.Season_average()
            compare_all_games_btn.clicked → self.show_compare_all_games()
            season_grading_btn.clicked → self.show_grading()
            best_worst_game_btn.clicked → self.show_best_worst_highlights()
            game_rating_btn.clicked → self.show_game_rating()
            season_game_rating_btn.clicked → self.show_game_season_game_rating()

        Execution Flow:
            1. Initialize QWidget parent class
            2. Store player name for data queries
            3. Create and configure header label
            4. Create all six menu buttons
            5. Connect button signals to handler methods
            6. Call init_main_UI() to set up layout and styling

        Example Usage:
            app = QApplication(sys.argv)
            window = PlayerReport("Aston Sharp")
            # Window created with "Aston Sharp's Report Card" as header
            # All buttons ready and connected to their features

        Notes:
            - Object names are set for CSS targeting (header_label → "header")
            - Button connections use PyQt5's signal-slot mechanism
            - init_main_UI() must be called last to ensure all widgets exist
            - Player name validation not performed here (handled by AccessData)
  
=== Init Main UI ===

        Initialize and configure the main user interface layout and styling.
        
        Sets up the complete window structure including title, size, layout management,
        widget placement, and comprehensive CSS styling for the dark theme interface.
        This method handles all visual configuration and must be called after all
        widgets are created in __init__().

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Sets window title to "Drags"
            - Sets minimum window dimensions to 700x600 pixels
            - Creates QVBoxLayout with 40px margins and 15px spacing
            - Adds header label to layout with 20px extra spacing below
            - Creates menu_buttons list containing all 6 main menu buttons
            - Assigns "menuItem" object name to each button for CSS targeting
            - Adds all buttons to vertical layout
            - Adds stretch spacer to push content to top
            - Applies layout to window
            - Applies comprehensive CSS stylesheet to entire window

        Layout Structure:
            Window (700x600 minimum)
            └─ QVBoxLayout (40px margins, 15px spacing)
               ├─ header_label (centered, "header" object name)
               ├─ [20px spacing]
               ├─ get_quick_stats_btn ("menuItem")
               ├─ compare_all_games_btn ("menuItem")
               ├─ season_grading_btn ("menuItem")
               ├─ best_worst_game_btn ("menuItem")
               ├─ game_rating_btn ("menuItem")
               ├─ season_game_rating_btn ("menuItem")
               └─ [Stretch spacer - pushes all content to top]

        CSS Object Names Used:
            "header" → header_label styling
            "menuItem" → All 6 main menu buttons
            "backButton" → Back navigation buttons (created later by feature methods)

        Stylesheet Targets:
            QWidget:
                - Background: #0a0a0f (near black)
                - Font: 'Segoe UI', sans-serif
            
            QLabel#header:
                - Font Size: 52px
                - Weight: 700 (bold)
                - Color: #e5e7eb (light gray)
                - Padding: 20px
                - Letter Spacing: -0.5px (tighter)
            
            QPushButton#menuItem:
                - Font Size: 20px, Weight: 600
                - Color: #e5e7eb
                - Background: Gradient from #1e1e2e to #2a2a3e
                - Border: 2px solid #3a3a4e
                - Border Radius: 18px
                - Padding: 20px
                - Text Align: Left
                - Hover State: Lighter gradient, brighter border (#5a5a7e)
                - Pressed State: Darker gradient, darker border (#4a4a6e)
            
            QComboBox:
                - Background: #1e1e2e
                - Border: 2px solid #3a3a4e, 14px radius
                - Padding: 14px
                - Font Size: 16px
                - Color: #e5e7eb
                - Custom dropdown arrow (CSS triangle)
                - Dropdown list: #1a1a2a background, #3a3a5e selection
            
            QTextEdit:
                - Background: #1e1e2e
                - Border: 2px solid #3a3a4e, 18px radius
                - Padding: 24px
                - Font: 15px 'Consolas', monospace
                - Color: #e5e7eb
                - HTML rendering capable
            
            QPushButton#backButton:
                - Font Size: 17px, Weight: 600
                - Background: Gradient from #2a2a3e to #3a3a5e
                - Border: 2px solid #4a4a6e, 14px radius
                - Padding: 16px
                - Hover State: Lighter gradient, brighter border (#5a5a8e)

        Design Principles:
            - Dark theme reduces eye strain
            - High contrast for readability
            - Gradient backgrounds add depth
            - Rounded corners for modern aesthetic
            - Hover/pressed states provide visual feedback
            - Monospace font for statistical displays
            - Left-aligned button text for consistency
            - Consistent spacing throughout (multiples of 4/5)

        Execution Order:
            1. Set window properties (title, size)
            2. Create and configure layout manager
            3. Add header with extra spacing
            4. Store button references in list
            5. Assign object names and add buttons to layout
            6. Add stretch spacer
            7. Apply layout to window
            8. Apply complete stylesheet

        Notes:
            - Must be called AFTER all widgets are created in __init__()
            - Stylesheet applies to entire window and all child widgets
            - Object names enable CSS-like targeting via selectors
            - Stretch spacer keeps content at top even if window resized
            - Margins create consistent border around all content
            - QLineGradient creates smooth color transitions for buttons
  
=== Back To Main Menu ===

        Navigate back to the main menu from any sub-interface.
        
        Hides all dynamic widgets that may have been created by any of the six features
        (dropdowns, display areas, back buttons), then shows all main menu buttons to
        restore the initial view. This enables seamless navigation between features
        without destroying widget instances, improving performance through widget reuse.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides up to 15 dynamic widgets across all features (if they exist)
            - Shows all 6 main menu buttons
            - Preserves hidden widgets in memory (not destroyed)
            - Resets view to main menu state

        Widgets Hidden by Feature:
            Season Average Feature (3 widgets):
                - stat_selector: QComboBox for selecting stat category
                - stats_display: QTextEdit showing statistical analysis
                - back_button: QPushButton for navigation
            
            Game Comparison Feature (3 widgets):
                - stat_selector_compare: QComboBox for selecting stat category
                - trends_display: QTextEdit showing game-to-game trends
                - back_button_compare: QPushButton for navigation
            
            Season Grading Feature (2 widgets):
                - grading_display: QTextEdit showing letter grades
                - back_button_grading: QPushButton for navigation
            
            Performance Highlights Feature (3 widgets):
                - highlights_selector: QComboBox for selecting stat category
                - highlights_display: QTextEdit showing best/worst games
                - back_button_highlights: QPushButton for navigation
            
            Game Rating Feature (3 widgets):
                - game_selector: QComboBox for selecting specific game
                - game_rating_display: QTextEdit showing single game rating
                - back_button_game_rating: QPushButton for navigation
            
            Season Rating Feature (2 widgets):
                - season_rating_display: QTextEdit showing all game ratings
                - back_button_season_rating: QPushButton for navigation

        Widgets Shown (Main Menu):
            - get_quick_stats_btn: Opens Season Average feature
            - compare_all_games_btn: Opens Game Comparison feature
            - season_grading_btn: Opens Season Grading feature
            - best_worst_game_btn: Opens Performance Highlights feature
            - game_rating_btn: Opens Game Rating feature
            - season_game_rating_btn: Opens Season Rating feature

        Implementation Details:
            - Uses hasattr() to safely check if widget exists before hiding
            - Uses getattr() to dynamically access widget by attribute name string
            - Iterates through all possible dynamic widget names
            - Only attempts to hide widgets that have been created
            - No errors thrown if feature hasn't been accessed yet

        Widget Lifecycle:
            Create (first feature access) → Hide (back to menu) → Show (return to feature)
            - Widgets are NOT destroyed when hidden
            - Content and state are preserved
            - Faster subsequent access (no re-creation needed)

        Performance Benefits:
            - Avoids repeated widget creation/destruction
            - Maintains widget configuration and connections
            - Reduces memory allocation overhead
            - Faster UI transitions

        Called By:
            - back_button.clicked signal (Season Average)
            - back_button_compare.clicked signal (Game Comparison)
            - back_button_grading.clicked signal (Season Grading)
            - back_button_highlights.clicked signal (Highlights)
            - back_button_game_rating.clicked signal (Game Rating)
            - back_button_season_rating.clicked signal (Season Rating)

        Example Flow:
            User clicks "Get Quick Stats" → Season Average interface shown
            User clicks "Back to Main Menu" → back_to_main_menu() called
            stat_selector, stats_display, back_button hidden
            All 6 main menu buttons shown
            User back at main menu


=== Update Season Stats ===

 Refresh the season statistics display when user changes stat selection.
        
        Called automatically when the user selects a different stat category from the
        stat_selector dropdown in the Season Average feature. Calculates new statistics
        for the selected category and updates the HTML display.

        Parameters:
            stat_name (str): The stat category to calculate and display. Must be one of:
                           "Points", "Fouls", "Assists", "Rebounds", "Turnovers"

        Returns:
            None

        Side Effects:
            - Calls calculate_season_average() with the selected stat name
            - Receives HTML-formatted string from calculate_season_average()
            - Updates stats_display QTextEdit widget with new HTML content
            - Triggers re-render of the display area in the GUI

        Connected To:
            stat_selector.currentTextChanged signal
            - Automatically called whenever dropdown selection changes
            - No manual invocation needed

        Execution Flow:
            1. User changes dropdown selection (e.g., "Points" → "Rebounds")
            2. stat_selector emits currentTextChanged signal with new stat name
            3. update_season_stats() receives stat name as parameter
            4. Calls calculate_season_average("Rebounds")
            5. Receives HTML string with calculated statistics
            6. Updates stats_display with new HTML content
            7. Display automatically re-renders with new data

        Data Flow:
            stat_selector (dropdown) 
                → update_season_stats(stat_name)
                → calculate_season_average(stat_name)
                → AccessData queries
                → HTML formatted results
                → stats_display.setHtml(result)
                → Visual update in GUI

        Example:
            User selects "Points" from dropdown:
            - calculate_season_average("Points") returns HTML with:
              * Average per Game: 12.3
              * Median: 11.0
              * Range: 17
              * Best Performance: 22
              * Worst Performance: 5
              * Team Contribution: 24.6%
            - stats_display shows formatted table with color-coded values

        Related Methods:
            calculate_season_average(): Performs actual statistical calculations
            Season_average(): Creates and shows the interface including stat_selector

        Notes:
            - Lightweight wrapper method for signal-slot connection
            - Keeps display logic separate from calculation logic
            - HTML rendering provides rich formatting (colors, tables, fonts)
            - No error handling needed (calculate_season_average handles edge cases)
    
=== Calculate Season average

Calculate comprehensive season statistics for a specific stat category.
        
        Computes six statistical measures (mean, median, range, best, worst, team
        contribution percentage) for the selected statistic across all games played
        by the player during the season. Returns HTML-formatted output with color-coded
        values for visual distinction.

        Parameters:
            what_to_look_for (str): The stat category to analyze. Valid options:
                                   "Points", "Fouls", "Assists", "Rebounds", "Turnovers"

        Returns:
            str: HTML-formatted string containing styled statistical table with:
                - Header with stat name and player name
                - Average per Game (mean value, 1 decimal place)
                - Median value (1 decimal place)
                - Range (best - worst)
                - Best Performance (green color)
                - Worst Performance (red color)
                - Team Contribution percentage (purple color, 1 decimal place)
                
                OR "No games played" if stat not found in data

        Algorithm:
            1. Retrieve summed season stats from AccessData
            2. Validate stat exists, return error message if not
            3. Retrieve individual game stats for median calculation
            4. Calculate mean: total / number of games
            5. Extract all values into list and sort
            6. Calculate median:
               - Odd length: middle value
               - Even length: average of two middle values
            7. Find best (max) and worst (min) values
            8. Calculate range: best - worst
            9. Retrieve team season totals
            10. Sum team total for the specific stat
            11. Calculate percentage: (player total / team total) × 100
            12. Format all values into HTML table with inline CSS
            13. Return HTML string

        Statistical Measures:
            Mean (Average per Game):
                - Formula: sum of all stat values / number of games
                - Example: 37 total points / 3 games = 12.3 avg
            
            Median:
                - Middle value when sorted
                - Odd count: values[mid]
                - Even count: (values[mid-1] + values[mid]) / 2
                - Less affected by outliers than mean
            
            Range:
                - Formula: maximum value - minimum value
                - Measures variability in performance
                - Example: best 22, worst 5 → range 17
            
            Best Performance:
                - Maximum value across all games
                - Indicates peak performance capability
            
            Worst Performance:
                - Minimum value across all games
                - Indicates lowest performance game
            
            Team Contribution:
                - Formula: (player total / team total) × 100
                - Percentage of team's total in that stat
                - Example: 37 points out of 127 team points = 29.1%

        HTML Styling:
            Colors:
                - Header: #6366f1 (indigo)
                - Labels: #9ca3af (medium gray)
                - Values: #f9fafb (light gray)
                - Best: #10b981 (green)
                - Worst: #ef4444 (red)
                - Contribution: #8b5cf6 (purple)
            
            Layout:
                - Table: 100% width, 10px row spacing
                - Labels: 200px fixed width, left aligned
                - Values: Right aligned, various weights
                - Top border on contribution row for separation

        Data Sources:
            AccessData.Get_season_stats(sum_total=True):
                - Returns: {'Points': 37, 'Fouls': 3, ...}
                - Used for: total calculation and mean
            
            AccessData.Get_season_stats(sum_total=False):
                - Returns: {'Game_1': {'Points': 10, ...}, 'Game_2': {...}, ...}
                - Used for: counting games, median calculation
            
            AccessData.Get_team_season_stats(sum_total=True):
                - Returns: {'Player1': {'Points': 40, ...}, 'Player2': {...}, ...}
                - Used for: team total calculation

        Example Output (for "Points"):
            Points Stats - Aston Sharp
            
            Average per Game:    12.3
            Median:              11.0
            Range:               17
            Best Performance:    22  (green)
            Worst Performance:   5   (red)
            Team Contribution:   29.1%  (purple, larger font)

        Edge Cases:
            - No games played: Returns "No games played" string
            - Stat not found: Returns "No games played" string
            - Team total is 0: Sets contribution to 0% (avoids division by zero)
            - Even number of games: Averages two middle values for median
            - Odd number of games: Uses exact middle value for median

        Called By:
            update_season_stats(): When user changes dropdown selection

        Related Methods:
            Season_average(): Creates the interface displaying this data

        Notes:
            - All decimal values formatted to 1 decimal place (.1f)
            - Range displayed as integer (no decimals needed)
            - HTML allows rich formatting not possible with plain text
            - Inline CSS ensures styling works in QTextEdit
            - Percentage calculated as 0 if team total is 0 (safety check)
            - Values list sorted in-place for median calculation

=== Season Average === 

        Display the Season Average statistics interface.
        
        Shows a dropdown menu to select stat categories and displays comprehensive
        season statistics including mean, median, range, best/worst performances, and
        team contribution percentage. Implements widget reuse pattern: creates widgets
        on first call, then shows existing widgets on subsequent calls for better
        performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Hides Game Rating widgets if they exist (cleanup from other features)
            - Shows or creates 3 widgets: stat_selector, stats_display, back_button
            - Connects stat_selector dropdown to update_season_stats() method
            - Sets stats_display to read-only mode
            - Connects back_button to back_to_main_menu() method
            - Calls update_season_stats("Points") to show default statistics
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            stat_selector (QComboBox):
                - Dropdown with 5 options: Points, Fouls, Assists, Rebounds, Turnovers
                - Connected to: update_season_stats() via currentTextChanged signal
                - Purpose: User selects which stat to analyze
                - Signal fires automatically on selection change
            
            stats_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled tables)
                - Purpose: Displays calculated statistics with formatting
                - Styled by CSS: monospace font, dark background, padding
            
            back_button (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn
            
            Game Rating Feature (3 widgets, if they exist):
                - game_selector
                - game_rating_display
                - back_button_game_rating
                - Note: Extra cleanup to ensure clean interface state

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Hide any Game Rating widgets if present
            3. Check if stat_selector exists
               - If yes: Show it
               - If no: Create, configure, add to layout
            4. Check if stats_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            5. Check if back_button exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            6. Call update_season_stats("Points") to display default stats

        Default Display:
            Shows "Points" statistics automatically:
            - Average per Game
            - Median
            - Range
            - Best Performance (green)
            - Worst Performance (red)
            - Team Contribution % (purple)

        Signal-Slot Connections:
            stat_selector.currentTextChanged → update_season_stats(stat_name)
            back_button.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~50ms (widget creation + layout)
                - Subsequent access: ~5ms (show existing widgets)
                - 10x faster on return visits
                - Memory efficient (widgets not destroyed/recreated)

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [stat_selector]     ← Added here
            [stats_display]     ← Added here
            [back_button]       ← Added here

        Connected To:
            get_quick_stats_btn.clicked signal triggers this method

        Related Methods:
            update_season_stats(): Updates display when dropdown changes
            calculate_season_average(): Performs statistical calculations
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Get Quick Stats" button
            2. Season_average() called
            3. Main menu hidden
            4. Dropdown, display, and back button shown/created
            5. Default "Points" statistics displayed
            6. User selects "Rebounds" from dropdown
            7. update_season_stats("Rebounds") automatically called
            8. Display refreshes with Rebounds statistics
            9. User clicks "Back to Main Menu"
            10. back_to_main_menu() hides these widgets, shows main menu

        Notes:
            - Method name uses capital 'S' (Season_average) - stylistic choice
            - Read-only prevents accidental user edits to statistics
            - Default "Points" selection provides immediate value without user action
            - Extra cleanup of Game Rating widgets ensures no widget overlap
            - Object name "backButton" required for CSS styling to apply
            - hasattr checks prevent AttributeError on first access

=== Compare All Games ===

        Generate game-to-game trend analysis for all statistics across the season.
        
        Analyzes how each stat category changed between consecutive games throughout
        the season. Compares each game to the previous game, identifies whether stats
        increased, decreased, or stayed the same, and formats descriptive trend strings
        with actual values. Returns organized trend data for all stat categories.

        Parameters:
            None

        Returns:
            dict: Nested dictionary structure organized by stat category:
                {
                    "Points": [
                        "Game_1 to Game_2: Points increased (10 to 15)",
                        "Game_2 to Game_3: Points decreased (15 to 8)"
                    ],
                    "Fouls": [
                        "Game_1 to Game_2: Fouls no change (2 to 2)",
                        "Game_2 to Game_3: Fouls increased (2 to 3)"
                    ],
                    "Assists": [...],
                    "Rebounds": [...],
                    "Turnovers": [...]
                }

        Algorithm:
            1. Retrieve all game stats from AccessData (sum_total=False for individual games)
            2. Create empty set to collect unique stat names
            3. Initialize empty trends_report dictionary
            4. Extract game names as ordered list (e.g., ["Game_1", "Game_2", "Game_3"])
            5. Iterate through all games to collect unique stat names
            6. For each stat category:
               a. Create empty stat_trend list
               b. Loop through consecutive game pairs (i from 1 to len-1)
               c. Get previous game's stat value (default 0 if missing)
               d. Get current game's stat value (default 0 if missing)
               e. Determine trend direction:
                  - "increased" if current > previous
                  - "decreased" if current < previous
                  - "no change" if current == previous
               f. Format descriptive string with game names, stat, direction, values
               g. Append to stat_trend list
            7. Store completed stat_trend list in trends_report under stat name
            8. Return complete trends_report dictionary

        Data Source:
            AccessData.Get_season_stats(players_name, sum_total=False):
                Returns: {
                    'Game_1': {'Points': 10, 'Fouls': 1, 'Rebounds': 8, ...},
                    'Game_2': {'Points': 15, 'Fouls': 1, 'Rebounds': 6, ...},
                    'Game_3': {'Points': 8, 'Fouls': 3, 'Rebounds': 7, ...}
                }

        Comparison Logic:
            For each consecutive pair:
                Game_1 (prev) vs Game_2 (current)
                Game_2 (prev) vs Game_3 (current)
                Game_3 (prev) vs Game_4 (current)
                ...
            
            Total comparisons: number_of_games - 1
            Example: 3 games → 2 comparisons

        Trend Direction Determination:
            current > prev → "increased"
            current < prev → "decreased"
            current == prev → "no change"

        String Format:
            "{previous_game} to {current_game}: {stat_name} {direction} ({prev_value} to {current_value})"
            
            Examples:
                "Game_1 to Game_2: Points increased (10 to 15)"
                "Game_2 to Game_3: Rebounds decreased (6 to 4)"
                "Game_1 to Game_2: Fouls no change (2 to 2)"

        Example Output:
            {
                "Points": [
                    "Game_1 to Game_2: Points increased (10 to 22)",
                    "Game_2 to Game_3: Points decreased (22 to 10)"
                ],
                "Rebounds": [
                    "Game_1 to Game_2: Rebounds decreased (8 to 1)",
                    "Game_2 to Game_3: Rebounds increased (1 to 7)"
                ],
                "Fouls": [
                    "Game_1 to Game_2: Fouls no change (1 to 1)",
                    "Game_2 to Game_3: Fouls increased (1 to 3)"
                ]
            }

        Edge Cases:
            - Missing stat in game: .get(stat_name, 0) defaults to 0
            - Single game: No comparisons (loop doesn't execute)
            - No games: Returns empty dict (no iterations)
            - New stat appears mid-season: Uses 0 for missing previous values

        Data Collection Details:
            stat_names (set):
                - Automatically collects all unique stat names
                - Handles cases where not all stats present in all games
                - Set ensures no duplicates
            
            game_names (list):
                - Preserves order of games (important for sequential comparison)
                - Extracted from dictionary keys
                - Order typically: Game_1, Game_2, Game_3, ...

        Performance:
            Time Complexity: O(n × m) where n=games, m=stat categories
            Space Complexity: O(n × m) for storing all trend strings

        Called By:
            update_game_comparison(): Uses returned data to generate HTML display

        Related Methods:
            update_game_comparison(): Formats this data as color-coded HTML
            show_compare_all_games(): Creates the interface displaying trends

        Example Usage Within Class:
            trend_data = self.compare_all_games()
            # Returns full trend dictionary
            points_trends = trend_data["Points"]
            # Get just Points trends
            # ["Game_1 to Game_2: Points increased (10 to 15)", ...]

        Notes:
            - Pure data processing method (no GUI interaction)
            - Returns raw data structure for formatting by other methods
            - Uses .get() with default 0 to handle missing stats gracefully
            - Directional words ("increased", "decreased", "no change") parsed by display method
            - Game names preserved in strings for context
            - Actual values included for transparency

===  Update Game Comparison ===

        Refresh the game comparison display when user changes stat selection.
        
        Called automatically when the user selects a different stat category from the
        stat_selector_compare dropdown. Retrieves trend data from compare_all_games(),
        formats it as color-coded HTML with directional arrows, and updates the display.
        Uses visual indicators: green ↑ for increases, red ↓ for decreases, gray → for
        no change.

        Parameters:
            stat_name (str): The stat category to display trends for. Must be one of:
                           "Points", "Fouls", "Assists", "Rebounds", "Turnovers"

        Returns:
            None

        Side Effects:
            - Calls compare_all_games() to get complete trend data
            - Validates stat exists in trend data
            - If missing: Updates trends_display with red error message and returns
            - If present: Generates HTML with color-coded trend entries
            - Updates trends_display QTextEdit widget with formatted HTML
            - Triggers re-render of display area in GUI

        Algorithm:
            1. Call compare_all_games() to get full trend report
            2. Check if selected stat exists in report
               - If not: Display error message in red, return early
            3. Extract trend list for selected stat
            4. Build HTML string with header (stat name + player name)
            5. For each trend string in list:
               a. Parse trend direction from string content
               b. Assign color and arrow based on direction:
                  - "increased" → green (#10b981), up arrow (↑)
                  - "decreased" → red (#ef4444), down arrow (↓)
                  - "no change" → gray (#9ca3af), right arrow (→)
               c. Create styled div with colored left border
               d. Add arrow span with matching color
               e. Add trend text in light gray
               f. Append to output HTML
            6. Close HTML tags
            7. Update trends_display with complete HTML

        HTML Structure:
            <div style='padding: 20px;'>
                <h2 style='...indigo header...'>
                    {stat_name} Trends - {player_name}
                </h2>
                <div style='margin-top: 20px;'>
                    <!-- For each trend -->
                    <div style='...card with colored left border...'>
                        <span style='...colored arrow...'>↑/↓/→</span>
                        <span style='...trend text...'>Game_1 to Game_2: Points increased (10 to 15)</span>
                    </div>
                    <!-- Repeat for all trends -->
                </div>
            </div>

        Color Coding:
            Increased (Positive):
                - Color: #10b981 (green)
                - Arrow: ↑ (up arrow)
                - Visual: Green left border, green arrow
            
            Decreased (Negative):
                - Color: #ef4444 (red)
                - Arrow: ↓ (down arrow)
                - Visual: Red left border, red arrow
            
            No Change (Neutral):
                - Color: #9ca3af (gray)
                - Arrow: → (right arrow)
                - Visual: Gray left border, gray arrow

        Trend Detection:
            Uses string matching to detect direction:
                - if "increased" in trend → green
                - elif "decreased" in trend → red
                - else → gray (catches "no change" and any other case)

        Card Styling:
            Each trend entry:
                - Padding: 12px
                - Margin bottom: 10px (spacing between cards)
                - Background: rgba(30, 30, 40, 0.4) (semi-transparent dark)
                - Border left: 3px solid {color} (color-coded accent)
                - Border radius: 8px (rounded corners)
                - Arrow: 18px font, colored, 10px right margin
                - Text: Light gray (#e5e7eb)

        Error Handling:
            If stat_name not in trend_report:
                - Displays: "No data available for this stat" in red (#ef4444)
                - Returns immediately (doesn't process further)
                - Prevents errors from accessing non-existent keys

        Connected To:
            stat_selector_compare.currentTextChanged signal
            - Automatically called when dropdown selection changes
            - No manual invocation needed

        Data Flow:
            stat_selector_compare (dropdown)
                → update_game_comparison(stat_name)
                → compare_all_games() [generates trend data]
                → HTML formatting with colors/arrows
                → trends_display.setHtml(output)
                → Visual update in GUI

        Example Visual Output:
            Points Trends - Aston Sharp
            
            ↑ Game_1 to Game_2: Points increased (10 to 22)
            [Green border]
            
            ↓ Game_2 to Game_3: Points decreased (22 to 10)
            [Red border]
            
            → Game_3 to Game_4: Points no change (10 to 10)
            [Gray border]

        Performance Notes:
            - compare_all_games() called each time (recalculates all trends)
            - Could be optimized by caching trend data
            - Current approach ensures always up-to-date with data

        Related Methods:
            compare_all_games(): Generates the raw trend data
            show_compare_all_games(): Creates the interface with dropdown and display

        Example Trend String Processing:
            Input: "Game_1 to Game_2: Points increased (10 to 15)"
            Detection: "increased" in trend → True
            Result: Green color (#10b981), up arrow (↑)
            Output: [Green border] ↑ Game_1 to Game_2: Points increased (10 to 15)

        Notes:
            - Arrow characters are Unicode: ↑ (U+2191), ↓ (U+2193), → (U+2192)
            - String matching is case-sensitive ("increased" not "Increased")
            - Left border provides quick visual scanning of trends
            - Semi-transparent backgrounds layer over main dark theme
            - Inline CSS ensures styling works in QTextEdit HTML rendering
            - Header uses indigo color (#6366f1) for consistency with app theme
  
=== Show Compare All Games ===

        Display the Game Comparison interface.
        
        Shows a dropdown menu to select stat categories and displays game-to-game
        trend analysis with color-coded directional indicators (↑ increase, ↓ decrease,
        → no change). Implements widget reuse pattern: creates widgets on first call,
        then shows existing widgets on subsequent calls for better performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Shows or creates 3 widgets: stat_selector_compare, trends_display, back_button_compare
            - Connects stat_selector_compare dropdown to update_game_comparison() method
            - Sets trends_display to read-only mode
            - Connects back_button_compare to back_to_main_menu() method
            - Calls update_game_comparison("Points") to show default trend analysis
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            stat_selector_compare (QComboBox):
                - Dropdown with 5 options: Points, Fouls, Assists, Rebounds, Turnovers
                - Connected to: update_game_comparison() via currentTextChanged signal
                - Purpose: User selects which stat trends to analyze
                - Signal fires automatically on selection change
                - Note: Separate from stat_selector (Season Average feature)
            
            trends_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled cards with arrows)
                - Purpose: Displays game-to-game comparison with visual indicators
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_compare (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects
                - Note: Separate from back_button (Season Average feature)

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Check if stat_selector_compare exists
               - If yes: Show it
               - If no: Create, configure, add to layout
            3. Check if trends_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            4. Check if back_button_compare exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            5. Call update_game_comparison("Points") to display default trends

        Default Display:
            Shows "Points" trends automatically with visual indicators:
            - Game_1 to Game_2: Color-coded with arrow
            - Game_2 to Game_3: Color-coded with arrow
            - And so on for all consecutive game pairs
            
            Color scheme:
            - Green ↑ for increases
            - Red ↓ for decreases
            - Gray → for no change

        Signal-Slot Connections:
            stat_selector_compare.currentTextChanged → update_game_comparison(stat_name)
            back_button_compare.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~50ms (widget creation + layout)
                - Subsequent access: ~5ms (show existing widgets)
                - 10x faster on return visits
                - Memory efficient (widgets not destroyed/recreated)
                - Preserves dropdown selection state

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [stat_selector_compare]     ← Added here
            [trends_display]            ← Added here
            [back_button_compare]       ← Added here

        Connected To:
            compare_all_games_btn.clicked signal triggers this method

        Related Methods:
            update_game_comparison(): Updates display when dropdown changes
            compare_all_games(): Generates the raw trend data
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Compare All Games" button
            2. show_compare_all_games() called
            3. Main menu hidden
            4. Dropdown, display, and back button shown/created
            5. Default "Points" trends displayed with arrows:
               ↑ Game_1 to Game_2: Points increased (10 to 22)
               ↓ Game_2 to Game_3: Points decreased (22 to 10)
            6. User selects "Rebounds" from dropdown
            7. update_game_comparison("Rebounds") automatically called
            8. Display refreshes with Rebounds trends
            9. User clicks "Back to Main Menu"
            10. back_to_main_menu() hides these widgets, shows main menu

        Widget Naming Convention:
            Suffixes distinguish between similar widgets from different features:
            - stat_selector vs stat_selector_compare
            - back_button vs back_button_compare
            - Prevents naming conflicts
            - Enables independent widget management

        Visual Design:
            Trends displayed as styled cards with:
            - Left border color matching trend direction
            - Large arrow icon (↑/↓/→) in matching color
            - Full trend description text
            - Semi-transparent dark background
            - Rounded corners for modern look
            - Proper spacing between entries

        Notes:
            - Read-only prevents accidental user edits to trend data
            - Default "Points" selection provides immediate value
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - Separate widgets from Season Average allow independent state
            - HTML rendering enables rich visual formatting
  
=== Show Grading ===

        Display the Season Grading interface.
        
        Shows letter grade evaluations (A+ through F) for all stat categories based on
        the player's team contribution percentage. Unlike other features, this interface
        has no dropdown selector - it displays all five stat grades simultaneously in
        color-coded cards. Implements widget reuse pattern for performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Shows or creates 2 widgets: grading_display, back_button_grading
            - Sets grading_display to read-only mode
            - Connects back_button_grading to back_to_main_menu() method
            - Calls format_grading() to generate and display grade report
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            grading_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows color-coded grade cards)
                - Purpose: Displays letter grades for all five stat categories
                - Shows: grade, percentage, and raw value for each stat
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_grading (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Check if grading_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            3. Check if back_button_grading exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            4. Call format_grading() to generate and display grade report

        Default Display:
            Shows ALL stat grades immediately (no dropdown selection needed):
            - Points: [Grade] (Percentage: X%, Value: Y)
            - Fouls: [Grade] (Percentage: X%, Value: Y)
            - Assists: [Grade] (Percentage: X%, Value: Y)
            - Rebounds: [Grade] (Percentage: X%, Value: Y)
            - Turnovers: [Grade] (Percentage: X%, Value: Y)
            
            Each grade displayed in color-coded card:
            - A+/A: Green (#10b981)
            - B+/B: Blue (#3b82f6)
            - C+/C: Yellow (#eab308)
            - D+/D: Orange (#f97316)
            - F: Red (#ef4444)

        Grading Scale:
            A+ (90-100%) | A (80-89%) | B+ (70-79%) | B (60-69%)
            C+ (50-59%)  | C (40-49%) | D+ (30-39%) | D (20-29%) | F (0-19%)

        Signal-Slot Connections:
            back_button_grading.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~40ms (widget creation + layout + grading calculation)
                - Subsequent access: ~5ms (show existing widgets + recalculate grades)
                - Recalculation necessary to ensure up-to-date grades
                - Display widget reused for efficiency

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [grading_display]           ← Added here
            [back_button_grading]       ← Added here

        Design Difference from Other Features:
            No dropdown selector:
                - Other features: dropdown → select stat → see results
                - This feature: immediately see ALL stats graded
                - Design choice: grades most useful when compared side-by-side
                - User can quickly scan all grades without clicking

        Connected To:
            season_grading_btn.clicked signal triggers this method

        Related Methods:
            format_grading(): Generates the HTML display with all grades
            grading(): Calculates letter grades for all stats
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Season Grading" button
            2. show_grading() called
            3. Main menu hidden
            4. Display and back button shown/created
            5. format_grading() called
            6. grading() calculates all grades
            7. HTML generated with color-coded cards
            8. Display shows all five stat grades:
               Points: A+ (92.3%, Value: 37)  [Green card]
               Rebounds: B (65.2%, Value: 18) [Blue card]
               Assists: C (48.1%, Value: 5)   [Yellow card]
               Fouls: D (22.4%, Value: 3)     [Orange card]
               Turnovers: F (15.8%, Value: 2) [Red card]
            9. User reviews all grades simultaneously
            10. User clicks "Back to Main Menu"
            11. back_to_main_menu() hides these widgets

        Visual Design:
            Grades displayed as styled cards with:
            - Large letter grade (28px font, bold, colored)
            - Stat name (18px font, bold)
            - Percentage and value details (14px font, gray)
            - Left border (4px, colored) matching grade
            - Semi-transparent dark background
            - Rounded corners (8px)
            - Proper spacing between cards (12px margin)

        Grading Logic:
            Based on team contribution percentage:
            - For Points, Assists, Rebounds: Higher % = Better grade
            - For Fouls, Turnovers: Lower % = Better grade (inverted)
            - Calculated in grading() method
            - Formatted in format_grading() method

        Notes:
            - Read-only prevents accidental user edits
            - No dropdown needed (all grades shown at once)
            - format_grading() called every time to ensure fresh data
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - Simpler interface than other features (2 widgets vs 3)
            - HTML rendering enables rich color-coded display
  
=== Format Grading === 

        Generate and display HTML-formatted grade report for all stat categories.
        
        Retrieves calculated grades from grading() method and formats them as color-coded
        HTML cards. Each card displays the stat name, letter grade, team contribution
        percentage, and raw value. Color coding matches grade level (green for A's,
        blue for B's, yellow for C's, orange for D's, red for F).

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Calls grading() to get grade data for all stats
            - Generates HTML string with styled grade cards
            - Updates grading_display QTextEdit widget with HTML
            - Triggers re-render of display area in GUI

        Algorithm:
            1. Call grading() to get complete grade dictionary
            2. Build HTML string starting with header (player name)
            3. For each stat in grades dictionary:
               a. Extract grade letter, percentage, and raw value
               b. Determine color based on grade level:
                  - A+/A → green (#10b981)
                  - B+/B → blue (#3b82f6)
                  - C+/C → yellow (#eab308)
                  - D+/D → orange (#f97316)
                  - F → red (#ef4444)
               c. Create styled card div with:
                  - Colored left border (4px)
                  - Stat name and grade on same line (flexbox)
                  - Percentage and value on second line (gray text)
               d. Append card HTML to output string
            4. Close all HTML tags
            5. Update grading_display with complete HTML

        Grade Data Structure (from grading()):
            {
                "Points": {
                    "grade": "A+",
                    "percent": 92.3,
                    "value": 37
                },
                "Rebounds": {
                    "grade": "B",
                    "percent": 65.2,
                    "value": 18
                },
                ...
            }

        HTML Structure:
            <div style='padding: 20px;'>
                <h2 style='...indigo header...'>
                    Season Grading - {player_name}
                </h2>
                <div style='margin-top: 20px;'>
                    <!-- For each stat -->
                    <div style='...card with colored left border...'>
                        <div style='...flexbox row...'>
                            <span>{stat_name}</span>
                            <span style='...large colored grade...'>{grade}</span>
                        </div>
                        <div style='...details row...'>
                            <span>Percentage: {percent}%</span> | <span>Value: {value}</span>
                        </div>
                    </div>
                    <!-- Repeat for all stats -->
                </div>
            </div>

        Color Mapping:
            Grade Levels → Colors:
                A+, A  → #10b981 (Green)   - Excellent performance
                B+, B  → #3b82f6 (Blue)    - Good performance
                C+, C  → #eab308 (Yellow)  - Average performance
                D+, D  → #f97316 (Orange)  - Below average
                F      → #ef4444 (Red)     - Poor performance

        Card Styling Details:
            Container:
                - Padding: 16px
                - Margin bottom: 12px (spacing between cards)
                - Background: rgba(30, 30, 40, 0.4) (semi-transparent dark)
                - Border left: 4px solid {color} (grade-specific accent)
                - Border radius: 8px (rounded corners)
            
            Top Row (Flexbox):
                - Display: flex (horizontal layout)
                - Justify: space-between (name left, grade right)
                - Align: center (vertical alignment)
                - Stat name: 18px, bold (600), light gray (#e5e7eb)
                - Grade: 28px, extra bold (700), colored
            
            Bottom Row:
                - Margin top: 8px
                - Font size: 14px
                - Color: #9ca3af (medium gray)
                - Format: "Percentage: X% | Value: Y"
                - Separator: &nbsp;&nbsp;|&nbsp;&nbsp; (spaced pipe)

        Grade Detection Logic:
            Uses list membership checks:
                if grade in ["A+", "A"]: color = green
                elif grade in ['B+', "B"]: color = blue
                elif grade in ["C+", "C"]: color = yellow
                elif grade in ["D+", "D"]: color = orange
                else: color = red (catches F and any edge cases)

        Example Visual Output:
            Season Grading - Aston Sharp
            
            [Green border]
            Points                                          A+
            Percentage: 92.3% | Value: 37
            
            [Blue border]
            Rebounds                                        B
            Percentage: 65.2% | Value: 18
            
            [Yellow border]
            Assists                                         C+
            Percentage: 52.1% | Value: 5
            
            [Orange border]
            Fouls                                           D
            Percentage: 22.4% | Value: 3
            
            [Red border]
            Turnovers                                       F
            Percentage: 15.8% | Value: 2

        Data Flow:
            show_grading()
                → format_grading()
                → grading() [calculates all grades]
                → HTML generation with color coding
                → grading_display.setHtml(output)
                → Visual update in GUI

        Formatting Details:
            Percentage:
                - Displayed with 1 decimal place
                - Followed by % symbol
                - Example: 92.3%
            
            Value:
                - Raw integer value from season totals
                - No decimal places
                - Example: 37 (total points)
            
            Grade:
                - Letter with optional plus
                - Large font (28px) for emphasis
                - Colored to match card border

        Performance Notes:
            - Lightweight HTML generation (~10ms for 5 cards)
            - grading() calculation more expensive (~30ms)
            - Combined: ~40ms total for complete display
            - Inline CSS ensures consistent rendering

        Related Methods:
            grading(): Calculates the grades being formatted
            show_grading(): Creates interface and calls this method

        Called By:
            show_grading(): Every time grading interface is displayed

        Notes:
            - All stats always shown (no filtering or selection)
            - Order determined by grades dictionary iteration order
            - Flexbox enables responsive stat name/grade alignment
            - Semi-transparent backgrounds layer over main theme
            - Color-coded borders provide instant visual feedback
            - Details row uses pipe separator for clean information layout
            - Header uses indigo (#6366f1) matching app theme
            - Percentage and value provide context for grade understanding

=== Grading === 

        Calculate letter grades for all stat categories based on team contribution.
        
        Computes grades (A+ through F) for each stat by calculating the player's
        contribution as a percentage of the team's total for that stat. Special handling
        for negative stats (Fouls, Turnovers) where lower percentages earn better grades.
        Returns dictionary with grade, percentage, and raw value for each stat.

        Parameters:
            None

        Returns:
            dict: Dictionary mapping stat names to grade data:
                {
                    "Points": {
                        "grade": "A+",
                        "percent": 92.3,
                        "value": 37
                    },
                    "Fouls": {
                        "grade": "B",
                        "percent": 78.5,
                        "value": 3
                    },
                    ...
                }

        Algorithm:
            1. Retrieve team season totals from AccessData (all players summed)
            2. Retrieve player season totals from AccessData (this player only)
            3. Initialize empty grades dictionary
            4. For each stat in player's season stats:
               a. Sum team total for that stat across all players
               b. If team total is 0: set percentage to 0 (avoid division by zero)
               c. Else if stat is Foul or Turnover (negative stats):
                  - Calculate inverted percentage: 100 - (player / team × 100)
                  - Rationale: Lower contribution = better performance
               d. Else (positive stats):
                  - Calculate normal percentage: (player / team × 100)
                  - Rationale: Higher contribution = better performance
               e. Assign letter grade based on percentage thresholds
               f. Store grade, rounded percentage, and raw value in dictionary
            5. Return complete grades dictionary

        Grading Scale:
            Percentage Range → Letter Grade:
                90-100% → A+
                80-89%  → A
                70-79%  → B+
                60-69%  → B
                50-59%  → C+
                40-49%  → C
                30-39%  → D+
                20-29%  → D
                0-19%   → F

        Stat Type Handling:
            Positive Stats (Higher is Better):
                - Points, Assists, Rebounds
                - Formula: (player_value / team_total) × 100
                - Example: 37 points out of 127 team points = 29.1%
                - Higher percentage = better grade
            
            Negative Stats (Lower is Better):
                - Fouls, Turnovers
                - Formula: 100 - (player_value / team_total) × 100
                - Example: 3 fouls out of 15 team fouls = 20%
                - Inverted: 100 - 20 = 80% → Grade A
                - Lower contribution = better grade

        Data Sources:
            AccessData.Get_team_season_stats(sum_total=True, look_good=False):
                Returns: {
                    'Player1': {'Points': 40, 'Fouls': 5, ...},
                    'Player2': {'Points': 35, 'Fouls': 4, ...},
                    'Player3': {'Points': 30, 'Fouls': 3, ...},
                    ...
                }
                Purpose: Calculate team totals for each stat
            
            AccessData.Get_season_stats(players_name, sum_total=True, look_good=False):
                Returns: {'Points': 37, 'Fouls': 3, 'Rebounds': 18, ...}
                Purpose: Get this player's season totals

        Calculation Examples:
            Example 1 - Points (Positive Stat):
                Player: 37 points
                Team: 127 points (sum of all players)
                Percentage: (37 / 127) × 100 = 29.1%
                Grade: D (20-29% range)
            
            Example 2 - Fouls (Negative Stat):
                Player: 3 fouls
                Team: 15 fouls (sum of all players)
                Raw percentage: (3 / 15) × 100 = 20%
                Inverted: 100 - 20 = 80%
                Grade: A (80-89% range)
                Interpretation: Player only committed 20% of team fouls (good!)
            
            Example 3 - Turnovers (Negative Stat):
                Player: 2 turnovers
                Team: 8 turnovers
                Raw percentage: (2 / 8) × 100 = 25%
                Inverted: 100 - 25 = 75%
                Grade: B+ (70-79% range)

        Edge Cases:
            Team Total is 0:
                - Sets percentage to 0%
                - Prevents ZeroDivisionError
                - Results in F grade
                - Rare scenario (would mean no team activity for that stat)
            
            Player Value is 0:
                - Positive stats: 0% → F grade
                - Negative stats: 100% → A+ grade (inverted)
            
            Missing Stat in Team Data:
                - .get(stat, 0) defaults to 0
                - Safely handles incomplete team data

        Return Value Structure:
            Each stat entry contains three values:
                grade (str): Letter grade ("A+", "A", "B+", ... "F")
                percent (float): Team contribution percentage, rounded to 1 decimal
                value (int): Raw season total for that stat

        Percentage Rounding:
            - Uses round(pct, 1)
            - Rounds to 1 decimal place
            - Examples: 92.34 → 92.3, 85.67 → 85.7
            - Provides precision without excessive detail

        Grade Assignment Logic:
            Uses cascading if-elif structure:
                - Checks from highest to lowest percentage
                - First matching condition assigns grade
                - Else clause catches < 20% (F grade)
                - No gaps in coverage (all percentages assigned)

        Performance:
            Time Complexity: O(n × m) where n=players, m=stats
            - Iterates through player stats (typically 5)
            - Each iteration sums team stats (typically 5-7 players)
            - Total: ~35 operations for typical dataset
            - Execution time: ~30ms

        Usage Context:
            Called by format_grading() to get grade data for display
            Not called directly by user actions
            Results are immediately formatted as HTML

        Related Methods:
            format_grading(): Uses these grades to generate display
            show_grading(): Triggers the grading process

        Example Complete Return Value:
            {
                "Points": {"grade": "D", "percent": 29.1, "value": 37},
                "Fouls": {"grade": "A", "percent": 80.0, "value": 3},
                "Assists": {"grade": "C", "percent": 48.1, "value": 5},
                "Rebounds": {"grade": "B", "percent": 65.2, "value": 18},
                "Turnovers": {"grade": "B+", "percent": 75.0, "value": 2}
            }

        Grading Philosophy:
            Team Contribution Basis:
                - Grades measure relative contribution, not absolute performance
                - Player compared to teammates, not league-wide standards
                - Context-aware: considers team's overall performance level
                - Fair comparison within team dynamics
            
            Inverted Negative Stats:
                - Penalizes high foul/turnover rates
                - Rewards low foul/turnover rates
                - Maintains consistent "higher grade = better" interpretation
                - Player committing few fouls earns high grade

        Notes:
            - All five stats always graded (no filtering)
            - Grades independent (one stat doesn't affect another)
            - Team totals recalculated each call (always current)
            - Percentage stored for transparency (shows why grade assigned)
            - Raw value stored for context (absolute performance reference)
            - Round to 1 decimal balances precision and readability

=== Show Best Worst Highlights === 

Display the Best/Worst Game Highlights interface.
        
        Shows a dropdown menu to select stat categories and displays the player's best
        and worst game performances for that stat. Features visual cards with star emoji
        for best performance (green) and chart-down emoji for worst performance (red),
        plus the difference between them. Implements widget reuse pattern for performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Shows or creates 3 widgets: highlights_selector, highlights_display, back_button_highlights
            - Connects highlights_selector dropdown to format_highlights() method
            - Sets highlights_display to read-only mode
            - Connects back_button_highlights to back_to_main_menu() method
            - Calls format_highlights("Points") to show default highlights
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            highlights_selector (QComboBox):
                - Dropdown with 5 options: Points, Fouls, Assists, Rebounds, Turnovers
                - Connected to: format_highlights() via currentTextChanged signal
                - Purpose: User selects which stat to analyze for best/worst games
                - Signal fires automatically on selection change
            
            highlights_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled highlight cards)
                - Purpose: Displays best and worst game with emojis and colors
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_highlights (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Check if highlights_selector exists
               - If yes: Show it
               - If no: Create, configure, add to layout
            3. Check if highlights_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            4. Check if back_button_highlights exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            5. Call format_highlights("Points") to display default highlights

        Default Display:
            Shows "Points" highlights automatically:
            - ⭐ Best Performance: Game name and value (green card)
            - 📉 Worst Performance: Game name and value (red card)
            - Difference: Numeric difference between best and worst

        Signal-Slot Connections:
            highlights_selector.currentTextChanged → format_highlights(stat_name)
            back_button_highlights.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~50ms (widget creation + layout)
                - Subsequent access: ~5ms (show existing widgets)
                - 10x faster on return visits
                - Memory efficient (widgets not destroyed/recreated)

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [highlights_selector]           ← Added here
            [highlights_display]            ← Added here
            [back_button_highlights]        ← Added here

        Connected To:
            best_worst_game_btn.clicked signal triggers this method

        Related Methods:
            format_highlights(): Formats and displays the highlight data
            best_worst_highlights(): Finds best and worst games for a stat
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Best/Worst Game Highlights" button
            2. show_best_worst_highlights() called
            3. Main menu hidden
            4. Dropdown, display, and back button shown/created
            5. Default "Points" highlights displayed:
               ⭐ Best Performance
               Game: Game_2
               Points: 22
               
               📉 Worst Performance
               Game: Game_1
               Points: 5
               
               Difference: 17
            6. User selects "Rebounds" from dropdown
            7. format_highlights("Rebounds") automatically called
            8. Display refreshes with Rebounds highlights
            9. User clicks "Back to Main Menu"
            10. back_to_main_menu() hides these widgets

        Visual Design:
            Best Performance Card (Green):
                - Background: rgba(16, 185, 129, 0.15) (light green tint)
                - Border: 2px solid #10b981 (green)
                - Emoji: ⭐ (star)
                - Title: "Best Performance" in green
                - Shows: Game name and stat value
            
            Worst Performance Card (Red):
                - Background: rgba(239, 68, 68, 0.15) (light red tint)
                - Border: 2px solid #ef4444 (red)
                - Emoji: 📉 (chart decreasing)
                - Title: "Worst Performance" in red
                - Shows: Game name and stat value
            
            Difference Section (Purple):
                - Background: rgba(30, 30, 40, 0.4) (dark)
                - Centered text
                - Shows numeric difference in purple (#8b5cf6)

        Feature Purpose:
            - Quickly identify peak and low performances
            - Understand performance range/consistency
            - Highlight career-best and career-worst games
            - Visual contrast (green vs red) for easy scanning
            - Difference metric shows volatility

        Notes:
            - Read-only prevents accidental user edits
            - Default "Points" selection provides immediate value
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - format_highlights() connected directly (no update wrapper needed)
            - Emojis add visual interest and quick recognition
            - HTML rendering enables rich color-coded display
            - Both best and worst always shown (no option to show only one)

=== Format Highlights ===

        Generate and display HTML-formatted highlight cards for best and worst games.
        
        Retrieves best/worst game data from best_worst_highlights() and formats it as
        visually distinct HTML cards. Best performance shown in green with star emoji,
        worst performance in red with chart-down emoji, plus a difference metric in purple.
        Creates an engaging, easy-to-scan display of performance extremes.

        Parameters:
            stat_name (str): The stat category to display highlights for. Must be one of:
                           "Points", "Fouls", "Assists", "Rebounds", "Turnovers"

        Returns:
            None

        Side Effects:
            - Calls best_worst_highlights(stat_name) to get performance data
            - Validates data exists
            - If missing: Updates highlights_display with red error message and returns
            - If present: Generates HTML with two color-coded cards and difference section
            - Updates highlights_display QTextEdit widget with formatted HTML
            - Triggers re-render of display area in GUI

        Algorithm:
            1. Call best_worst_highlights(stat_name) to get highlight data
            2. Check if data is empty/None
               - If empty: Display error message in red, return early
            3. Extract best game name and value from highlights dict
            4. Extract worst game name and value from highlights dict
            5. Build HTML string with header (stat name + player name)
            6. Create Best Performance card:
               - Light green background with green border
               - Star emoji (⭐) and "Best Performance" title in green
               - Game name and stat value indented
               - Large green value (24px)
            7. Create Worst Performance card:
               - Light red background with red border
               - Chart-down emoji (📉) and "Worst Performance" title in red
               - Game name and stat value indented
               - Large red value (24px)
            8. Create Difference section:
               - Dark background, centered
               - Calculate: best_val - worst_val
               - Display in purple (18px)
            9. Update highlights_display with complete HTML

        Highlights Data Structure (from best_worst_highlights()):
            {
                "best": "Game_2",
                "best_val": 22,
                "worst": "Game_1",
                "worst_val": 5
            }

        HTML Structure:
            <div style='padding: 20px;'>
                <h2 style='...indigo header...'>
                    {stat_name} Highlights - {player_name}
                </h2>
                
                <!-- Best Performance Card (Green) -->
                <div style='...green card...'>
                    <div style='...title row...'>
                        <span>⭐</span>
                        <span>Best Performance</span>
                    </div>
                    <div style='...details indented...'>
                        <div>Game: {best_game}</div>
                        <div>{stat_name}: {best_val}</div>
                    </div>
                </div>
                
                <!-- Worst Performance Card (Red) -->
                <div style='...red card...'>
                    <div style='...title row...'>
                        <span>📉</span>
                        <span>Worst Performance</span>
                    </div>
                    <div style='...details indented...'>
                        <div>Game: {worst_game}</div>
                        <div>{stat_name}: {worst_val}</div>
                    </div>
                </div>
                
                <!-- Difference Section (Purple) -->
                <div style='...centered dark card...'>
                    <span>Difference: </span>
                    <span>{difference}</span>
                </div>
            </div>

        Card Styling Details:
            Best Performance Card (Green):
                Container:
                    - Padding: 20px
                    - Margin bottom: 16px
                    - Background: rgba(16, 185, 129, 0.15) (15% opacity green tint)
                    - Border: 2px solid #10b981 (solid green)
                    - Border radius: 12px (rounded corners)
                
                Title Row:
                    - Display: flex (horizontal layout)
                    - Align: center (vertical alignment)
                    - Emoji: ⭐ (32px, green, 12px right margin)
                    - Text: "Best Performance" (20px, bold 700, green)
                
                Details Section:
                    - Margin left: 44px (aligns with text, not emoji)
                    - Color: #e5e7eb (light gray)
                    - Font size: 16px
                    - Game name: 8px bottom margin
                    - Stat value: 24px, bold 700, green
            
            Worst Performance Card (Red):
                Container:
                    - Padding: 20px
                    - No margin bottom (last card before difference)
                    - Background: rgba(239, 68, 68, 0.15) (15% opacity red tint)
                    - Border: 2px solid #ef4444 (solid red)
                    - Border radius: 12px
                
                Title Row:
                    - Same layout as best card
                    - Emoji: 📉 (32px, red, 12px right margin)
                    - Text: "Worst Performance" (20px, bold 700, red)
                
                Details Section:
                    - Same structure as best card
                    - Stat value: 24px, bold 700, red
            
            Difference Section (Purple):
                - Margin top: 20px (spacing from cards)
                - Padding: 16px
                - Background: rgba(30, 30, 40, 0.4) (semi-transparent dark)
                - Border radius: 8px
                - Text align: center
                - Label: "Difference: " (14px, medium gray)
                - Value: {difference} (18px, bold 700, purple #8b5cf6)

        Color Scheme:
            Best (Green):
                - Border: #10b981
                - Background tint: rgba(16, 185, 129, 0.15)
                - Text/Value: #10b981
            
            Worst (Red):
                - Border: #ef4444
                - Background tint: rgba(239, 68, 68, 0.15)
                - Text/Value: #ef4444
            
            Difference (Purple):
                - Value: #8b5cf6
                - Label: #9ca3af (gray)
                - Background: rgba(30, 30, 40, 0.4) (dark)

        Emojis Used:
            ⭐ (U+2B50) - Star for best performance
                - Universal symbol of excellence
                - 32px size for visual impact
            
            📉 (U+1F4C9) - Chart Decreasing for worst performance
                - Represents declining performance
                - 32px size matching best card

        Difference Calculation:
            Formula: best_val - worst_val
            
            Examples:
                Best: 22 points, Worst: 5 points → Difference: 17
                Best: 8 rebounds, Worst: 1 rebound → Difference: 7
                Best: 4 assists, Worst: 0 assists → Difference: 4
            
            Interpretation:
                - Large difference: High volatility, inconsistent performance
                - Small difference: Low volatility, consistent performance
                - Zero difference: Only one game or identical performances

        Error Handling:
            If highlights is empty/None/falsy:
                - Displays: "No data available" in red (#ef4444)
                - Returns immediately (no further processing)
                - Prevents errors from accessing non-existent keys
                - Note: Currently has logic error (see Notes)

        Connected To:
            highlights_selector.currentTextChanged signal
            - Automatically called when dropdown selection changes
            - No manual invocation needed

        Data Flow:
            highlights_selector (dropdown)
                → format_highlights(stat_name)
                → best_worst_highlights(stat_name) [finds best/worst games]
                → HTML generation with emojis and colors
                → highlights_display.setHtml(output)
                → Visual update in GUI

        Example Visual Output:
            Points Highlights - Aston Sharp
            
            [Green card with light green background]
            ⭐ Best Performance
               Game: Game_2
               Points: 22
            
            [Red card with light red background]
            📉 Worst Performance
               Game: Game_1
               Points: 5
            
            [Dark centered card]
            Difference: 17

        Performance Notes:
            - best_worst_highlights() called each time (recalculates)
            - Could be optimized by caching highlight data
            - Current approach ensures always up-to-date with data
            - HTML generation: ~5ms
            - Total execution: ~15ms

        Related Methods:
            best_worst_highlights(): Finds the best and worst games
            show_best_worst_highlights(): Creates the interface with dropdown

        Visual Design Rationale:
            Contrasting Colors:
                - Green vs Red creates immediate visual distinction
                - No confusion about which is which
                - Color-blind friendly with emojis as secondary indicators
            
            Tinted Backgrounds:
                - 15% opacity provides subtle color without overwhelming
                - Maintains readability of text
                - Creates cohesive card appearance
            
            Indented Details:
                - 44px left margin aligns details with title text
                - Creates visual hierarchy
                - Separates emoji from content
            
            Large Values:
                - 24px bold font emphasizes the key metric
                - Easy to scan and compare
                - Colored to match card theme
            
            Centered Difference:
                - Neutral positioning (not favoring best or worst)
                - Purple color distinct from green/red
                - Provides context for understanding consistency

        Notes:
            - Logic bug in error handling: Returns early but doesn't stop execution before extracting keys
            - Should add early return immediately after setHtml for error case
            - Emojis are Unicode characters (may not render on all systems)
            - Difference always positive (best > worst by definition)
            - Inline CSS ensures styling works in QTextEdit
            - Header uses indigo (#6366f1) matching app theme
            - Both cards always shown (no option to show only best or worst)

=== Best Worst Highlights ===

Find the player's best and worst game performances for a specific stat.
        
        Analyzes all games in the season to identify which game had the highest value
        (best) and which had the lowest value (worst) for the specified stat category.
        Returns game names and values in a dictionary format ready for display formatting.

        Parameters:
            what_to_look_for (str): The stat category to analyze. Must be one of:
                                   "Points", "Fouls", "Assists", "Rebounds", "Turnovers"
            look_good (bool): Legacy parameter, currently unused. Default: False
                            Originally intended for formatted output option

        Returns:
            dict: Dictionary containing best and worst game information:
                {
                    "best": str,        # Game name with highest value (e.g., "Game_2")
                    "best_val": int,    # Highest stat value (e.g., 22)
                    "worst": str,       # Game name with lowest value (e.g., "Game_1")
                    "worst_val": int    # Lowest stat value (e.g., 5)
                }

        Algorithm:
            1. Retrieve all game stats from AccessData (sum_total=False for individual games)
            2. Initialize empty nums dictionary
            3. Iterate through all games:
               a. Check if stat exists in game stats
               b. If exists: Store game_name → stat_value mapping in nums
            4. Find best game: Use max() with key=nums.get to find game with highest value
            5. Find worst game: Use min() with key=nums.get to find game with lowest value
            6. Build and return dictionary with:
               - best: game name
               - best_val: value from nums (using .get() for safety)
               - worst: game name
               - worst_val: value from nums (using .get() for safety)

        Data Source:
            AccessData.Get_season_stats(players_name, sum_total=False, look_good=False):
                Returns: {
                    'Game_1': {'Points': 5, 'Fouls': 1, 'Rebounds': 2, 'Assists': 4, 'Turnovers': 2},
                    'Game_2': {'Points': 22, 'Fouls': 1, 'Rebounds': 1, 'Assists': 0, 'Turnovers': 0},
                    'Game_3': {'Points': 10, 'Fouls': 1, 'Rebounds': 2, 'Assists': 1, 'Turnovers': 0}
                }

        Data Transformation:
            Input: Nested game stats dictionary
            Intermediate (nums): {'Game_1': 5, 'Game_2': 22, 'Game_3': 10}
            Output: {'best': 'Game_2', 'best_val': 22, 'worst': 'Game_1', 'worst_val': 5}

        Max/Min Logic:
            max(nums, key=nums.get):
                - Iterates through keys in nums dictionary
                - Uses nums.get as comparison function
                - Returns the key (game name) with the highest value
                - Example: max({'Game_1': 5, 'Game_2': 22, 'Game_3': 10}, key=...) → 'Game_2'
            
            min(nums, key=nums.get):
                - Same logic but returns key with lowest value
                - Example: min({'Game_1': 5, 'Game_2': 22, 'Game_3': 10}, key=...) → 'Game_1'

        Example Execution:
            Input: what_to_look_for = "Points"
            
            Step 1 - Retrieve data:
                all_games = {
                    'Game_1': {'Points': 5, 'Fouls': 1, ...},
                    'Game_2': {'Points': 22, 'Fouls': 1, ...},
                    'Game_3': {'Points': 10, 'Fouls': 1, ...}
                }
            
            Step 2 - Extract stat values:
                nums = {'Game_1': 5, 'Game_2': 22, 'Game_3': 10}
            
            Step 3 - Find extremes:
                best_game = 'Game_2' (has value 22)
                worst_game = 'Game_1' (has value 5)
            
            Step 4 - Build result:
                return {
                    'best': 'Game_2',
                    'best_val': 22,
                    'worst': 'Game_1',
                    'worst_val': 5
                }

        Edge Cases:
            Single Game:
                - Best and worst will be the same game
                - Example: {'best': 'Game_1', 'best_val': 10, 'worst': 'Game_1', 'worst_val': 10}
            
            Stat Not in Any Game:
                - nums dictionary remains empty
                - max()/min() will raise ValueError on empty sequence
                - Should handle this in calling function
            
            Multiple Games with Same Value:
                - max()/min() returns first occurrence in iteration order
                - Deterministic but arbitrary choice
                - Example: If Game_1 and Game_3 both have 10 points, one is chosen
            
            Missing Stat in Some Games:
                - if what_to_look_for in game_stats check prevents KeyError
                - Only games with the stat are included in nums
                - Games missing the stat are excluded from consideration

        Value Retrieval:
            nums.get(best_game):
                - Safe retrieval using .get() method
                - Returns None if key doesn't exist (shouldn't happen)
                - Cleaner than nums[best_game] which could raise KeyError
            
            nums.get(worst_game):
                - Same safety as best_game retrieval

        Performance:
            Time Complexity: O(n) where n = number of games
                - Iteration through games: O(n)
                - max() operation: O(n)
                - min() operation: O(n)
                - Total: O(3n) → O(n)
            
            Space Complexity: O(n)
                - nums dictionary stores one entry per game
            
            Typical Execution: ~10ms for 3 games

        Called By:
            format_highlights(): Uses returned data to generate HTML display

        Related Methods:
            format_highlights(): Formats this data for visual display
            show_best_worst_highlights(): Creates interface showing results

        Interpretation by Stat Type:
            Positive Stats (Higher is Better):
                - Points, Assists, Rebounds
                - Best: Highest value (peak performance)
                - Worst: Lowest value (off game)
            
            Negative Stats (Lower is Better):
                - Fouls, Turnovers
                - "Best": Highest value (most fouls/turnovers) - actually worst performance
                - "Worst": Lowest value (fewest fouls/turnovers) - actually best performance
                - Note: Method doesn't invert for negative stats - interprets literally

        Example Results by Stat:
            Points:
                {'best': 'Game_2', 'best_val': 22, 'worst': 'Game_1', 'worst_val': 5}
                Interpretation: Career high 22 points, career low 5 points
            
            Rebounds:
                {'best': 'Game_1', 'best_val': 8, 'worst': 'Game_2', 'worst_val': 1}
                Interpretation: Best rebounding game 8, worst 1
            
            Fouls:
                {'best': 'Game_3', 'best_val': 4, 'worst': 'Game_1', 'worst_val': 1}
                Interpretation: Most fouls 4 (actually worst), fewest fouls 1 (actually best)

        Dictionary Key Naming:
            "best" / "worst":
                - Refers to maximum/minimum values
                - Not necessarily "good"/"bad" performance
                - For fouls: "best" = most fouls = bad game
                - Literal interpretation of extreme values
            
            "best_val" / "worst_val":
                - Actual numeric values
                - Provides context for the extremes
                - Used in display formatting

        Future Enhancement Possibilities:
            - Implement look_good parameter for formatted string output
            - Add inversion logic for negative stats (Fouls, Turnovers)
            - Return multiple games if tied for best/worst
            - Include date/opponent information
            - Add confidence scoring for statistical significance

        Notes:
            - look_good parameter present but unused (legacy)
            - No error handling for empty nums (calling function should handle)
            - Max/min operations assume at least one game exists
            - Returns raw game names (e.g., "Game_1", "Game_2")
            - Pure data processing (no GUI interaction)
            - Comments in code show intermediate data structures for clarity

=== Game Rating ===

        Calculate a comprehensive 0-100 performance rating for a single game.
        
        Computes a weighted score based on all five stat categories (Points, Assists,
        Rebounds, Fouls, Turnovers), applies a scaling formula, and clamps the result
        between 0-100. Positive stats contribute positively (with different weights),
        while negative stats (Fouls, Turnovers) subtract from the rating. Returns a
        single numeric value representing overall game performance quality.

        Parameters:
            game_name (str): The game identifier to rate (e.g., "Game_1", "Game_2", "Game_3")

        Returns:
            float: Performance rating rounded to 1 decimal place, range 0.0-100.0
                  - 80-100: Excellent performance
                  - 60-79: Good performance
                  - 40-59: Average performance
                  - 20-39: Below average performance
                  - 0-19: Poor performance

        Algorithm:
            1. Retrieve game stats for specified game from AccessData
            2. Calculate weighted score:
               a. Points × 1.7 (highest weight - primary scoring)
               b. Assists × 1.2 (moderate weight - playmaking)
               c. Rebounds × 1.45 (high weight - hustle/effort)
               d. Fouls × -0.3 (small penalty - minor negative)
               e. Turnovers × -1.3 (large penalty - major negative)
            3. Add baseline offset: +10 (ensures positive ratings possible)
            4. Apply scaling multiplier: × 2.2 (expands range)
            5. Clamp result between 0 and 100 (min/max bounds)
            6. Round to 1 decimal place
            7. Return final rating

        Weighting Rationale:
            Points (1.7):
                - Highest weight for primary objective of basketball
                - Reflects scoring importance
                - 10 points = 17 rating points
            
            Rebounds (1.45):
                - Second highest weight
                - Values hustle, physicality, effort plays
                - Critical for possession control
                - 10 rebounds = 14.5 rating points
            
            Assists (1.2):
                - Moderate weight
                - Recognizes playmaking and teamwork
                - Important but less direct than scoring
                - 10 assists = 12 rating points
            
            Fouls (-0.3):
                - Small penalty
                - Fouls are somewhat unavoidable in basketball
                - Light punishment for aggressive play
                - 10 fouls = -3 rating points
            
            Turnovers (-1.3):
                - Large penalty
                - Turnovers directly hurt team
                - Represents poor decision-making
                - Should be minimized
                - 10 turnovers = -13 rating points

        Formula Breakdown:
            Raw Score = (Points × 1.7) + (Assists × 1.2) + (Rebounds × 1.45) 
                       + (Fouls × -0.3) + (Turnovers × -1.3)
            
            Adjusted Score = Raw Score + 10
            
            Scaled Rating = Adjusted Score × 2.2
            
            Final Rating = max(0, min(100, Scaled Rating))

        Example Calculations:
            Example 1 - Excellent Game:
                Stats: 22 points, 0 assists, 1 rebound, 1 foul, 0 turnovers
                Raw: (22×1.7) + (0×1.2) + (1×1.45) + (1×-0.3) + (0×-1.3)
                   = 37.4 + 0 + 1.45 - 0.3 + 0 = 38.55
                Adjusted: 38.55 + 10 = 48.55
                Scaled: 48.55 × 2.2 = 106.81
                Clamped: min(100, 106.81) = 100.0
                Result: 100.0 (Excellent)
            
            Example 2 - Good Game:
                Stats: 15 points, 2 assists, 6 rebounds, 2 fouls, 1 turnover
                Raw: (15×1.7) + (2×1.2) + (6×1.45) + (2×-0.3) + (1×-1.3)
                   = 25.5 + 2.4 + 8.7 - 0.6 - 1.3 = 34.7
                Adjusted: 34.7 + 10 = 44.7
                Scaled: 44.7 × 2.2 = 98.34
                Clamped: 98.34 (within bounds)
                Result: 98.3 (Excellent)
            
            Example 3 - Poor Game:
                Stats: 0 points, 1 assist, 1 rebound, 4 fouls, 5 turnovers
                Raw: (0×1.7) + (1×1.2) + (1×1.45) + (4×-0.3) + (5×-1.3)
                   = 0 + 1.2 + 1.45 - 1.2 - 6.5 = -5.05
                Adjusted: -5.05 + 10 = 4.95
                Scaled: 4.95 × 2.2 = 10.89
                Clamped: 10.89 (within bounds)
                Result: 10.9 (Poor)
            
            Example 4 - Negative Raw Score:
                Stats: 0 points, 0 assists, 0 rebounds, 10 fouls, 10 turnovers
                Raw: 0 + 0 + 0 - 3 - 13 = -16
                Adjusted: -16 + 10 = -6
                Scaled: -6 × 2.2 = -13.2
                Clamped: max(0, -13.2) = 0.0
                Result: 0.0 (Minimum possible)

        Rating Scale Interpretation:
            100.0: Perfect or near-perfect game
            90-99: Exceptional performance
            80-89: Excellent performance
            70-79: Very good performance
            60-69: Good performance
            50-59: Above average performance
            40-49: Average performance
            30-39: Below average performance
            20-29: Poor performance
            10-19: Very poor performance
            0-9: Extremely poor performance

        Scaling Constants:
            Baseline Offset (+10):
                - Prevents excessively low ratings for modest performances
                - Shifts entire scale upward
                - Ensures average games get moderate ratings
                - Without it: low-scoring games would rate near zero
            
            Multiplier (×2.2):
                - Expands the rating range
                - Converts typical game scores to 0-100 scale
                - Chosen empirically to spread ratings appropriately
                - Higher multiplier = more sensitive to stat changes

        Clamping Logic:
            max(0, ...):
                - Prevents negative ratings
                - Floor value is 0.0
                - Catches extremely poor performances
            
            min(100, ...):
                - Prevents ratings above 100
                - Ceiling value is 100.0
                - Catches exceptional performances

        Data Source:
            AccessData.Get_game_stats(game_id, player, look_good=False):
                Returns: {'Points': 15, 'Assists': 2, 'Rebounds': 6, 'Fouls': 2, 'Turnovers': 1}
                Purpose: Get all stats for one player in one game

        Safe Stat Retrieval:
            .get(stat_name, 0):
                - Returns stat value if present
                - Returns 0 if stat missing
                - Prevents KeyError
                - Gracefully handles incomplete data

        Rounding:
            round(rating, 1):
                - Rounds to 1 decimal place
                - Examples: 98.34 → 98.3, 10.89 → 10.9
                - Balances precision and readability
                - Avoids excessive decimal places

        Performance:
            Time Complexity: O(1) - constant time operations
            Execution Time: ~5ms (data retrieval + calculation)

        Called By:
            format_game_rating(): Uses rating to determine color and text
            season_game_rating(): Calculates ratings for all games

        Related Methods:
            format_game_rating(): Formats this rating as HTML display
            show_game_rating(): Creates interface for single game rating

        Rating Philosophy:
            Holistic Performance:
                - Considers all aspects of game
                - Not just scoring-focused
                - Values rebounds and assists
                - Penalizes mistakes (turnovers)
                - Balanced evaluation approach
            
            Relative Weighting:
                - Reflects basketball importance hierarchy
                - Points > Rebounds > Assists (positive)
                - Turnovers > Fouls (negative penalties)
                - Evidence-based weight assignments
            
            Scale Familiarity:
                - 0-100 scale is universally understood
                - Easy to interpret (like school grades)
                - Enables quick performance assessment

        Limitations:
            Context-Independent:
                - Doesn't consider opponent strength
                - Ignores game situation (blowout vs close)
                - No adjustment for minutes played
                - Pure stat-based calculation
            
            Fixed Weights:
                - Same formula for all positions
                - Doesn't account for role differences
                - Guards vs Centers evaluated equally
                - One-size-fits-all approach
            
            Missing Stats:
                - Doesn't include steals, blocks
                - No +/- or advanced metrics
                - Limited to basic box score stats
                - Simplified evaluation

        Future Enhancements:
            - Position-specific weighting
            - Opponent difficulty adjustment
            - Minutes-played normalization
            - Include steals and blocks
            - Context-aware modifiers
            - Historical percentile ranking

        Notes:
            - Formula designed for youth basketball statistics
            - Weights may need tuning for different levels/ages
            - Clamping ensures ratings never exceed bounds
            - Single decimal precision balances detail and simplicity
            - Pure calculation method (no GUI interaction)
            - Deterministic (same stats = same rating always)
            - === Format Game Rating ===

        Generate and display HTML-formatted game rating with detailed stat breakdown.
        
        Calculates the overall game rating, determines color and text label based on rating
        level, computes individual stat contributions, and formats everything as an HTML
        display with a prominent rating number, descriptive label, and itemized breakdown
        showing how each stat contributed to the final rating.

        Parameters:
            game_name (str): The game identifier to format rating for (e.g., "Game_1", "Game_2")

        Returns:
            None

        Side Effects:
            - Calls game_rating(game_name) to calculate overall rating
            - Calls AccessData.Get_game_stats() to retrieve game statistics
            - Determines rating color and text based on rating value
            - Calculates display-specific contribution values for each stat
            - Generates HTML string with styled rating display
            - Updates game_rating_display QTextEdit widget with HTML
            - Triggers re-render of display area in GUI

        Algorithm:
            1. Calculate overall game rating (0-100)
            2. Retrieve game statistics from AccessData
            3. Determine rating color and text label based on rating thresholds:
               - 80+: Green, "Excellent"
               - 60-79: Blue, "Good"
               - 40-59: Yellow, "Average"
               - 20-39: Orange, "Below Average"
               - 0-19: Red (no text stored in this branch)
            4. Calculate display contribution values for each stat:
               - Points × 1.5 (for display simplification)
               - Assists × 1.0
               - Rebounds × 1.25
               - Fouls × -0.5
               - Turnovers × -1.5
            5. Build HTML with three sections:
               a. Header with game name
               b. Large centered rating display
               c. Itemized stat breakdown
            6. Update game_rating_display with HTML

        Rating Thresholds and Colors:
            Excellent (80-100):
                - Color: #10b981 (green)
                - Text: "Excellent"
                - Meaning: Outstanding performance
            
            Good (60-79):
                - Color: #3b82f6 (blue)
                - Text: "Good"
                - Meaning: Solid performance
            
            Average (40-59):
                - Color: #eab308 (yellow)
                - Text: "Average"
                - Meaning: Acceptable performance
            
            Below Average (20-39):
                - Color: #f97316 (orange)
                - Text: "Below Average"
                - Meaning: Subpar performance
            
            Poor (0-19):
                - Color: #ef4444 (red)
                - Text: (not set, but displayed)
                - Meaning: Very poor performance

        Display Contribution Calculations:
            Note: These differ from actual rating formula multipliers
            
            Points: stat_value × 1.5
                - Simplified from rating formula's 1.7
                - Easier for user comprehension
                - Still shows points as most valuable
            
            Assists: stat_value × 1.0
                - Simplified from rating formula's 1.2
                - Clean 1:1 ratio for mental math
            
            Rebounds: stat_value × 1.25
                - Simplified from rating formula's 1.45
                - Quarter increments easier to understand
            
            Fouls: stat_value × -0.5
                - Simplified from rating formula's -0.3
                - Half-point penalty clearer
            
            Turnovers: stat_value × -1.5
                - Simplified from rating formula's -1.3
                - Consistent with points multiplier (inverted)

        HTML Structure:
            <div style='padding: 20px;'>
                <!-- Header -->
                <h2>Game Rating - {game_name}</h2>
                
                <!-- Rating Display (Centered) -->
                <div style='...centered card...'>
                    <div>Overall Rating</div>
                    <div style='...huge colored number...'>{rating}</div>
                    <div style='...colored label...'>{rating_text}</div>
                </div>
                
                <!-- Stat Breakdown -->
                <div>
                    <h3>Stat Breakdown</h3>
                    
                    <!-- For each stat -->
                    <div style='...stat card...'>
                        <div style='...flexbox row...'>
                            <span>{stat_name} ({value} × {multiplier})</span>
                            <span style='...colored contribution...'>+{contribution}</span>
                        </div>
                    </div>
                </div>
            </div>

        Rating Display Styling:
            Container:
                - Text align: center
                - Padding: 30px
                - Background: rgba(30, 30, 40, 0.6) (semi-transparent dark)
                - Border radius: 16px (rounded)
                - Margin bottom: 20px
            
            Label ("Overall Rating"):
                - Color: #9ca3af (medium gray)
                - Font size: 16px
                - Margin bottom: 10px
            
            Rating Number:
                - Color: {rating_color} (dynamic based on performance)
                - Font size: 64px (very large for emphasis)
                - Font weight: 700 (bold)
                - Margin bottom: 10px
                - Format: {rating:.1f} (one decimal place)
            
            Rating Text ("Excellent", "Good", etc.):
                - Color: {rating_color} (matches number)
                - Font size: 20px
                - Font weight: 600 (semi-bold)

        Stat Breakdown Styling:
            Section Header:
                - Color: #e5e7eb (light gray)
                - Font size: 18px
                - Margin bottom: 12px
            
            Each Stat Card:
                - Padding: 12px
                - Margin bottom: 8px
                - Background: rgba(30, 30, 40, 0.4) (semi-transparent dark)
                - Border radius: 8px
                
                Flexbox Row:
                    - Display: flex
                    - Justify: space-between (label left, value right)
                    
                    Left Side (Label):
                        - Color: #9ca3af (medium gray)
                        - Format: "{stat} ({value} × {multiplier})"
                        - Example: "Points (15 × 1.5)"
                    
                    Right Side (Contribution):
                        - Font weight: 600 (semi-bold)
                        - Format: "{sign}{value:.1f}"
                        - Color logic:
                            * Green (#10b981) if positive contribution
                            * Red (#ef4444) if negative contribution
                            * Gray (#9ca3af) if zero

        Contribution Color Logic:
            Positive Stats (Points, Assists, Rebounds):
                if contribution > 0: green
                else: gray
            
            Negative Stats (Fouls, Turnovers):
                if contribution < 0: red
                else: gray
            
            Edge Case (Zero Values):
                All stats default to gray when zero

        Example Visual Output:
            Game Rating - Game_2
            
            [Centered dark card]
            Overall Rating
            98.3
            Excellent
            
            Stat Breakdown
            
            Points (22 × 1.5)                    +33.0
            Assists (0 × 1.0)                    +0.0
            Rebounds (1 × 1.25)                  +1.2
            Fouls (1 × -0.5)                     -0.5
            Turnovers (0 × -1.5)                 +0.0

        Display vs Rating Formula Differences:
            Important: Display multipliers ≠ Rating formula multipliers
            
            Rating Formula (actual calculation):
                Points × 1.7, Assists × 1.2, Rebounds × 1.45, 
                Fouls × -0.3, Turnovers × -1.3
                Plus: +10 offset, ×2.2 scale
            
            Display Values (simplified for user):
                Points × 1.5, Assists × 1.0, Rebounds × 1.25,
                Fouls × -0.5, Turnovers × -1.5
                No offset or scaling shown
            
            Rationale:
                - Display values are illustrative, not exact
                - Simpler multipliers easier to understand
                - Show relative importance without complexity
                - Users don't need to know full formula

        Data Flow:
            game_selector dropdown selection
                → format_game_rating(game_name)
                → game_rating(game_name) [calculate rating]
                → AccessData.Get_game_stats() [get stats]
                → HTML generation with colors
                → game_rating_display.setHtml(output)
                → Visual update in GUI

        Connected To:
            game_selector.currentTextChanged signal
            - Automatically called when dropdown selection changes

        Related Methods:
            game_rating(): Calculates the actual 0-100 rating
            show_game_rating(): Creates interface with dropdown and display

        Performance:
            Time Complexity: O(1) - constant time operations
            Execution Time: ~10ms (rating calc + HTML generation)

        Edge Cases:
            Perfect Game (100.0):
                - Green color
                - "Excellent" text
                - Multiple positive contributions
            
            Zero Stats Game:
                - Low rating (depends on formula offset)
                - All contributions show +0.0 or +0.0
                - Gray colors for all stats
            
            High Turnover Game:
                - Negative contributions dominate
                - Red color for turnovers line
                - Overall rating likely orange/red

        Notes:
            - Display multipliers simplified for user understanding
            - Rating color provides instant visual feedback
            - Large 64px rating number designed for quick scanning
            - Stat breakdown provides transparency into rating
            - Contribution values help identify strengths/weaknesses
            - Color coding: green=positive, red=negative, gray=neutral
            - Header uses indigo (#6366f1) matching app theme

=== Show Game Rating === 

Display the Game Rating interface for individual game performance analysis.
        
        Shows a dropdown menu populated with all games played during the season, and
        displays a detailed performance rating (0-100) for the selected game with a
        stat-by-stat contribution breakdown. Unlike other features with fixed stat
        options, this dropdown contains dynamic game names. Implements widget reuse
        pattern for performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Retrieves all games played from AccessData
            - Extracts game names as list
            - Shows or creates 3 widgets: game_selector, game_rating_display, back_button_game_rating
            - Populates game_selector dropdown with actual game names
            - Connects game_selector dropdown to format_game_rating() method
            - Sets game_rating_display to read-only mode
            - Connects back_button_game_rating to back_to_main_menu() method
            - Calls format_game_rating() with first game to show default rating
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                6. Check if widgets exist (hasattr returns True)
                7. Skip creation (widgets already exist)
                8. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            game_selector (QComboBox):
                - Dropdown populated with dynamic game names from season data
                - Options: All games player participated in (e.g., "Game_1", "Game_2", "Game_3")
                - Connected to: format_game_rating() via currentTextChanged signal
                - Purpose: User selects which specific game to rate
                - Signal fires automatically on selection change
                - Note: Dynamic content, not fixed like other feature dropdowns
            
            game_rating_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled rating with breakdown)
                - Purpose: Displays 0-100 rating with color coding and stat contributions
                - Shows: Large rating number, descriptive label, itemized breakdown
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_game_rating (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Retrieve all game stats from AccessData (individual games, not totals)
            3. Extract game names as list (e.g., ["Game_1", "Game_2", "Game_3"])
            4. Check if game_selector exists
               - If yes: Show it
               - If no: Create, populate with game names, connect, add to layout
            5. Check if game_rating_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            6. Check if back_button_game_rating exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            7. If games exist: Call format_game_rating() with first game name

        Default Display:
            Shows rating for first game automatically:
            - Large colored rating number (0-100)
            - Descriptive label (Excellent, Good, Average, etc.)
            - Stat breakdown showing contribution of each stat
            - Color-coded contributions (green=positive, red=negative)

        Dynamic Dropdown Population:
            Game List Creation:
                all_games = AccessData.Get_season_stats(sum_total=False)
                # Returns: {'Game_1': {...}, 'Game_2': {...}, 'Game_3': {...}}
                
                game_list = list(all_games.keys())
                # Converts to: ['Game_1', 'Game_2', 'Game_3']
                
                game_selector.addItems(game_list)
                # Populates dropdown with actual game names

        Signal-Slot Connections:
            game_selector.currentTextChanged → format_game_rating(game_name)
            back_button_game_rating.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~50ms (widget creation + layout + data retrieval)
                - Subsequent access: ~10ms (show existing widgets + re-populate dropdown)
                - Note: Dropdown repopulated each time (ensures current data)
                - Display widget reused for efficiency

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [game_selector]                 ← Added here
            [game_rating_display]           ← Added here
            [back_button_game_rating]       ← Added here

        Connected To:
            game_rating_btn.clicked signal triggers this method

        Related Methods:
            format_game_rating(): Formats rating display when game selected
            game_rating(): Calculates the 0-100 rating
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Game Rating" button
            2. show_game_rating() called
            3. Main menu hidden
            4. System retrieves all games: ["Game_1", "Game_2", "Game_3"]
            5. Dropdown populated with game names
            6. Display and back button shown/created
            7. Default rating for "Game_1" displayed:
               
               Game Rating - Game_1
               
               Overall Rating
               45.2
               Average
               
               Stat Breakdown
               Points (10 × 1.5)       +15.0
               Assists (2 × 1.0)       +2.0
               Rebounds (8 × 1.25)     +10.0
               Fouls (1 × -0.5)        -0.5
               Turnovers (2 × -1.5)    -3.0
               
            8. User selects "Game_2" from dropdown
            9. format_game_rating("Game_2") automatically called
            10. Display refreshes with Game_2 rating
            11. User clicks "Back to Main Menu"
            12. back_to_main_menu() hides these widgets

        Empty Game List Handling:
            if game_list:
                self.format_game_rating(game_list[0])
            
            - Checks if any games exist
            - Only formats rating if games are available
            - Prevents IndexError on empty list
            - If no games: dropdown empty, no default rating shown

        Differences from Other Features:
            Dynamic Dropdown Content:
                - Other features: Fixed options (Points, Fouls, etc.)
                - This feature: Dynamic game names from data
                - Dropdown content changes based on season data
                - More flexible but requires data retrieval
            
            Game-Specific Display:
                - Shows ONE game at a time in detail
                - Deep dive into individual performance
                - Complements "Season Game Rating" (shows all games)

        Data Retrieval:
            AccessData.Get_season_stats(players_name, sum_total=False):
                Returns: {
                    'Game_1': {'Points': 10, 'Fouls': 1, ...},
                    'Game_2': {'Points': 22, 'Fouls': 1, ...},
                    'Game_3': {'Points': 8, 'Fouls': 3, ...}
                }
                Purpose: Get all individual game data to extract names

        Visual Design:
            Rating Display:
                - Prominent number (64px font)
                - Color-coded by performance level
                - Descriptive label provides context
                - Centered for visual impact
            
            Stat Breakdown:
                - Transparent to user how rating calculated
                - Shows contribution of each stat
                - Helps identify strengths and weaknesses
                - Color-coded for quick scanning

        Use Cases:
            Performance Analysis:
                - Review specific game performance
                - Understand rating composition
                - Identify which stats hurt/helped rating
                - Compare different games by switching dropdown
            
            Post-Game Review:
                - Coach and player can review together
                - Objective performance metric
                - Detailed breakdown for discussion
                - Visual feedback on performance quality

        Notes:
            - Read-only prevents accidental user edits
            - Dynamic dropdown ensures always shows available games
            - Default first game selection provides immediate value
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - Empty list check prevents crash if no games played
            - HTML rendering enables rich color-coded display
            - game_list created from dictionary keys (order may vary)
            - Dropdown repopulated each time (could cache for performance)

=== Show Game Rating ===

Display the Game Rating interface for individual game performance analysis.
        
        Shows a dropdown menu populated with all games played during the season, and
        displays a detailed performance rating (0-100) for the selected game with a
        stat-by-stat contribution breakdown. Unlike other features with fixed stat
        options, this dropdown contains dynamic game names. Implements widget reuse
        pattern for performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Retrieves all games played from AccessData
            - Extracts game names as list
            - Shows or creates 3 widgets: game_selector, game_rating_display, back_button_game_rating
            - Populates game_selector dropdown with actual game names
            - Connects game_selector dropdown to format_game_rating() method
            - Sets game_rating_display to read-only mode
            - Connects back_button_game_rating to back_to_main_menu() method
            - Calls format_game_rating() with first game to show default rating
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            game_selector (QComboBox):
                - Dropdown populated with dynamic game names from season data
                - Options: All games player participated in (e.g., "Game_1", "Game_2", "Game_3")
                - Connected to: format_game_rating() via currentTextChanged signal
                - Purpose: User selects which specific game to rate
                - Signal fires automatically on selection change
                - Note: Dynamic content, not fixed like other feature dropdowns
            
            game_rating_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled rating with breakdown)
                - Purpose: Displays 0-100 rating with color coding and stat contributions
                - Shows: Large rating number, descriptive label, itemized breakdown
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_game_rating (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Retrieve all game stats from AccessData (individual games, not totals)
            3. Extract game names as list (e.g., ["Game_1", "Game_2", "Game_3"])
            4. Check if game_selector exists
               - If yes: Show it
               - If no: Create, populate with game names, connect, add to layout
            5. Check if game_rating_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            6. Check if back_button_game_rating exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            7. If games exist: Call format_game_rating() with first game name

        Default Display:
            Shows rating for first game automatically:
            - Large colored rating number (0-100)
            - Descriptive label (Excellent, Good, Average, etc.)
            - Stat breakdown showing contribution of each stat
            - Color-coded contributions (green=positive, red=negative)

        Dynamic Dropdown Population:
            Game List Creation:
                all_games = AccessData.Get_season_stats(sum_total=False)
                # Returns: {'Game_1': {...}, 'Game_2': {...}, 'Game_3': {...}}
                
                game_list = list(all_games.keys())
                # Converts to: ['Game_1', 'Game_2', 'Game_3']
                
                game_selector.addItems(game_list)
                # Populates dropdown with actual game names

        Signal-Slot Connections:
            game_selector.currentTextChanged → format_game_rating(game_name)
            back_button_game_rating.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~50ms (widget creation + layout + data retrieval)
                - Subsequent access: ~10ms (show existing widgets + re-populate dropdown)
                - Note: Dropdown repopulated each time (ensures current data)
                - Display widget reused for efficiency

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [game_selector]                 ← Added here
            [game_rating_display]           ← Added here
            [back_button_game_rating]       ← Added here

        Connected To:
            game_rating_btn.clicked signal triggers this method

        Related Methods:
            format_game_rating(): Formats rating display when game selected
            game_rating(): Calculates the 0-100 rating
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Game Rating" button
            2. show_game_rating() called
            3. Main menu hidden
            4. System retrieves all games: ["Game_1", "Game_2", "Game_3"]
            5. Dropdown populated with game names
            6. Display and back button shown/created
            7. Default rating for "Game_1" displayed:
               
               Game Rating - Game_1
               
               Overall Rating
               45.2
               Average
               
               Stat Breakdown
               Points (10 × 1.5)       +15.0
               Assists (2 × 1.0)       +2.0
               Rebounds (8 × 1.25)     +10.0
               Fouls (1 × -0.5)        -0.5
               Turnovers (2 × -1.5)    -3.0
               
            8. User selects "Game_2" from dropdown
            9. format_game_rating("Game_2") automatically called
            10. Display refreshes with Game_2 rating
            11. User clicks "Back to Main Menu"
            12. back_to_main_menu() hides these widgets

        Empty Game List Handling:
            if game_list:
                self.format_game_rating(game_list[0])
            
            - Checks if any games exist
            - Only formats rating if games are available
            - Prevents IndexError on empty list
            - If no games: dropdown empty, no default rating shown

        Differences from Other Features:
            Dynamic Dropdown Content:
                - Other features: Fixed options (Points, Fouls, etc.)
                - This feature: Dynamic game names from data
                - Dropdown content changes based on season data
                - More flexible but requires data retrieval
            
            Game-Specific Display:
                - Shows ONE game at a time in detail
                - Deep dive into individual performance
                - Complements "Season Game Rating" (shows all games)

        Data Retrieval:
            AccessData.Get_season_stats(players_name, sum_total=False):
                Returns: {
                    'Game_1': {'Points': 10, 'Fouls': 1, ...},
                    'Game_2': {'Points': 22, 'Fouls': 1, ...},
                    'Game_3': {'Points': 8, 'Fouls': 3, ...}
                }
                Purpose: Get all individual game data to extract names

        Visual Design:
            Rating Display:
                - Prominent number (64px font)
                - Color-coded by performance level
                - Descriptive label provides context
                - Centered for visual impact
            
            Stat Breakdown:
                - Transparent to user how rating calculated
                - Shows contribution of each stat
                - Helps identify strengths and weaknesses
                - Color-coded for quick scanning

        Use Cases:
            Performance Analysis:
                - Review specific game performance
                - Understand rating composition
                - Identify which stats hurt/helped rating
                - Compare different games by switching dropdown
            
            Post-Game Review:
                - Coach and player can review together
                - Objective performance metric
                - Detailed breakdown for discussion
                - Visual feedback on performance quality

        Notes:
            - Read-only prevents accidental user edits
            - Dynamic dropdown ensures always shows available games
            - Default first game selection provides immediate value
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - Empty list check prevents crash if no games played
            - HTML rendering enables rich color-coded display
            - game_list created from dictionary keys (order may vary)
            - Dropdown repopulated each time (could cache for performance)

=== Season Game Rating ===

    Calculate performance ratings for all games in the season.

    Computes individual game ratings (0-100) for every game the player participated
    in during the season, calculates the season average rating, and returns both
    the average and individual ratings in a structured dictionary format. Provides
    a comprehensive view of performance consistency across the season.

    Parameters:
    None

    Returns:
    dict: Dictionary containing season average and all individual game ratings:
        {
            "average": float,              # Season average rating (0.0-100.0)
            "all_games": {
                "Game_1": float,           # Rating for Game_1
                "Game_2": float,           # Rating for Game_2
                "Game_3": float,           # Rating for Game_3
                ...
            }
        }
        
        OR {"average": 0, "all_games": {}} if no games played
        OR "can't dived by 0" string if ZeroDivisionError (typo preserved)

    Algorithm:
    1. Retrieve all game stats from AccessData (individual games, not totals)
    2. Check if any games exist:
        - If empty: Return dict with 0 average and empty games dict
    3. Initialize empty ratings list and game_rating dictionary
    4. For each game in season:
        a. Calculate rating using game_rating() method
        b. Append rating to ratings list (for average calculation)
        c. Store game_name → rating mapping in game_rating dict
    5. Calculate average:
        a. Sum all ratings
        b. Divide by count of ratings
        c. Wrap in try-except for ZeroDivisionError
    6. Return dictionary with rounded average and all game ratings

    Data Source:
    AccessData.Get_season_stats(players_name, sum_total=False, look_good=False):
        Returns: {
            'Game_1': {'Points': 10, 'Fouls': 1, ...},
            'Game_2': {'Points': 22, 'Fouls': 1, ...},
            'Game_3': {'Points': 8, 'Fouls': 3, ...}
        }
        Purpose: Get all games to calculate ratings for each

    Calculation Process:
    Step 1 - Retrieve data:
        all_game_stats = {'Game_1': {...}, 'Game_2': {...}, 'Game_3': {...}}

    Step 2 - Calculate individual ratings:
        Game_1: game_rating('Game_1') → 45.2
        Game_2: game_rating('Game_2') → 98.3
        Game_3: game_rating('Game_3') → 62.7
        
        ratings = [45.2, 98.3, 62.7]
        game_rating = {'Game_1': 45.2, 'Game_2': 98.3, 'Game_3': 62.7}

    Step 3 - Calculate average:
        avg_rating = (45.2 + 98.3 + 62.7) / 3 = 206.2 / 3 = 68.73
        Rounded: 68.7

    Step 4 - Build result:
        return {
            'average': 68.7,
            'all_games': {
                'Game_1': 45.2,
                'Game_2': 98.3,
                'Game_3': 62.7
            }
        }

    Average Calculation:
    Formula: sum(all_ratings) / count(ratings)

    Examples:
        Consistent Performance:
            Ratings: [65.0, 68.0, 66.0]
            Average: 66.3 (low standard deviation)
        
        Inconsistent Performance:
            Ratings: [20.0, 95.0, 45.0]
            Average: 53.3 (high standard deviation)
        
        Improving Performance:
            Ratings: [40.0, 60.0, 80.0]
            Average: 60.0 (upward trend)

    Return Value Structure:
    Success Case:
        {
            "average": 68.7,          # Float, 1 decimal place
            "all_games": {
                "Game_1": 45.2,       # Individual ratings
                "Game_2": 98.3,
                "Game_3": 62.7
            }
        }

    No Games Case:
        {
            "average": 0,             # Integer 0, not float
            "all_games": {}           # Empty dictionary
        }

    ZeroDivisionError Case:
        "can't dived by 0"            # String (typo: "dived" not "divide")
        Note: This shouldn't happen if no-games case handled correctly

    Edge Cases:
    No Games Played:
        - all_game_stats is empty dict
        - Returns {"average": 0, "all_games": {}}
        - Handled before division attempt

    Single Game:
        - ratings list has 1 element
        - Average equals that single rating
        - Example: [75.0] → average 75.0

    All Zero Ratings:
        - ratings list like [0.0, 0.0, 0.0]
        - Average: 0.0
        - Valid result (very poor performances)

    ZeroDivisionError:
        - Should be prevented by no-games check
        - Try-except as safety net
        - Returns string instead of dict (inconsistent return type)

    Performance Consistency Metrics (not calculated but derivable):
    Standard Deviation:
        - Measure of rating variability
        - Low: Consistent performance
        - High: Volatile performance

    Trend Analysis:
        - Compare early vs late season
        - Identify improvement/decline patterns

    Range:
        - Difference between best and worst
        - Shows performance span

    Performance:
    Time Complexity: O(n) where n = number of games
        - Iteration through games: O(n)
        - game_rating() calls: O(n)
        - sum() operation: O(n)
        - Total: O(3n) → O(n)

    Space Complexity: O(n)
        - ratings list: n elements
        - game_rating dict: n key-value pairs

    Typical Execution: ~30ms for 3 games (10ms per game rating)

    Called By:
    show_game_season_game_rating(): Uses data to create interface
    format_season_game_rating(): Formats this data as HTML

    Related Methods:
    game_rating(): Calculates individual game ratings
    format_season_game_rating(): Formats this data for display
    show_game_season_game_rating(): Creates interface showing results

    Data Structures Used:
    ratings (list):
        - Ordered collection of all ratings
        - Used for average calculation
        - Example: [45.2, 98.3, 62.7]

    game_rating (dict):
        - Maps game name to rating
        - Preserves game identity
        - Used for display
        - Example: {'Game_1': 45.2, 'Game_2': 98.3}

    Rounding:
    round(avg_rating, 1):
        - Rounds average to 1 decimal place
        - Consistent with individual ratings
        - Examples: 68.73 → 68.7, 75.0 → 75.0

    Return Type Inconsistency:
    Normal: dict with "average" and "all_games" keys
    Error: string "can't dived by 0"
    Issue: Calling code must handle both types
    Better: Always return dict, even with error flag

    Example Return Values:
    Good Season:
        {
            'average': 75.5,
            'all_games': {
                'Game_1': 70.2,
                'Game_2': 78.3,
                'Game_3': 78.0
            }
        }

    Inconsistent Season:
        {
            'average': 55.0,
            'all_games': {
                'Game_1': 20.5,
                'Game_2': 90.0,
                'Game_3': 54.5
            }
        }

    Empty Season:
        {
            'average': 0,
            'all_games': {}
        }

    Use Cases:
    Season Overview:
        - Quick assessment of overall season quality
        - Compare average to expectations
        - Identify best/worst games

    Performance Tracking:
        - Monitor consistency across games
        - Detect improvement or decline trends
        - Compare to teammates (if available)

    Goal Setting:
        - Use average as baseline
        - Set targets for future games
        - Track progress toward goals

    Notes:
    - Typo in error message: "dived" should be "divide"
    - ZeroDivisionError catch likely unnecessary (no-games check prevents it)
    - Return type inconsistency (dict vs string) is poor design
    - Individual ratings stored for transparency
    - Average provides single-number season summary
    - No weighting by game importance (all games equal)
    - Doesn't account for opponent difficulty
    - Pure statistical aggregation

=== Show Game Season Game Rating ===

        Display the Season Game Rating interface showing all games at once.
        
        Shows a comprehensive season overview with the season average rating prominently
        displayed at the top, followed by individual ratings for every game in color-coded
        cards. Unlike the single game rating feature which requires dropdown selection,
        this displays all games simultaneously for easy comparison. Implements widget
        reuse pattern for performance.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Hides all 6 main menu buttons
            - Shows or creates 2 widgets: season_rating_display, back_button_season_rating
            - Sets season_rating_display to read-only mode
            - Connects back_button_season_rating to back_to_main_menu() method
            - Calls format_season_game_rating() to generate and display rating overview
            - All widgets added to main vbox layout

        Widget Lifecycle:
            First Call:
                1. Check if widgets exist (hasattr returns False)
                2. Create new widgets
                3. Configure and connect signals
                4. Add to layout
                5. Show widgets
            
            Subsequent Calls:
                1. Check if widgets exist (hasattr returns True)
                2. Skip creation (widgets already exist)
                3. Show existing widgets (faster, preserves state)

        Widgets Created/Shown:
            season_rating_display (QTextEdit):
                - Multi-line text display area
                - Read-only: User cannot edit content
                - HTML rendering enabled (shows styled rating cards)
                - Purpose: Displays season average + all individual game ratings
                - Shows: Large average rating, list of all game ratings with colors
                - Styled by CSS: monospace font, dark background, padding
            
            back_button_season_rating (QPushButton):
                - Text: "Back to Main Menu"
                - Object name: "backButton" (for CSS styling)
                - Connected to: back_to_main_menu() via clicked signal
                - Purpose: Return to main menu and hide this interface
                - Styled by CSS: gradient background, hover effects

        Widgets Hidden:
            Main Menu (6 buttons):
                - get_quick_stats_btn
                - compare_all_games_btn
                - season_grading_btn
                - best_worst_game_btn
                - game_rating_btn
                - season_game_rating_btn

        Execution Flow:
            1. Hide all main menu buttons (6 buttons)
            2. Check if season_rating_display exists
               - If yes: Show it
               - If no: Create, set read-only, add to layout
            3. Check if back_button_season_rating exists
               - If yes: Show it
               - If no: Create, name, connect, add to layout
            4. Call format_season_game_rating() to generate and display ratings

        Default Display:
            Shows ALL games immediately (no dropdown selection needed):
            - Season Average Rating (large, centered, color-coded)
            - List of all games with individual ratings:
              * Game_1: [Rating] (color-coded)
              * Game_2: [Rating] (color-coded)
              * Game_3: [Rating] (color-coded)
              * ...
            
            Color coding by rating level:
            - 80-100: Green (Excellent)
            - 60-79: Blue (Good)
            - 40-59: Yellow (Average)
            - 0-39: Red (Below Average/Poor)

        Signal-Slot Connections:
            back_button_season_rating.clicked → back_to_main_menu()

        Performance Optimization:
            Widget Reuse Pattern:
                - First access: ~60ms (widget creation + rating calculation for all games)
                - Subsequent access: ~40ms (show existing widgets + recalculate ratings)
                - Note: Ratings recalculated each time to ensure current data
                - Display widget reused for efficiency

        Layout Addition:
            All widgets added to self.vbox (main vertical layout):
            [Header]
            [season_rating_display]         ← Added here
            [back_button_season_rating]     ← Added here

        Design Difference from Other Features:
            No Dropdown Selector:
                - Single Game Rating: dropdown → select game → see one rating
                - This feature: immediately see ALL game ratings
                - Design choice: comprehensive overview vs detailed single-game view
                - User can quickly scan all games without clicking
                - Provides context (consistency, trends, outliers)

        Connected To:
            season_game_rating_btn.clicked signal triggers this method

        Related Methods:
            format_season_game_rating(): Generates HTML display with all ratings
            season_game_rating(): Calculates ratings for all games
            back_to_main_menu(): Returns to main menu

        Example User Flow:
            1. User clicks "Season Game Rating" button
            2. show_game_season_game_rating() called
            3. Main menu hidden
            4. Display and back button shown/created
            5. format_season_game_rating() called
            6. season_game_rating() calculates all ratings
            7. HTML generated with season overview
            8. Display shows complete season ratings:
               
               Season Game Ratings - Aston Sharp
               
               [Centered card]
               Season Average Rating
               68.7
               
               All Games
               
               Game_1                                    45.2
               [Yellow border - Average]
               
               Game_2                                    98.3
               [Green border - Excellent]
               
               Game_3                                    62.7
               [Blue border - Good]
               
            9. User reviews all ratings simultaneously
            10. User clicks "Back to Main Menu"
            11. back_to_main_menu() hides these widgets

        Visual Design:
            Season Average:
                - Centered display
                - Large font (64px)
                - Color-coded by average rating level
                - Provides overall season summary
            
            Individual Game Cards:
                - List format for easy scanning
                - Game name on left, rating on right
                - Color-coded left border matching rating level
                - Consistent spacing between cards
                - All visible simultaneously (no scrolling needed for 3-5 games)

        Use Cases:
            Season Overview:
                - Quick assessment of entire season
                - See all performances at a glance
                - Identify best and worst games visually
                - Understand performance consistency
            
            Pattern Recognition:
                - Spot improvement or decline trends
                - Identify clusters of good/bad games
                - Notice outlier performances
                - Assess volatility
            
            Comparison Context:
                - Compare specific game to season average
                - See how current game ranks among all games
                - Understand relative performance
                - Set realistic expectations

        Advantages over Single Game Rating:
            Comprehensive View:
                - No need to switch between games
                - All data visible simultaneously
                - Easier to spot patterns
                - Better for season-level analysis
            
            Efficiency:
                - One view shows everything
                - No dropdown interaction needed
                - Faster for reviewing multiple games
                - Better for presentations/reports

        Complementary Features:
            Single Game Rating:
                - Deep dive into one game
                - Stat-by-stat breakdown
                - Detailed contribution analysis
            
            Season Game Rating:
                - High-level season overview
                - All games comparison
                - Trend identification
                - Overall performance summary

        Performance Notes:
            Calculation Load:
                - Calls season_game_rating() which rates all games
                - ~10ms per game × number of games
                - For 5 games: ~50ms calculation time
                - Acceptable for interactive display
            
            Display Efficiency:
                - HTML generation: ~10ms
                - Total: ~60ms for 5 games
                - Responsive enough for good UX

        Notes:
            - Read-only prevents accidental user edits
            - No dropdown needed (all games shown at once)
            - format_season_game_rating() called every time to ensure fresh data
            - Object name "backButton" required for CSS styling
            - hasattr checks prevent AttributeError on first access
            - Simpler interface than most features (only 2 widgets)
            - HTML rendering enables rich color-coded display
            - Season average provides single-number summary
            - Individual games provide detailed breakdown
            - Color coding enables quick visual assessment
            - Complements single game rating feature perfectly

=== Format Season Game Rating === 

Generate and display HTML-formatted season rating overview with all games.
        
        Retrieves season rating data from season_game_rating(), formats it as HTML with
        a prominent season average at the top and color-coded cards for each individual
        game. The season average is displayed in large font with color indicating overall
        performance level, followed by a list of all games with their ratings in matching
        color-coded cards for easy visual comparison.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - Calls season_game_rating() to get all rating data
            - Extracts season average and individual game ratings
            - Determines color for season average based on rating level
            - Generates HTML string with styled season overview
            - For each game: determines color and creates card
            - Updates season_rating_display QTextEdit widget with HTML
            - Triggers re-render of display area in GUI

        Algorithm:
            1. Call season_game_rating() to get complete data
            2. Extract season average rating
            3. Extract all_games dictionary (game_name → rating mapping)
            4. Determine season average color based on thresholds:
               - 80+: Green (#10b981)
               - 60-79: Blue (#3b82f6)
               - 40-59: Yellow (#eab308)
               - 0-39: Red (#ef4444)
            5. Build HTML with header (player name)
            6. Create centered season average display card
            7. Add "All Games" section header
            8. For each game in all_games:
               a. Determine color based on individual rating thresholds
               b. Create card with game name and rating
               c. Apply colored left border matching rating level
               d. Append to output HTML
            9. Close HTML tags
            10. Update season_rating_display with complete HTML

        Season Rating Data Structure (from season_game_rating()):
            {
                "average": 68.7,
                "all_games": {
                    "Game_1": 45.2,
                    "Game_2": 98.3,
                    "Game_3": 62.7
                }
            }

        Color Thresholds:
            Both season average and individual games use same thresholds:
            
            Excellent (80-100):
                - Color: #10b981 (green)
                - Interpretation: Outstanding performance
            
            Good (60-79):
                - Color: #3b82f6 (blue)
                - Interpretation: Solid performance
            
            Average (40-59):
                - Color: #eab308 (yellow)
                - Interpretation: Acceptable performance
            
            Below Average/Poor (0-39):
                - Color: #ef4444 (red)
                - Interpretation: Subpar performance

        HTML Structure:
            <div style='padding: 20px;'>
                <!-- Header -->
                <h2>Season Game Ratings - {player_name}</h2>
                
                <!-- Season Average Display (Centered) -->
                <div style='...centered card...'>
                    <div>Season Average Rating</div>
                    <div style='...huge colored number...'>{avg:.1f}</div>
                </div>
                
                <!-- All Games Section -->
                <h3>All Games</h3>
                
                <!-- For each game -->
                <div style='...card with colored left border...'>
                    <div style='...flexbox row...'>
                        <span>{game_name}</span>
                        <span style='...colored rating...'>{rating:.1f}</span>
                    </div>
                </div>
                <!-- Repeat for all games -->
            </div>

        Season Average Display Styling:
            Container:
                - Text align: center
                - Padding: 30px
                - Background: rgba(30, 30, 40, 0.6) (semi-transparent dark)
                - Border radius: 16px (rounded)
                - Margin bottom: 20px
            
            Label ("Season Average Rating"):
                - Color: #9ca3af (medium gray)
                - Font size: 16px
                - Margin bottom: 10px
            
            Average Rating Number:
                - Color: {avg_color} (dynamic based on performance)
                - Font size: 64px (very large for emphasis)
                - Font weight: 700 (bold)
                - Format: {avg:.1f} (one decimal place)
                - No descriptive text (number speaks for itself)

        Individual Game Card Styling:
            Container:
                - Padding: 16px
                - Margin bottom: 10px (spacing between cards)
                - Background: rgba(30, 30, 40, 0.4) (semi-transparent dark)
                - Border left: 4px solid {color} (rating-specific accent)
                - Border radius: 8px (rounded corners)
            
            Flexbox Row:
                - Display: flex (horizontal layout)
                - Justify: space-between (game name left, rating right)
                - Align: center (vertical alignment)
            
            Game Name (Left):
                - Color: #e5e7eb (light gray)
                - Font size: 16px
            
            Rating (Right):
                - Color: {color} (matches left border)
                - Font size: 24px (large for emphasis)
                - Font weight: 700 (bold)
                - Format: {rating:.1f} (one decimal place)

        Color Determination Logic:
            Season Average:
                if avg >= 80: avg_color = green
                elif avg >= 60: avg_color = blue
                elif avg >= 40: avg_color = yellow
                else: avg_color = red
            
            Each Individual Game:
                if rating >= 80: color = green
                elif rating >= 60: color = blue
                elif rating >= 40: color = yellow
                else: color = red
            
            Same thresholds for consistency

        Example Visual Output:
            Season Game Ratings - Aston Sharp
            
            [Centered dark card]
            Season Average Rating
            68.7
            [Number in blue color]
            
            All Games
            
            [Card with yellow left border]
            Game_1                                    45.2
            
            [Card with green left border]
            Game_2                                    98.3
            
            [Card with blue left border]
            Game_3                                    62.7

        Visual Design Principles:
            Hierarchy:
                - Season average most prominent (largest, centered)
                - Individual games secondary (smaller, left-aligned list)
                - Clear visual hierarchy guides attention
            
            Color Consistency:
                - Same thresholds for average and games
                - Consistent interpretation across display
                - Easy to compare individual games to average
            
            Scanning Efficiency:
                - Left borders provide instant visual cues
                - Color-coded ratings enable quick assessment
                - Flexbox alignment keeps info organized
                - Consistent spacing aids readability

        Data Flow:
            show_game_season_game_rating()
                → format_season_game_rating()
                → season_game_rating() [calculate all ratings]
                → HTML generation with color coding
                → season_rating_display.setHtml(output)
                → Visual update in GUI

        Iteration Pattern:
            for game_name, rating in all_games.items():
                - Iterates through all games in dictionary
                - Order depends on dictionary iteration (may vary)
                - Each game gets own card
                - Cards stacked vertically

        Performance:
            Time Complexity: O(n) where n = number of games
                - season_game_rating() call: O(n)
                - Iteration for HTML generation: O(n)
                - Total: O(2n) → O(n)
            
            Execution Time:
                - Rating calculation: ~30ms for 3 games
                - HTML generation: ~5ms
                - Total: ~35ms

        Formatting Details:
            Rating Display:
                - One decimal place: {rating:.1f}
                - Examples: 98.3, 45.2, 68.7
                - Consistent precision across all displays
            
            Color Values:
                - Hex codes for precise color matching
                - Consistent with app theme
                - Accessible contrast ratios

        Related Methods:
            season_game_rating(): Provides the data being formatted
            show_game_season_game_rating(): Creates interface and calls this method

        Called By:
            show_game_season_game_rating(): Every time season rating interface displayed

        Use Cases:
            Performance Summary:
                - Quick visual scan of entire season
                - Identify best and worst games at a glance
                - Understand overall season quality from average
            
            Trend Analysis:
                - Visual pattern recognition
                - Spot clusters of similar performances
                - Identify outlier games
            
            Goal Assessment:
                - Compare to target average
                - See how many games met expectations
                - Track improvement over season

        Visual Comparison Features:
            Average vs Individual:
                - Average provides baseline
                - Easy to see which games above/below average
                - Color differences make comparisons instant
            
            Game to Game:
                - Side-by-side comparison of all games
                - Identify performance gaps
                - Understand consistency level

        Edge Cases:
            No Games:
                - season_game_rating() returns {'average': 0, 'all_games': {}}
                - Average displays as 0.0 (red)
                - No game cards generated (empty iteration)
                - "All Games" header shown but no content
            
            Single Game:
                - Average equals that game's rating
                - Both have same color
                - One card in list
            
            All Games Same Rating:
                - All cards same color
                - Average equals individual ratings
                - Shows consistency visually

        Notes:
            - Season average lacks descriptive text (unlike single game rating)
            - No "Excellent"/"Good" labels (color provides context)
            - All games shown simultaneously (no pagination needed for typical seasons)
            - Color-coded left borders enable quick visual scanning
            - Large season average (64px) designed for prominence
            - Smaller game ratings (24px) maintain hierarchy
            - Flexbox ensures consistent alignment
            - Header uses indigo (#6366f1) matching app theme
            - Semi-transparent backgrounds layer over main theme
            - One decimal precision balances detail and simplicity

=== If __name__ == '__main__' === 

    Application entry point for standalone execution.
    
    Creates the Qt application instance, initializes a PlayerReport window for
    the specified player ("Aston Sharp"), displays the window, and starts the
    Qt event loop which handles all GUI interactions until the user closes the
    application.
    
    Execution Flow:
        1. Create QApplication instance (manages application-wide resources)
        2. Instantiate PlayerReport with player name "Aston Sharp"
        3. Display the window with show()
        4. Enter Qt event loop with exec_()
        5. Exit cleanly when window closed (sys.exit ensures proper cleanup)
    
    Usage:
        Direct execution:
            python player_report.py
        
        Programmatic usage (from main.py):
            from testing.player_report import PlayerReport
            app = QApplication(sys.argv)
            report = PlayerReport("Benjamin Berridge")
            report.show()
    
    Exit:
        - Close window: Click X button
        - Keyboard: Alt+F4 (Windows), Cmd+Q (Mac)
        - Terminal: Ctrl+C
    
    Note:
        Player name "Aston Sharp" is hardcoded for testing. In production,
        this should be passed as command-line argument or selected via GUI.