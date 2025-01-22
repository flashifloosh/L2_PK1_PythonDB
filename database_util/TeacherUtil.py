import csv
import hashlib
import json
import os

import FreeSimpleGUI as sg

from database_util.Database import Database
from gui.LoginManager import LoginManager
from gui.WindowManager import WindowManager
from images.ImageUtil import ImageUtil


class TeacherUtil:
    verification_code = "code12"

    # Daten werden gesammelt beim Lehrer registrieren
    @classmethod
    def teacher_register(cls, fname, lname, email, password, verification_code):
        fname = fname.strip()
        lname = lname.strip()
        email = email.strip()
        password = password.strip()
        verification_code = verification_code.strip()

        # Check, ob die Mail schon vergeben wurde oder ein Feld frei gelassen wurde.
        # Überprüfung der korrektheit der Mail und der Länge des Passworts als auch des Verification Codes.
        Database.connect()
        query = 'SELECT email FROM teacher WHERE email = ?'
        if Database.cursor.execute(query, (email,)).fetchone():
            Database.close()
            raise Exception("Diese E-Mail Adresse ist bereits registriert")
        elif fname == '' or lname == '' or email == '' or password == '' or verification_code == '':
            Database.close()
            raise Exception("Bitte füllen Sie alle Felder aus")
        elif '@' not in email or '.' not in email:
            Database.close()
            raise Exception("Bitte geben Sie eine gültige E-Mail Adresse ein")
        elif len(password) < 8:
            Database.close()
            raise Exception("Das Passwort muss mindestens 8 Zeichen lang sein")
        elif verification_code != cls.verification_code:
            Database.close()
            raise Exception("Der Verifizierungscode ist ungültig")

        # Das Passwort wird gehashed, sodass die Sicherheit gewährleistet wird.
        # Der Benutzer wird mit den entsprechenden Daten in der Datenbank angelegt.
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'INSERT INTO teacher (fname, lname, email, secret, verify) VALUES (?, ?, ?, ?, ?)'
        Database.cursor.execute(query, (fname, lname, email, hashed_pw, verification_code))
        Database.conn.commit()
        Database.close()

    # Beim Lehrer Login wird zuerst das Passwort gehashed und mit dem hash Wert der Datenbank verglichen.
    # Es wird dann die Mail mit der Datenbank verglichen und der entsprechende Nutzer wird eingeloggt.
    # Fehler bei falscher Mail oder Passwort.
    @classmethod
    def teacher_login(cls, email, password):
        Database.connect()
        email = email.strip()  # Remove leading and trailing whitespace
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'SELECT id, fname, lname, email FROM teacher WHERE email = ? AND secret = ?'
        Database.cursor.execute(query, (email, hashed_pw))
        teacher = Database.cursor.fetchone()
        if teacher is None:
            Database.close()
            raise Exception("E-Mail oder Passwort falsch")
        LoginManager.set_teacher(teacher)
        Database.close()

    # Bezieht alle Noten eines Schülers
    @classmethod
    def get_student_grades(cls, student_id):
        Database.connect()
        query = 'SELECT subject, grade FROM certificate WHERE student = ?'
        Database.cursor.execute(query, (student_id,))
        grades = Database.cursor.fetchall()
        Database.close()
        return grades

    # Bereitstellung eines Layouts für Schüler, da es öfters verwendet wird
    @classmethod
    def generate_common_layout(cls, student):
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
                sg.Column(cls.generate_student_info(student))
            ]
        ]

    # Gibt die E-Mail und Klasse eines Schülers aus
    @classmethod
    def generate_student_info(cls, student):
        from database_util.Database import Database
        student = Database.get_student(student[3])
        return [
            [sg.Text('Klasse:'), sg.Text(f'{student[4]}')],
            [sg.Text('E-Mail:'), sg.Text(f'{student[3]}')],
        ]

    # Methode um einen Schüler aus dem System zu löschen
    @classmethod
    def delete_student(cls, student):
        from database_util.Database import Database
        Database.delete_student(student[3])
        from gui.teacher.TeacherStudentSelection import TeacherStudentSelection
        WindowManager.update(TeacherStudentSelection().get_layout(LoginManager.get_class()),
                             TeacherStudentSelection.event_handler, size=(400, 300))
        LoginManager.set_student(None)

    # Methode um Noten eines Schülers zu importieren
    @classmethod
    def import_cert_from_file(cls, filename):
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        if not os.path.isfile(filename):
            sg.popup('Bitte geben Sie einen gültigen Dateipfad an.')
            return

        # Überprüft, ob die Datei eine JSON- oder CSV-Datei ist.
        # Wenn es eine CSV-Datei ist, wird das Trennzeichen bestimmt und die Datei eingelesen.
        # Wenn es eine JSON-Datei ist, wird die Datei eingelesen.
        if filename.lower().endswith('.csv'):
            try:
                with open(filename, 'r') as csvfile:
                    sample = csvfile.read(1024)
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(sample)
                    csvfile.seek(0)
                    reader = csv.reader(csvfile, dialect)

                    subject_ids = next(reader)
                    grade_values = next(reader)
            except csv.Error:
                sg.popup('Konnte das Trennzeichen nicht bestimmen. Bitte überprüfen Sie die CSV-Datei.')
                return
        elif filename.lower().endswith('.json'):
            try:
                with open(filename, 'r') as jsonfile:
                    data = json.load(jsonfile)
                    subject_ids = list(data.keys())
                    grade_values = [str(value) if value != 0 else "" for value in data.values()]
            except json.JSONDecodeError:
                sg.popup('Die JSON-Datei ist ungültig.')
                return
        else:
            sg.popup('Bitte wählen Sie eine CSV- oder JSON-Datei aus.')
            return

        # Zuordnung der Fach-IDs zu Fachnamen
        subjects = Database.get_subjects()
        subject_id_to_name = {subject[0]: subject[1] for subject in subjects}
        subject_names = [subject_id_to_name.get(subject_id, subject_id) for subject_id in subject_ids]

        # Bezieht alle möglichen Noten aus der Datenbank
        valid_grades = {str(grade[0]) for grade in Database.get_grades()}

        # Überprüft, ob die Noten auch gültig sind
        for grade in grade_values:
            if grade and grade not in valid_grades:
                sg.popup('Die Datei enthält ungültige Noten.')
                return

        # Überprüft, ob die Datei andere Noten beinhaltet, als bereits bei einem Schüler hinterlegt sind.
        # Wenn dies der Fall ist, werden die Noten überschrieben und ansonsten nicht.
        student_id = LoginManager.get_student()[0]
        teacher_id = LoginManager.get_teacher()[0]
        changes = []
        Database.connect()
        for subject_name, new_grade in zip(subject_names, grade_values):
            if new_grade:
                query = 'SELECT grade FROM certificate WHERE student = ? AND subject = (SELECT id FROM subject WHERE name = ?)'
                Database.cursor.execute(query, (student_id, subject_name))
                existing_record = Database.cursor.fetchone()
                old_grade = existing_record[0] if existing_record else None
                if old_grade is None:
                    changes.append((subject_name, None, new_grade, student_id, subject_name, teacher_id))
                elif str(old_grade) != str(new_grade):
                    changes.append((subject_name, old_grade, new_grade, student_id, subject_name, teacher_id))
        Database.close()
        if not changes:
            sg.popup('Keine Änderungen gefunden.', no_titlebar=True, location=WindowManager.last_location,
                     keep_on_top=True, modal=True)
            return

        # Abfrage, ob man sich sicher ist, die Änderung der Noten zu machen
        changes_layout = [
            [sg.Text('Möchten Sie die folgenden Änderungen speichern?')],
            *[[sg.Text(
                f'{subject_name}: {old_grade} -> {new_grade}' if old_grade is not None else f'{subject_name}: {new_grade}')]
                for subject_name, old_grade, new_grade, _, _, _ in changes],
            [sg.Button('Ja', key='confirm'), sg.Button('Abbrechen', key='cancel')]
        ]
        changes_window = sg.Window('Info', changes_layout, modal=True)

        # Window-Objekt wird geschlossen, wenn der Nutzer auf "Ja" oder "Abbrechen" klickt.
        # Wenn der Nutzer auf "Ja" klickt, werden die Änderungen in der Datenbank gespeichert.
        # Danach springt man zurück auf die vorherige Seite. Und eine Nachricht wird angezeigt.
        while True:
            event, _ = changes_window.read()
            if event == 'confirm':
                Database.connect()
                for subject_name, old_grade, new_grade, student_id, subject_name, teacher_id in changes:
                    if old_grade is None:
                        query = 'INSERT INTO certificate (student, subject, grade, teacher) VALUES (?, (SELECT id FROM subject WHERE name = ?), ?, ?)'
                        Database.cursor.execute(query, (student_id, subject_name, new_grade, teacher_id))
                    else:
                        query = 'UPDATE certificate SET grade = ?, teacher = ? WHERE student = ? AND subject = (SELECT id FROM subject WHERE name = ?)'
                        Database.cursor.execute(query, (new_grade, teacher_id, student_id, subject_name))
                Database.conn.commit()
                Database.close()
                changes_window.close()
                from gui.teacher.TeacherStudentPage import TeacherStudentPage
                WindowManager.update(TeacherStudentPage.get_layout(LoginManager.get_student()),
                                     TeacherStudentPage.event_handler, size=(400, 300))
                WindowManager.popup_quick_message('Noten importiert und gespeichert.')
                break
            elif event in (sg.WIN_CLOSED, 'cancel'):
                changes_window.close()
                break
