# Rated 760/1000

import json
import os 
import shutil
from typing import Optional, Dict, Any

class AccessData:
    data: Dict[str, Any] = {}
    file_path: str = ""
    _initialized: bool = False
    
    def __init__(self):
        try:
            self.initialize()
        except Exception as e:
            print(f"INIT ERROR: {e}")

    def __repr__(self):
        game_count = len(self.data) if isinstance(self.data, dict) else 0 
        player_count = 0

        for game in self.data.values():
            if isinstance(game, dict) and "Lineup" in game:
                for team in game["Lineup"].values():
                    player_count += len(team) if isinstance(team, list) else 0
        return f"<AccessData file={self.file_path or 'Unknown'}\n games={game_count} players={player_count}>"
    
    def __str__(self):
        game_count = len(self.data) if isinstance(self.data, dict) else 0
        player_count = 0

        for game in self.data.values():
            if isinstance(game, dict) and "Lineup" in game:
                for team in game["Lineup"].values():
                    player_count += len(team) if isinstance(team, list) else 0
        return f"File: {self.file_path or "Unknown"}\n Games Loaded: {game_count}\n Total Players: {player_count}"

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            cls()
            cls._initialized = True

    def initialize(self, load: bool = False, filename: str = "Data.json") -> Optional[Dict[str, Any]]:
        if not isinstance(load, bool):
            raise TypeError(f"Expected bool for 'load', got {type(load).__name__}")
        
        if not isinstance(filename, str):
            raise TypeError(f"Expected str for 'filename', got {type(filename).__name__}")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.abspath(os.path.join(base_dir, "Database", filename))
        self.file_path = data_file

        if not os.path.isfile(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        try:
            with open(data_file, 'r', encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError(f"Invalid JSON structure - root must be an object (dict)")
                AccessData.data = data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON Decode error: {e}")
        except OSError as e:
            raise RuntimeError(f"OS error while reading file: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")
        if load:
            return AccessData.data
        
    def save(self, filename: Optional[str] = None, backup: bool = True) -> bool:
        if not isinstance(self.data, dict):
            raise ValueError("Cannot save: data must be a dict")
        
        save_path = filename or self.file_path
        if not save_path:
            raise ValueError("File path is not set")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            if backup and os.path.exists(save_path):
                backup_path = f"{save_path}.bak"
                shutil.copy2(save_path, backup_path)
            
            temp_path = f"{save_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as temp_file:
                json.dump(self.data, temp_file, indent=4, ensure_ascii=False)

            os.replace(temp_file, save_path)
            return True
        except (OSError, IOError) as e:
            print(f"Save error: failed to write file: {e}")
            return False
        except Exception as e:
            print(f"Save error: unexpected error: {e}")
            return False

    @classmethod
    def get_details(cls, game: str, look_good: bool = False):
        cls._ensure_initialized()

        if not isinstance(game, str): 
            return {"error": f"Game {game} must be a string"}
        
        if not isinstance(look_good, bool):
            return f"error: look_good ({look_good}) must be a boolean"

        if not game or game not in cls.data:
            return {"error": f"invalid game: {game}"}

        game_stats = cls.data.get(game, {})

        if game_stats == {}:
            return {"error": f"game: {game} not found"}

        details = game_stats.get("Details", {})

        if look_good:
            output = ["--------------------- Details ------------------------"]
            for detail, stat in details.items():
                output.append(f"{detail}: {stat}")
            output.append("--------------------------------------------------")
            return "\n".join(output)
        else:
            return details.copy()

    @classmethod
    def get_a_lineup(cls, game: str, team: str, look_good: bool =False): 
        cls._ensure_initialized()

        if not isinstance(game, str):
            return f"Error: game ({game}) must be a string"
        
        if not isinstance(team, str):
            return f"Error: team ({team}) must be a string"
        
        if not isinstance(look_good, bool):
            return f"Error: look_good ({look_good}) must be boolean"

        game_stats = cls.data.get(game, {})

        if not game_stats:
            return {"Error": f"{game} is not valid"}

        team_players = game_stats.get("Lineup", {}).get(team, [])
        
        if not team_players:
            return {"Error": f"Team: {team} not found in Game: {game}"}
        
        if look_good:
            output = ["----------------- Team players ----------------------"]
            for num, player in enumerate(team_players, start=1):
                output.append(f"{num}. {player}")
            return "\n\n".join(output)
        else:
            return team_players.copy()
    
    @classmethod
    def get_quarter_stats(cls, game: str, quarter: str, look_good: bool = False):
        cls._ensure_initialized()

        if not isinstance(game, str):
            return {"error": f"game must be a string"}
        
        if not isinstance(quarter, str):
            return {"error": f"quarter must be a string"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        game_stats = cls.data.get(game, {})

        if not game_stats: # Only b/c {} == None
            return {"error": f"game: {game} not found"}
        
        quarters = game_stats.get("Quarters")
        quarter_stats = quarters.get(quarter, {})

        if not quarter_stats:
            return {"error": f"quarter: {quarter} not found"}
        
        if look_good:
            output = [f"-------------------- {game}: {quarter} stats --------------------------"]
            for players_name, players_stats in quarter_stats.items():
                stat_line = ", ".join(f"{stat_name}: {stat_value}" for stat_name, stat_value in players_stats.items())
                output.append(f"{players_name}: {stat_line}\n")
            return "\n".join(output)
        else:
            return quarter_stats.copy()

    @classmethod
    def get_specific_Stats(cls, game: str, quarter: str, player: str, look_good: bool = False): # Original name: find_a_players_quarter_stats and gets specific stats for a player
        cls._ensure_initialized()

        if not isinstance(game, str):
            return {"error": f"game must be a string"}

        if not isinstance(quarter, str):
            return {"error": f"the_quarter must be a string"}

        if not isinstance(player, str):
            return {"error": f"player_name must be a string"}

        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        game_stats = cls.data.get(game, {})

        if not game_stats:
            return {"error": f"{game} not found"}
        
        quarter_stats = game_stats.get("Quarters").get(quarter, {})
        if not quarter_stats:
            return {'error': f'Quarter: {quarter} not found'}
        
        players_stats = quarter_stats.get(player, {})
        if not players_stats:
            return {"error": f"Player: {player} not found"}
        
        if look_good:
            output = f"-------------------- {player} stats in {game} in {quarter} ----------------------------\n"
            for stat_name, stat_value in players_stats.items():
                output += f"    - {stat_name}: {stat_value}\n"
            return output
        else:
            return players_stats

    @classmethod
    def get_game_stats(cls, game: str, player: str, look_good: bool = False): # Original name: get_total_stats sums up a games stats
        cls._ensure_initialized()
        
        if not isinstance(game, str):
            return {"error": f"game_name must be a string"}

        if not isinstance(player, str):
            return {"error": f"player must be a string"}

        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}
        
        game_stats = cls.data.get(game, {})
        
        if not game:
            return {"error": f"{game} not found"}
        
        quarters = game_stats.get("Quarters", {})
        if not quarters:
            return {}
        
        totals = {}

        for _, quarter_stats in quarters.items():
            for player_name, stats in quarter_stats.items():
                if player and player_name != player:
                    continue

                if player_name not in totals:
                    totals[player_name] = {key: 0 for key in stats}

                for stat_name, value in stats.items():
                    totals[player_name][stat_name] += value 


        if look_good:
            if player:
                formatted = [f"------------------ Game: {game} ------------------\n"]
                player_stats = totals.get(player, {})
                formatted.extend( f"{stat}: {value}" for stat, value in player_stats.items())
                return "\n".join(formatted)
            else:
                lines = [f"------------------ Game: {game} Stats ------------------------\n"]
                for player_name, stats in totals.items():
                    stat_line = ", ".join(f"{key}: {value}" for key, value in stats.items())
                    lines.append(f"{player_name}: {stat_line}")
                return "\n".join(lines)
        else:
            return totals if not player else totals.get(player, {})
    
    @classmethod
    def get_season_stats(cls, player: str, sum_total: bool = False, look_good: bool = False):
        cls._ensure_initialized()

        if not isinstance(player, str):
            return {"error": f"players_name must be a string"}
        
        if not isinstance(sum_total, bool):
            return {"error": f"sum_total must be a boolean"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        total = {}

        if sum_total:
            for game_name, game_stats in cls.data.items():
                for quarter, quarter_stats in game_stats["Quarters"].items():
                    if player in quarter_stats:
                        for stat_name, stat_value in quarter_stats[player].items():
                            total[stat_name] = total.get(stat_name, 0) + stat_value                          

            if look_good:
                output = f"Season stats for {player}\n"
                for stat, value in total.items():
                    output += f"    - {stat}: {value}\n"
                return output
            else:
                return total
        else:
            
            game_totals = {}

            for game_name, game_stats in cls.data.items():

                players_total = {}

                for quarter_stats in game_stats["Quarters"].values():
                    if player in quarter_stats:
                        for players_stat_name, players_stat_value in quarter_stats[player].items():
                            players_total[players_stat_name] = players_total.get(players_stat_name, 0) + players_stat_value
                
                if players_total:
                    game_totals[game_name] = players_total
            
            # {'Game_1': {'Points': 0, 'Fouls': 1, 'Rebounds': 1, 'Assists': 1, 'Turnovers': 5}, 'Game_2': {'Points': 3, 'Fouls': 2, 'Rebounds': 1, 'Assists': 2, 'Turnovers': 1}, 'Game 3': {'Points': 0, 'Fouls': 4, 'Rebounds': 1, 'Assists': 0, 'Turnovers': 0}}

            if look_good:
                output = f"------------------------- Game stats for {player} -------------------------------\n"
                for game_name, game_stats in game_totals.items():
                    output += f"----------- {game_name} stats: ------------\n"
                    for stat_name, stat_value in game_stats.items():
                        output += f"    - {stat_name}: {stat_value}\n"
                        if stat_name == "Turnovers":
                            output += "\n"
                return output        
            else:
                return game_totals

    @classmethod
    def get_team_season_stats(cls, sum_total: bool = False, look_good: bool = False):
        cls._ensure_initialized()

        if not isinstance(sum_total, bool):
            return {"error": f"sum_total must be a boolean"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        if sum_total:
            team_totals = {}

            for game_name, game_data in cls.data.items():
                for quarter_name, quarter_stats in game_data["Quarters"].items():
                    for players_name, players_stats in quarter_stats.items():
                        if players_name not in team_totals:
                            team_totals[players_name] = {}  # {"Myles Dragone": None}
                        for stat_name, stat_value in players_stats.items():
                            team_totals[players_name][stat_name] = team_totals[players_name].get(stat_name, 0) + stat_value # {"Myles Dragone": {"Points": 3}}
            
            if look_good:
                output = "---------------- Newport Raiders U16 Boys Julie Season stats ----------------\n"

                for team_players_name, team_players_stats in team_totals.items():
                    output += f"\n                       {team_players_name}                               \n"
                    for team_players_stat_name, team_players_stat_value in team_players_stats.items():
                        output += f"                            - {team_players_stat_name}: {team_players_stat_value}\n"
                
                return output
            else:
                return team_totals
        else:
            game_team_totals = {}
                
            for game_name, game_data in cls.data.items():
                
                player_total = {}

                for quarter_name, quarter_stats in game_data["Quarters"].items():
                    for players_name, players_data in quarter_stats.items():
                        if players_name not in player_total:
                            player_total[players_name] = {} # {"Myles Dragone": {}}
                        for player_stat_name, player_stat_value in players_data.items():
                            player_total[players_name][player_stat_name] = player_total[players_name].get(player_stat_name, 0) + player_stat_value

                game_team_totals[game_name] = player_total
            
            if look_good:
                output = ""
                output += f"---------------------- Newport Raiders U16 Boys Julie Season stats ----------------------\n"
                # 'Game_1': {'Benjamin Berridge': {'Points': 10, 'Fouls': 1, 'Rebounds': 8, 'Assists': 0, 'Turnovers': 2}
                for game_stat_name, game_stat_value in game_team_totals.items():
                    output += f"\n\n{game_stat_name}                                   \n"
                    for players_name, players_stats in game_stat_value.items():
                        output += f"\n\n{players_name}                                     \n"
                        for stat_name, stat_value in players_stats.items():
                            output += f"\n{stat_name}: {stat_value}                       "
                return output
            else:
                return game_team_totals

    @classmethod
    def get_quarter_season_stats(cls, player: str, quarter: str, sum_total: bool = False, look_good: bool = False): # Made by me does the same thing as get_season_stats but only for quarter stats 
        cls._ensure_initialized()

        if not isinstance(player, str):
            return {"error": f"players_name must be a string"}
        
        if not isinstance(quarter, str):
            return {"error": f"what_quarter must be a string"}
        
        if not isinstance(sum_total, bool):
            return {"error": f"sum_total must be a boolean"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        totals = {}

        if quarter not in cls.data["Game_1"]["Quarters"]:
            return {"Error": f"Quarter: {quarter} not found"}

        if sum_total:
            for game_name, game_stats in cls.data.items():
                if quarter in game_stats["Quarters"]:
                    if player in game_stats["Quarters"][quarter]:
                        for stat, value in game_stats["Quarters"][quarter][player].items():
                            totals[stat] = totals.get(stat, 0) + value

            if look_good:
                output = f"All of {quarter} stats together for {player}\n"
                for stat, value in totals.items():
                    output += f"    - {stat}: {value}\n"
                return output
            else:
                return totals       
        else:
            game_totals = {}

            for game_name, game_stats in cls.data.items():

                players_totals = {}

                if quarter in game_stats["Quarters"]:
                    if player in game_stats["Quarters"][quarter]:
                        for stat_name, stat_value in game_stats["Quarters"][quarter][player].items():
                            players_totals[stat_name] = players_totals.get(stat_name, 0) + stat_value
                
                if players_totals:
                    game_totals[game_name] = players_totals            

            
        
            # {'Game_1': {'Points': 0, 'Fouls': 1, 'Rebounds': 1, 'Assists': 1, 'Turnovers': 4}, 'Game_2': {'Points': 0, 'Fouls': 1, 'Rebounds': 0, 'Assists': 1, 'Turnovers': 0}, 'Game 3': {'Points': 0, 'Fouls': 2, 'Rebounds': 0, 'Assists': 0, 'Turnovers': 0}}
            if look_good:
                output = f"============= Seasons {quarter} stats for {player} =============\n"

                for game_stat_name, game_stats in game_totals.items():
                    output += f"    ---------------- Game: {game_stat_name} {quarter} stats ----------------\n"                    
                    for game_Stat_name, game_stat_value in game_stats.items():
                        output += f"       - {game_Stat_name}: {game_stat_value}\n"

                return output
            else:
                return game_totals

    @classmethod
    def get_highest_stats_quarter(cls, game: str, quarter: str, what_to_look_for: str, look_good: bool = False): # Original name: find_a_players_quarter_stats finds out who got the most stats in a quarter
        cls._ensure_initialized()

        if not isinstance(game, str):
            return {"error": f"game must be a string"}
        
        if not isinstance(quarter, str):
            return {"error": f"quarter must be a string"}
        
        if not isinstance(what_to_look_for, str):
            return {"error": f"what_to_look_for must be a string"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        game_stats = cls.data.get(game, {})

        if not game_stats:
            return {"Error": f"Game: {game} not found"}
        
        quarter_stats = game_stats.get("Quarters").get(quarter, {})

        if not quarter_stats:
            return {"Error": f"Quarter: {quarter} not found"}
        
        nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in quarter_stats.items()] # all stats like points fouls blah blah blah

        if not nums:
            if look_good:
                return {"Error": f"stat: {what_to_look_for} not found"}
            else:
                return None
        
        max_stat_value = max(value for _, value in nums)

        if max_stat_value == 0:
            if look_good:
                return f"No one got any {what_to_look_for} in {game} of {quarter}"
            else:
                return None

        top_players = [player for player, value in nums if value == max_stat_value]


        resultstr = f"{top_players[0]}: {max_stat_value}"if len(top_players) == 1 else f"Tied at {max_stat_value} {what_to_look_for}: {', '.join(top_players)}"
        
        if look_good:
            return f"In {quarter} of {game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
        else:
            return {player: max_stat_value for player in top_players}


    @classmethod
    def get_highest_stats_game(cls, game: str, what_to_look_for: str, look_good: bool = False): # Original name: highest_stats_game does the same as get_highest_stats_quarter but does it for a game
        cls._ensure_initialized()

        if not isinstance(game, str):
            return {"error": f"game must be a string"}
        
        if not isinstance(what_to_look_for, str):
            return {"error": f"what_to_look_for must be a string"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        game_stats = cls.get_game_stats(game=game, player="", look_good=False)
        if not game_stats:
            return {'error': f'Game: {game} not found'}
        
        nums = [(player, stats.get(what_to_look_for,0)) for player, stats in game_stats.items() if what_to_look_for in stats]

        if not nums:
            return {'error': f'Stats: No Stats for {what_to_look_for} in {game}' if look_good else None}
        
        max_value = max(value for _, value in nums)

        if max_value == 0:
            if look_good:
                return f"No {what_to_look_for} was found in {game}"
            else:
                return None

        top_players = [player for player, value in nums if value == max_value]

        resultstr = (f"{top_players[0]}: {max_value}" if len(top_players) == 1 else f"Tied at {max_value} {what_to_look_for}: {', '.join(top_players)}")

        if look_good:
            return f"In {game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
        else:
            return {player: max_value for player in top_players}            
        
    @classmethod
    def specific_players_best_stat(cls, player: str, what_to_look_for: str, look_good: bool = False): # Original name: find_players_best_stat does exactly what the name says
        cls._ensure_initialized()

        if not isinstance(player, str):
            return {"error": f"players_name must be a string"}
        
        if not isinstance(what_to_look_for, str):
            return {"error": f"what_to_look_for must be a string"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        best_val = -1
        best_game = None
        best_quarter = None

        for game, game_stats in cls.data.items():
            for quarter, quarter_stats in game_stats["Quarters"].items():
                if player in quarter_stats and what_to_look_for in quarter_stats[player]:
                    value = quarter_stats[player][what_to_look_for]
                    if value > best_val:
                        best_val = value
                        best_game = game
                        best_quarter = quarter

        if best_val == -1:
            if look_good:
                return f"{player} has no recorded {what_to_look_for}"
            else:
                return None
        else:
            if look_good:
                return f"{player} got the most {what_to_look_for} ({best_val}) in {best_quarter} of {best_game}"
            else:
                return f"{what_to_look_for} {best_val}"
    
    @classmethod
    def check_player(cls, game: str, team: str, player: str, look_good: bool = False):
        cls._ensure_initialized()

        if not isinstance(game, str):
            return {"error": f"game must be a string"}
    
        if not isinstance(team, str):
            return {"error": f"team must be a string"}
        
        if not isinstance(player, str):
            return {"error": f"player_name must be a string"}
        
        if not isinstance(look_good, bool):
            return {"error": f"look_good must be a boolean"}

        if game not in cls.data:
            return {"error": f"Could not find Game: {game}"}
        
        game_stats = cls.data.get(game, {})

        if team not in game_stats["Lineup"]:
            return {"error": f"Could not find Team: {team}"}
        
        team_players = game_stats.get("Lineup").get(team)

        if player not in team_players:
            if look_good:
                output = f"{player} was not found in {game} of {team}"
                return output
            else:
                return False
        else:
            if look_good:
                output = f"{player} was found in {game} of {team}"
                return output
            else:
                return True
            
if __name__ == '__main__':
    app = AccessData()
    print(app.__repr__())