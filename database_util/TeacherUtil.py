import hashlib

from database_util.Database import Database
from gui.LoginManager import LoginManager


class TeacherUtil:
    verification_code = "code12"

    @classmethod
    def teacher_register(cls, fname, lname, email, password, verification_code):
        fname = fname.strip()
        lname = lname.strip()
        email = email.strip()
        password = password.strip()
        verification_code = verification_code.strip()

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
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'INSERT INTO teacher (fname, lname, email, secret, verify) VALUES (?, ?, ?, ?, ?)'
        Database.cursor.execute(query, (fname, lname, email, hashed_pw, verification_code))
        Database.conn.commit()
        Database.close()

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

    @classmethod
    def get_student_grades(cls, student_id):
        Database.connect()
        query = 'SELECT subject, grade FROM certificate WHERE student = ?'
        Database.cursor.execute(query, (student_id,))
        grades = Database.cursor.fetchall()
        Database.close()
        return grades

