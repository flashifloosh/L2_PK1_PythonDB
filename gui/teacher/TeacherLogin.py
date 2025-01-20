import FreeSimpleGUI as sg

from database_util.TeacherUtil import TeacherUtil
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherLogin:

    # Die grafische Oberfläche für den Lehrerlogin wird generiert
    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text('Lehrer Anmeldung', size=(30, 1), font=('Helvetica', 15), text_color='black')
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

    # Die Aktionen der Buttons wird definiert.
    # Beim zurück Button wird der PreLogin geladen.
    # Beim login wird geschaut, ob alle Daten korrekt sind und dann wird der Lehrer weitergeleitet an die Klassenselektion.
    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.teacher.TeacherPreLogin import TeacherPreLogin
            WindowManager.update(TeacherPreLogin().get_layout(), TeacherPreLogin.event_handler)
        elif event == 'login':
            try:
                TeacherUtil.teacher_login(values['email'], values['password'])
                from gui.teacher.TeacherClassSelection import TeacherClassSelection
                WindowManager.update(
                    TeacherClassSelection().get_layout(),
                    TeacherClassSelection.event_handler, size=(400, 300))
            except Exception as e:
                sg.popup_ok(e, location=WindowManager.last_location, no_titlebar=True, keep_on_top=True, modal=True)