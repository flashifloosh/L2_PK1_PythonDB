from gui.student.StudentStartpage import StudentStartpage
from Database import Database

import FreeSimpleGUI as sg


class StudentLogin:

    def __init__(self):
        self.layout = [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Schüler Anmeldung', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Text('E-Mail:', size=(15, 1)),
                sg.InputText(key='email', size=(15, 1))
            ],
            [
                sg.Text('Passwort:', size=(15, 1)),
                sg.InputText(key='password', password_char='*', size=(15, 1))
            ],
            [
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]
        self.window = sg.Window('Schüler Anmeldung', self.layout, size=(300, 150), element_justification='c',
                                finalize=True)
        while True:
            event, values = self.window.read()
            if event == 'back':
                self.window.close()
                StudentStartpage()
                break
            if event == 'login':
                print('Login button clicked')
                self.window.close()
                if Database().student_login(values['email'], values['password']):
                    print('Login successful')
                else:
                    print('Login failed')
                break
            if event == sg.WIN_CLOSED:
                break
