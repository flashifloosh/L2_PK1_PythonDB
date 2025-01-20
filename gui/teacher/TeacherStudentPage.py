import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherStudentPage:

    @classmethod
    def get_layout(cls, student):
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text(f'Schüler: {student[1]}, {student[0]}', size=(20, 1), font=('Helvetica', 15),
                        text_color='black')
            ],
            [
                sg.Column(cls.generate_student_info(student))
            ],
            [
                sg.Button("Noten", key='cert', size=(10, 2)),
                sg.Button("Schüler löschen", key='delete_student', size=(15, 2))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
            LoginManager.set_teacher(None)
            LoginManager.set_student(None)
        elif event == 'back':
            from gui.teacher.TeacherStudentSelection import TeacherStudentSelection
            WindowManager.update(TeacherStudentSelection().get_layout(LoginManager.get_class()),
                                 TeacherStudentSelection.event_handler, size=(400, 300))
            LoginManager.set_student(None)
        elif event == 'delete_student':
            response = sg.popup_yes_no('Möchten Sie den Schüler wirklich löschen?', title='Schüler löschen',
                                       keep_on_top=True,
                                       modal=True, location=WindowManager.last_location, text_color='red')
            if response == 'Yes':
                Database.delete_student(LoginManager.get_student()[2])
                from gui.teacher.TeacherStudentSelection import TeacherStudentSelection
                WindowManager.update(TeacherStudentSelection().get_layout(LoginManager.get_class()),
                                     TeacherStudentSelection.event_handler, size=(400, 300))
                LoginManager.set_student(None)
        elif event == 'cert':
            from gui.teacher.TeacherStudentCert import TeacherStudentCert
            WindowManager.update(TeacherStudentCert.get_layout(LoginManager.get_student()),
                                 TeacherStudentCert.event_handler, size=(400, 300))

    @classmethod
    def generate_student_info(cls, student):
        student = Database.get_student(student[2])
        return [
            [sg.Text('Vorname:'), sg.Text(f'{student[1]}')],
            [sg.Text('Nachname:'), sg.Text(f'{student[2]}')],
            [sg.Text('Klasse:'), sg.Text(f'{student[4]}')],
            [sg.Text('E-Mail:'), sg.Text(f'{student[3]}')],
        ]
