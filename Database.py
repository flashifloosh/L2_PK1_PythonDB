import hashlib
import os.path
import sqlite3 as db


class Database:
    def __init__(self):
        import sqlite3 as db
        import os
        self.cursor = None
        self.conn = None
        self.create_db()

    @classmethod
    def create_db(cls):
        if not os.path.exists('data.db'):
            cls.connect()
            with open('script.sql', 'r') as f:
                cls.cursor.executescript(f.read())
                cls.conn.commit()
            cls.close()

    @classmethod
    def connect(cls):
        cls.conn = db.connect('data.db')
        cls.cursor = cls.conn.cursor()

    @classmethod
    def close(cls):
        cls.conn.close()

    @classmethod
    def student_register(cls, fname, lname, email, password, schoolclass):
        # encrypt password to sha256
        cls.connect()
        schoolclass_value = schoolclass[0] if isinstance(schoolclass, tuple) else schoolclass
        if cls.cursor.execute('SELECT * FROM student WHERE email = ?', (email,)).fetchone():
            cls.close()
            raise Exception("Diese E-Mail Adresse ist bereits registriert")
        elif fname == '' or lname == '' or email == '' or password == '' or schoolclass == '':
            cls.close()
            raise Exception("Bitte füllen Sie alle Felder aus")
        elif len(password) < 8:
            cls.close()
            raise Exception("Das Passwort muss mindestens 8 Zeichen lang sein")
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cls.cursor.execute('INSERT INTO student (fname, lname, email, secret, class) VALUES (?, ?, ?, ?, ?)',
                           (fname, lname, email, hashed_pw, schoolclass_value))
        cls.conn.commit()
        cls.close()
        return True

    @classmethod
    def student_login(cls, email, password):
        cls.connect()
        # TODO encrypt password to sha256 and compare
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        cls.cursor.execute('SELECT * FROM student WHERE email = ? AND secret = ?', (email, hashed_pw))
        if cls.cursor.fetchone():
            cls.close()
            return True
        else:
            cls.close()
            return False

    @classmethod
    def getSchoolclasses(cls):
        cls.connect()
        cls.cursor.execute('SELECT classname FROM class')
        classes = cls.cursor.fetchall()
        cls.close()
        return classes

    def get_student(self, email):
        self.connect()
        self.cursor.execute('SELECT * FROM student WHERE email = ?', (email,))
        student = self.cursor.fetchone()
        self.close()
        return student