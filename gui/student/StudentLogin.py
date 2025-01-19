from database_util.StudentUtil import StudentUtil
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil

import FreeSimpleGUI as sg


class StudentLogin:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Schüler Anmeldung', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Text('E-Mail:', size=(15, 1)),
                sg.InputText(key='email', size=(20, 1))
            ],
            [
                sg.Text('Passwort:', size=(15, 1)),
                sg.InputText(key='password', password_char='*', size=(20, 1))
            ],
            [
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentPreLogin import StudentPreLogin
            WindowManager.update(StudentPreLogin().get_layout(), StudentPreLogin.event_handler)
        elif event == 'login':
            try:
                StudentUtil.student_login(values['email'], values['password'])
                from gui.student.StudentStartpage import StudentStartpage
                WindowManager.update(
                    StudentStartpage().get_layout(),
                    StudentStartpage.event_handler)
            except Exception as e:
                sg.popup_ok(e, location=WindowManager.last_location, no_titlebar=True, keep_on_top=True, modal=True)
