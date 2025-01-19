from database_util.Database import Database

# https://freesimplegui.readthedocs.io/

from gui.WindowManager import WindowManager

Database()


class Core:

    def __init__(self):
        WindowManager.run()
