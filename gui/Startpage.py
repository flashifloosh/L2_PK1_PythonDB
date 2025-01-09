import FreeSimpleGUI as sg

from gui.student.StudentStartpage import StudentStartpage
from gui.WindowManager import WindowManager


class Startpage:

    def __init__(self):
        WindowManager.handle_event = self.handle_event

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Text('Schulsystem', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Schüler', key='student', size=(10, 1)),
                sg.Button('Lehrer', key='teacher', size=(10, 1))
            ]
        ]

    @staticmethod
    def handle_event(event, values):
        if event == 'student':
            WindowManager.update(StudentStartpage().get_layout())
            print("test")
        elif event == 'teacher':
            print('Teacher button clicked')

