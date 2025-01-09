from Database import Database

# https://freesimplegui.readthedocs.io/
import FreeSimpleGUI as sg

from gui.Startpage import Startpage
from gui.WindowManager import WindowManager

Database()


class Core:

    def __init__(self):
        WindowManager.run()
