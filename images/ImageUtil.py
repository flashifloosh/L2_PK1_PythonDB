import os, sys

class ImageUtil:

    @classmethod
    def get_back_image(cls):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'images', 'back.png')
        else:
            return os.path.join('images', 'back.png')