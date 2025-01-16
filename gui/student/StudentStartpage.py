import FreeSimpleGUI as sg
from gui.WindowManager import WindowManager


class StudentStartpage:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Text(size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Noten', key='grades', size=(10, 1))
            ]

        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
        elif event == 'grades':
            from gui.student.CertificatePage import CertificatePage
            WindowManager.update(CertificatePage().get_layout(), CertificatePage.event_handler)
        elif event == sg.WIN_CLOSED:
            pass
