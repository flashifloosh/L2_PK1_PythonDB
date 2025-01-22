from database_util.Database import Database

from gui.WindowManager import WindowManager


class Core:

    # Legt die Datenbank an und führt den Window Manager aus.
    def __init__(self):
        WindowManager.run()
        Database()
