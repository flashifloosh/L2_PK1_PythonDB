from database_util.Database import Database
import hashlib

from gui.LoginManager import LoginManager


class TeacherUtil:

    verification_code = "abAB12"

    @classmethod
    def teacher_register(cls, fname, lname, email, password, verification_code):
        Database.connect()
        query = 'SELECT email FROM teacher WHERE email = ?'
        if Database.cursor.execute(query, (email,)).fetchone():
            Database.close()
            raise Exception("Diese E-Mail Adresse ist bereits registriert")
        elif fname == '' or lname == '' or email == '' or password == '' or verification_code == '':
            Database.close()
            raise Exception("Bitte füllen Sie alle Felder aus")
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
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'SELECT id, fname, lname, email FROM teacher WHERE email = ? AND secret = ?'
        Database.cursor.execute(query, (email, hashed_pw))
        teacher = Database.cursor.fetchone()
        if teacher is None:
            Database.close()
            raise Exception("E-Mail oder Passwort falsch")
        LoginManager.set_teacher(teacher)
        Database.close()
