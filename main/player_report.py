# Rated 942/1000

import sys
import os
from typing import Optional, Dict, Any
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.accessing_data import AccessData
from utils.write import write_to
from utils.logging import Logging
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt
from datetime import datetime, timezone
import uuid

logger = Logging(service_name="player_report_service", user_id="N/A")
create_log = logger.create_log


class Backend:
    
    @staticmethod
    def calculate_season_average(player: str, stat: str) -> Dict[str, Any]:

        sum_games_stats = AccessData.get_season_stats(player=player, sum_total=True)
        
        if sum_games_stats is None or stat not in sum_games_stats:
            return None
        
        all_games_stats = AccessData.get_season_stats(player=player, sum_total=False)
        if not all_games_stats:
            return None
            
        games_played = len(all_games_stats)
        mean_val = sum_games_stats[stat] / games_played
        values = [game.get(stat, 0) for game in all_games_stats.values()]
        values.sort()
        
        if not values:
            return None
        
        mid = len(values) // 2
        median_val = values[mid] if len(values) % 2 != 0 else (values[mid - 1] + values[mid]) / 2
        best_val = max(values)
        worst_val = min(values)
        range_val = best_val - worst_val
        
        team_stats = AccessData.get_team_season_stats(sum_total=True, look_good=False)
        if team_stats is None:
            team_total = 0
        else:
            team_total = sum(player_stats.get(stat, 0) for player_stats in team_stats.values())
        
        percent = (sum_games_stats[stat] / team_total * 100) if team_total > 0 else 0
        
        return {
            'mean': mean_val,
            'median': median_val,
            'range': range_val,
            'best': best_val,
            'worst': worst_val,
            'percent': percent
        }
    
    @staticmethod
    def get_grading_data(player: str) -> Dict[str, Any]:
        summed_team_stats = AccessData.get_team_season_stats(True, False)
        summed_player_season_stats = AccessData.get_season_stats(player=player, sum_total=True, look_good=False)
        
        if summed_team_stats is None or summed_player_season_stats is None:
            return None
        
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
    
    @staticmethod
    def get_comparison_data(player: str) -> Dict[str, Any]:
        all_games_stats = AccessData.get_season_stats(player=player)
        
        if not all_games_stats:
            return {}
        
        stat_names = set()
        trends_report = {}
        game_names = list(all_games_stats.keys())
        
        for stats in all_games_stats.values():
            stat_names.update(stats.keys())
        
        for stat_name in stat_names:
            stat_trend = []
            for i in range(1, len(game_names)):
                prev = all_games_stats[game_names[i-1]].get(stat_name, 0)
                current = all_games_stats[game_names[i]].get(stat_name, 0)
                arrow = "increased" if current > prev else "decreased" if current < prev else "no change"
                stat_trend.append(f"{game_names[i-1]} to {game_names[i]}: {stat_name} {arrow} ({prev} to {current})")
            trends_report[stat_name] = stat_trend
        
        return trends_report
    
    @staticmethod
    def get_highlights(player: str, stat: str) -> Dict[str, Any]:
        all_games = AccessData.get_season_stats(player=player, sum_total=False)
        
        if not all_games:
            return None
        
        nums = {}
        for game_name, game_stats in all_games.items():
            if stat in game_stats:
                nums[game_name] = game_stats.get(stat, 0)
        
        if not nums:
            return None
        
        best_game = max(nums, key=nums.get)
        worst_game = min(nums, key=nums.get)
        
        return {"best": best_game, "best_val": nums[best_game], "worst": worst_game, "worst_val": nums[worst_game]}
    
    @staticmethod
    def calculate_game_rating(player: str, game_name: str) -> float:
        game_stats = AccessData.get_game_stats(game=game_name, player=player, look_good=False)
        
        if game_stats is None:
            return 0
        
        scores = (
            game_stats.get('Points', 0) * 1.7 +
            game_stats.get('Assists', 0) * 1.2 +
            game_stats.get('Rebounds', 0) * 1.45 +
            game_stats.get('Fouls', 0) * -0.3 +
            game_stats.get('Turnovers', 0) * -1.3
        )
        
        rating = max(0, min(100, (scores + 10) * 2.2))
        return round(rating, 1)
    
    @staticmethod
    def get_season_ratings(player: str) -> Dict[str, Any]:
        all_game_stats = AccessData.get_season_stats(player=player, sum_total=False, look_good=False)
        
        if not all_game_stats:
            return {"average": 0, "all_games": {}}
        
        ratings = []
        game_rating = {}
        
        for game_name in all_game_stats.keys():
            rating = Backend.calculate_game_rating(player, game_name)
            ratings.append(rating)
            game_rating[game_name] = rating
        
        try:
            avg_rating = sum(ratings) / len(ratings)
        except ZeroDivisionError:
            return {"average": 0, "all_games": {}}
        
        return {"average": round(avg_rating, 1), "all_games": game_rating}


