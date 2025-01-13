from gui.WindowManager import WindowManager
from gui.student.StudentPreLogin import StudentPreLogin
from Database import Database

import FreeSimpleGUI as sg


class StudentLogin:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
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
            if Database().student_login(values['email'], values['password']):
                print('Login successful')
                from gui.student.StudentStartpage import StudentStartpage
                WindowManager.update(StudentStartpage().get_layout(), StudentStartpage.event_handler)
            else:
                print('Login failed')
        elif event == sg.WIN_CLOSED:
            pass
