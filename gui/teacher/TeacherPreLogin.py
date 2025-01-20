import FreeSimpleGUI as sg

from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherPreLogin:

    # Die grafische Oberfläche für den LehrerPreLogin wird generiert, bzw bereitgestellt.
    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Lehrer', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1)),
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
        elif event == 'register':
            from gui.teacher.TeacherRegister import TeacherRegister
            WindowManager.update(TeacherRegister().get_layout(), TeacherRegister.event_handler, size=(400, 225))
        elif event == 'login':
            from gui.teacher.TeacherLogin import TeacherLogin
            WindowManager.update(TeacherLogin.get_layout(), TeacherLogin.event_handler, size=(400, 150))
