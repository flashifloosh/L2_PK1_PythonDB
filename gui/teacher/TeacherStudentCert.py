import FreeSimpleGUI as sg

from database_util.CertificateUtil import CertificateUtil
from database_util.Database import Database
from database_util.TeacherUtil import TeacherUtil
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherStudentCert:

    # Die grafische Oberfläche für den TeacherStudentCert wird generiert, bzw bereitgestellt.
    @classmethod
    def get_layout(cls, student):
        return [
            [
                sg.Button("Abmelden", key='logout', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Button(key='back', image_filename=ImageUtil.get_back_image(), image_subsample=30, border_width=0,
                          button_color=('white', sg.theme_background_color())),
                sg.Text(f'Schüler: {student[2]}, {student[1]}', size=(20, 1), font=('Helvetica', 15),
                        text_color='black')
            ],
            [
                sg.Column(cls.generate_cert_table(student))
            ],
            [
                sg.Button("Speichern", key='save', size=(10, 1)),
            ],
            [
                sg.Button("Importieren als CSV", key='import_csv', size=(10, 2)),
                sg.Button("Exportieren als CSV", key='export_csv', size=(10, 2)),
            ],
            [

                sg.Button("Importieren als JSON", key='import_json', size=(10, 2)),
                sg.Button("Exportieren als JSON", key='export_json', size=(10, 2))
            ]
        ]

    # Die Aktionen der Buttons wird definiert.
    # Beim logout Button wird die Startpage geladen.
    # Beim back Button, wird die TeacherStudentPage geladen.
    # Die Import Funktionen fordern auf das entsprechende Element auszuwählen.
    # Die Export Funktionen fordern auf ein entsprechendes Element zu deklarieren, wo die Daten gespeichert werden.
    # Insofern man speichert werden die Noten in der Datenbank des Schülers geupdated.
    @staticmethod
    def event_handler(event, values):
        if event == 'logout':
            from gui.Startpage import Startpage
            WindowManager.update(Startpage().get_layout(), Startpage.event_handler)
            LoginManager.set_teacher(None)
            LoginManager.set_student(None)
        elif event == 'back':
            from gui.teacher.TeacherStudentPage import TeacherStudentPage
            WindowManager.update(TeacherStudentPage().get_layout(LoginManager.get_student()),
                                 TeacherStudentPage.event_handler, size=(400, 300))
        elif event == 'import_csv':
            filename = sg.popup_get_file('Öffnen', file_types=(('CSV Files', '*.csv'),))
            if filename:
                TeacherUtil.import_cert_from_file(filename)
        elif event == 'import_json':
            filename = sg.popup_get_file('Öffnen', file_types=(('JSON Files', '*.json'),))
            if filename:
                TeacherUtil.import_cert_from_file(filename)
        elif event == 'export_csv':
            student = LoginManager.get_student()
            filename = sg.popup_get_file('Speichern als', save_as=True, default_extension='.csv',
                                         default_path=f'cert_{student[1]}.{student[2]}.csv')
            if filename:
                CertificateUtil.export_file_for_teacher(filename, file_format='csv')
                WindowManager.popup_quick_message('Erfolgreich exportiert.')
        elif event == 'export_json':
            student = LoginManager.get_student()
            filename = sg.popup_get_file('Speichern als', save_as=True, default_extension='.json',
                                         default_path=f'cert_{student[1]}.{student[2]}.json')
            if filename:
                CertificateUtil.export_file_for_teacher(filename, file_format='json')
                WindowManager.popup_quick_message('Erfolgreich exportiert.')
        elif event == 'save':
            CertificateUtil.save_grades(values)
            WindowManager.popup_quick_message('Noten gespeichert.')

    # Die generierung der Zertifikatsansicht wird durchgeführt.
    # Dafür werden alle benötigten Daten aus der Datenbank bezogen.
    # Da die Anzeige immer gleich ist, werden die Fächernamen gelistet und die Noten aus der Datenbank hineingeschrieben.
    @classmethod
    def generate_cert_table(cls, student):
        student_id = student[0]
        Database.connect()
        query = 'SELECT subject.name, certificate.grade FROM certificate JOIN subject ON certificate.subject = subject.id WHERE certificate.student = ?'
        Database.cursor.execute(query, (student_id,))
        certificates = Database.cursor.fetchall()

        subjects = Database.get_subjects()
        subjects = [subject[1] for subject in subjects]

        grades = Database.get_grades()
        grades = [grade[0] for grade in grades]

        Database.close()

        layout = [
            [sg.Text('Fach', size=(20, 1)), sg.Text('Note', size=(10, 1))],
            [sg.Text('_' * 100, size=(30, 1))]
        ]

        cert_dict = {cert[0]: cert[1] for cert in certificates}
        for subject in subjects:
            grade = cert_dict.get(subject, '')
            layout.append([sg.Text(subject, size=(20, 1)),
                           sg.Combo(grades, default_value=grade, key=f'{subject}_grade', size=(10, 1), readonly=True)])

        return layout