class Style:
    
    @staticmethod
    def get_stylesheet() -> str:
        return """
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
        """
    
    @staticmethod
    def format_season_average(data: Dict[str, Any], player: str, stat: str) -> str:
        if data is None:
            return "<p>No game data available</p>"
        
        return f"""
            <div style='padding: 20px;'>
                <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; white-space: nowrap; font-size: 20px;'>
                    {stat} Stats - {player}
                </h2>
                <table style='width: 100%; border-spacing: 0 10px;'>
                    <tr>
                        <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Average per Game:</td>
                        <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{data['mean']:.1f}</td>
                    </tr>
                    <tr>
                        <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Median:</td>
                        <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{data['median']:.1f}</td>
                    </tr>
                    <tr>
                        <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Range:</td>
                        <td style='color: #f9fafb; font-weight: 600; text-align: right;'>{data['range']}</td>
                    </tr>
                    <tr>
                        <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Best Performance:</td>
                        <td style='color: #10b981; font-weight: 700; text-align: right;'>{data['best']}</td>
                    </tr>
                    <tr>
                        <td style='color: #9ca3af; padding: 8px 0; width: 200px;'>Worst Performance:</td>
                        <td style='color: #ef4444; font-weight: 700; text-align: right;'>{data['worst']}</td>
                    </tr>
                    <tr style='border-top: 1px solid #374151;'>
                        <td style='color: #9ca3af; padding: 12px 0 0 0; width: 200px;'>Team Contribution:</td>
                        <td style='color: #8b5cf6; font-weight: 700; font-size: 18px; text-align: right; padding: 12px 0 0 0;'>{data['percent']:.1f}%</td>
                    </tr>
                </table>
            </div>
        """
    
    @staticmethod
    def format_grading(grades: Dict[str, Any], player: str) -> str:
        output = f"""
        <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                Season Grading - {player}
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
        return output
    
    @staticmethod
    def format_comparison(trends: Dict[str, Any], player: str, stat: str) -> str:
        if not trends or stat not in trends:
            return "<p style='color: #ef4444;'>No data available for this stat</p>"
        
        stats_trends = trends[stat]
        output = f"""
            <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; white-space: nowrap; font-size: 20px;'>
                {stat} Trends - {player}
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
        return output
    
    @staticmethod
    def format_highlights(highlights: Dict[str, Any], player: str, stat: str) -> str:
        if not highlights:
            return "<p style='color: #ef4444;'>No data available</p>"
        
        best_game = highlights['best']
        best_val = highlights['best_val']
        worst_game = highlights['worst']
        worst_val = highlights['worst_val']
        
        return f"""
                    <div style='padding: 20px;'>
            <h2 style='color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px; font-size: 22px;'>
                {stat} Highlights - {player}
            </h2>
            
            <div style='padding: 20px; margin-bottom: 16px; background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 12px;'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <span style='color: #10b981; font-size: 32px; margin-right: 12px;'>⭐</span>
                    <span style='color: #10b981; font-size: 20px; font-weight: 700;'>Best Performance</span>
                </div>
                <div style='color: #e5e7eb; font-size: 16px; margin-left: 44px;'>
                    <div style='margin-bottom: 8px;'><strong>Game:</strong> {best_game}</div>
                    <div><strong>{stat}:</strong> <span style='color: #10b981; font-size: 24px; font-weight: 700;'>{best_val}</span></div>
                </div>
            </div>
            
            <div style='padding: 20px; background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 12px;'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <span style='color: #ef4444; font-size: 32px; margin-right: 12px;'>📉</span>
                    <span style='color: #ef4444; font-size: 20px; font-weight: 700;'>Worst Performance</span>
                </div>
                <div style='color: #e5e7eb; font-size: 16px; margin-left: 44px;'>
                    <div style='margin-bottom: 8px;'><strong>Game:</strong> {worst_game}</div>
                    <div><strong>{stat}:</strong> <span style='color: #ef4444; font-size: 24px; font-weight: 700;'>{worst_val}</span></div>
                </div>
            </div>
            
            <div style='margin-top: 20px; padding: 16px; background: rgba(30, 30, 40, 0.4); border-radius: 8px; text-align: center;'>
                <span style='color: #9ca3af; font-size: 14px;'>Difference: </span>
                <span style='color: #8b5cf6; font-size: 18px; font-weight: 700;'>{best_val - worst_val}</span>
            </div>
        </div>
        """
    
    @staticmethod
    def format_game_rating(rating: float, game_name: str, game_stats: Dict[str, Any]) -> str:
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
            rating_text = "Poor"
        
        points_contrib = game_stats.get('Points', 0) * 1.5
        assists_contrib = game_stats.get('Assists', 0) * 1.0
        rebounds_contrib = game_stats.get('Rebounds', 0) * 1.25
        fouls_contrib = game_stats.get('Fouls', 0) * -0.5
        turnovers_contrib = game_stats.get('Turnovers', 0) * -1.5
        
        return f"""
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
    
    @staticmethod
    def format_season_ratings(data: Dict[str, Any], player: str) -> str:
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
                    Season Game Ratings - {player}
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
            <div style='padding: 12px; margin-bottom: 8px; background: rgba(30, 30, 40, 0.4); border-left: 4px solid {color}; border-radius: 8px;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #e5e7eb;'>{game_name}</span>
                    <span style='color: {color}; font-weight: 700;'>{rating:.1f}</span>
                </div>
            </div>
            """
        
        output += "</div>"
        return output


