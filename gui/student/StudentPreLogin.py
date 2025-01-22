import FreeSimpleGUI as sg

from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class StudentPreLogin:

    # Die grafische Oberfläche für den StudentPreLogin wird generiert, bzw bereitgestellt.
    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color()), ),
                sg.Text('Schüler', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1)),
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]

    # Die Aktionen der Buttons wird definiert.
    # Beim zurück Button wird die Startpage geladen.
    # Beim Registrieren wird der Schüler an die entsprechende grafische Oberfläche weitergeleitet.
    # Wohingegen der Login Button zum StudentLogin weiterleitet.
    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
        elif event == 'register':
            from gui.student.StudentRegister import StudentRegister
            WindowManager.update(StudentRegister().get_layout(), StudentRegister.event_handler, size=(400, 230))
        elif event == 'login':
            from gui.student.StudentLogin import StudentLogin
            WindowManager.update(StudentLogin.get_layout(), StudentLogin.event_handler, size=(400, 150))
