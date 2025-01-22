import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherStudentSelection:
    student_email_map = {}

    # Die grafische Oberfläche für die TeacherStudentSelection wird generiert.
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
                sg.Text('Wählen Sie einen Schüler:', size=(20, 1))
            ],
            [
                sg.Column(cls.generate_student_list(schoolclass))
            ],
            [
                sg.Button("Anzeigen", key='show', size=(10, 2)),
            ]
        ]

    # Die Aktionen der Buttons wird definiert.
    # Beim logout Button wird die Startpage geladen.
    # Der back button bringt einen auf die TeacherClassSelection zurück.
    # Insofern man sich den Schüler anschaut, sieht man die Daten des Schülers.
    @classmethod
    def event_handler(cls, event, values):
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
            cls.selected_student(values)

    # Legt das DropDown Menü an, sodass der Lehrer alle Schüler einer Klasse aufgelistet bekommt.
    # Dafür muss eine Klasse ausgewählt worden sein, damit diese dann abgefragt werden kann.
    @classmethod
    def generate_student_list(cls, schoolclass):
        students = Database.get_students(schoolclass)
        cls.student_email_map = {f"{s[1]}, {s[0]}": s[2] for s in students}
        student_names = sorted([f"{s[1]}, {s[0]}" for s in students])
        layout = [
            [sg.Listbox(values=student_names, size=(30, 10), key='student_list',
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
        ]
        return layout

    # Diese Methode ist dafür zuständig festzulegen welcher Schüler ausgewählt wurde um die entsprechenden Daten zu beziehen.
    @classmethod
    def selected_student(cls, values):
        selected_student = values['student_list'][0] if values['student_list'] else None
        if selected_student:
            student_mail = cls.student_email_map[selected_student]
            student_info = Database.get_student(student_mail)
            LoginManager.set_student(student_info)
            from gui.teacher.TeacherStudentPage import TeacherStudentPage
            WindowManager.update(TeacherStudentPage.get_layout(student_info),
                                 TeacherStudentPage.event_handler, size=(400, 200))
        else:
            sg.popup("Bitte wählen Sie einen Schüler aus", location=WindowManager.last_location, no_titlebar=True,
                     keep_on_top=True, modal=True)