class Utils:
    
    @staticmethod
    def check_error(result: Any) -> tuple:
        if isinstance(result, dict) and result.get("log_level") == "ERROR":
            error_msg = result.get("error", {}).get("message", "Unknown error")
            return True, f"<p style='color: #ef4444;'>Error: {error_msg}</p>"
        return False, None
    
    @staticmethod
    def log_action(level: str, message: str, where: str, user_id: str, source_ip: str, request_id: str, error: Dict = None) -> None:
        try:
            log_entry = create_log(
                level=level,
                message=message,
                where=where,
                user_id=user_id,
                source_ip=source_ip,
                request_id=request_id,
                error=error
            )
            write_to("C:/Users/Drags Jrs/Drags/Database/log/player_report_log.json", log_entry)
        except Exception as e:
            print(f"Logging error: {e}")


class PlayerReport(QWidget):
    
    current_time = datetime.now()
    error_message = {}
    user_id: str = "N/A"  
    source_ip: str = "N/A"  
    request_id: str = "N/A"

    def __init__(self, players_name: str = "", user_id: str = "anonymous", source_ip: Optional[str] = None):
        try:
            super().__init__()
            self.user_id = user_id
            self.source_ip = source_ip
            self.request_id = str(uuid.uuid4())
            self.current_time = datetime.now(timezone.utc)

            if not isinstance(players_name, str):
                return {'error': f"players_name must be a string"}

            self.players_name = players_name

            self.get_quick_stats_btn = QPushButton("Get Quick Stats")
            self.compare_all_games_btn = QPushButton("Compare All Games")
            self.season_grading_btn = QPushButton("Season Grading")
            self.best_worst_game_btn = QPushButton("Best/Worst Game Highlights")
            self.game_rating_btn = QPushButton("Game Rating")
            self.season_game_rating_btn = QPushButton("Season Game Rating")

            self.get_quick_stats_btn.clicked.connect(self.season_average)
            self.compare_all_games_btn.clicked.connect(self.show_compare_all_games)
            self.season_grading_btn.clicked.connect(self.show_grading)
            self.best_worst_game_btn.clicked.connect(self.show_best_worst_highlights)
            self.game_rating_btn.clicked.connect(self.show_game_rating)
            self.season_game_rating_btn.clicked.connect(self.show_game_season_game_rating)

            Utils.log_action(
                level="INFO",
                message="PlayerReport initialized successfully",
                where="__init__",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
        
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="PlayerReport initialized failed",
                where="__init__",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )
            return

        self.init_main_UI()

    def init_main_UI(self):
        try:
            self.setWindowTitle("Drags")
            self.setMinimumSize(700, 600)

            self.vbox = QVBoxLayout()
            self.vbox.setContentsMargins(40, 40, 40, 40)
            self.vbox.setSpacing(15)

            self.header_label = QLabel(f"{self.players_name}'s Report Card")
            self.header_label.setAlignment(Qt.AlignCenter)
            self.header_label.setObjectName("header")
            self.header_label.setWordWrap(True)
            self.vbox.addWidget(self.header_label)
            self.vbox.addSpacing(20)

            self.menu_buttons = [
                self.get_quick_stats_btn,
                self.compare_all_games_btn,
                self.season_grading_btn,
                self.best_worst_game_btn,
                self.game_rating_btn,
                self.season_game_rating_btn
            ]

            for btn in self.menu_buttons:
                btn.setObjectName("menuItem")
                self.vbox.addWidget(btn)

            self.vbox.addStretch()
            self.setLayout(self.vbox)

            self.setStyleSheet(Style.get_stylesheet())

            Utils.log_action(
                level="INFO",
                message="init_main_UI ran successfully",
                where="init_main_UI",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="init_main_UI failed",
                where="init_main_UI",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )
            return

    def _hide_menu_buttons(self):
        try:
            for btn in self.menu_buttons:
                btn.hide()

            Utils.log_action(
                level="INFO",
                message="_hide_menu_buttons ran successfully",
                where="_hide_menu_buttons",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_hide_menu_buttons failed",
                where="_hide_menu_buttons",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _back_to_main_menu(self):
        try:
            for attr in ["stat_selector", "stats_display", "back_button",
                        "stat_selector_compare", "trends_display", "back_button_compare",
                        "grading_display", "back_button_grading",
                        "highlights_selector", "highlights_display", "back_button_highlights", 
                        "game_selector", "game_rating_display", "back_button_game_rating",
                        "season_rating_display", "back_button_season_rating"]:
                if hasattr(self, attr):
                    getattr(self, attr).hide()

            for btn in self.menu_buttons:
                btn.show()
            
            Utils.log_action(
                level="INFO",
                message="_back_to_main_menu ran successfully",
                where="_back_to_main_menu",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_back_to_main_menu failed",
                where="_back_to_main_menu",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


    def _update_season_stats(self, stat_name: str):
        try:
            if not isinstance(stat_name, str):
                return {'error': f'stat_name must be a string'}
        
            result = self._calculate_season_average(stat_name)
            self.stats_display.setHtml(result)
        
            Utils.log_action(
                level="INFO",
                message="_update_season_stats ran successfully",
                where="_update_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_update_season_stats failed",
                where="_update_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _calculate_season_average(self, stat_name: str) -> str:
        try:
            if not isinstance(stat_name, str):
                return {'error': f"stat_name must be a string"}
            
            # Backend: Get data
            data = Backend.calculate_season_average(self.players_name, stat_name)
            
            # Check for errors
            is_error, error_html = Utils.check_error(data)
            if is_error:
                return error_html
            
            # Style: Format HTML
            output = Style.format_season_average(data, self.players_name, stat_name)
            
            Utils.log_action(
                level="INFO",
                message="_calculate_season_average ran successfully",
                where="_calculate_season_average",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

            return output

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_calculate_season_average failed",
                where="_calculate_season_average",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )
            return f"<p style='color: #ef4444;'>Error: {str(e)}</p>"

    def season_average(self):
        try:
            self._hide_menu_buttons()

            if hasattr(self, "stat_selector"):
                self.stat_selector.show()
            if hasattr(self, "stats_display"):
                self.stats_display.show()
            if hasattr(self, "back_button"):
                self.back_button.show()

            if not hasattr(self, "stat_selector"):
                self.stat_selector = QComboBox()
                self.stat_selector.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
                self.stat_selector.currentTextChanged.connect(self._update_season_stats)
                self.vbox.addWidget(self.stat_selector)

            if not hasattr(self, "stats_display"):
                self.stats_display = QTextEdit()
                self.stats_display.setReadOnly(True)
                self.vbox.addWidget(self.stats_display)

            if not hasattr(self, "back_button"):
                self.back_button = QPushButton("Back to Main Menu")
                self.back_button.setObjectName("backButton")
                self.back_button.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button)

            self._update_season_stats("Points")

            Utils.log_action(
                level="INFO",
                message="Season_average ran successfully",
                where="Season_average",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="Season_average failed",
                where="Season_average",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


    def _update_game_comparison(self, stat_name: str):
        try:
            if not isinstance(stat_name, str):
                return {'error': f'stat_name must be a string'}
            
            trend_report = Backend.get_comparison_data(self.players_name)

            is_error, error_html = Utils.check_error(trend_report)
            if is_error:
                self.trends_display.setHtml(error_html)
                return
            
            output = Style.format_comparison(trend_report, self.players_name, stat_name)
            self.trends_display.setHtml(output)

            Utils.log_action(
                level="INFO",
                message="_update_game_comparison ran successfully",
                where="_update_game_comparison",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_update_game_comparison failed",
                where="_update_game_comparison",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def show_compare_all_games(self):
        try:
            self._hide_menu_buttons()

            if hasattr(self, "stat_selector_compare"):
                self.stat_selector_compare.show()
            if hasattr(self, "trends_display"):
                self.trends_display.show()
            if hasattr(self, "back_button_compare"):
                self.back_button_compare.show()

            if not hasattr(self, "stat_selector_compare"):
                self.stat_selector_compare = QComboBox()
                self.stat_selector_compare.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
                self.stat_selector_compare.currentTextChanged.connect(self._update_game_comparison)
                self.vbox.addWidget(self.stat_selector_compare)

            if not hasattr(self, "trends_display"):
                self.trends_display = QTextEdit()
                self.trends_display.setReadOnly(True)
                self.vbox.addWidget(self.trends_display)

            if not hasattr(self, "back_button_compare"):
                self.back_button_compare = QPushButton("Back to Main Menu")
                self.back_button_compare.setObjectName("backButton")
                self.back_button_compare.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button_compare)

            self._update_game_comparison("Points")

            Utils.log_action(
                level="INFO",
                message="show_compare_all_games ran successfully",
                where="show_compare_all_games",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="show_compare_all_games failed",
                where="show_compare_all_games",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


    def show_grading(self):
        try:
            self._hide_menu_buttons()

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
                self.back_button_grading.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button_grading)
            
            self._format_grading()
        
            Utils.log_action(
                level="INFO",
                message="show_grading ran successfully",
                where="show_grading",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="show_grading failed",
                where="show_grading",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _format_grading(self):
        try:
            grades = Backend.get_grading_data(self.players_name)

            is_error, error_html = Utils.check_error(grades)
            if is_error:
                self.grading_display.setHtml(error_html)
                return
            
            output = Style.format_grading(grades, self.players_name)
            self.grading_display.setHtml(output)
        
            Utils.log_action(
                level="INFO",
                message="_format_grading ran successfully",
                where="_format_grading",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_format_grading failed",
                where="_format_grading",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def show_best_worst_highlights(self):
        try:
            self._hide_menu_buttons()

            if hasattr(self, "highlights_selector"):
                self.highlights_selector.show()
            if hasattr(self, "highlights_display"):
                self.highlights_display.show()
            if hasattr(self, "back_button_highlights"):
                self.back_button_highlights.show()

            if not hasattr(self, "highlights_selector"):
                self.highlights_selector = QComboBox()
                self.highlights_selector.addItems(["Points", "Fouls", "Assists", "Rebounds", "Turnovers"])
                self.highlights_selector.currentTextChanged.connect(self._format_highlights)
                self.vbox.addWidget(self.highlights_selector)

            if not hasattr(self, "highlights_display"):
                self.highlights_display = QTextEdit()
                self.highlights_display.setReadOnly(True)
                self.vbox.addWidget(self.highlights_display)

            if not hasattr(self, "back_button_highlights"):
                self.back_button_highlights = QPushButton("Back to Main Menu")
                self.back_button_highlights.setObjectName("backButton")
                self.back_button_highlights.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button_highlights)

            self._format_highlights("Points")
        
            Utils.log_action(
                level="INFO",
                message="show_best_worst_highlights ran successfully",
                where="show_best_worst_highlights",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="show_best_worst_highlights failed",
                where="show_best_worst_highlights",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _format_highlights(self, stat_name: str):
        try:
            if not isinstance(stat_name, str):
                return {'error': 'stat_name must be a string'}

            highlights = Backend.get_highlights(self.players_name, stat_name)

            is_error, error_html = Utils.check_error(highlights)
            if is_error:
                self.highlights_display.setHtml(error_html)
                return
            
            output = Style.format_highlights(highlights, self.players_name, stat_name)
            self.highlights_display.setHtml(output)
        
            Utils.log_action(
                level="INFO",
                message="_format_highlights ran successfully",
                where="_format_highlights",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_format_highlights failed",
                where="_format_highlights",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


    def show_game_rating(self):
        try:
            self._hide_menu_buttons()

            all_games = AccessData.get_season_stats(player=self.players_name, sum_total=False)
            
            is_error, error_html = Utils.check_error(all_games)
            if is_error:
                return
            
            game_list = list(all_games.keys())

            if hasattr(self, "game_selector"):
                self.game_selector.show()
            else:
                self.game_selector = QComboBox()
                self.game_selector.addItems(game_list)
                self.game_selector.currentTextChanged.connect(self._format_game_rating)
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
                self.back_button_game_rating.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button_game_rating)

            if game_list:
                self._format_game_rating(game_list[0])

            Utils.log_action(
                level="INFO",
                message="show_game_rating ran successfully",
                where="show_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
    
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="show_game_rating failed",
                where="show_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _format_game_rating(self, game_name: str):
        try:
            if not isinstance(game_name, str):
                return {'error': f'game_name must be a string'}

            rating = Backend.calculate_game_rating(self.players_name, game_name)
            game_stats = AccessData.get_game_stats(game=game_name, player=self.players_name, look_good=False)
            
            # Check for error
            is_error, error_html = Utils.check_error(game_stats)
            if is_error:
                self.game_rating_display.setHtml(error_html)
                return
            
            output = Style.format_game_rating(rating, game_name, game_stats)
            self.game_rating_display.setHtml(output)
        
            Utils.log_action(
                level="INFO",
                message="_format_game_rating ran successfully",
                where="_format_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_format_game_rating failed",
                where="_format_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


    def show_game_season_game_rating(self):
        try:
            self._hide_menu_buttons()

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
                self.back_button_season_rating.clicked.connect(self._back_to_main_menu)
                self.vbox.addWidget(self.back_button_season_rating)
                
            self._format_season_game_rating()    

            Utils.log_action(
                level="INFO",
                message="show_game_season_game_rating ran successfully",
                where="show_game_season_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="show_game_season_game_rating failed",
                where="show_game_season_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )

    def _format_season_game_rating(self):
        try:
            data = Backend.get_season_ratings(self.players_name)

            is_error, error_html = Utils.check_error(data)
            if is_error:
                self.season_rating_display.setHtml(error_html)
                return
            
            output = Style.format_season_ratings(data, self.players_name)
            self.season_rating_display.setHtml(output)

            Utils.log_action(
                level="INFO",
                message="_format_season_game_rating ran successfully",
                where="_format_season_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            Utils.log_action(
                level="ERROR",
                message="_format_season_game_rating failed",
                where="_format_season_game_rating",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id,
                error=error
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player_report = PlayerReport(players_name="Myles Dragone", user_id="admin", source_ip="192.168.1.1")
    player_report.show()
    sys.exit(app.exec_())



# ============================================================================
# END OF FILE: player_report.py
# ============================================================================
# MODULE: Basketball Player Report Card System - GUI Component
# LOCATION: C:/Users/Drags Jrs/Drags/testing/player_report.py
# ============================================================================
# IF NEEDED: If you want the full docstring go to docs/player_report_doc.md
#=============================================================================

# ============================================================================
# FILE STATISTICS
# ============================================================================
# TOTAL CLASSES: 1 (PlayerReport)
# TOTAL METHODS: 27
# TOTAL LINES: ~1000 (excluding docstrings)
# TOTAL LINES (with docs): ~5000+
# WIDGETS CREATED: 15 dynamic widgets across 6 features
# ============================================================================

# ============================================================================
# FEATURE SUMMARY
# ============================================================================
# 1. Season Average Stats - Statistical analysis (mean, median, range, etc.)
# 2. Game Comparison - Game-to-game trend analysis with arrows
# 3. Season Grading - Letter grades (A+ to F) based on team contribution
# 4. Best/Worst Highlights - Performance extremes with difference metric
# 5. Game Rating - Individual game 0-100 rating with breakdown
# 6. Season Game Rating - All game ratings with season average
# ============================================================================
# ============================================================================
# PERFORMANCE NOTES
# ============================================================================
# Widget Reuse Pattern:
#   - First access: ~50ms (creation + layout)
#   - Subsequent: ~5-10ms (show existing)
#   - 5-10x performance improvement
#
# Rating Calculations:
#   - Single game rating: ~5ms
#   - Season rating (3 games): ~30ms
#   - Acceptable for interactive use
#
# HTML Rendering:
#   - Generation: ~5-10ms
#   - QTextEdit render: ~15ms
#   - Total display update: ~20-25ms
# ============================================================================

# ============================================================================
# DEPENDENCIES
# ============================================================================
# External Libraries:
#   - PyQt5 (5.x): GUI framework
#   - sys: System parameters
#   - os: Path operations
#
# Internal Modules:
#   - utils.accessing_data.AccessData: Data layer
#   - Database/Data.json: Game statistics storage
#
# Python Version:
#   - Minimum: Python 3.7 (f-strings, type hints)
#   - Tested: Python 3.13
# ============================================================================

# ============================================================================
# DESIGN PATTERNS USED
# ============================================================================
# 1. Widget Reuse Pattern:
#    - Create once, show/hide for performance
#    - Preserves state between views
#
# 2. Single Page Application:
#    - One window, multiple views
#    - Dynamic content loading
#
# 3. Signal-Slot Architecture:
#    - Qt's event-driven model
#    - Automatic UI updates
#
# 4. Separation of Concerns:
#    - Calculation methods separate from display
#    - Format methods separate from data retrieval
#
# 5. HTML Templating:
#    - Inline CSS for styling
#    - f-strings for dynamic content
# ============================================================================

# ============================================================================
# FUTURE ENHANCEMENTS
# ============================================================================
# SHORT-TERM:
# - Add player selection dropdown in main menu
# - Implement data export (PDF, CSV)
# - Add print functionality
# - Include game date/opponent info
#
# MEDIUM-TERM:
# - Multi-player comparison view
# - Team-wide analytics dashboard
# - Historical trend graphs (using matplotlib)
# - Customizable rating formula weights
#
# LONG-TERM:
# - Database backend (SQLite/PostgreSQL)
# - Web-based version (Flask/Django)
# - Real-time game stat entry
# - Mobile app version
# - Advanced analytics (shot charts, heat maps)
# ============================================================================

# ============================================================================
# TESTING RECOMMENDATIONS
# ============================================================================
# Unit Tests Needed:
# - game_rating() with various stat combinations
# - grading() with edge cases (0 totals, missing stats)
# - calculate_season_average() with 1, 2, 3+ games
# - best_worst_highlights() with identical values
#
# Integration Tests:
# - Full user workflows through each feature
# - Widget state management across navigation
# - Data consistency across features
#
# UI Tests:
# - Responsive layout at various window sizes
# - HTML rendering across different Qt versions
# - Color accessibility (contrast ratios)
# ============================================================================

# ============================================================================
# MAINTENANCE NOTES
# ============================================================================
# When Adding New Features:
# 1. Add button to __init__() menu_buttons list
# 2. Create show_*, format_*, and calculation methods
# 3. Add widget names to back_to_main_menu() hide list
# 4. Follow widget reuse pattern (hasattr checks)
# 5. Update this file statistics section
#
# When Modifying Styling:
# - All CSS in init_main_UI() setStyleSheet()
# - Use object names for targeted styling
# - Maintain color scheme consistency
# - Test HTML rendering in QTextEdit
#
# When Updating Calculations:
# - Document formula changes in method docstrings
# - Consider backward compatibility
# - Update related format methods
# - Test edge cases thoroughly
# ============================================================================

# ============================================================================
# COLOR PALETTE REFERENCE
# ============================================================================
# Primary Colors:
#   Background:     #0a0a0f  (Near black)
#   Card Background: #1e1e2e  (Dark gray)
#   Accent:         #6366f1  (Indigo)
#
# Status Colors:
#   Success/Good:   #10b981  (Green)
#   Info/Neutral:   #3b82f6  (Blue)
#   Warning:        #eab308  (Yellow)
#   Caution:        #f97316  (Orange)
#   Error/Bad:      #ef4444  (Red)
#   Special:        #8b5cf6  (Purple)
#
# Text Colors:
#   Primary:        #e5e7eb  (Light gray)
#   Secondary:      #9ca3af  (Medium gray)
#   Tertiary:       #f9fafb  (Near white)
# ============================================================================

# ============================================================================
# AUTHOR & LICENSE INFORMATION
# ============================================================================
# Author: Drags Jrs
# Created: 2025
# Last Modified: 2025
# Version: 2.3.7
# Status: Production
# 
# License: None hopefully
# Copyright: © 2025 Drags Jrs. All rights reserved.
#
# Repository HTTPS: [https://github.com/SigmaCoder12205/Basketball-Stats.git]
# ============================================================================

# ============================================================================
# ACKNOWLEDGMENTS
# ============================================================================
# - PyQt5 Development Team for the excellent GUI framework
# - Newport Raiders U16 Boys Julie team for the use case and test
# - Shout out to again to the Newport Raiders U16 Boys Julie team for everything 
# - Don't forget my parents for helping me and giving the motivation to keep going
# - And sadly my brother, for nothing...   
# ============================================================================
