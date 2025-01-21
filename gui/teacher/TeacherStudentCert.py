import FreeSimpleGUI as sg
from database_util.Database import Database
from database_util.TeacherUtil import TeacherUtil
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil
import csv
import os


class TeacherStudentCert:

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
                sg.Button("Importieren", key='import', size=(10, 2)),
                sg.Button("Exportieren", key='export', size=(10, 2))
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
            from gui.teacher.TeacherStudentPage import TeacherStudentPage
            WindowManager.update(TeacherStudentPage().get_layout(LoginManager.get_student()),
                                 TeacherStudentPage.event_handler, size=(400, 300))
        elif event == 'import':
            filename = sg.popup_get_file('Open', file_types=(('CSV Files', '*.csv'),))
            if filename:
                TeacherStudentCert.import_from_csv(filename)
        elif event == 'export':
            student = LoginManager.get_student()
            filename = sg.popup_get_file('Save As', save_as=True, default_extension='.csv',
                                         default_path=f'cert_{student[1]}.{student[2]}.csv')
            if filename:
                TeacherStudentCert.export_to_csv(filename)
                sg.popup_quick_message('Registrierung erfolgreich', location=WindowManager.last_location)
        elif event == 'save':
            TeacherStudentCert.save_grades(values)
            sg.popup_quick_message('Registrierung erfolgreich', location=WindowManager.last_location)

    @classmethod
    def save_grades(cls, values):
        student_id = LoginManager.get_student()[0]
        teacher_id = LoginManager.get_teacher()[0]

        Database.connect()
        for key, value in values.items():
            if key.endswith('_grade'):
                subject_name = key.replace('_grade', '')
                new_grade = value
                if not new_grade:
                    continue
                # Get the subject_id from the subject name
                query = 'SELECT id FROM subject WHERE name = ?'
                Database.cursor.execute(query, (subject_name,))
                subject_id = Database.cursor.fetchone()[0]
                # Check if the grade already exists
                query = 'SELECT grade, teacher FROM certificate WHERE student = ? AND subject = ?'
                Database.cursor.execute(query, (student_id, subject_id))
                existing_record = Database.cursor.fetchone()
                if existing_record:
                    existing_grade, existing_teacher = existing_record
                    # Only update if the new grade is different from the existing grade
                    if new_grade != existing_grade:
                        query = 'UPDATE certificate SET grade = ?, teacher = ? WHERE student = ? AND subject = ?'
                        Database.cursor.execute(query, (new_grade, teacher_id, student_id, subject_id))
                else:
                    # Insert a new grade
                    query = 'INSERT INTO certificate (student, subject, grade, teacher) VALUES (?, ?, ?, ?)'
                    Database.cursor.execute(query, (student_id, subject_id, new_grade, teacher_id))
        Database.conn.commit()
        Database.close()

    @classmethod
    def generate_cert_table(cls, student):
        student_id = student[0]
        Database.connect()
        query = 'SELECT subject.name, certificate.grade FROM certificate JOIN subject ON certificate.subject = subject.id WHERE certificate.student = ?'
        Database.cursor.execute(query, (student_id,))
        certificates = Database.cursor.fetchall()

        # Fetch all subjects from the database
        subjects = Database.get_subjects()
        subjects = [subject[1] for subject in subjects]

        # Fetch all grades from the database
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

    @classmethod
    def export_to_csv(cls, filename):
        student = LoginManager.get_student()
        subjects = Database.get_subjects()
        subject_names = [subject[1] for subject in subjects]
        student_grades = TeacherUtil.get_student_grades(student[0])

        grade_values = []
        for subject in subjects:
            grade_value = next((grade[1] for grade in student_grades if grade[0] == subject[0]), "")
            grade_values.append(grade_value)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(subject_names)
            writer.writerow(grade_values)

    @classmethod
    def import_from_csv(cls, filename):
        # Validate and sanitize the file path
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        if not os.path.isfile(filename):
            sg.popup('Bitte geben Sie einen gültigen Dateipfad an.')
            return

        # Check if the file is a CSV
        if not filename.lower().endswith('.csv'):
            sg.popup('Bitte wählen Sie eine CSV-Datei aus.')
            return

        # Detect the separator
        with open(filename, 'r') as csvfile:
            sample = csvfile.read(1024)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)

            subject_names = next(reader)
            grade_values = next(reader)

        # Fetch all valid grades from the database
        valid_grades = {str(grade[0]) for grade in Database.get_grades()}

        # Check if all grades in the CSV are valid
        for grade in grade_values:
            if grade and grade not in valid_grades:
                sg.popup('Die CSV-Datei enthält ungültige Noten.')
                return

        student_id = LoginManager.get_student()[0]
        teacher_id = LoginManager.get_teacher()[0]
        changes = []
        Database.connect()
        for subject_name, new_grade in zip(subject_names, grade_values):
            if new_grade:
                query = 'SELECT id FROM subject WHERE name = ?'
                Database.cursor.execute(query, (subject_name,))
                subject_id = Database.cursor.fetchone()[0]
                query = 'SELECT grade FROM certificate WHERE student = ? AND subject = ?'
                Database.cursor.execute(query, (student_id, subject_id))
                existing_record = Database.cursor.fetchone()
                old_grade = existing_record[0] if existing_record else None
                if old_grade is None:
                    changes.append((subject_name, None, new_grade, student_id, subject_id, teacher_id))
                elif str(old_grade) != str(new_grade):
                    changes.append((subject_name, old_grade, new_grade, student_id, subject_id, teacher_id))
        Database.close()
        if not changes:
            sg.popup('Keine Änderungen gefunden.')
            return

        changes_layout = [
            [sg.Text('Möchten Sie die folgenden Änderungen speichern?')],
            *[[sg.Text(
                f'{subject_name}: {old_grade} -> {new_grade}' if old_grade is not None else f'{subject_name}: {new_grade}')]
                for subject_name, old_grade, new_grade, _, _, _ in changes],
            [sg.Button('Ja', key='confirm'), sg.Button('Abbrechen', key='cancel')]
        ]
        changes_window = sg.Window('Info', changes_layout, modal=True)

        while True:
            event, _ = changes_window.read()
            if event == 'confirm':
                Database.connect()
                for subject_name, old_grade, new_grade, student_id, subject_id, teacher_id in changes:
                    if old_grade is None:
                        query = 'INSERT INTO certificate (student, subject, grade, teacher) VALUES (?, ?, ?, ?)'
                        Database.cursor.execute(query, (student_id, subject_id, new_grade, teacher_id))
                    else:
                        query = 'UPDATE certificate SET grade = ?, teacher = ? WHERE student = ? AND subject = ?'
                        Database.cursor.execute(query, (new_grade, teacher_id, student_id, subject_id))
                Database.conn.commit()
                Database.close()
                changes_window.close()
                from gui.teacher.TeacherStudentPage import TeacherStudentPage
                WindowManager.update(TeacherStudentPage.get_layout(LoginManager.get_student()),
                                     TeacherStudentPage.event_handler, size=(400, 300))
                break
            elif event in (sg.WIN_CLOSED, 'cancel'):
                changes_window.close()
                break
