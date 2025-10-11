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

=== PLAYER REPORT === 

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

=== INIT ===

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
  
=== INIT MAIN UI ===

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
  
=== BACK TO MAIN MENU ===

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