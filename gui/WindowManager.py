import FreeSimpleGUI as sg

from images.ImageUtil import ImageUtil


class WindowManager:
    last_location = (None, None)
    window = None

    # Die default grafische Oberfläche wird hier deklariert mit seinen Parametern.
    @classmethod
    def update(cls, new_layout, event_handler, size=(400, 100), r_loc=(0, 0)):
        if cls.window is not None:
            cls.window.close()
        cls.window = sg.Window("Schulsystem", new_layout, location=cls.last_location,
                               element_justification='c', finalize=True, size=size,
                               relative_location=r_loc, icon=ImageUtil.get_book_icon())
        cls.event_handler = event_handler # Vererbung des eventhandlers der jeweiligen Klasse

    # Allgemeine Aktionen die bei Fenstern ausgeführt werden, sind hier gelistet.
    # Das Schließen und, dass ein neues Fenster an der gleichen Stelle erscheint.
    @classmethod
    def run(cls):
        from gui.Startpage import Startpage
        cls.update(Startpage.get_layout(), Startpage.event_handler)
        while True:
            event, values = cls.window.read()
            if cls.window is not None and cls.window.TKroot.winfo_exists():
                cls.last_location = cls.window.CurrentLocation()
            if event == sg.WIN_CLOSED:
                break
            cls.event_handler(event, values)

    # Haupteventhandler, gibt den eventhandler weiter an die anderen Module, sodass diese diesen verändern können.
    @classmethod
    def event_handler(cls, event, values):
        pass

    # Standardisierung der Popup Quick Messages
    @classmethod
    def popup_quick_message(cls, message, ):
        sg.popup_quick_message(message, location=cls.last_location, background_color="green", text_color="white")

