import sys
sys.path.append("C:/Users/Drags Jrs/Drags")
from PyQt5.QtWidgets import QApplication
from scripts.tracer import global_trace
from testing.player_report import PlayerReport
from utils.accessing_data import AccessData

if __name__ == "__main__":
    sys.settrace(global_trace)
    app = QApplication(sys.argv)

    obj1 = PlayerReport("Myles Dragone")
    obj2 = AccessData()
    obj1.show()

    exit_code = app.exec_()
    sys.settrace(None)
    sys.exit(exit_code)
