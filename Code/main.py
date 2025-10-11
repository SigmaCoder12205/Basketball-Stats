import sys
sys.path.append("C:/Users/Drags Jrs/Drags/Code/main")
from PyQt5.QtWidgets import QApplication
from testing.player_report import PlayerReport

if __name__ == "__main__":
    app = QApplication(sys.argv)
    drags = PlayerReport("Aston Sharp")
    drags.show()
    sys.exit(app.exec_())