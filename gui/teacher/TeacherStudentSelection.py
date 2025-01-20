import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherStudentSelection:

    @classmethod
    def get_layout(cls, schoolclass):
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text(f"Klasse {schoolclass}", size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Column(cls.generate_student_list(schoolclass))
            ],
            [
                sg.Button("Anzeigen", key='show', size=(10, 2)),
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage.get_layout(), Startpage.event_handler)
            LoginManager.set_teacher(None)
            LoginManager.set_class(None)
        elif event == 'back':
            from gui.teacher.TeacherClassSelection import TeacherClassSelection
            WindowManager.update(TeacherClassSelection.get_layout(), TeacherClassSelection.event_handler,
                                 size=(400, 300))
            LoginManager.set_class(None)
        elif event == 'show':
            selected_student_key = None
            for key, value in values.items():
                if isinstance(value, list) and value:
                    selected_student_key = key
                    break
            if selected_student_key:
                student_info = selected_student_key
                LoginManager.set_student(student_info)
                from gui.teacher.TeacherStudentPage import TeacherStudentPage
                WindowManager.update(TeacherStudentPage.get_layout(student_info),
                                     TeacherStudentPage.event_handler, size=(400, 200))
            else:
                sg.popup("Bitte wählen Sie einen Schüler aus")

    @classmethod
    def generate_student_list(cls, schoolclass):
        students = Database.get_students(schoolclass)
        layout = []
        for s in students:
            student_name = f"{s[1]}, {s[0]}"
            layout.append([sg.Listbox([student_name], key=s, size=(30, 5))])
        return layout