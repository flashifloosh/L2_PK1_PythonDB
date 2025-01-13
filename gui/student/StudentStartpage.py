import FreeSimpleGUI as sg
from gui.WindowManager import WindowManager


class StudentStartpage:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button("Abmelden", key='back', image_filename='./images/back.png', image_subsample=30,
                          border_width=0),
                sg.Text(size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Noten', key='grades', size=(10, 1))
            ]

        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
        elif event == 'grades':
            print("Grades")
        elif event == sg.WIN_CLOSED:
            pass
