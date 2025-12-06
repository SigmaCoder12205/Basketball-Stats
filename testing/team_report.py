"""
IDEAS:

GET QUICK STATS:
    Points, Fouls, Rebounds, Assists, Turnovers

    Average per game: like average team points per game
    Show average in; Median, Range
    Show team best performer for the stat 
    Show team worst performer for the stat
    Show a list of team contributors

COMPARE ALL GAMES:
    Points, Fouls, Rebounds, Assists, Turnovers

    Show a increase or decrease in the stat from game to game  (Game_1 to Game_2
                                                                Game_2 to Game_3)

SEASONAL GRADING:
    Points, Fouls, Rebounds, Assists, Turnovers

    Show for each stat a grade, show player the best player percentage out of the team and value
    At the bottom show for all players

BEST/WORST GAME HIGHLIGHTS:
    Points, Fouls, Rebounds, Assists, Turnovers
    
    Show the teams best and worst performance for the season 
    Show standout players for each best game and worst game.
    Show the difference for each game
    Also show the difference between the player who performed the best and worst for each best game and worst  

GAME RATING
    
"""


import sys 
import urllib
import os
import socket
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import PyQt5

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.accessing_data import AccessData
from utils.write import write_to

class Backend:
    pass

class Utils:
    pass

class Style:
    pass

class TeamReport:
    pass
