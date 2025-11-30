import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.write import write_to
from utils.accessing_data import AccessData as asd
from utils import accessing_data as ad

"""
==== FOLDER PATH ====

Folder PATH listing for volume Windows
Volume serial number is E062-215C
C:.
│   copy.txt
│   cspell.json
│   ideas.txt
│   quick_copy.md
│   Todo.md
│   __init__.py
│
├───.vscode
│       launch.json
│       settings.json
│
├───Database
│   │   Data.json
│   │
│   └───log
│           accessing_data_log.json
│           accessing_data_lpg.json
│           player_report_errors.json
│
├───docs
│       accessing_data_doc.md
│       player_report_doc.md
│       system_architecture.md
│
├───git
│       .gitignore
│       .gitmodules
│
├───main
│   │   main.py
│   │   __init__.py
│   │
│   └───__pycache__
│           main.cpython-313.pyc
│           __init__.cpython-313.pyc
│
├───Old-basketball-stats
│   │   .gitignore
│   │   cspell.json
│   │
│   ├───.vscode
│   │       launch.json
│   │       settings.json
│   │
│   ├───Blueprints
│   │       AppIdeas.txt
│   │       Copy.txt
│   │       designs.txt
│   │       Todo.txt
│   │
│   ├───Code
│   │   │   AccessingData.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           AccessingData.cpython-313.pyc
│   │           __init__.cpython-313.pyc
│   │
│   ├───Database
│   │       Data.json
│   │
│   ├───testing
│   │   │   .gitignore
│   │   │   functionTesting.py
│   │   │   __init__.py
│   │   │
│   │   ├───sandbox
│   │   │   │   admin.ps1
│   │   │   │   analytics.py
│   │   │   │   comparing.py
│   │   │   │   main.py
│   │   │   │   playground.py
│   │   │   │   Reports.py
│   │   │   │   __init__.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           Improvement.cpython-313.pyc
│   │   │           playground.cpython-313.pyc
│   │   │           __init__.cpython-313.pyc
│   │   │
│   │   └───__pycache__
│   │           functionTesting.cpython-313.pyc
│   │           __init__.cpython-313.pyc
│   │
│   └───UI
│       └───UI
│               PlayerReport.py
│
├───testing
│   │   player_report.py
│   │   test_file.py
│   │   __init__.py
│   │
│   └───__pycache__
│           player_report.cpython-313.pyc
│
├───UI
│       designs.txt
│
└───utils
    │   accessing_data.py
    │   write.py
    │   __init__.py
    │
    └───__pycache__
            accessing_data.cpython-313.pyc
            write.cpython-313.pyc
            __init__.cpython-313.pyc


====  TEST RESULTS FOR utils.accessing_data.py ====

    - get_public_ip()     ALL GOOD
    - create_log()        ALL GOOD
    - AccessData          ALL GOOD

"""



if __name__ == '__main__':
    ins = asd(user_id="Owner")