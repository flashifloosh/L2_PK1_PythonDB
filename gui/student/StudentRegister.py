import FreeSimpleGUI as sg

from database_util.Database import Database
from database_util.StudentUtil import StudentUtil
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class StudentRegister:

    # Die grafische Oberfläche für die Schülerregstrierung wird generiert.
    @staticmethod
    def get_layout():
        schoolclasses = [row[0] for row in Database.get_schoolclasses()]
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
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
                sg.Combo(schoolclasses, key='schoolclass', s=(13, 1), readonly=True)
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1))
            ]
        ]

    # Die Aktionen der Buttons wird definiert.
    # Beim zurück Button wird der StudentPreLogin geladen.
    # Beim Registrieren wird zunächst überprüft, ob das Passwort und das abzugleichende Passwort identisch sind.
    # Insofern die Passwörter übereinstimmen wird noch überprüft, ob alle Felder schon ausgefüllt sind.
    # Beim korrekten Ausfüllen wird der StudentPreLogin geladen und ein Popup kommt als Rückmeldung.
    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentPreLogin import StudentPreLogin
            WindowManager.update(StudentPreLogin().get_layout(), StudentPreLogin.event_handler)
        elif event == 'register':
            if values['password'] == values['confirm_password']:
                try:
                    StudentUtil.student_register(values['first_name'], values['last_name'], values['email'],
                                                 values['password'],
                                                 f'{values['schoolclass']}')
                    from gui.student.StudentPreLogin import StudentPreLogin
                    WindowManager.update(StudentPreLogin.get_layout(), StudentPreLogin.event_handler)
                    WindowManager.popup_quick_message('Registrierung erfolgreich')
                except Exception as e:
                    sg.popup_ok(e, location=WindowManager.last_location, keep_on_top=True, modal=True, no_titlebar=True)
            else:
                sg.popup_ok('Die Passwörter stimmen nicht überein.')
