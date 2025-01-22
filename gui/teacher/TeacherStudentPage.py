import FreeSimpleGUI as sg

from database_util.TeacherUtil import TeacherUtil
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager


class TeacherStudentPage:

    # Die grafische Oberfläche für die TeacherStudentCert wird generiert.
    @classmethod
    def get_layout(cls, student):
        layout = TeacherUtil.generate_common_layout(student)
        layout.append([
            sg.Button("Noten", key='cert', size=(10, 2)),
            sg.Button("Schüler löschen", key='delete_student', size=(15, 2))
        ])
        return layout

    # Die Aktionen der Buttons wird definiert.
    # Beim logout Button wird die Startpage geladen.
    # Beim back Button, wird die TeacherStudentSelection geladen.
    # Beim Löschen eines Benutzers bekommt man eine Sicherheitsabfrage. Insofern diese bestätigt wird, wird dieser gelöscht.
    # Der vierte Button leitet einen weiter an TeacherStudentCert.
    @classmethod
    def event_handler(cls, event, values):
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
            response = sg.popup_yes_no('Möchten Sie den Schüler wirklich löschen?',
                                       keep_on_top=True,
                                       modal=True, location=WindowManager.last_location, text_color='white',
                                       no_titlebar=True, background_color="red")
            if response == 'Yes':
                TeacherUtil.delete_student(LoginManager.get_student())
        elif event == 'cert':
            from gui.teacher.TeacherStudentCert import TeacherStudentCert
            WindowManager.update(TeacherStudentCert.get_layout(LoginManager.get_student()),
                                 TeacherStudentCert.event_handler, size=(400, 400))
