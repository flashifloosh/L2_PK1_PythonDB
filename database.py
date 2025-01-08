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
        cls.cursor.execute('INSERT INTO student (fname, lname, email, secret, class) VALUES (?, ?, ?, ?, ?)',
                           (fname, lname, email, password, schoolclass_value))
        cls.conn.commit()
        cls.close()
        print('Registration successful')

    @classmethod
    def student_login(cls, email, password):
        cls.connect()
        # TODO encrypt password to sha256 and compare
        cls.cursor.execute('SELECT * FROM student WHERE email = ? AND secret = ?', (email, password))
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
