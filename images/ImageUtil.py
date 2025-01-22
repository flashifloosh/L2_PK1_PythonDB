import os
import sys


class ImageUtil:

    # Methode um das Bild für den Zurück Button zu bekommen
    @classmethod
    def get_back_image(cls):
        # Wenn das Programm als .exe ausgeführt wird, wird das Bild aus dem temporären Verzeichnis genommen
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'images', 'back.png')
        else:
            return os.path.join('images', 'back.png')

    # Methode um das Icon zu bekommen
    @classmethod
    def get_book_icon(cls):
        # Wenn das Programm als .exe ausgeführt wird, wird das Icon aus dem temporären Verzeichnis genommen
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'images', 'book.ico')
        else:
            return os.path.join('images', 'book.ico')
