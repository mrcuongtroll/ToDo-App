"""
To bundle executable version of this program:
    - Install pyinstaller package
    - Open this project folder in terminal
    - Run the following command:
        pyinstaller --hidden-import babel.numbers --onedir -w main.py --runtime-hook addlib.py
"""


import babel.numbers
from login_window import *


if __name__ == '__main__':
    create_login_window()
