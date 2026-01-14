# Rated 760/1000
import sys
from pathlib import Path
try:
    from utils import write
except ImportError:
    import write
try:
    from utils.logging import Logging
except ImportError:
    from logging import Logging
import json
import os
import shutil
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from functools import lru_cache
import pprint

BASE = Path.home() / "Drags"
DB_ERRORS = Path.home() / "Database" / "errors"
DB_ERRORS.mkdir(parents=True, exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.extend([str(BASE)])
sys.path.insert(0, str(PROJECT_ROOT))

logger = Logging(service_name="access_data_service", user_id="N/A")
create_log = logger.create_log

class AccessData:
    data: Dict[str, Any] = None
    file_path: str = ""
    _initialized: bool = False
    current_time = datetime.now()
    error_message = {}
    user_id: str = "N/A"
    source_ip: str = "N/A"
    request_id: str = "N/A"

    def __init__(self, user_id: str = "anonymous", source_ip: Optional[str] = None):
        self.user_id = user_id
        self.source_ip = source_ip
        self.request_id = str(uuid.uuid4())
        self.current_time = datetime.now(timezone.utc)
        self.error_message = {}
        if AccessData.data is None:
            AccessData.data = {}

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
            return log_entry

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
            return log_entry

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

        # Navigate from src/utils/accessing_data.py up to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
            return log_entry

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
            return log_entry

    def get_details(self, game: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not game or game not in self.data:
                return {'error': f"game was not found in the dataset: {game}"}

            game_stats = self.data.get(game, {})

            details = game_stats.get("Details", {})

            log_entry = create_log(
                        level="INFO",
                        message="get_details ran successfully",
                        where="get_details",
                        user_id=self.user_id,
                        source_ip=self.source_ip,
                        request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def get_lineup(self, game: str, team: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {game}"}

            if not isinstance(team, str):
                return {'error': f"team must be a string not {team}"}

            game_stats = self.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")

            team_players = game_stats.get("Lineup", {}).get(team, [])

            if not team_players:
                raise KeyError("Could not find the team")
            log_entry = create_log(
                        level="INFO",
                        message="get_lineup ran successfully",
                        where="get_lineup",
                        user_id=self.user_id,
                        source_ip=self.source_ip,
                        request_id=self.request_id
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
                  user_id=self.user_id,
                  source_ip=self.source_ip,
                  request_id=self.request_id
              )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

            return log_entry

    def get_quarter_stats(self, game: str, quarter: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not isinstance(quarter, str):
                return {'error': f"quarter must be a string not {type(quarter)}"}

            game_stats = self.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")

            quarters = game_stats.get("Quarters")
            quarter_stats = quarters.get(quarter, {})

            if not quarter_stats:
                raise KeyError("Could not find the quarter")

            log_entry = create_log(
                        level="INFO",
                        message="get_quarter_stats ran successfully",
                        where="get_quarter_stats",
                        user_id=self.user_id,
                        source_ip=self.source_ip,
                        request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def get_specific_stats(self, game: str, quarter: str, player: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not isinstance(quarter, str):
                return {'error': f"quarter must be a string not {type(quarter)}"}

            if not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}

            game_stats = self.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")

            quarter_stats = game_stats.get("Quarters", {}).get(quarter, {})
            if not quarter_stats:
                raise KeyError("Could not find the quarter")

            players_stats = quarter_stats.get(player, {})
            if not players_stats:
                raise KeyError("Could not find the player")


            log_entry = create_log(
                        level="INFO",
                        message="get_specific_stats ran successfully",
                        where="get_specific_stats",
                        user_id=self.user_id,
                        source_ip=self.source_ip,
                        request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def get_game_stats(self, game: str, player: str = None):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if player is not None and not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}

            game_stats = self.data.get(game, {})

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

            log_entry = create_log(
                level="INFO",
                message="get_game_stats ran successfully",
                where="get_game_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return totals
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_game_stats failed",
                where="get_game_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_season_stats(self, player: str, sum_total: bool = False):
        try:
            self._ensure_initialized()

            if not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}
            if not isinstance(sum_total, bool):
                return {'error': f"sum_total must be a bool not {type(sum_total)}"}

            # Calculate stats
            if sum_total:
                total = {}
                for game_name, game_stats in self.data.items():
                    for quarter, quarter_stats in game_stats["Quarters"].items():
                        if player in quarter_stats:
                            for stat_name, stat_value in quarter_stats[player].items():
                                total[stat_name] = total.get(stat_name, 0) + stat_value

                output = total
            else:
                game_totals = {}
                for game_name, game_stats in self.data.items():
                    players_total = {}
                    for quarter_stats in game_stats["Quarters"].values():
                        if player in quarter_stats:
                            for stat_name, stat_value in quarter_stats[player].items():
                                players_total[stat_name] = players_total.get(stat_name, 0) + stat_value
                    if players_total:
                        game_totals[game_name] = players_total

                output = game_totals

            log_entry = create_log(
                level="INFO",
                message="get_season_stats ran successfully",
                where="get_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="get_season_stats failed",
                where="get_season_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_team_season_stats(self, sum_total: bool = False):
        try:
            self._ensure_initialized()

            if not isinstance(sum_total, bool):
                return {'error': f"sum_total must be a bool not {type(sum_total)}"}

            if sum_total:
                team_totals = {}

                for game_name, game_data in self.data.items():
                    for quarter_name, quarter_stats in game_data["Quarters"].items():
                        for players_name, players_stats in quarter_stats.items():
                            if players_name not in team_totals:
                                team_totals[players_name] = {}
                            for stat_name, stat_value in players_stats.items():
                                team_totals[players_name][stat_name] = team_totals[players_name].get(stat_name, 0) + stat_value

                log_entry = create_log(
                    level="INFO",
                    message="get_team_season_stats ran successfully",
                    where="get_team_season_stats",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
                )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                return team_totals
            else:
                game_team_totals = {}

                for game_name, game_data in self.data.items():

                    player_total = {}

                    for quarter_name, quarter_stats in game_data["Quarters"].items():
                        for players_name, players_data in quarter_stats.items():
                            if players_name not in player_total:
                                player_total[players_name] = {}
                            for player_stat_name, player_stat_value in players_data.items():
                                player_total[players_name][player_stat_name] = player_total[players_name].get(player_stat_name, 0) + player_stat_value

                    game_team_totals[game_name] = player_total

                log_entry = create_log(
                    level="INFO",
                    message="get_team_season_stats ran successfully",
                    where="get_team_season_stats",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_quarter_season_stats(self, player: str, quarter: str, sum_total: bool = False):
        try:
            self._ensure_initialized()

            if not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}

            if not isinstance(quarter, str):
                return {'error': f"quarter must be a string not {type(quarter)}"}

            if not isinstance(sum_total, bool):
                return {'error': f"sum_total must be a bool not {type(sum_total)}"}

            totals = {}

            if quarter not in self.data.get("Game_1", {}).get("Quarters", {}):
                raise KeyError("Could not find the quarter")

            if sum_total:
                for game_name, game_stats in self.data.items():
                    if quarter in game_stats["Quarters"]:
                        if player in game_stats["Quarters"][quarter]:
                            for stat, value in game_stats["Quarters"][quarter][player].items():
                                totals[stat] = totals.get(stat, 0) + value

                log_entry = create_log(
                    level="INFO",
                    message="get_quarter_season_stats ran successfully",
                    where="get_quarter_season_stats",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
                )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                return totals
            else:
                game_totals = {}

                for game_name, game_stats in self.data.items():

                    players_totals = {}

                    if quarter in game_stats["Quarters"]:
                        if player in game_stats["Quarters"][quarter]:
                            for stat_name, stat_value in game_stats["Quarters"][quarter][player].items():
                                players_totals[stat_name] = players_totals.get(stat_name, 0) + stat_value

                    if players_totals:
                        game_totals[game_name] = players_totals

                log_entry = create_log(
                    level="INFO",
                    message="get_quarter_season_stats ran successfully",
                    where="get_quarter_season_stats",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_highest_stats_quarter(self, game: str, quarter: str, what_to_look_for: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not isinstance(quarter, str):
                return {'error': f"quarter must be a string not {type(quarter)}"}

            if not isinstance(what_to_look_for, str):
                return {'error': f"what_to_look_for must be a string not {type(what_to_look_for)}"}

            game_stats = self.data.get(game, {})

            if not game_stats:
                raise KeyError("Could not find the game")

            quarter_stats = game_stats.get("Quarters", {}).get(quarter, {})

            if not quarter_stats:
                raise KeyError("Could not find the quarter")

            nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in quarter_stats.items()]

            if not nums:
                return {'error': f"No stats found for {what_to_look_for}"}

            max_stat_value = max(value for _, value in nums)

            if max_stat_value == 0:
                return {'error': f"No stats found for {what_to_look_for}"}

            top_players = [player for player, value in nums if value == max_stat_value]

            log_entry = create_log(
                level="INFO",
                message="get_highest_stats_quarter ran successfully",
                where="get_highest_stats_quarter",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_highest_stats_game(self, game: str, what_to_look_for: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not isinstance(what_to_look_for, str):
                return {'error': f"what_to_look_for must be a string not {type(what_to_look_for)}"}

            game_stats = self.get_game_stats(game=game, player=None)
            if not game_stats:
                raise KeyError("Could not find the game")

            nums = [(player, stats.get(what_to_look_for, 0)) for player, stats in game_stats.items() if what_to_look_for in stats]

            if not nums:
                return {'error': f"No stats found for {what_to_look_for}"}

            max_value = max(value for _, value in nums)

            if max_value == 0:
                return {'error': f"No stats found for {what_to_look_for}"}

            top_players = [player for player, value in nums if value == max_value]

            log_entry = create_log(
                level="INFO",
                message="get_highest_stats_game ran successfully",
                where="get_highest_stats_game",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
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
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def specific_players_best_stat(self, player: str, what_to_look_for: str):
        try:
            self._ensure_initialized()

            if not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}

            if not isinstance(what_to_look_for, str):
                return {'error': f"what_to_look_for must be a string not {type(what_to_look_for)}"}

            best_val = -1
            best_game = None
            best_quarter = None

            for game, game_stats in self.data.items():
                for quarter, quarter_stats in game_stats["Quarters"].items():
                    if player in quarter_stats and what_to_look_for in quarter_stats[player]:
                        value = quarter_stats[player][what_to_look_for]
                        if value > best_val:
                            best_val = value
                            best_game = game
                            best_quarter = quarter

            if best_val == -1:
                return {'error': f"No stats found for {player}"}
            else:
                log_entry = create_log(
                    level="INFO",
                    message="specific_players_best_stat ran successfully",
                    where="specific_players_best_stat",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
                )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

                return {what_to_look_for: best_val, "game": best_game, "quarter": best_quarter}

        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="specific_players_best_stat failed",
                where="specific_players_best_stat",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def check_player(self, game: str, team: str, player: str):
        try:
            self._ensure_initialized()

            if not isinstance(game, str):
                return {'error': f"game must be a string not {type(game)}"}

            if not isinstance(team, str):
                return {'error': f"team must be a string not {type(team)}"}

            if not isinstance(player, str):
                return {'error': f"player must be a string not {type(player)}"}

            if game not in self.data:
                raise KeyError("game not in the dataset")

            game_stats = self.data.get(game, {})

            if team not in game_stats.get("Lineup", {}):
                raise KeyError("team not in the game")

            team_players = game_stats.get("Lineup", {}).get(team, [])

            if player not in team_players:
                log_entry = create_log(
                    level="INFO",
                    message="check_player ran successfully",
                    where="check_player",
                    user_id=self.user_id,
                    source_ip=self.source_ip,
                    request_id=self.request_id
                )
                write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
                return False
            else:
                log_entry = create_log(
                    level="INFO",
                    message="check_player ran successfully",
                    where="check_player",
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
                message="check_player failed",
                where="check_player",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    @lru_cache(maxsize=256)
    def get_quick_team_stats(self, game: str, what_to_look_for: str = "Points"):
        try:
          if not isinstance(game, str):
              return {'error': f"game must be a string not {type(game)}"}

          if not isinstance(what_to_look_for, str):
              return {'error': f"what_to_look_fro must be a string not {type(what_to_look_for)}"}

          if game not in self.data:
              return {'error': f"game not found: {game}"}

          if what_to_look_for not in ["Points", "Fouls", "Assists", "Rebounds", "turnovers"]:
              return {"error": f"invaild what_to_look_for: {what_to_look_for}"}

          # all_stats
          stats = {}
          game_data = self.data[game]

          for quarter_name, quarter_data in game_data.get("Quarters", {}).items():
              for player_name, player_stats in quarter_data.items():
                  if player_name not in stats:
                      stats[player_name] = {}
                  for stat_name, stat_value in player_stats.items():
                      if stat_name not in stats[player_name]:
                          stats[player_name][stat_name] = 0
                      stats[player_name][stat_name] += stat_value
          # Team Best performer
          best_performer = self.get_highest_stats_game(game=game, what_to_look_for=what_to_look_for)

          # Team worst performer

          value_stats = {} # {players_name: {what_to_look_for: stat_value}, players_name: {what_to_look_for: stat_value}}
          for player_name, player_data in stats.items():
            if player_name not in value_stats.items():
                value_stats[player_name] = {}
                for stat_name, stat_value in player_data.items():
                    if stat_name == what_to_look_for:
                        if stat_name not in value_stats[player_name]:
                            value_stats[player_name][stat_name] = stat_value

          worst_performer = min(value_stats.items(), key=lambda item: item[1][what_to_look_for])

          # list of team contruibtos
          contribtors = {} # {players_name: {"percentage_of_team": int, "value", int, "total out of team": int out of int}}
          added_up_stats = 0

          for players_name, player_stats in value_stats.items():
              for stat_name, stat_value in player_stats.items():
                  added_up_stats += stat_value

          for players_name, player_stats in value_stats.items():
              stat_value = player_stats.get(what_to_look_for, 0)
              percentage_out_of_team = round((stat_value / added_up_stats) * 100 if added_up_stats > 0 else 0, 2)
              contribtors[players_name] = {
                  "percentage_of_team": percentage_out_of_team,
                  "value": stat_value,
                  "team_total": added_up_stats
              }

          sorted_contributors = sorted(contribtors.items(), key=lambda item: item[1]["value"], reverse=True)

          log_entry = create_log(
              level="INFO",
              message="get_quick_team_stats ran successfully",
              where="get_quick_team_stats",
              user_id=self.user_id,
              source_ip=self.source_ip,
              request_id=self.request_id
          )
          write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)

          #pprint.pprint({"all_stats": stats, "best_performer": best_performer, "worst_performer": worst_performer, "test": sorted_contributors})
          return {"all_stats": stats, "best_performer": best_performer, "worst_performer": worst_performer, "sorted_contributors": sorted_contributors}

        except Exception as e:
          error = {"type": type(e).__name__, 'message': str(e)}
          log_entry = create_log(
                level="ERROR",
                message="check_player failed",
                where="check_player",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
          write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
          return log_entry

    @lru_cache(maxsize=256)
    def get_quick_team_season_stats(self, player: str, what_to_look_for: str):
      pass
      

class Formatter:

    def __init__(self, user_id: str = "anonymous", source_ip: Optional[str] = None):
        self.user_id = user_id
        self.source_ip = source_ip
        self.request_id = str(uuid.uuid4())
        self.current_time = datetime.now(timezone.utc)

    def format_get_details(self, game: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")

            details = AccessData.get_details(game=game)

            output = ["--------------------- Details ------------------------"]
            for detail, stat in details.items():
                output.append(f"{detail}: {stat}")
            output.append("--------------------------------------------------")

            log_entry = create_log(
                level="INFO",
                message="format_get_details ran successfully",
                where="format_get_details",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return "\n".join(output)
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_details failed",
                where="format_get_details",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry
    def format_get_lineup(self, game: str, team: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")
            if not isinstance(team, str):
                raise TypeError("team must be a string")

            team_players = AccessData.get_lineup(game=game, team=team)

            output = ["----------------- Team players ----------------------"]
            for num, player in enumerate(team_players, start=1):
                output.append(f"{num}. {player}")

            log_entry = create_log(
                level="INFO",
                message="format_get_lineup ran successfully",
                where="format_get_lineup",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return "\n\n".join(output)
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_lineup failed",
                where="format_get_lineup",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry
    def format_get_quarter_stats(self, game: str, quarter: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")
            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")

            quarter_stats = AccessData.get_quarter_stats(game=game, quarter=quarter)

            output = [f"------------------ {quarter} stats for {game} ------------------"]
            for player, stats in quarter_stats.items():
                output.append(f"\n{player} stats:")
                for stat_name, stat_value in stats.items():
                    output.append(f"   - {stat_name}: {stat_value}")

            log_entry = create_log(
                level="INFO",
                message="format_get_quarter_stats ran successfully",
                where="format_get_quarter_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return "\n".join(output)
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_quarter_stats failed",
                where="format_get_quarter_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry
    def format_get_specific_stats(self, game: str, quarter: str, player: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")
            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")
            if not isinstance(player, str):
                raise TypeError("player must be a string")

            specific_stats = AccessData.get_specific_stats(game=game, quarter=quarter, player=player)

            output = [f"------------------ {player} stats for {quarter} of {game} ------------------"]
            for stat_name, stat_value in specific_stats.items():
                output.append(f"   - {stat_name}: {stat_value}")

            log_entry = create_log(
                level="INFO",
                message="format_get_specific_stats ran successfully",
                where="format_get_specific_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return "\n".join(output)
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_specific_stats failed",
                where="format_get_specific_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_game_stats(self, game: str, player: str = None):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")
            if player is not None and not isinstance(player, str):
                raise TypeError("player must be a string")

            game_stats = AccessData.get_game_stats(game=game, player=player)

            if player:
                formatted = [f"------------------ Game: {game} ------------------\n"]
                player_stats = game_stats.get(player, {})
                formatted.extend(f"{stat}: {value}" for stat, value in player_stats.items())
                output = "\n".join(formatted)
            else:
                lines = [f"------------------ Game: {game} Stats ------------------------\n"]
                for player_name, stats in game_stats.items():
                    stat_line = ", ".join(f"{key}: {value}" for key, value in stats.items())
                    lines.append(f"{player_name}: {stat_line}")
                output = "\n".join(lines)

            log_entry = create_log(
                level="INFO",
                message="format_get_game_stats ran successfully",
                where="format_get_game_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_game_stats failed",
                where="format_get_game_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_season_stats(self, player: str, sum_total: bool = False):
        try:
            if not isinstance(player, str):
                raise TypeError("player must be a string")
            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")

            season_stats = AccessData.get_season_stats(player=player, sum_total=sum_total)

            if sum_total:
                output = f"Season stats for {player}\n"
                for stat, value in season_stats.items():
                    output += f"    - {stat}: {value}\n"
            else:
                output = f"------------------------- Game stats for {player} -------------------------------\n"
                for game_name, game_stats in season_stats.items():
                    output += f"----------- {game_name} stats: ------------\n"
                    for stat_name, stat_value in game_stats.items():
                        output += f"    - {stat_name}: {stat_value}\n"
                        if stat_name == "Turnovers":
                            output += "\n"

            log_entry = create_log(
                level="INFO",
                message="format_get_season_stats ran successfully",
                where="format_get_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_season_stats failed",
                where="format_get_season_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_team_season_stats(self, sum_total: bool = False):
        try:
            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")

            team_season_stats = AccessData.get_team_season_stats(sum_total=sum_total)

            if sum_total:
                output = "---------------- Newport Raiders U16 Boys Julie Season stats ----------------\n"
                for team_players_name, team_players_stats in team_season_stats.items():
                    output += f"\n                       {team_players_name}                               \n"
                    for team_players_stat_name, team_players_stat_value in team_players_stats.items():
                        output += f"                            - {team_players_stat_name}: {team_players_stat_value}\n"
            else:
                output = f"---------------------- Newport Raiders U16 Boys Julie Season stats ----------------------\n"
                for game_stat_name, game_stat_value in team_season_stats.items():
                    output += f"\n\n{game_stat_name}                                   \n"
                    for players_name, players_stats in game_stat_value.items():
                        output += f"\n\n{players_name}                                     \n"
                        for stat_name, stat_value in players_stats.items():
                            output += f"\n{stat_name}: {stat_value}                       "

            log_entry = create_log(
                level="INFO",
                message="format_get_team_season_stats ran successfully",
                where="format_get_team_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_team_season_stats failed",
                where="format_get_team_season_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_quarter_season_stats(self, player: str, quarter: str, sum_total: bool = False):
        try:
            if not isinstance(player, str):
                raise TypeError("player must be a string")

            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")

            if not isinstance(sum_total, bool):
                raise TypeError("sum_total must be a bool")

            quarter_season_stats = AccessData.get_quarter_season_stats(player=player, quarter=quarter, sum_total=sum_total)

            if sum_total:
                output = f"------------- {player}'s {quarter} Season Stats (Total) -------------\n"
                for stat_name, stat_value in quarter_season_stats.items():
                    output += f"    {stat_name}: {stat_value}\n"
            else:
                output = f"------------- {player}'s {quarter} Stats by Game -------------\n"
                for game_name, game_stats in quarter_season_stats.items():
                    output += f"\n{game_name}:\n"
                    for stat_name, stat_value in game_stats.items():
                        output += f"    {stat_name}: {stat_value}\n"

            log_entry = create_log(
                level="INFO",
                message="format_get_quarter_season_stats ran successfully",
                where="format_get_quarter_season_stats",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_quarter_season_stats failed",
                where="format_get_quarter_season_stats",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_highest_stats_quarter(self, game: str, quarter: str, what_to_look_for: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")

            if not isinstance(quarter, str):
                raise TypeError("quarter must be a string")

            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")

            highest_stats = AccessData.get_highest_stats_quarter(game=game, quarter=quarter, what_to_look_for=what_to_look_for)

            if highest_stats is None:
                output = f"No stats found for {what_to_look_for} in {game} {quarter}"
            else:
                output = f"------------- Highest {what_to_look_for} in {game} {quarter} -------------\n"
                for player_name, stat_value in highest_stats.items():
                    output += f"    {player_name}: {stat_value}\n"

            log_entry = create_log(
                level="INFO",
                message="format_get_highest_stats_quarter ran successfully",
                where="format_get_highest_stats_quarter",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_highest_stats_quarter failed",
                where="format_get_highest_stats_quarter",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_get_highest_stats_game(self, game: str, what_to_look_for: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")

            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")

            highest_stats = AccessData.get_highest_stats_game(game=game, what_to_look_for=what_to_look_for)

            if highest_stats is None:
                output = f"No stats found for {what_to_look_for} in {game}"
            else:
                output = f"------------- Highest {what_to_look_for} in {game} Game -------------\n"
                for player_name, stat_value in highest_stats.items():
                    output += f"    {player_name}: {stat_value}\n"

            log_entry = create_log(
                level="INFO",
                message="format_get_highest_stats_game ran successfully",
                where="format_get_highest_stats_game",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_get_highest_stats_game failed",
                where="format_get_highest_stats_game",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_specific_players_best_stat(self, player: str, what_to_look_for: str):
        try:
            if not isinstance(player, str):
                raise TypeError("player must be a string")

            if not isinstance(what_to_look_for, str):
                raise TypeError("what_to_look_for must be a string")

            best_stat = AccessData.specific_players_best_stat(player=player, what_to_look_for=what_to_look_for)

            if best_stat is None:
                output = f"No stats found for {player}"
            else:
                output = f"------------- {player}'s Best {what_to_look_for} Performance -------------\n"
                output += f"    Stat: {best_stat[what_to_look_for]}\n"
                output += f"    Game: {best_stat['game']}\n"
                output += f"    Quarter: {best_stat['quarter']}\n"

            log_entry = create_log(
                level="INFO",
                message="format_specific_players_best_stat ran successfully",
                where="format_specific_players_best_stat",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(

                level="ERROR",
                message="format_specific_players_best_stat failed",
                where="format_specific_players_best_stat",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry

    def format_check_player(self, game: str, team: str, player: str):
        try:
            if not isinstance(game, str):
                raise TypeError("game must be a string")

            if not isinstance(team, str):
                raise TypeError("team must be a string")

            if not isinstance(player, str):
                raise TypeError("player must be a string")

            is_player_in_game = AccessData.check_player(game=game, team=team, player=player)

            if is_player_in_game:
                output = f"✓ {player} played for {team} in {game}"
            else:
                output = f"✗ {player} did NOT play for {team} in {game}"

            log_entry = create_log(
                level="INFO",
                message="format_check_player ran successfully",
                where="format_check_player",
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return output
        except Exception as e:
            error = {"type": type(e).__name__, 'message': str(e)}
            log_entry = create_log(
                level="ERROR",
                message="format_check_player failed",
                where="format_check_player",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
            write.write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
            return log_entry


if __name__ == '__main__':
    app = AccessData()
    print(app.get_quick_team_season_stats(player="Myles Dragone", what_to_look_for="Fouls"))





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
# TOTAL CLASSES: 2   (AccessData, Formatter)
# TOTAL METHODS: 1
# TOTAL FUNCTIONS AND METHODS: 28
# TOTAL LINES: ~1700
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
