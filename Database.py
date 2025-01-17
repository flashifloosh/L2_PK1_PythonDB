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
        query = 'SELECT * FROM student WHERE email = ?'
        if cls.cursor.execute(query, (email,)).fetchone():
            cls.close()
            raise Exception("Diese E-Mail Adresse ist bereits registriert")
        elif fname == '' or lname == '' or email == '' or password == '' or schoolclass == '':
            cls.close()
            raise Exception("Bitte füllen Sie alle Felder aus")
        elif len(password) < 8:
            cls.close()
            raise Exception("Das Passwort muss mindestens 8 Zeichen lang sein")
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'INSERT INTO student (fname, lname, email, secret, class) VALUES (?, ?, ?, ?, ?)'
        cls.cursor.execute(query, (fname, lname, email, hashed_pw, schoolclass))
        cls.conn.commit()
        cls.close()
        return True

    @classmethod
    def student_login(cls, email, password):
        cls.connect()
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = 'SELECT * FROM student WHERE email = ? AND secret = ?'
        cls.cursor.execute(query, (email, hashed_pw))
        if cls.cursor.fetchone():
            cls.close()
            return True
        else:
            cls.close()
            return False

    @classmethod
    def get_schoolclasses(cls):
        cls.connect()
        query = 'SELECT classname FROM class'
        cls.cursor.execute(query)
        classes = cls.cursor.fetchall()
        cls.close()
        return classes

    @classmethod
    def get_subjects(cls):
        cls.connect()
        query = 'SELECT name FROM subject'
        cls.cursor.execute(query)
        subjects = cls.cursor.fetchall()
        cls.close()
        return subjects

    @classmethod
    def get_student(cls, email):
        cls.connect()
        query = 'SELECT fname, lname, email, class FROM student WHERE email = ?'
        cls.cursor.execute(query, (email,))
        student = cls.cursor.fetchone()
        return student
