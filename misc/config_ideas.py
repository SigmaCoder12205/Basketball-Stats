
from pathlib import Path
from datetime import datetime
"""
curr = Path.cwd()

curr2 = Path('.')

# print(f"CURR: {curr.absolute()}\nCURR2: {curr2.absolute()}\nCHECK IF EQUAL: {curr.absolute() == curr2.absolute()}")
# print(curr.samefile(curr2))
# print(Path.home())

with open("test.txt", "w") as file:
    file.write("Testing")

file = Path('test.txt')
# print(file.absolute())

file_stat = file.stat()

# print(f"{file} SIZE: {file_stat.st_size} Bytes\n MTIME {file_stat.st_mtime}")

print(datetime.fromtimestamp(file_stat.st_mtime))

"""

home_dir = Path.cwd()

data_path = Path(home_dir / "utils" / "accessing_data.py")

print(data_path.absolute().read_text())