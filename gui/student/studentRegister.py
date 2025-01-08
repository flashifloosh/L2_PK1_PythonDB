from database import Database

import FreeSimpleGUI as sg


class StudentRegister:

    def __init__(self):
        self.layout = [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Schüler Registrierung', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Text('Vorname:', size=(15, 1)),
                sg.InputText(key='first_name', size=(15, 1))
            ],
            [
                sg.Text('Nachname:', size=(15, 1)),
                sg.InputText(key='last_name', size=(15, 1))
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
                sg.Text('Klasse:', size=(15, 1)),
                sg.DropDown(Database.getSchoolclasses(), key='schoolclass', size=(15, 1))
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1))
            ]
        ]
        self.window = sg.Window('Schüler Registrierung', self.layout, size=(300, 200), element_justification='c',
                                finalize=True)
        while True:
            event, values = self.window.read()
            if event == 'back':
                self.window.close()
                from studentStartpage import StudentStartpage
                StudentStartpage()
                break
            if event == 'register':
                print('Register button clicked')
                self.window.close()
                fname = values['first_name']
                lname = values['last_name']
                email = values['email']
                password = values['password']
                schoolclass = values['schoolclass']

                Database().student_register(fname, lname, email, password, schoolclass)
                break
            if event == sg.WIN_CLOSED:
                break