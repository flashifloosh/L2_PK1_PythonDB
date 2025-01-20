import FreeSimpleGUI as sg

from gui.WindowManager import WindowManager
from gui.student.StudentPreLogin import StudentPreLogin
from gui.teacher.TeacherPreLogin import TeacherPreLogin


class Startpage:

    # Die grafische Oberfläche für die Startpage wird generiert.
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

    # Die Aktionen der Buttons wird definiert.
    # Beim student-Button wird man an die StudentPreLogin weitergeleitet. (Neues Fenster öffnet sich)
    # dasselbe gilt für den teacher-Button, equivalent wird er an TeacherPreLogin weitergeleitet. (Neues Fenster öffnet sich)
    @staticmethod
    def event_handler(event, values):
        if event == 'student':
            WindowManager.update(StudentPreLogin().get_layout(), StudentPreLogin.event_handler)
        elif event == 'teacher':
            WindowManager.update(TeacherPreLogin().get_layout(), TeacherPreLogin.event_handler)
