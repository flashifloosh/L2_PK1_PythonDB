import csv
import json

from database_util.Database import Database
from database_util.StudentUtil import StudentUtil
from database_util.TeacherUtil import TeacherUtil
from gui.LoginManager import LoginManager


class CertificateUtil:

    # Zusammenstellung des Zertifikats aus Note und Fachname.
    # Gibt dann für einen Schüler eine Liste aus, die aus allen Noten besteht.
    @classmethod
    def get_cert(cls, student):
        Database.connect()
        query = 'SELECT subject, grade FROM certificate WHERE student = ?'
        Database.cursor.execute(query, (student,))
        certificate = Database.cursor.fetchall()
        Database.close()
        return certificate

    # Anforderung der Noten beschreibungen, da der Schüler nicht die Zahl wie der Lehrer bekommt.
    # Der Schüler bekommt die Namen der Noten angezeigt.
    @classmethod
    def get_grade_descriptions(cls, student, subjects):
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

        return grade_descriptions

    # Fordert die Noten aus der Datenbank an für den Schüler, damit dieser seine Noten exportieren kann.
    @classmethod
    def export_cert_for_student(cls, filename, file_format='csv'):
        student = LoginManager.get_student()
        subjects = Database.get_subjects()
        grades = cls.get_cert(student[0])
        cls.export_cert(filename, subjects, grades, file_format, export_subject_id=False)

    # Exportiert die Noten eines Schülers, wenn der Leherer einen ausgewählt hat.
    @classmethod
    def export_file_for_teacher(cls, filename, file_format='csv'):
        student = LoginManager.get_student()
        subjects = Database.get_subjects()
        grades = TeacherUtil.get_student_grades(student[0])
        cls.export_cert(filename, subjects, grades, file_format, export_subject_id=True)

    # legt fest, wie die Dateien angelegt werden sollen, bezüglich der Syntax.
    @classmethod
    def export_cert(cls, filename, subjects, grades, file_format='csv', export_subject_id=False):
        subject_identifiers = [subject[0] if export_subject_id else subject[1] for subject in subjects]
        grade_dict = {grade[0]: grade[1] for grade in grades}

        if file_format == 'json':
            grade_values = [grade_dict.get(subject[0], 0) for subject in subjects]  # Use 0 if there's no value
        else:
            grade_values = [grade_dict.get(subject[0], '') for subject in
                            subjects]  # Use empty string if there's no value

        # Deklarierung der Syntax in der csv Datei
        if file_format == 'csv':
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(subject_identifiers)
                writer.writerow(grade_values)

        # Deklarierung der Syntax in der json Datei
        elif file_format == 'json':
            data = {subject: grade for subject, grade in zip(subject_identifiers, grade_values)}
            with open(filename, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=4)

    # Speichert die Noten des Schülers in der Datenbank.
    @classmethod
    def save_grades(cls, values):
        student_id = LoginManager.get_student()[0]
        teacher_id = LoginManager.get_teacher()[0]

        # Verbindung zur Datenbank
        Database.connect()

        # Durchgehen der Werte und speichern der Noten in der Datenbank
        for key, value in values.items():
            if key.endswith('_grade'):
                # Bekomme den Schulfachnamen mit dem Suffix '_grade'
                subject_name = key.replace('_grade', '')
                new_grade = value
                # Speichere nur, wenn eine Note eingegeben wurde
                if not new_grade:
                    continue

                # Bekomme die ID des Schulfachs
                query = 'SELECT id FROM subject WHERE name = ?'
                Database.cursor.execute(query, (subject_name,))
                subject_id = Database.cursor.fetchone()[0]

                # Überprüfe, ob der Schüler bereits eine Note in diesem Fach hat
                query = 'SELECT grade, teacher FROM certificate WHERE student = ? AND subject = ?'
                Database.cursor.execute(query, (student_id, subject_id))
                existing_record = Database.cursor.fetchone()
                # überprüfe, ob die Note auch die identische ist, wenn nicht wird die Note geändert.
                if existing_record:
                    existing_grade, existing_teacher = existing_record
                    if new_grade != existing_grade:
                        query = 'UPDATE certificate SET grade = ?, teacher = ? WHERE student = ? AND subject = ?'
                        Database.cursor.execute(query, (new_grade, teacher_id, student_id, subject_id))
                else:
                    # Füge die Note hinzu, wenn der Schüler noch keine Note in diesem Fach hat
                    query = 'INSERT INTO certificate (student, subject, grade, teacher) VALUES (?, ?, ?, ?)'
                    Database.cursor.execute(query, (student_id, subject_id, new_grade, teacher_id))
        Database.conn.commit()
        Database.close()
