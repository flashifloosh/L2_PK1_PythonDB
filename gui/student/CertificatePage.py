import FreeSimpleGUI as sg
from database_util.Database import Database
from database_util.StudentUtil import StudentUtil
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
import csv


class CertificatePage:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button("Zurück", key='back', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Text(size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                cls.generate_cert_table(LoginManager.get_student())
            ],
            [
                sg.Button('Exportieren', key='export', size=(10, 1))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentStartpage import StudentStartpage
            WindowManager.update(StudentStartpage().get_layout(), StudentStartpage.event_handler)
        elif event == 'export':
            filename = sg.popup_get_file('Save As', save_as=True, default_extension='.csv', default_path='cert.csv')
            if filename:
                CertificatePage.export_to_csv(filename)
                sg.user_settings_set_entry('-filename-', filename)
                sg.popup('Export successful!')
        elif event == sg.WIN_CLOSED:
            pass

    @classmethod
    def generate_cert_table(cls, student):
        subjects = Database.get_subjects()
        subject_names = [subject[1] for subject in subjects]
        student_grades = StudentUtil.student_cert(student[3])
        grades = Database.get_grades()

        grade_descriptions = []
        for subject in subjects:
            grade_value = next((grade[0] for grade in student_grades if grade[1] == subject[0]), None)
            if grade_value is not None:
                grade_description = next((g[1] for g in grades if g[0] == grade_value), "")
            else:
                grade_description = ""
            grade_descriptions.append(grade_description)

        layout = [
            [sg.Table(
                values=[grade_descriptions],
                headings=subject_names,
                display_row_numbers=False,
                num_rows=2,
                size=(sum(len(name) for name in subject_names) * 10, 200),
                vertical_scroll_only=True,
                hide_vertical_scroll=True,
            )]
        ]

        return layout

    @classmethod
    def export_to_csv(cls, filename):
        student = LoginManager.get_student()
        subjects = Database.get_subjects()
        subject_names = [subject[1] for subject in subjects]
        student_grades = StudentUtil.student_cert(student[3])
        grades = Database.get_grades()

        grade_descriptions = []
        for subject in subjects:
            grade_value = next((grade[0] for grade in student_grades if grade[1] == subject[0]), None)
            if grade_value is not None:
                grade_description = next((g[1] for g in grades if g[0] == grade_value), "")
            else:
                grade_description = ""
            grade_descriptions.append(grade_description)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(subject_names)
            writer.writerow(grade_descriptions)
