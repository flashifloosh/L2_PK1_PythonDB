import FreeSimpleGUI as sg

from gui.WindowManager import WindowManager



class StudentStartpage:

    def __init__(self):
        WindowManager.handle_event = handle_event

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Schüler Startseite', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1)),
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]

    def handle_event(self, event, values):
        if event == 'back':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout())
    #  elif event == 'register':
    #  WindowManager.update_layout(StudentRegister().get_layout())
    #   elif event == 'login':
    #  WindowManager.update_layout(StudentLogin().get_layout())
