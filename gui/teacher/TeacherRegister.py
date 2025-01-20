import FreeSimpleGUI as sg

from database_util.TeacherUtil import TeacherUtil
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherRegister:

    # Die grafische Oberfläche für die Lehrerregistrierung wird generiert.
    @staticmethod
    def get_layout():
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Lehrer Registrierung', size=(30, 1), font=('Helvetica', 15), text_color='black')
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
                sg.Text('Verifizierungs-Code:', size=(20, 1), ),
                sg.InputText(key='verify', s=(15, 1))
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1))
            ]
        ]

    # Die Aktionen der Buttons wird definiert.
    # Beim zurück Button wird der TeacherPreLogin geladen.
    # Beim Registrieren wird zunächst überprüft, ob das Passwort und das abzugleichende Passwort identisch sind. Wenn nicht, bekommt man einen Fehler.
    # Insofern die Passwörter übereinstimmen wird noch überprüft, ob alle Felder schon ausgefüllt sind und ob der richtige Verifizierungscode angegeben wurde,
    # beim korrekten Ausfüllen wird der TeacherPreLogin geladen und ein Popup kommt als Rückmeldung. Ansonsten wird man nicht weitergeleitet.
    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.teacher.TeacherPreLogin import TeacherPreLogin
            WindowManager.update(TeacherPreLogin().get_layout(), TeacherPreLogin.event_handler)
        elif event == 'register':
            if values['password'] == values['confirm_password']:
                try:
                    TeacherUtil.teacher_register(values['first_name'], values['last_name'], values['email'],
                                                 values['password'],
                                                 values['verify'])
                    from gui.teacher.TeacherPreLogin import TeacherPreLogin
                    WindowManager.update(TeacherPreLogin().get_layout(), TeacherPreLogin.event_handler)
                    sg.popup_ok('Registrierung erfolgreich', location=WindowManager.last_location, no_titlebar=True, keep_on_top=True, modal=True)
                except Exception as e:
                    sg.popup_ok(e, location=WindowManager.last_location, no_titlebar=True, keep_on_top=True, modal=True)
            else:
                sg.popup_ok('Die Passwörter stimmen nicht überein.')
