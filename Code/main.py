import sys
sys.path.append("C:/Users/Drags Jrs/Drags")
from PyQt5.QtWidgets import QApplication
from testing.player_report import PlayerReport
from utils.accessing_data import AccessData

if __name__ == "__main__":
    print(AccessData.check_player(12, "Newport Raiders U16 Boys Julie", "Myles Dragone", False))