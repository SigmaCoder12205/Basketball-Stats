# Rated 740/1000

import json
from pathlib import Path

class AccessData:
    data = {}
    _initialized = False

    def __init__(self):
        self.Initialize()

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            instance = cls()
            cls._initialized = True

    def Initialize(self, load=False, filename="Data.json"):
        try:
            data_file = r"C:\Users\Drags Jrs\Mylesbasketballstatsanddata\Database\Data.json"
            with open(data_file, "r") as file:
                AccessData.data = json.load(file)
                
        except FileNotFoundError:
            print(f"File not found: {data_file}") 
            return None
        except json.JSONDecodeError:
            print(f"Error reading JSON from {data_file}")  
            return None
        except Exception as e:
            print(f"Unknown error: {e}")
            return None
        
        if load:
            return AccessData.data

        
    @classmethod
    def Get_details(cls, game=None, look_good=False): # Original name: quick_game_details gets the details in a game 
        cls._ensure_initialized()
        if not game or game not in cls.data:
            return {"Error": f"Invalid game: {game}"}

        game_stats = cls.data.get(game, {})

        if game_stats == {}:
            return {"Error": f"Game: {game} not found"}

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
    def Get_a_lineup(cls, game=None, team=None, look_good=False): # Original name: get_a_team gets a lineup in a game
        cls._ensure_initialized()
        game_stats = cls.data.get(game, {})

        if not game_stats:
            return {"Error": f"{game} is not valid"}

        team_players = game_stats.get("Lineup", {}).get(team, [])
        
        if not team_players:
            return {"error": f"{team} not found in {game}"}
        
        if look_good:
            output = ["----------------- Team players ----------------------"]
            for num, player in enumerate(team_players, start=1):
                output.append(f"{num}. {player}")
            return "\n\n".join(output)
        else:
            return team_players
    
    @classmethod
    def Get_quarter_stats(cls, game=None, quarter=None, look_good=False): # Same name gets quarter stats
        cls._ensure_initialized()
        game_stats = cls.data.get(game, {})

        if not game_stats:
            return {"error": f"Game: {game} not found"}
        
        quarters = game_stats.get("Quarters")
        quarter_stats = quarters.get(quarter, {})

        if not quarter_stats:
            return {"error": f"Quarter: {quarter} not found"}
        
        if look_good:
            output = [f"-------------------- {game}: {quarter} stats --------------------------"]
            for players_name, players_stats in quarter_stats.items():
                stat_line = ", ".join(f"{stat_name}: {stat_value}" for stat_name, stat_value in players_stats.items())
                output.append(f"{players_name}: {stat_line}\n")
            return "\n".join(output)
        else:
            return quarter_stats.copy()

    @classmethod
    def Get_specific_Stats(cls, Game=None, the_quarter=None, player_name=None, look_good=False): # Original name: find_a_players_quarter_stats and gets specific stats for a player
        cls._ensure_initialized()
        game = cls.data.get(Game, {})
        if not game:
            return {"error": f"{Game} not found"}
        
        quarter_stats = game.get("Quarters").get(the_quarter, {})
        if not quarter_stats:
            return {'error': f'Quarter: {the_quarter} not found'}
        
        players_stats = quarter_stats.get(player_name, {})
        if not players_stats:
            return {"error": f"Player: {player_name} not found"}
        
        if look_good:
            output = f"-------------------- {player_name} stats in {Game} in {the_quarter} ----------------------------\n"
            for stat_name, stat_value in players_stats.items():
                output += f"    - {stat_name}: {stat_value}\n"
            return output
        else:
            return players_stats

    @classmethod
    def Get_game_stats(cls, game_id=None, player=None, look_good=False): # Original name: get_total_stats sums up a games stats
        cls._ensure_initialized()
        game = cls.data.get(game_id, {})
        if not game:
            return {"error": f"{game_id} not found"}
        
        quarters = game.get("Quarters", {})
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
                formatted = [f"------------------ Game: {game_id} ------------------\n"]
                player_stats = totals.get(player, {})
                formatted.extend( f"{stat}: {value}" for stat, value in player_stats.items())
                return "\n".join(formatted)
            else:
                lines = [f"------------------ Game: {game_id} Stats ------------------------\n"]
                for player_name, stats in totals.items():
                    stat_line = ", ".join(f"{key}: {value}" for key, value in stats.items())
                    lines.append(f"{player_name}: {stat_line}")
                return "\n".join(lines)
        else:
            return totals if not player else totals.get(player, {})
    
    @classmethod
    def Get_season_stats(cls, players_name, sum_total=False, look_good=False): # Original name: player_season_stat this sums up all the games for a player if sum_total = True otherwise just shows every game and their stats
        cls._ensure_initialized()
        total = {}

        if sum_total:
            for game_name, game_stats in cls.data.items():
                for quarter, quarter_stats in game_stats["Quarters"].items():
                    if players_name in quarter_stats:
                        for stat_name, stat_value in quarter_stats[players_name].items():
                            total[stat_name] = total.get(stat_name, 0) + stat_value                          

            if look_good:
                output = f"Season stats for {players_name}\n"
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
                    if players_name in quarter_stats:
                        for players_stat_name, players_stat_value in quarter_stats[players_name].items():
                            players_total[players_stat_name] = players_total.get(players_stat_name, 0) + players_stat_value
                
                if players_total:
                    game_totals[game_name] = players_total
            
            # {'Game_1': {'Points': 0, 'Fouls': 1, 'Rebounds': 1, 'Assists': 1, 'Turnovers': 5}, 'Game_2': {'Points': 3, 'Fouls': 2, 'Rebounds': 1, 'Assists': 2, 'Turnovers': 1}, 'Game 3': {'Points': 0, 'Fouls': 4, 'Rebounds': 1, 'Assists': 0, 'Turnovers': 0}}

            if look_good:
                output = f"------------------------- Game stats for {players_name} -------------------------------\n"
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
    def Get_team_season_stats(cls, sum_total=False, look_good=False):
        cls._ensure_initialized()
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
    def Get_quarter_season_stats(cls, player_name, what_quarter, sum_total=False, look_good=False): # Made by me does the same thing as get_season_stats but only for quarter stats 
        cls._ensure_initialized()
        totals = {}

        if what_quarter not in cls.data["Game_1"]["Quarters"]:
            return {"Error": f"Quarter: {what_quarter} not found"}

        if sum_total:
            for game_name, game_stats in cls.data.items():
                if what_quarter in game_stats["Quarters"]:
                    if player_name in game_stats["Quarters"][what_quarter]:
                        for stat, value in game_stats["Quarters"][what_quarter][player_name].items():
                            totals[stat] = totals.get(stat, 0) + value

            if look_good:
                output = f"All of {what_quarter} stats together for {player_name}\n"
                for stat, value in totals.items():
                    output += f"    - {stat}: {value}\n"
                return output
            else:
                return totals       
        else:
            game_totals = {}

            for game_name, game_stats in cls.data.items():

                players_totals = {}

                if what_quarter in game_stats["Quarters"]:
                    if player_name in game_stats["Quarters"][what_quarter]:
                        for stat_name, stat_value in game_stats["Quarters"][what_quarter][player_name].items():
                            players_totals[stat_name] = players_totals.get(stat_name, 0) + stat_value
                
                if players_totals:
                    game_totals[game_name] = players_totals            

            
        
            # {'Game_1': {'Points': 0, 'Fouls': 1, 'Rebounds': 1, 'Assists': 1, 'Turnovers': 4}, 'Game_2': {'Points': 0, 'Fouls': 1, 'Rebounds': 0, 'Assists': 1, 'Turnovers': 0}, 'Game 3': {'Points': 0, 'Fouls': 2, 'Rebounds': 0, 'Assists': 0, 'Turnovers': 0}}
            if look_good:
                output = f"============= Seasons {what_quarter} stats for {player_name} =============\n"

                for game_stat_name, game_stats in game_totals.items():
                    output += f"    ---------------- Game: {game_stat_name} {what_quarter} stats ----------------\n"                    
                    for game_Stat_name, game_stat_value in game_stats.items():
                        output += f"       - {game_Stat_name}: {game_stat_value}\n"

                return output
            else:
                return game_totals

    @classmethod
    def Get_highest_stats_quarter(cls, Game, Quarter, what_to_look_for, look_good=False): # Original name: find_a_players_quarter_stats finds out who got the most stats in a quarter
        cls._ensure_initialized()
        game = cls.data.get(Game, {})

        if not game:
            return {"Error": f"Game: {Game} not found"}
        
        quarter_stats = game.get("Quarters").get(Quarter, {})

        if not quarter_stats:
            return {"Error": f"Quarter: {Quarter} not found"}
        
        nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in quarter_stats.items()] # all stats like points fouls blah blah blah

        if not nums:
            if look_good:
                return {"Error": f"stat: {what_to_look_for} not found"}
            else:
                return None
        
        max_stat_value = max(value for _, value in nums)

        if max_stat_value == 0:
            if look_good:
                return f"No one got any {what_to_look_for} in {Game} of {Quarter}"
            else:
                return None

        top_players = [player for player, value in nums if value == max_stat_value]


        resultstr = f"{top_players[0]}: {max_stat_value}"if len(top_players) == 1 else f"Tied at {max_stat_value} {what_to_look_for}: {', '.join(top_players)}"
        
        if look_good:
            return f"In {Quarter} of {Game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
        else:
            return {player: max_stat_value for player in top_players}


    @classmethod
    def Get_highest_stats_game(cls, Game, what_to_look_for, look_good=False): # Original name: highest_stats_game does the same as get_highest_stats_quarter but does it for a game
        cls._ensure_initialized()
        game_stats = cls.Get_game_stats(Game)
        if not game_stats:
            return {'error': f'Game: {Game} not found'}
        
        nums = [(player, stats.get(what_to_look_for,0)) for player, stats in game_stats.items() if what_to_look_for in stats]

        if not nums:
            return {'error': f'Stats: No Stats for {what_to_look_for} in {Game}' if look_good else None}
        
        max_value = max(value for _, value in nums)

        if max_value == 0:
            if look_good:
                return f"No {what_to_look_for} was found in {Game}"
            else:
                return None

        top_players = [player for player, value in nums if value == max_value]

        resultstr = (f"{top_players[0]}: {max_value}" if len(top_players) == 1 else f"Tied at {max_value} {what_to_look_for}: {', '.join(top_players)}")

        if look_good:
            return f"In {Game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
        else:
            return {player: max_value for player in top_players}            
        
    @classmethod
    def Specific_players_best_stat(cls, players_name, what_to_look_for, look_good=False): # Original name: find_players_best_stat does exactly what the name says
        cls._ensure_initialized()
        best_val = -1
        best_game = None
        best_quarter = None

        for game, game_stats in cls.data.items():
            for quarter, quarter_stats in game_stats["Quarters"].items():
                if players_name in quarter_stats and what_to_look_for in quarter_stats[players_name]:
                    value = quarter_stats[players_name][what_to_look_for]
                    if value > best_val:
                        best_val = value
                        best_game = game
                        best_quarter = quarter

        if best_val == -1:
            if look_good:
                return f"{players_name} has no recorded {what_to_look_for}"
            else:
                return None
        else:
            if look_good:
                return f"{players_name} got the most {what_to_look_for} ({best_val}) in {best_quarter} of {best_game}"
            else:
                return f"{what_to_look_for} {best_val}"
    
    @classmethod
    def Check_player(cls, what_game, team, players_name, look_good=False): # check if a player played in a specific game
        cls._ensure_initialized()
        if what_game not in cls.data:
            return {"error": f"Could not find Game: {what_game}"}
        
        game_stats = cls.data.get(what_game, {})

        if team not in game_stats["Lineup"]:
            return {"error": f"Could not find Team: {team}"}
        
        team_players = game_stats.get("Lineup").get(team)

        if players_name not in team_players:
            if look_good:
                output = f"{players_name} was not found in {what_game} of {team}"
                return output
            else:
                return False
        else:
            if look_good:
                output = f"{players_name} was found in {what_game} of {team}"
                return output
            else:
                return True