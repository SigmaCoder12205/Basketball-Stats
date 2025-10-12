import sys
"""System-specific parameters and functions for path manipulation and application control"""

import os
"""Operating system interface for file path operations and directory navigation"""

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Add parent directory to Python's module search path to enable local imports.
Resolves the path: testing/player_report.py → Drags/ → add to sys.path[0]
This allows importing utils.accessing_data without ModuleNotFoundError.
"""

from utils.accessing_data import AccessData
"""
Import the AccessData class which provides all data retrieval methods.
Acts as the intermediary between this GUI and the Data.json file.
Used extensively throughout PlayerReport for all statistical queries.
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QTextEdit,
                             QComboBox)
"""
Import PyQt5 GUI widgets:
- QApplication: Main application controller and event loop manager
- QWidget: Base widget class (parent of PlayerReport)
- QLabel: Display static text (headers, titles)
- QLineEdit: Single-line text input (imported but currently unused)
- QPushButton: Clickable buttons for menu navigation
- QVBoxLayout: Vertical layout manager for widget arrangement
- QTextEdit: Multi-line display with HTML rendering capability
- QComboBox: Dropdown menus for stat/game selection
"""

from PyQt5.QtCore import Qt
"""
Import Qt core module for constants and enums.
Used for: widget alignment (Qt.AlignCenter), object naming, and other Qt core functionality.
"""

