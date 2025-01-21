import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


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
            print('import')
        elif event == 'export':
            print('export')
        elif event == 'save':
            TeacherStudentCert.save_grades(values)

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
