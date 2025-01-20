import os.path
import sqlite3 as db
import sys


class Database:
    cursor = None
    conn = None

    def __init__(self):
        self.create_db()

    @classmethod
    def create_db(cls):
        if not os.path.exists('./data.db'):
            cls.connect()
            # Get the absolute path to the script.sql file
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(base_path, 'database_util', 'script.sql')
            if not os.path.exists(file):
                file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'script.sql')
            with open(file, 'r') as f:
                cls.cursor.executescript(f.read())
                cls.conn.commit()
            cls.close()

    @classmethod
    def connect(cls):
        cls.conn = db.connect('./data.db')
        cls.cursor = cls.conn.cursor()

    @classmethod
    def close(cls):
        cls.conn.close()

    @classmethod
    def get_schoolclasses(cls):
        cls.connect()
        query = 'SELECT classname FROM class'
        cls.cursor.execute(query)
        classes = cls.cursor.fetchall()
        cls.close()
        return list(classes)

    @classmethod
    def get_subjects(cls):
        cls.connect()
        query = 'SELECT name FROM subject'
        cls.cursor.execute(query)
        subjects = cls.cursor.fetchall()
        cls.close()
        return list(subjects)

    @classmethod
    def get_grades(cls):
        cls.connect()
        query = 'SELECT value FROM grade'
        cls.cursor.execute(query)
        grades = cls.cursor.fetchall()
        cls.close()
        return grades

    @classmethod
    def get_teacher(cls, email):
        cls.connect()
        query = 'SELECT id, fname, lname, email FROM teacher WHERE email = ?'
        cls.cursor.execute(query, (email,))
        teacher = cls.cursor.fetchone()
        return teacher

    @classmethod
    def get_student(cls, email):
        cls.connect()
        query = 'SELECT id, fname, lname, email, class FROM student WHERE email = ?'
        cls.cursor.execute(query, (email,))
        student = cls.cursor.fetchone()
        return student

    @classmethod
    def get_students(cls, schoolclass):
        cls.connect()
        query = 'SELECT fname, lname, email, class FROM student WHERE class = ?'
        cls.cursor.execute(query, (schoolclass,))
        students = cls.cursor.fetchall()
        cls.close()
        return students

    @classmethod
    def delete_student(cls, email):
        cls.connect()
        # Retrieve the student's ID based on their email
        query = 'SELECT id FROM student WHERE email = ?'
        cls.cursor.execute(query, (email,))
        student_id = cls.cursor.fetchone()

        if student_id:
            student_id = student_id[0]
            # Delete certificates associated with the student if exists
            cls.cursor.execute('DELETE FROM certificate WHERE student = ?', (student_id,))
            # Delete the student record
            cls.cursor.execute('DELETE FROM student WHERE id = ?', (student_id,))
            cls.conn.commit()
        cls.close()
