import FreeSimpleGUI as sg


class WindowManager:
    last_location = (None, None)
    window = None
    student = None
    teacher = None

    @classmethod
    def update(cls, new_layout, event_handler, size=(400, 100), r_loc=(0, 0)):
        if cls.window is not None:
            cls.window.close()
        cls.window = sg.Window("Schulsystem", new_layout, location=cls.last_location,
                               element_justification='c', finalize=True, size=size,
                               relative_location=r_loc)
        cls.event_handler = event_handler

    @classmethod
    def set_student(cls, student):
        cls.student = student

    @classmethod
    def get_student(cls):
        return cls.student

    @classmethod
    def run(cls):
        from gui.Startpage import Startpage
        cls.update(Startpage().get_layout(), Startpage().event_handler)
        while True:
            event, values = cls.window.read()
            cls.last_location = cls.window.CurrentLocation()
            if event == sg.WIN_CLOSED:
                break
            cls.event_handler(event, values)

    @classmethod
    def event_handler(cls, event, values):
        pass
