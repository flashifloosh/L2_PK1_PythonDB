import FreeSimpleGUI as sg

from database_util.CertificateUtil import CertificateUtil
from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager


class StudentCertificatePage:
    # Die grafische Oberfläche für die StudentCertificatePage wird generiert, bzw bereitgestellt.
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
                sg.Button('Exportieren als JSON', key='export_json', size=(10, 2)),
                sg.Button('Exportieren als CSV', key='export_csv', size=(10, 2))

            ]
        ]

    # Die Aktionen der export Buttons wird definiert.
    # Beim zurück Button wird die StudentStartpage geladen.
    # Wenn man die Datei als csv exportiert, wird diese automatisch als .csv Datei abgespeichert.
    # Wenn man die Datei jedoch als json exportiert, wird diese automatisch als .json Datei abgespeichert.
    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentStartpage import StudentStartpage
            WindowManager.update(StudentStartpage().get_layout(), StudentStartpage.event_handler)
        elif event == 'export_csv':
            filename = sg.popup_get_file('Save As', save_as=True, default_extension='.csv', default_path='cert.csv')
            if filename:
                CertificateUtil.export_cert_for_student(filename, file_format='csv')
                sg.user_settings_set_entry('-filename-', filename)
                WindowManager.popup_quick_message('Erfolgreich exportiert.')
        elif event == 'export_json':
            filename = sg.popup_get_file('Save As', save_as=True, default_extension='.json', default_path='cert.json')
            if filename:
                CertificateUtil.export_cert_for_student(filename, file_format='json')
                sg.user_settings_set_entry('-filename-', filename)
                WindowManager.popup_quick_message('Erfolgreich exportiert.')

    # Die Zertifikatstabelle wird generiert für den Schüler
    @classmethod
    def generate_cert_table(cls, student):
        subjects = Database.get_subjects()
        subject_names = [subject[1] for subject in subjects]
        grade_descriptions = CertificateUtil.get_grade_descriptions(student, subjects)

        layout = [
            [sg.Table(
                values=[grade_descriptions],
                headings=subject_names,
                display_row_numbers=False,
                num_rows=2,
                size=(sum(len(name) for name in subject_names) * 10, 200),
                vertical_scroll_only=False,
                hide_vertical_scroll=True,
            )]
        ]

        return layout
