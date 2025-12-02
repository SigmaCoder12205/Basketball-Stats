import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.write import write_to
from utils.accessing_data import AccessData as asd
from utils import accessing_data as ad

if __name__ == '__main__':
    ins = asd(user_id="Owner")
    print(ins.check_player(game="Game_1", team="Newport Raiders U16 Boys Julie", player="Myles Dragone", look_good=True))