import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager


class TeacherClassSelection:
    @classmethod
    def get_layout(cls):
        user = LoginManager.get_teacher()
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Text(f'Hallo {user[0]}', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            cls.generate_class_buttons()
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
            LoginManager.set_teacher(None)
        elif event in [c[0] for c in Database.get_schoolclasses()]:
            LoginManager.set_class(event)
            from gui.teacher.TeacherStudentSelection import TeacherStudentSelection
            WindowManager.update(TeacherStudentSelection().get_layout(event), TeacherStudentSelection.event_handler,
                                 size=(400, 300))

    @classmethod
    def generate_class_buttons(cls):
        classes = Database.get_schoolclasses()
        layout = []
        for i in range(0, len(classes), 3):
            row = [sg.Button(classes[i][0], key=classes[i][0], size=(10, 2))]
            if i + 1 < len(classes):
                row.append(sg.Button(classes[i + 1][0], key=classes[i + 1][0], size=(10, 2)))
            if i + 2 < len(classes):
                row.append(sg.Button(classes[i + 2][0], key=classes[i + 2][0], size=(10, 2)))
            layout.append(row)
        return layout
