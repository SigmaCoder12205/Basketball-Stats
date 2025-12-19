"""
IDEAS:

GET QUICK STATS:
    Points, Fouls, Rebounds, Assists, Turnovers

    - Show team best performer for the stat
    - Show team worst performer for the stat
    - Show a list of team contributors

GET QUICK SEASON STATS:
    Points, Fouls, Rebounds, Assists, Turnovers

    - Average per game: like average team points per game
    - Show average in; Median, Range
    - Show team best performer for the stat
    - Show team worst performer for the stat
    - Show a list of team contributors


COMPARE ALL GAMES:
    Points, Fouls, Rebounds, Assists, Turnovers

    - Show a increase or decrease in the stat from game to game  (Game_1 to Game_2
                                                                Game_2 to Game_3)

SEASONAL GRADING:
    Points, Fouls, Rebounds, Assists, Turnovers

    - Show for each stat a grade, show player the best player percentage out of the team and value
    - At the bottom show for all players

BEST/WORST GAME HIGHLIGHTS:
    Points, Fouls, Rebounds, Assists, Turnovers

    - Show the teams best and worst performance for the season
    - Show standout players for each best game and worst game.
    - Show the difference for each game
    - Also show the difference between the player who performed the best and worst for each best game and worst

GAME RATING:
    Points, Fouls, Rebounds, Assists, Turnovers
    Game_1, Game_2, Game_3

    - Shows rating overall (out of 300 because of 3 games)
    - Shows specific game rating with a system of something like 20 below is ranked poor and so and so on
    - Shows specific stat rating without the game and uses the system of 20 below is ranked poor etc
    - Shows both stat and game rating so like in Game_1 Points was ranked whatever

SEASON RATING:
    Points, Fouls, Rebounds, Assists, Turnovers
    Game_1, Game_2, Game_3

    - Does the same as game rating but only for the season

"""


import sys
import urllib
import os
import socket
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import PyQt5
from typing import Optional, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.accessing_data import AccessData
from utils.logging import Logging

class Backend:
    def __init__(self, user_id: str = "anonymous", source_ip: Optional[str] = None):
        self.Access_Data = AccessData()
        self.logging = Logging()
        self.user_id = user_id
        self.source_ip = source_ip
        self.request_id = str(uuid.uuid4())
        self.current_time = datetime.now(timezone.utc)


    def get_quick_stats(self, game: str, what_to_look_for: str):
      try:
        ALLOWED_STATS = {"Points", "Fouls", "Assists", "Rebounds", "Turnovers"}

        if type(game) is not str:
          return {'error': "game must be string"}
        if type(what_to_look_for) is not str:
            return {'error': "what_to_look_for must be string"}

        game = game.strip()
        what_to_look_for = what_to_look_for.strip()

        if not game:
          return {"error": "game cannot be empty"}
        if not what_to_look_for:
          return {"error": "what_to_look_for cannot be empty"}
        if what_to_look_for not in ALLOWED_STATS:
          return {"error": "invalid what_to_look_for"}


        result = self.Access_Data.get_quick_team_stats(game=game, what_to_look_for=what_to_look_for)


        if not isinstance(result, dict):
          return {'error': "internal error"}

        if result.get("level") == "ERROR":
          return {"error": "internal error"}

        return result

      except Exception as e:
        error = {"type": type(e).__name__, 'message': str(e)}
        log_entry = self.logging.create_log(
                level="ERROR",
                message="check_player failed",
                where="check_player",
                error=error,
                user_id=self.user_id,
                source_ip=self.source_ip,
                request_id=self.request_id
            )
        write_to("C:/Users/Drags Jrs/Drags/Database/log/accessing_data_log.json", log_entry)
        return log_entry

class Utils:
    pass

class Style:
    def __init__(self):
        pass

class TeamReport:
    def __init__(self):
        pass

if __name__ == '__main__':
  backend = Backend()
  test = print(backend.get_quick_stats(game="Game_1", what_to_look_for="Rebounds"))
