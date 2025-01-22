import FreeSimpleGUI as sg

from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager


class StudentStartpage:
    # Legt das Layout fest für die StudentStartpage.
    @classmethod
    def get_layout(cls):
        user = LoginManager.get_student()
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Text(f'Hallo {user[1]}', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Noten', key='grades', size=(10, 2))
            ]

        ]

    # Buttons werden definiert.
    # Weiterleitung an Startpage oder an StudentCertificatePage, entsprechend dem Button.
    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
            LoginManager.set_student(None)
        elif event == 'grades':
            from gui.student.StudentCertificatePage import StudentCertificatePage
            WindowManager.update(StudentCertificatePage().get_layout(), StudentCertificatePage.event_handler, size=(600, 300))
        elif event == sg.WIN_CLOSED:
            pass
