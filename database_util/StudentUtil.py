from database_util.Database import Database
import hashlib

from gui.LoginManager import LoginManager


class StudentUtil:
    @classmethod
    def student_register(cls, fname, lname, email, password, schoolclass):
        Database.connect()
        query = 'SELECT * FROM student WHERE email = ?'
        if Database.cursor.execute(query, (email,)).fetchone():
            Database.close()
            raise Exception("Diese E-Mail Adresse ist bereits registriert")
        elif fname == '' or lname == '' or email == '' or password == '' or schoolclass == '':
            Database.close()
            raise Exception("Bitte füllen Sie alle Felder aus")
        elif len(password) < 8:
            Database.close()
            raise Exception("Das Passwort muss mindestens 8 Zeichen lang sein")
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'INSERT INTO student (fname, lname, email, secret, class) VALUES (?, ?, ?, ?, ?)'
        Database.cursor.execute(query, (fname, lname, email, hashed_pw, schoolclass))
        Database.conn.commit()
        Database.close()
        return True

    @classmethod
    def student_login(cls, email, password):
        Database.connect()
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'SELECT * FROM student WHERE email = ? AND secret = ?'
        Database.cursor.execute(query, (email, hashed_pw))
        student = Database.cursor.fetchone()
        if not student:
            Database.close()
            raise Exception("E-Mail oder Passwort falsch")
        LoginManager.set_student(student)
        Database.close()
