import FreeSimpleGUI as sg


class WindowManager:
    last_location = (None, None)

    @classmethod
    def update(cls, new_layout, event_handler):
        cls.window.close()
        cls.window = sg.Window('Schulsystem', new_layout, size=(300, 100), location=cls.last_location,
                               element_justification='c', finalize=True)
        cls.handle_event = event_handler

    @classmethod
    def run(cls):
        from gui.Startpage import Startpage
        cls.window = sg.Window('Schulsystem', Startpage.get_layout(), size=(300, 100), location=cls.last_location,
                               element_justification='c', finalize=True)
        cls.handle_event = Startpage.handle_event
        while True:
            event, values = cls.window.read()
            cls.last_location = cls.window.CurrentLocation()
            if event == sg.WIN_CLOSED:
                break
            cls.handle_event(event, values)

    @classmethod
    def handle_event(cls, event, values):
        if event == sg.WIN_CLOSED:
            cls.window.close()
        pass
