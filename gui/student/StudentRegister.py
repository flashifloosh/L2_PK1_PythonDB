from Database import Database
from gui.WindowManager import WindowManager

import FreeSimpleGUI as sg


class StudentRegister:

    @staticmethod
    def get_layout():
        return [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Schüler Registrierung', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Text('Vorname:', size=(15, 1)),
                sg.InputText(key='first_name', size=(20, 1))
            ],
            [
                sg.Text('Nachname:', size=(15, 1)),
                sg.InputText(key='last_name', size=(20, 1))
            ],
            [
                sg.Text('E-Mail:', size=(15, 1)),
                sg.InputText(key='email', size=(20, 1))
            ],
            [
                sg.Text('Passwort:', size=(20, 1)),
                sg.InputText(key='password', password_char='*', size=(15, 1))
            ],
            [
                sg.Text('Passwort Bestätigen:', size=(20, 1)),
                sg.InputText(key='confirm_password', password_char='*', size=(15, 1))
            ],
            [
                sg.Text('Klasse:', size=(20, 1), ),
                sg.Combo(Database.get_schoolclasses(), key='schoolclass', s=(13, 1), readonly=True)
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentPreLogin import StudentPreLogin
            WindowManager.update(StudentPreLogin().get_layout(), StudentPreLogin.event_handler)
        elif event == 'register':
            if values['password'] == values['confirm_password']:
                try:
                    Database.student_register(values['first_name'], values['last_name'], values['email'],
                                              values['password'],
                                              f'{values['schoolclass']}')
                    sg.popup_ok('Registrierung erfolgreich', location=WindowManager.last_location)
                except Exception as e:
                    sg.popup_ok(e, location=WindowManager.last_location, title='', keep_on_top=True, modal=True)
            else:
                sg.popup_ok('Die Passwörter stimmen nicht überein.')

