# Rated 760/1000
import sys
sys.path.extend(r"C:/Users/Drags Jrs/Drags")
import json
import os 
os.makedirs("C:/Users/Drags Jrs/Database/errors", exist_ok=True)
import shutil
import socket
import uuid
import urllib.request
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from utils import write 

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_public_ip() -> str:
    try:
        return urllib.request.urlopen("https://api.ipify.org").read().decode()
    except Exception as e:
        return socket.gethostbyname(socket.gethostname())
    
def create_log(
        level: str,
        message: str,
        where: str,
        error: Optional[Dict[str, Any]] = None,
        service_name: str = "access_data_service",
        host: str = socket.gethostname(),
        user_id: str = "N/A",
        source_ip: str = "N/A",
        request_id: str = str(uuid.uuid4())
) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "log_level": level,
        "service_name": service_name,
        "host": host,
        "message": message,
        "where": where,
        "user_id": user_id,
        "source_ip": source_ip,
        "request_id": request_id,
        **({"error": error} if error else {})
    }

class AccessData:
    data: Dict[str, Any] = {}
    file_path: str = ""
    _initialized: bool = False
    current_time = datetime.now()
    error_message = {}
    
    def __init__(self, user_id: str = "anonymous", source_ip: Optional[str] = None):
        self.user_id = user_id
        self.source_ip = source_ip
        self.request_id = str(uuid.uuid4())
        self.current_time = datetime.now(timezone.utc)
        self.error_message = {}
        
        try:
            self.initialize()
            log_entry = create_log(
                level="INFO",
                message="AccessData initialized successfully",
                where="__init__",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="AccessData initialized failed",
                where="__init__",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    def __repr__(self):
        self.error_message = {}
        try:
            game_count = len(self.data) if isinstance(self.data, dict) else 0 
            player_count = 0

            for game in self.data.values():
                if isinstance(game, dict) and "Lineup" in game:
                    for team in game["Lineup"].values():
                        player_count += len(team) if isinstance(team, list) else 0

            log_entry = create_log(
                level="INFO",
                message="__repr__ ran successfully",
                where="__repr__",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            
            return f"<AccessData file={self.file_path or 'Unknown'}\n games={game_count} players={player_count}>"
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="__repr__ failed",
                where="__repr__",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    
    def __str__(self):
        self.error_message = {}
        try:
            game_count = len(self.data) if isinstance(self.data, dict) else 0
            player_count = 0

            for game in self.data.values():
                if isinstance(game, dict) and "Lineup" in game:
                    for team in game["Lineup"].values():
                        player_count += len(team) if isinstance(team, list) else 0
            
            log_entry = create_log(
                level="INFO",
                message="__str__ ran successfully",
                where="__str__",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            
            return f"File: {self.file_path or "Unknown"}\n Games Loaded: {game_count}\n Total Players: {player_count}"

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="__str__ failed",
                where="__str__",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def _ensure_initialized(cls):
        cls.error_message = {}
        if not cls._initialized:
            cls()
            cls._initialized = True

    def initialize(self, load: bool = False, filename: str = "Data.json") -> Optional[Dict[str, Any]]:
        if not isinstance(load, bool):
            raise TypeError('load must be a bool')
                    
        if not isinstance(filename, str):
            raise TypeError('filename must be a str')
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.abspath(os.path.join(base_dir, "Database", filename))
        self.file_path = data_file

        if not os.path.isfile(data_file):
            raise FileNotFoundError("Could not find the file. Or wrong data format")
        
        try:
            with open(data_file, 'r', encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Invalid data format")
                AccessData.data = data

            log_entry = create_log(
                            level="INFO",
                            message="initialize ran successfully",
                            where="initialize",
                            user_id=self.user_id,
                            source_ip=self.source_ip,
                            request_id=self.request_id
                        )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

            if load:
                return AccessData.data
        
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="initialize failed",
                where="initialize",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
        
    def save(self, filename: Optional[str] = None, backup: bool = True) -> bool:
        if not isinstance(self.data, dict):
            raise TypeError('self.data must be a dict')
        
        save_path = filename or self.file_path
        if not save_path:
            raise TypeError('File path not set')
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            if backup and os.path.exists(save_path):
                backup_path = f"{save_path}.bak"
                shutil.copy2(save_path, backup_path)
            
            temp_path = f"{save_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as temp_file:
                json.dump(self.data, temp_file, indent=4, ensure_ascii=False)

            os.replace(temp_path, save_path)

            log_entry = create_log(
                            level="INFO",
                            message="save ran successfully",
                            where="save",
                            user_id=self.user_id,
                            source_ip=self.source_ip,
                            request_id=self.request_id
                        )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

            return True
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="save failed",
                where="save",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def get_details(cls, game: str, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str): 
                raise TypeError("game must be a string")
                        
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")
            if not game or game not in cls.data:
                raise KeyError("Could not find the game")

            game_stats = cls.data.get(game, {})

            details = game_stats.get("Details", {})

            if look_good:
                output = ["--------------------- Details ------------------------"]
                for detail, stat in details.items():
                    output.append(f"{detail}: {stat}")
                output.append("--------------------------------------------------")

                log_entry = create_log(
                            level="INFO",
                            message="get_details ran successfully",
                            where="get_details",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                return "\n".join(output)
            else:

                log_entry = create_log(
                            level="INFO",
                            message="get_details ran successfully",
                            where="get_details",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                return details.copy()
            
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_details failed",
                where="get_details",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    @classmethod
    def get_lineup(cls, game: str, team: str, look_good: bool =False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")
            
            if not isinstance(team, str):
                raise TypeError("team must be a string")
                
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            game_stats = cls.data.get(game, {})
            
            if not game_stats:
                raise KeyError("Could not find the game")

            team_players = game_stats.get("Lineup", {}).get(team, [])
            
            if not team_players:
                raise KeyError("Could not find the team")
            
            if look_good:
                output = ["----------------- Team players ----------------------"]
                for num, player in enumerate(team_players, start=1):
                    output.append(f"{num}. {player}")
                
                log_entry = create_log(
                            level="INFO",
                            message="get_lineup ran successfully",
                            where="get_lineup",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return "\n\n".join(output)
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_lineup ran successfully",
                            where="get_lineup",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return team_players.copy()
            
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_lineup failed",
                where="get_lineup",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
    @classmethod
    def get_quarter_stats(cls, game: str, quarter: str, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")
            
            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            game_stats = cls.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")

            quarters = game_stats.get("Quarters")
            quarter_stats = quarters.get(quarter, {})

            if not quarter_stats:
                raise KeyError("Could not find the quarter")
            
            if look_good:
                output = [f"-------------------- {game}: {quarter} stats --------------------------"]
                for players_name, players_stats in quarter_stats.items():
                    stat_line = ", ".join(f"{stat_name}: {stat_value}" for stat_name, stat_value in players_stats.items())
                    output.append(f"{players_name}: {stat_line}\n")
                
                log_entry = create_log(
                            level="INFO",
                            message="get_quarter_stats ran successfully",
                            where="get_quarter_stats",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return "\n".join(output)
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_quarter_stats ran successfully",
                            where="get_quarter_stats",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return quarter_stats.copy()
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_quarter_stats failed",
                where="get_quarter_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def get_specific_stats(cls, game: str, quarter: str, player: str, look_good: bool = False): # Original name: find_a_players_quarter_stats and gets specific stats for a player
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")

            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")

            if not isinstance(player, str):
                raise TypeError("player must be a string")

            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            game_stats = cls.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")
            
            quarter_stats = game_stats.get("Quarters").get(quarter, {})
            if not quarter_stats:
                raise KeyError("Could not find the quarter")
            
            players_stats = quarter_stats.get(player, {})
            if not players_stats:
                raise KeyError("Could not find the player")
            
            if look_good:
                output = f"-------------------- {player} stats in {game} in {quarter} ----------------------------\n"
                for stat_name, stat_value in players_stats.items():
                    output += f"    - {stat_name}: {stat_value}\n"
                
                log_entry = create_log(
                            level="INFO",
                            message="get_specific_stats ran successfully",
                            where="get_specific_stats",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return output
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_specific_stats ran successfully",
                            where="get_specific_stats",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return players_stats
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_specific_stats failed",
                where="get_specific_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def get_game_stats(cls, game: str, player: str, look_good: bool = False): # Original name: get_total_stats sums up a games stats
        try:
            cls._ensure_initialized()
            
            if not isinstance(game, str):
                raise TypeError("game must be a string")

            if not isinstance(player, str):
                raise TypeError("player must be a string")

            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")
            
            game_stats = cls.data.get(game, {})
            
            if not game_stats:
                raise KeyError("Could not find the game")
            
            quarters = game_stats.get("Quarters", {})
            if not quarters:
                raise KeyError("Quarters not found")
            
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
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_game_stats ran successfully",
                                where="get_game_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return "\n".join(formatted)
                else:
                    lines = [f"------------------ Game: {game} Stats ------------------------\n"]
                    for player_name, stats in totals.items():
                        stat_line = ", ".join(f"{key}: {value}" for key, value in stats.items())
                        lines.append(f"{player_name}: {stat_line}")
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_game_stats ran successfully",
                                where="get_game_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return "\n".join(lines)
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_game_stats ran successfully",
                            where="get_game_stats",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                
                return totals if not player else totals.get(player, {})
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_game_stats failed",
                where="get_game_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    
    @classmethod
    def get_season_stats(cls, player: str, sum_total: bool = False, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(player, str):
                raise TypeError("player must be a string")
            
            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

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
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_season_stats ran successfully",
                                where="get_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_season_stats ran successfully",
                                where="get_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
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

                if look_good:
                    output = f"------------------------- Game stats for {player} -------------------------------\n"
                    for game_name, game_stats in game_totals.items():
                        output += f"----------- {game_name} stats: ------------\n"
                        for stat_name, stat_value in game_stats.items():
                            output += f"    - {stat_name}: {stat_value}\n"
                            if stat_name == "Turnovers":
                                output += "\n"
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_season_stats ran successfully",
                                where="get_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return output        
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_season_stats ran successfully",
                                where="get_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return game_totals
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_season_stats failed",
                where="get_season_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    @classmethod
    def get_team_season_stats(cls, sum_total: bool = False, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            if sum_total:
                team_totals = {}

                for game_name, game_data in cls.data.items():
                    for quarter_name, quarter_stats in game_data["Quarters"].items():
                        for players_name, players_stats in quarter_stats.items():
                            if players_name not in team_totals:
                                team_totals[players_name] = {}
                            for stat_name, stat_value in players_stats.items():
                                team_totals[players_name][stat_name] = team_totals[players_name].get(stat_name, 0) + stat_value
                
                if look_good:
                    output = "---------------- Newport Raiders U16 Boys Julie Season stats ----------------\n"

                    for team_players_name, team_players_stats in team_totals.items():
                        output += f"\n                       {team_players_name}                               \n"
                        for team_players_stat_name, team_players_stat_value in team_players_stats.items():
                            output += f"                            - {team_players_stat_name}: {team_players_stat_value}\n"
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_team_season_stats ran successfully",
                                where="get_team_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_team_season_stats ran successfully",
                                where="get_team_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return team_totals
            else:
                game_team_totals = {}
                    
                for game_name, game_data in cls.data.items():
                    
                    player_total = {}

                    for quarter_name, quarter_stats in game_data["Quarters"].items():
                        for players_name, players_data in quarter_stats.items():
                            if players_name not in player_total:
                                player_total[players_name] = {}
                            for player_stat_name, player_stat_value in players_data.items():
                                player_total[players_name][player_stat_name] = player_total[players_name].get(player_stat_name, 0) + player_stat_value

                    game_team_totals[game_name] = player_total
                
                if look_good:
                    output = ""
                    output += f"---------------------- Newport Raiders U16 Boys Julie Season stats ----------------------\n"
                    for game_stat_name, game_stat_value in game_team_totals.items():
                        output += f"\n\n{game_stat_name}                                   \n"
                        for players_name, players_stats in game_stat_value.items():
                            output += f"\n\n{players_name}                                     \n"
                            for stat_name, stat_value in players_stats.items():
                                output += f"\n{stat_name}: {stat_value}                       "
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_team_season_stats ran successfully",
                                where="get_team_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_team_season_stats ran successfully",
                                where="get_team_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return game_team_totals
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_team_season_stats failed",
                where="get_team_season_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def get_quarter_season_stats(cls, player: str, quarter: str, sum_total: bool = False, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(player, str):
                raise TypeError("player must be a string")
            
            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")
            
            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            totals = {}

            if quarter not in cls.data.get("Game_1", {}).get("Quarters", {}):
                raise KeyError("Could not find the quarter")

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
                    
                    log_entry = create_log(
                                level="INFO",
                                message="get_quarter_season_stats ran successfully",
                                where="get_quarter_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_quarter_season_stats ran successfully",
                                where="get_quarter_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
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

                if look_good:
                    output = f"============= Seasons {quarter} stats for {player} =============\n"

                    for game_stat_name, game_stats in game_totals.items():
                        output += f"    ---------------- Game: {game_stat_name} {quarter} stats ----------------\n"                    
                        for game_Stat_name, game_stat_value in game_stats.items():
                            output += f"       - {game_Stat_name}: {game_stat_value}\n"

                    log_entry = create_log(
                                level="INFO",
                                message="get_quarter_season_stats ran successfully",
                                where="get_quarter_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_quarter_season_stats ran successfully",
                                where="get_quarter_season_stats",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    
                    return game_totals
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_quarter_season_stats failed",
                where="get_quarter_season_stats",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

    @classmethod
    def get_highest_stats_quarter(cls, game: str, quarter: str, what_to_look_for: str, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")
            
            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")
            
            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            game_stats = cls.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")
            
            quarter_stats = game_stats.get("Quarters").get(quarter, {})

            if not quarter_stats:
                raise KeyError("Could not find the quarter")
            
            nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in quarter_stats.items()]

            if not nums:
                if look_good:
                    error_msg = f"Stat: {what_to_look_for} not found"
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_quarter ran successfully",
                                where="get_highest_stats_quarter",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return error_msg
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_quarter ran successfully",
                                where="get_highest_stats_quarter",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return None
            
            max_stat_value = max(value for _, value in nums)

            if max_stat_value == 0:
                if look_good:
                    msg = f"No one got any {what_to_look_for} in {game} of {quarter}"
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_quarter ran successfully",
                                where="get_highest_stats_quarter",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return msg
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_quarter ran successfully",
                                where="get_highest_stats_quarter",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return None

            top_players = [player for player, value in nums if value == max_stat_value]

            resultstr = f"{top_players[0]}: {max_stat_value}" if len(top_players) == 1 else f"Tied at {max_stat_value} {what_to_look_for}: {', '.join(top_players)}"
            
            if look_good:
                result = f"In {quarter} of {game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
                
                log_entry = create_log(
                            level="INFO",
                            message="get_highest_stats_quarter ran successfully",
                            where="get_highest_stats_quarter",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                return result
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_highest_stats_quarter ran successfully",
                            where="get_highest_stats_quarter",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                return {player: max_stat_value for player in top_players}
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_highest_stats_quarter failed",
                where="get_highest_stats_quarter",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)


    @classmethod
    def get_highest_stats_game(cls, game: str, what_to_look_for: str, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")
            
            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            game_stats = cls.get_game_stats(game=game, player="", look_good=False)
            if not game_stats:
                raise KeyError("Could not find the game")
            
            nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in game_stats.items() if what_to_look_for in stats]

            if not nums:
                raise KeyError(f"No stats found for {what_to_look_for}")
            
            max_value = max(value for _, value in nums)

            if max_value == 0:
                msg = f"Could not find {what_to_look_for} in {game}"
                if look_good:
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_game ran successfully",
                                where="get_highest_stats_game",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return msg
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="get_highest_stats_game ran successfully",
                                where="get_highest_stats_game",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return None

            top_players = [player for player, value in nums if value == max_value]

            resultstr = f"{top_players[0]}: {max_value}" if len(top_players) == 1 else f"Tied at {max_value} {what_to_look_for}: {', '.join(top_players)}"

            if look_good:
                result = f"In {game}, the {'leader' if len(top_players) == 1 else 'leaders'} for {what_to_look_for} was: {resultstr}"
                
                log_entry = create_log(
                            level="INFO",
                            message="get_highest_stats_game ran successfully",
                            where="get_highest_stats_game",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                return result
            else:
                log_entry = create_log(
                            level="INFO",
                            message="get_highest_stats_game ran successfully",
                            where="get_highest_stats_game",
                            user_id=cls.user_id,
                            source_ip=cls.source_ip,
                            request_id=cls.request_id
                        )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                return {player: max_value for player in top_players}            
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_highest_stats_game failed",
                where="get_highest_stats_game",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    @classmethod
    def specific_players_best_stat(cls, player: str, what_to_look_for: str, look_good: bool = False): # Original name: find_players_best_stat does exactly what the name says
        try:
            cls._ensure_initialized()

            if not isinstance(player, str):
                raise TypeError("player must be a string")
            
            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")
            
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

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
                    raise  TypeError(f"{player} has no recorded {what_to_look_for}")
                else:
                    return TypeError(f"{player} has no recorded {what_to_look_for}")
            else:
                if look_good:
                    log_entry = create_log(
                                level="INFO",
                                message="specific_players_best_stat ran successfully",
                                where="specific_players_best_stat",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                    return f"{player} got the most {what_to_look_for} ({best_val}) in {best_quarter} of {best_game}"
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="specific_players_best_stat ran successfully",
                                where="specific_players_best_stat",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                    return f"{what_to_look_for} {best_val}"
                
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="specific_players_best_stat failed",
                where="specific_players_best_stat",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
    
    @classmethod
    def check_player(cls, game: str, team: str, player: str, look_good: bool = False):
        try:
            cls._ensure_initialized()

            if not isinstance(game, str):
                raise TypeError("game must be a string")
        
            if not isinstance(team, str):
                raise TypeError("team must be a string")
            
            if not isinstance(player, str):
                raise TypeError("player must be a string")
            if not isinstance(look_good, bool):
                raise TypeError("look_good must be a bool")

            if game not in cls.data:
                raise KeyError("game not in the dataset")
            
            game_stats = cls.data.get(game, {})

            if team not in game_stats["Lineup"]:
                raise KeyError("team not in the game")
            
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
                    log_entry = create_log(
                                level="INFO",
                                message="check_player ran successfully",
                                where="check_player",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                    return output
                else:
                    log_entry = create_log(
                                level="INFO",
                                message="check_player ran successfully",
                                where="check_player",
                                user_id=cls.user_id,
                                source_ip=cls.source_ip,
                                request_id=cls.request_id
                            )
                    write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                    return True
    
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="check_player failed",
                where="check_player",
                error=error,
                user_id=cls.user_id,
                source_ip=cls.source_ip,
                request_id=cls.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

if __name__ == '__main__':
    app = AccessData()


# ============================================================================
# END OF FILE: accessing_data.py
# ============================================================================
# MODULE: Basketball Data Access Layer System 
# LOCATION: C:/Users/Drags Jrs/Drags/utils/accessing_data.py
# ============================================================================
# IF NEEDED: If you want the full docstring go to docs/accessing_data_doc.md
#=============================================================================

# ============================================================================
# FILE STATISTICS
# ============================================================================
# TOTAL CLASSES: 1 (AccessData)
# TOTAL METHODS: 18
# TOTAL FUNCTIONS (NOT IN CLASS): 2
# TOTAL FUNCTIONS AND METHODS: 20 
# TOTAL LINES: ~1000 
# ============================================================================

# ============================================================================
# FEATURE SUMMARY
# ============================================================================
#   1. UTILITY FUNCTIONS
#      
#    -    get_public_ip(): Retrieves public IP address with fallback to local hostname
#    -    create_log(): Generates structured JSON log entries with contextual metadata
#   
#   2. INITIALIZATION & REPRESENTATION
#
#    -   __init__: Initializes instance with user tracking, UUID generation, and automatic data loading
#    -   __repr__: Returns compact representation with game/player counts
#    -   __str__: Returns formatted string representation with statistics summary
#
#   3. DATA MANAGEMENT 
#
#    -   initialize(): Loads JSON data with validation and error logging
#    -   save(): Persists data with automatic backups and atomic write operations
#    -   _ensure_initialized(): Classmethod ensuring singleton-like initialization
#
#   4. QUERY METHODS (ALL CLASSMETHODS - RETURN RAW OR FORMATTED DATA) 
#
#    -  get_details(): Game metadata retrieval
#    -  get_lineup(): Team roster lookup
#    -  get_quarter_stats(): Quarter-level statistics
#    -  get_specific_stats(): Player stats for specific quarter
#    -  get_game_stats(): Aggregated game statistics by player
#    -  get_season_stats(): Player performance across all games
#    -  get_team_season_stats(): Full team season statistics
#    -  get_quarter_season_stats(): Quarter-specific season aggregates
#    -  get_highest_stats_quarter(): Find leading player in quarter for stat type
#    -  get_highest_stats_game(): Find leading player in game for stat type
#    -  specific_players_best_stat(): Player's best performance for specific stat
#    -  check_player(): Verify player participation in game
#
# ============================================================================
# ============================================================================
# PERFORMANCE NOTES
# ============================================================================
#   
#   STRENGTHS
#
#       - Class data as shared dictionary avoids redundant loads
#       - Atomic file operations prevent corruption
#       - Type hints enable IDE optimization
#       - Early returns in aggregation methods
# 
#   CONCERNS (WILL TRY AND FIX)
#
#       - Full aggregation: get_season_stats() iterates entire dataset every call
#       - Repeated string operations: Multiple .get() calls and .format() operations
#       - Memory overhead: Every look_good=True call creates large formatted strings
#       - JSON file locking: save() blocks on I/O with no async support
#   
#   SCALABILITY ISSUES
#       - Large datasets (1000+ games) will suffer from O(n) iterations
#       - No caching mechanism for frequently accessed aggregates
#       - Logging to JSON sequentially creates I/O bottleneck
#
# ============================================================================

# ============================================================================
# DEPENDENCIES
# ============================================================================
#   EXTERNAL
#
#       - json: Data serialization
#       - os: File/directory operations
#       - shutil: File backup operations
#       - socket: Hostname/IP resolution
#       - uuid: Request tracking
#       - urllib.request: Public IP lookup
#       - typing: Type hints
#       - datetime: Timestamps and timezone handling
#       - utils.write: Custom logging module (required)
#
#   INTERNAL
#
#       - Circular dependency risk: write module must exist and be importable
#
# ============================================================================

# ============================================================================
# DESIGN PATTERNS USED
# ============================================================================
#
#   SINGLETON-LIKE CLASS DATA
# 
#       - Shared class-level data dict reduces memory/load overhead
#       - Risk: Thread-unsafe mutations
#
#   CLASSMETHODS QUERY PATTERN
#
#       - Most methods are classmethods accessing shared data
#       - Advantage: No instance creation needed
#       - Disadvantage: Breaks encapsulation; all instances share state
#
#   OPTIONAL FORMATTING PATTERN
# 
#       - look_good parameter returns formatted vs. raw data
#       - Mixing presentation logic with data access violates SRP
#
#   REQUEST TRACKING
#
#       - UUID per operation enables request tracing
#       - Logged metadata for audit trails
#
#   DECORATOR-LIKE ERROR HANDLING
#   
#       - Try/except in every method logs to same JSON file
#       - Verbose but comprehensive error tracking
#
# ============================================================================

# ============================================================================
# FUTURE ENHANCEMENTS
# ============================================================================
#   
#   SHORT TERM (1-2 MONTHS)
#   
#       - Add caching layer: LRU cache for frequently accessed queries
#       - Optimize aggregations: Build indices on game/player names
#       - Async logging: Move log writes to thread pool
#       - Separate concerns: Create QueryBuilder and Formatter classes
#       - Batch operations: Add get_multiple_players_stats() method
#       - Query optimization: Cache season aggregates, invalidate on save
#
#   LONG TERM (3-6 MONTHS)
#
#       === Database migration: Replace JSON with SQLite/PostgreSQL ===
#           
#           - Enable complex queries without full-dataset iteration
#           - Add transactions for data consistency
#
#       - Analytics API: Pre-compute rankings, trends, percentiles
#       - Time-series support: Track stat changes across season
#       - Multi-season support: Current design assumes single season
#       - Data validation schema: JSONSchema or Pydantic models
#       - Rate limiting: Prevent abuse of expensive querie
#       - Audit logs: Separate write operations to audit table
#       - API layer: REST endpoints for remote data access
#
# ============================================================================

# ============================================================================
# TESTING RECOMMENDATIONS
# ============================================================================
#
#   UNIT TESTS
#       
#       - Test initialization with missing file
#       - Test save with corrupted data recovery
#       - Test type validation on all parameters
#       - Test edge cases (empty lineup, zero stats, tied leaders)
#       - Test classmethod state isolation
#
#   INTEGRATION TESTS
#
#       - Load real JSON, verify aggregation accuracy
#       - Backup file creation on save
#       - Log file format and completeness
#       - Error propagation and recovery'
#
#   PERFORMANCE TESTS 
#       
#       - Benchmark with 500+ games
#       - Profile memory usage for look_good=True calls
#       - Measure aggregation time for season stats
#
#   Edge Cases
#   
#       - Empty data structures
#       - Tied statistics (multiple players with same max)
#       - Missing keys in nested dictionaries
#       - Unicode player names
#       - Concurrent classmethod calls
#
#   LOAD TESTING
#   
#       - Stress test with 10,000+ queries
#       - Database connection pooling requirements
# ============================================================================

# ============================================================================
# MAINTENANCE NOTES
# ============================================================================
#   CURRENT DEBT
#
#       - Inconsistent error handling: Some methods raise, others return None
#       - Hardcoded paths: Database paths embedded in methods (should use config)
#
#   CORE MAINTENANCE
# 
#       - Remove duplicate error handling code (20+ nearly identical try/except blocks)
#       - Extract common patterns into private methods
#       - Document JSON schema expectations
#       - Add constants for magic strings (stat names, team names)
#       - Create config file for hardcoded paths
#   
#   MONITORING 
#
#       - Set up alerts for JSON log file size growth
#       - Monitor file I/O performance
#       - Track query response times
#       - Alert on unhandled exceptions
#
#   BACKWARDS COMPATIBILITY
# 
#       - Changing method signatures breaks API
#       - Consider versioning for JSON schema changes
#       - Add deprecation warnings before method renames
# 
#   DOCUMENTATION 
# 
#       - Add class-level docstring describing data structure
#       - Document required JSON schema with example
#       - Add usage examples for common queries
#       - Create migration guide for future database move
# ============================================================================
3
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
# - Newport Raiders U16 Boys Julie team for the use case and test
# - Shout out to again to the Newport Raiders U16 Boys Julie team for everything 
# - Don't forget my parents for helping me and giving the motivation to keep going
# - And sadly my brother, for nothing...   
# ============================================================================