class PlayerReport(QWidget):
    def __init__(self, players_name: str):
        super().__init__()
        self.players_name = players_name

        # Header
        self.header_label = QLabel(f"{self.players_name}'s Report Card")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setObjectName("header")

        # Buttons
        self.get_quick_stats_btn = QPushButton("Get Quick Stats")
        self.compare_all_games_btn = QPushButton("Compare All Games")
        self.season_grading_btn = QPushButton("Season Grading")
        self.best_worst_game_btn = QPushButton("Best/Worst Game Highlights")
        self.game_rating_btn = QPushButton("Game Rating")
        self.season_game_rating_btn = QPushButton("Season Game Rating")

        self.get_quick_stats_btn.clicked.connect(self.Season_average)
        self.compare_all_games_btn.clicked.connect(self.show_compare_all_games)
        self.season_grading_btn.clicked.connect(self.show_grading)
        self.best_worst_game_btn.clicked.connect(self.show_best_worst_highlights)
        self.game_rating_btn.clicked.connect(self.show_game_rating)
        self.season_game_rating_btn.clicked.connect(self.show_game_season_game_rating)

        self.init_main_UI()

    def init_main_UI(self):
        self.setWindowTitle("Drags")
        self.setMinimumSize(700, 600)

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(40, 40, 40, 40)
        self.vbox.setSpacing(15)

        # Header
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setObjectName("header")
        self.vbox.addWidget(self.header_label)
        self.vbox.addSpacing(20)

        # List of main menu buttons
        self.menu_buttons = [
            self.get_quick_stats_btn,
            self.compare_all_games_btn,
            self.season_grading_btn,
            self.best_worst_game_btn,
            self.game_rating_btn,
            self.season_game_rating_btn
        ]

        # Set object names and add buttons to layout
        for btn in self.menu_buttons:
            btn.setObjectName("menuItem")
            self.vbox.addWidget(btn)

        self.vbox.addStretch()
        self.setLayout(self.vbox)

        # Apply PyQt-compatible styling
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0f;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#header {
                font-size: 52px;
                font-weight: 700;
                color: #e5e7eb;
                padding: 20px;
                letter-spacing: -0.5px;
            }
            QPushButton#menuItem {
                font-size: 20px;
                font-weight: 600;
                color: #e5e7eb;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e1e2e, stop:1 #2a2a3e
                );
                border: 2px solid #3a3a4e;
                border-radius: 18px;
                padding: 20px;
                text-align: left;
            }
            QPushButton#menuItem:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2a3e, stop:1 #3a3a5e
                );
                border: 2px solid #5a5a7e;
            }
            QPushButton#menuItem:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2a, stop:1 #252535
                );
                border: 2px solid #4a4a6e;
            }
            QComboBox {
                background-color: #1e1e2e;
                border: 2px solid #3a3a4e;
                border-radius: 14px;
                padding: 14px;
                font-size: 16px;
                color: #e5e7eb;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #e5e7eb;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a2a;
                border: 2px solid #3a3a4e;
                selection-background-color: #3a3a5e;
                color: #e5e7eb;
                padding: 8px;
            }
            QTextEdit {
                background-color: #1e1e2e;
                border: 2px solid #3a3a4e;
                border-radius: 18px;
                padding: 24px;
                font-size: 15px;
                color: #e5e7eb;
                font-family: 'Consolas', monospace;
            }
            QPushButton#backButton {
                font-size: 17px;
                font-weight: 600;
                color: #e5e7eb;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2a3e, stop:1 #3a3a5e
                );
                border: 2px solid #4a4a6e;
                border-radius: 14px;
                padding: 16px;
            }
            QPushButton#backButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3a3a5e, stop:1 #4a4a7e
                );
                border: 2px solid #5a5a8e;
            }
        """)

                       
    def back_to_main_menu(self):
        # Hide dynamic widgets
        for attr in ["stat_selector", "stats_display", "back_button",
                    "stat_selector_compare", "trends_display", "back_button_compare",
                    "grading_display", "back_button_grading",
                    "highlights_selector", "highlights_display", "back_button_highlights", 
                    "game_selector", "game_rating_display", "back_button_game_rating",
                    "season_rating_display", "back_button_season_rating"]:
            if hasattr(self, attr):
                getattr(self, attr).hide()

        # Show main menu buttons again
        for btn in [self.get_quick_stats_btn, self.compare_all_games_btn,
                    self.season_grading_btn, self.best_worst_game_btn,
                    self.game_rating_btn, self.season_game_rating_btn]:
            btn.show()

    def update_season_stats(self, stat_name):
        result = self.calculate_season_average(stat_name)
        self.stats_display.setHtml(result)

    def calculate_season_average(self, what_to_look_for: str):
        sum_games_stats = AccessData.Get_season_stats(players_name=self.players_name, sum_total=True)

        if what_to_look_for not in sum_games_stats:
            return "No games played"
        
        all_games_stats = AccessData.Get_season_stats(players_name=self.players_name, sum_total=False)
        games_played = len(all_games_stats)

        mean_val = sum_games_stats[what_to_look_for] / games_played
        values = [game[what_to_look_for] for game in all_games_stats.values()]
        values.sort()
        mid = len(values) // 2
        median_val = values[mid] if len(values) % 2 != 0 else (values[mid - 1] + values[mid]) / 2 
        best_val = max(values)
        worst_val = min(values)
        range_val = best_val - worst_val
        team_stats = AccessData.Get_team_season_stats(sum_total=True, look_good=False)
        team_total = sum(player[what_to_look_for] for player in team_stats.values() if what_to_look_for in player) 
        percent = (sum_games_stats[what_to_look_for] / team_total * 100) if team_total > 0 else 0

        # HTML formatted output
        output = f"""
                <div style='padding: 20px;'>
                    <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; white-space: nowrap; font-size: 20px;'>
                        {what_to_look_for} Stats - {self.players_name}
                    </h2>
                    <table style='width: 100%; border-spacing: 0 10px;'>
                        <tr>
                            <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Average per Game:</td>
                            <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{mean_val:.1f}</td>
                        </tr>
                        <tr>
                            <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Median:</td>
                            <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{median_val:.1f}</td>
                        </tr>
                        <tr>
                            <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Range:</td>
                            <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{range_val}</td>
                        </tr>
                        <tr>
                            <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Best Performance:</td>
                            <td style='color: #10b981; font-weight: 700; text-align: right;'>{best_val}</td>
                        </tr>
                        <tr>
                            <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Worst Performance:</td>
                            <td style='color: #ef4444; font-weight: 700; text-align: right;'>{worst_val}</td>
                        </tr>
                        <tr style='border-top: 1px solid #374151;'>
                            <td style='color: #9ca3af; padding: 12px 0 0 0; width: 200px;'>Team Contribution:</td>
                            <td style='color: #8b5cf6; font-weight: 700; font-size: 18px; text-align: right; padding: 12px 0 0 0;'>{percent:.1f}%</td>
                        </tr>
                    </table>
                </div>
                """
        return output
    def Season_average(self):
        # Hide main menu buttons
        for attr in ["get_quick_stats_btn", "compare_all_games_btn", "season_grading_btn",
                    "best_worst_game_btn", "game_rating_btn", "season_game_rating_btn",
                    "game_selector", "game_rating_display", "back_button_game_rating"]:
            if hasattr(self, attr):
                getattr(self, attr).hide()


        if hasattr(self, "stat_selector"):
            self.stat_selector.show()
        if hasattr(self, "stats_display"):
            self.stats_display.show()
        if hasattr(self, "back_button"):
            self.back_button.show()

        # Avoid recreating widgets if they exist
        if not hasattr(self, "stat_selector"):
            self.stat_selector = QComboBox()
            self.stat_selector.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
            self.stat_selector.currentTextChanged.connect(self.update_season_stats)
            self.vbox.addWidget(self.stat_selector)

        if not hasattr(self, "stats_display"):
            self.stats_display = QTextEdit()
            self.stats_display.setReadOnly(True)
            self.vbox.addWidget(self.stats_display)

        if not hasattr(self, "back_button"):
            self.back_button = QPushButton("Back to Main Menu")
            self.back_button.setObjectName("backButton")  # ADD THIS
            self.back_button.clicked.connect(self.back_to_main_menu)
            self.vbox.addWidget(self.back_button)

        self.update_season_stats("Points")

    def compare_all_games(self):
        all_games_stats = AccessData.Get_season_stats(players_name=self.players_name)
        stat_names = set()
        trends_report = {}
        game_names = list(all_games_stats.keys()) # all games stat names

        for stats in all_games_stats.values():
            stat_names.update(stats.keys())

        for stat_name in stat_names:
            stat_trend = []

            for i in range(1, len(game_names)):
                prev = all_games_stats[game_names[i-1]].get(stat_name, 0)
                current = all_games_stats[game_names[i]].get(stat_name,0)
                arrow = "increased" if current > prev else "decreased" if current < prev else "no change"   
                stat_trend.append(f"{game_names[i-1]} to {game_names[i]}: {stat_name} {arrow} ({prev} to {current})")
            trends_report[stat_name] = stat_trend

        return trends_report
    
    def update_game_comparison(self, stat_name):
        trend_report = self.compare_all_games()

        if stat_name not in trend_report:
            self.trends_display.setHtml("<p style='color: #ef4444;'>No data available for this stat</p>")
            return

        stats_trends = trend_report[stat_name]
        output = f"""
            <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; white-space: nowrap; font-size: 20px;'>
                {stat_name} Trends - {self.players_name}
            </h2>
            <div style='margin-top: 20px;'>
        """

        for trend in stats_trends:
            if "increased" in trend:
                color = "#10b981"
                arrow = "↑"
            elif "decreased" in trend:
                color = "#ef4444"
                arrow = "↓"
            else:
                color = "#9ca3af"
                arrow = "→"

            output += f"""
            <div style='padding: 12px; margin-bottom: 10px; background: rgba(30, 30, 40, 0.4); border-left: 3px solid {color}; border-radius: 8px;'>
                <span style='color: {color}; font-size: 18px; margin-right: 10px;'>{arrow}</span>
                <span style='color: #e5e7eb;'>{trend}</span>
            </div>
            """

        output += "</div></div>"
        self.trends_display.setHtml(output)

    def show_compare_all_games(self):
        # Hide main menu buttons
        for btn in [self.get_quick_stats_btn, self.compare_all_games_btn,
                    self.season_grading_btn, self.best_worst_game_btn,
                    self.game_rating_btn, self.season_game_rating_btn]:
            btn.hide()

        if hasattr(self, "stat_selector_compare"):
            self.stat_selector_compare.show()
        if hasattr(self, "trends_display"):
            self.trends_display.show()
        if hasattr(self, "back_button_compare"):
            self.back_button_compare.show()


        if not hasattr(self, "stat_selector_compare"):
            self.stat_selector_compare = QComboBox()
            self.stat_selector_compare.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
            self.stat_selector_compare.currentTextChanged.connect(self.update_game_comparison)
            self.vbox.addWidget(self.stat_selector_compare)

        if not hasattr(self, "trends_display"):
            self.trends_display = QTextEdit()
            self.trends_display.setReadOnly(True)
            self.vbox.addWidget(self.trends_display)

        if not hasattr(self, "back_button_compare"):
            self.back_button_compare = QPushButton("Back to Main Menu")
            self.back_button_compare.setObjectName("backButton")  # ADD THIS
            self.back_button_compare.clicked.connect(self.back_to_main_menu)
            self.vbox.addWidget(self.back_button_compare)

        self.update_game_comparison("Points")

    def show_grading(self):
        for btn in [self.get_quick_stats_btn, self.compare_all_games_btn,
                    self.season_grading_btn, self.best_worst_game_btn,
                    self.game_rating_btn, self.season_game_rating_btn]:
            btn.hide()

        if hasattr(self, "grading_display"):
            self.grading_display.show()
        if hasattr(self, "back_button_grading"):
            self.back_button_grading.show()

        if not hasattr(self, "grading_display"):
            self.grading_display = QTextEdit()
            self.grading_display.setReadOnly(True)
            self.vbox.addWidget(self.grading_display)

        if not hasattr(self, "back_button_grading"):
            self.back_button_grading = QPushButton("Back to Main Menu")
            self.back_button_grading.setObjectName("backButton")
            self.back_button_grading.clicked.connect(self.back_to_main_menu)
            self.vbox.addWidget(self.back_button_grading)
        self.format_grading()

    def format_grading(self):
        grades = self.grading()
        output = f"""
        <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                Season Grading - {self.players_name}
            </h2>
            <div style='margin-top: 20px;'>
        """
        
        for stat_name, stat_data in grades.items():
            grade = stat_data['grade']
            percent = stat_data['percent']
            value = stat_data['value']

            if grade in ["A+", "A"]:
                color = "#10b981"
            elif grade in ['B+', "B"]:
                color = "#3b82f6"
            elif grade in ["C+", "C"]:
                color = "#eab308"
            elif grade in ["D+", "D"]:
                color = "#f97316"
            else:
                color = "#ef4444"

            output += f"""
                        <div style='padding: 16px; margin-bottom: 12px; background: rgba(30, 30, 40, 0.4); border-left: 4px solid {color}; border-radius: 8px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='color: #e5e7eb; font-size: 18px; font-weight: 600;'>{stat_name}</span>
                            <span style='color: {color}; font-size: 28px; font-weight: 700;'>{grade}</span>
                        </div>
                        <div style='margin-top: 8px; color: #9ca3af; font-size: 14px;'>
                            <span>Percentage: {percent}%</span> &nbsp;&nbsp;|&nbsp;&nbsp; <span>Value: {value}</span>
                        </div>
                    </div>
            """
        output += f"</div></div>"

        self.grading_display.setHtml(output)

    def grading(self):
        
        summed_team_stats = AccessData.Get_team_season_stats(True, False)
        summed_player_season_stats = AccessData.Get_season_stats(players_name=self.players_name, sum_total=True, look_good=False)
    
        grades = {}
        for stat, player_value in summed_player_season_stats.items():
            team_total = sum(players_stats.get(stat, 0) for players_stats in summed_team_stats.values())

            if team_total == 0:
                pct = 0
            else:
                if stat in ["Fouls", "Turnovers"]:
                    pct = 100 - (player_value / team_total) * 100
                else:
                    pct = (player_value / team_total) * 100

            if pct >= 90: grade = "A+"
            elif pct >= 80: grade = "A"
            elif pct >= 70: grade = "B+"
            elif pct >= 60: grade = "B"
            elif pct >= 50: grade = "C+"
            elif pct >= 40: grade = "C"
            elif pct >= 30: grade = "D+"
            elif pct >= 20: grade = "D"
            else: grade = "F"

            grades[stat] = {"grade": grade, "percent": round(pct, 1), "value": player_value}

        return grades
        
    def best_worst_highlights(self, what_to_look_for: str, look_good: bool = False):
        all_games = AccessData.Get_season_stats(players_name=self.players_name, sum_total=False, look_good=False)
        nums = {}
        # {'Game_1': {'Points': 5, 'Fouls': 1, 'Rebounds': 2, 'Assists': 4, 'Turnovers': 2}, 'Game_2': {'Points': 22, 'Fouls': 1, 'Rebounds': 1, 'Assists': 0, 'Turnovers': 0}, 'Game_3': {'Points': 10, 'Fouls': 1, 'Rebounds': 2, 'Assists': 1, 'Turnovers': 0}}
        
        for game_name, game_stats in all_games.items():
            if what_to_look_for in game_stats:
                nums[game_name] = game_stats[what_to_look_for]

    # {'Game_1': 5, 'Game_2': 22, 'Game_3': 10}

        best_game = max(nums, key=nums.get)
        worst_game = min(nums, key=nums.get)


        return {"best": best_game, "best_val": nums.get(best_game), "worst": worst_game, "worst_val": nums.get(worst_game)}
    
    def show_best_worst_highlights(self):
        for btn in [self.get_quick_stats_btn, self.compare_all_games_btn,
                    self.season_grading_btn, self.best_worst_game_btn,
                    self.game_rating_btn, self.season_game_rating_btn]:
                btn.hide()
        if hasattr(self , "highlights_selector"):
            self.highlights_selector.show()
        if hasattr(self, "highlights_display"):
            self.highlights_display.show()
        if hasattr(self, "back_button_highlights"):
            self.back_button_highlights.show()

        if not hasattr(self, "highlights_selector"):
            self.highlights_selector = QComboBox()
            self.highlights_selector.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
            self.highlights_selector.currentTextChanged.connect(self.format_highlights)
            self.vbox.addWidget(self.highlights_selector)

        if not hasattr(self, "highlights_display"):
            self.highlights_display = QTextEdit()
            self.highlights_display.setReadOnly(True)
            self.vbox.addWidget(self.highlights_display)

        if not hasattr(self, "back_button_highlights"):
            self.back_button_highlights = QPushButton("Back to Main Menu")
            self.back_button_highlights.setObjectName("backButton")
            self.back_button_highlights.clicked.connect(self.back_to_main_menu)  # FIX THIS
            self.vbox.addWidget(self.back_button_highlights)

        self.format_highlights("Points")

    def format_highlights(self, stat_name):
        highlights = self.best_worst_highlights(stat_name)
        
        if not highlights:
            self.highlights_display.setHtml("<p style='color: #ef4444;'>No data available</p>")
        
        best_game=highlights['best']
        best_val=highlights['best_val']
        worst_game=highlights['worst']
        worst_val=highlights['worst_val']

        output = f"""
                    <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                {stat_name} Highlights - {self.players_name}
            </h2>
            
            <div style='padding: 20px; margin-bottom: 16px; background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 12px;'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <span style='color: #10b981; font-size: 32px; margin-right: 12px;'>⭐</span>
                    <span style='color: #10b981; font-size: 20px; font-weight: 700;'>Best Performance</span>
                </div>
                <div style='color: #e5e7eb; font-size: 16px; margin-left: 44px;'>
                    <div style='margin-bottom: 8px;'><strong>Game:</strong> {best_game}</div>
                    <div><strong>{stat_name}:</strong> <span style='color: #10b981; font-size: 24px; font-weight: 700;'>{best_val}</span></div>
                </div>
            </div>
            
            <div style='padding: 20px; background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 12px;'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <span style='color: #ef4444; font-size: 32px; margin-right: 12px;'>📉</span>
                    <span style='color: #ef4444; font-size: 20px; font-weight: 700;'>Worst Performance</span>
                </div>
                <div style='color: #e5e7eb; font-size: 16px; margin-left: 44px;'>
                    <div style='margin-bottom: 8px;'><strong>Game:</strong> {worst_game}</div>
                    <div><strong>{stat_name}:</strong> <span style='color: #ef4444; font-size: 24px; font-weight: 700;'>{worst_val}</span></div>
                </div>
            </div>
            
            <div style='margin-top: 20px; padding: 16px; background: rgba(30, 30, 40, 0.4); border-radius: 8px; text-align: center;'>
                <span style='color: #9ca3af; font-size: 14px;'>Difference: </span>
                <span style='color: #8b5cf6; font-size: 18px; font-weight: 700;'>{best_val - worst_val}</span>
            </div>
        </div>
        """
        self.highlights_display.setHtml(output)

    def game_rating(self, game_name: str):
        game_stats = AccessData.Get_game_stats(game_id=game_name, player=self.players_name, look_good=False)

        scores = (
            game_stats.get('Points', 0) * 1.7 +
            game_stats.get('Assists', 0) * 1.2 +
            game_stats.get('Rebounds', 0) * 1.45 +
            game_stats.get('Fouls', 0) * -0.3 +
            game_stats.get('Turnovers', 0) * -1.3
        )

        rating = max(0, min(100, (scores + 10) * 2.2))

        return round(rating, 1)

    def format_game_rating(self, game_name):
        rating = self.game_rating(game_name)
        game_stats = AccessData.Get_game_stats(game_id=game_name, player=self.players_name, look_good=False)

        if rating >= 80:
            rating_color = "#10b981"
            rating_text = "Excellent"
        elif rating >= 60:
            rating_color = "#3b82f6"
            rating_text = "Good"
        elif rating >= 40:
            rating_color = "#eab308"
            rating_text = "Average"
        elif rating >= 20:
            rating_color = "#f97316"
            rating_text = "Below Average"
        else:
            rating_color = "#ef4444" 

        points_contrib = game_stats.get('Points', 0) * 1.5
        assists_contrib = game_stats.get('Assists') * 1.0
        rebounds_contrib = game_stats.get('Rebounds', 0) * 1.25
        fouls_contrib = game_stats.get('Fouls', 0) * -0.5
        turnovers_contrib = game_stats.get('Turnovers', 0) * -1.5

        output = f"""
                <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                Game Rating - {game_name}
            </h2>
            
            <div style='text-align: center; padding: 30px; background: rgba(30, 30, 40, 0.6); border-radius: 16px; margin-bottom: 20px;'>
                <div style='color: #9ca3af; font-size: 16px; margin-bottom: 10px;'>Overall Rating</div>
                <div style='color: {rating_color}; font-size: 64px; font-weight: 700; margin-bottom: 10px;'>{rating:.1f}</div>
                <div style='color: {rating_color}; font-size: 20px; font-weight: 600;'>{rating_text}</div>
            </div>
            
            <div style='margin-top: 20px;'>
                <h3 style='color: #e5e7eb; font-size: 18px; margin-bottom: 12px;'>Stat Breakdown</h3>
                
                <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: #9ca3af;'>Points ({game_stats.get('Points', 0)} × 1.5)</span>
                        <span style='color: {"#10b981" if points_contrib > 0 else "#9ca3af"}; font-weight: 600;'>+{points_contrib:.1f}</span>
                    </div>
                </div>
                
                <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: #9ca3af;'>Assists ({game_stats.get('Assists', 0)} × 1.0)</span>
                        <span style='color: {"#10b981" if assists_contrib > 0 else "#9ca3af"}; font-weight: 600;'>+{assists_contrib:.1f}</span>
                    </div>
                </div>
                
                <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: #9ca3af;'>Rebounds ({game_stats.get('Rebounds', 0)} × 1.25)</span>
                        <span style='color: {"#10b981" if rebounds_contrib > 0 else "#9ca3af"}; font-weight: 600;'>+{rebounds_contrib:.1f}</span>
                    </div>
                </div>
                
                <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: #9ca3af;'>Fouls ({game_stats.get('Fouls', 0)} × -0.5)</span>
                        <span style='color: {"#ef4444" if fouls_contrib < 0 else "#9ca3af"}; font-weight: 600;'>{fouls_contrib:.1f}</span>
                    </div>
                </div>
                
                <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-radius: 8px;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: #9ca3af;'>Turnovers ({game_stats.get('Turnovers', 0)} × -1.5)</span>
                        <span style='color: {"#ef4444" if turnovers_contrib < 0 else "#9ca3af"}; font-weight: 600;'>{turnovers_contrib:.1f}</span>
                    </div>
                </div>
            </div>
        </div>
        """

        self.game_rating_display.setHtml(output)

    def show_game_rating(self):
        for btn in [
            self.get_quick_stats_btn, self.compare_all_games_btn,
            self.season_grading_btn, self.best_worst_game_btn,
            self.game_rating_btn, self.season_game_rating_btn
        ]:
            btn.hide()

        all_games = AccessData.Get_season_stats(players_name=self.players_name, sum_total=False)
        game_list = list(all_games.keys())

        if hasattr(self, "game_selector"):
            self.game_selector.show()
        else:
            self.game_selector = QComboBox()
            self.game_selector.addItems(game_list)
            self.game_selector.currentTextChanged.connect(self.format_game_rating)
            self.vbox.addWidget(self.game_selector)

        if hasattr(self, "game_rating_display"):
            self.game_rating_display.show()
        else:
            self.game_rating_display = QTextEdit()
            self.game_rating_display.setReadOnly(True)
            self.vbox.addWidget(self.game_rating_display)

        if hasattr(self, "back_button_game_rating"):
            self.back_button_game_rating.show()
        else:
            self.back_button_game_rating = QPushButton("Back to Main Menu")
            self.back_button_game_rating.setObjectName("backButton")
            self.back_button_game_rating.clicked.connect(self.back_to_main_menu)
            self.vbox.addWidget(self.back_button_game_rating)

        if game_list:
            self.format_game_rating(game_list[0])


    def season_game_rating(self):
        all_game_stats = AccessData.Get_season_stats(players_name=self.players_name, sum_total=False, look_good=False)

        if not all_game_stats:
            return {"average": 0, "all_games": {}}


        ratings = []
        game_rating = {}

        for game_name in all_game_stats.keys():
            rating = self.game_rating(game_name=game_name)
            ratings.append(rating)
            game_rating[game_name] = rating

        try:
            avg_rating = sum(ratings) / len(ratings)
        except ZeroDivisionError:
            return f"can't dived by 0"

        return {"average": round(avg_rating, 1),
                "all_games": game_rating}
    
    def show_game_season_game_rating(self):
        for btn in [
            self.get_quick_stats_btn, self.compare_all_games_btn,
            self.season_grading_btn, self.best_worst_game_btn,
            self.game_rating_btn, self.season_game_rating_btn
        ]:
            btn.hide()

        if hasattr(self, "season_rating_display"):
            self.season_rating_display.show()
        else:
            self.season_rating_display = QTextEdit()
            self.season_rating_display.setReadOnly(True)
            self.vbox.addWidget(self.season_rating_display)
        
        if hasattr(self, "back_button_season_rating"):
            self.back_button_season_rating.show()
        else:
            self.back_button_season_rating = QPushButton("Back to Main Menu")
            self.back_button_season_rating.setObjectName("backButton")
            self.back_button_season_rating.clicked.connect(self.back_to_main_menu)
            self.vbox.addWidget(self.back_button_season_rating)
            
        self.format_season_game_rating()    
    def format_season_game_rating(self):
        data = self.season_game_rating()
        avg = data['average']
        all_games = data['all_games']

        if avg >= 80:
            avg_color = "#10b981"
        elif avg >= 60:
            avg_color = "#3b82f6"
        elif avg >= 40:
            avg_color = "#eab308"
        else:
            avg_color = "#ef4444"

        output = f"""
                 <div style='padding: 20px;'>
                <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                    Season Game Ratings - {self.players_name}
                </h2>
                
                <div style='text-align: center; padding: 30px; background: rgba(30, 30, 40, 0.6); border-radius: 16px; margin-bottom: 20px;'>
                    <div style='color: #9ca3af; font-size: 16px; margin-bottom: 10px;'>Season Average Rating</div>
                    <div style='color: {avg_color}; font-size: 64px; font-weight: 700;'>{avg:.1f}</div>
                </div>
                
                <h3 style='color: #e5e7eb; font-size: 18px; margin-bottom: 12px;'>All Games</h3>
        """

        for game_name, rating in all_games.items():
            if rating >= 80:
                color = "#10b981"
            elif rating >= 60:
                color = "#3b82f6"
            elif rating >= 40:
                color = "#eab308"
            else:
                color = "#ef4444"

            output += f"""
         <div style='padding: 16px; margin-bottom: 10px; background: rgba(30, 30, 40, 0.4); border-left: 4px solid {color}; border-radius: 8px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #e5e7eb; font-size: 16px;'>{game_name}</span>
                <span style='color: {color}; font-size: 24px; font-weight: 700;'>{rating:.1f}</span>
            </div>
        </div>
            """

        output += "</div/>"
        self.season_rating_display.setHtml(output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    drags = PlayerReport("Aston Sharp")
    drags.show()
    sys.exit(app.exec_())