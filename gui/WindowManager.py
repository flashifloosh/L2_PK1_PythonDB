from sys import maxsize

import FreeSimpleGUI as sg


class WindowManager:
    last_location = (None, None)

    @classmethod
    def update(cls, new_layout, event_handler, size=(400, 100), r_loc=(0, -30)):
        cls.window.close()
        cls.window = sg.Window("Schulsystem", new_layout, location=cls.last_location,
                               element_justification='c', resizable=True, finalize=True, size=size,
                               relative_location=r_loc)
        cls.event_handler = event_handler

    @classmethod
    def run(cls):
        from gui.Startpage import Startpage
        cls.window = sg.Window('Schulsystem', Startpage.get_layout(), size=(400, 100), location=cls.last_location,
                               element_justification='c', resizable=True, finalize=True)
        cls.event_handler = Startpage.event_handler
        while True:
            event, values = cls.window.read()
            cls.last_location = cls.window.CurrentLocation()
            if event == sg.WIN_CLOSED:
                cls.last_location = cls.window.CurrentLocation()
                break
            cls.event_handler(event, values)

    @classmethod
    def event_handler(cls, event, values):
        if event == sg.WIN_CLOSED:
            cls.window.close()
        pass
