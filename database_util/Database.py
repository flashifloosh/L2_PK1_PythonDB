import os.path
import sqlite3 as db
import sys


class Database:
    cursor = None
    conn = None

    # Erstellung der Datenbank (wird immer ausgeführt)
    def __init__(self):
        self.create_db()

    # Erstellt die Datenbank insofern sie noch nicht existiert, oder nicht im richtigen Verzeichnis ist.
    # Insofern der Pfad nicht existiert wird dieser ebenfalls angelegt.
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

    # connect methode um den Code übersichtlicher zu machen
    @classmethod
    def connect(cls):
        cls.conn = db.connect('./data.db')
        cls.cursor = cls.conn.cursor()

    # close methode um den Code übersichtlicher zu machen
    @classmethod
    def close(cls):
        cls.conn.close()

    # SQL Abfrage als Methode um die Klassennamen als Liste auszugeben
    @classmethod
    def get_schoolclasses(cls):
        cls.connect()
        query = 'SELECT classname FROM class'
        cls.cursor.execute(query)
        classes = cls.cursor.fetchall()
        cls.close()
        return list(classes)

    # SQL Abfrage als Methode um die Fächer als Liste auszugeben
    @classmethod
    def get_subjects(cls):
        cls.connect()
        query = 'SELECT id, name FROM subject'
        cls.cursor.execute(query)
        subjects = cls.cursor.fetchall()
        cls.close()
        return list(subjects)

    # SQL Abfrage als Methode um den gesamten Notendatensatz auszugeben
    @classmethod
    def get_grades(cls):
        cls.connect()
        query = 'SELECT value, description FROM grade'
        cls.cursor.execute(query)
        grades = cls.cursor.fetchall()
        cls.close()
        return grades

    # SQL Abfrage als Methode um den gesamten Lehrerdatensatz eines Lehrers auszugeben
    @classmethod
    def get_teacher(cls, email):
        cls.connect()
        query = 'SELECT id, fname, lname, email FROM teacher WHERE email = ?'
        cls.cursor.execute(query, (email,))
        teacher = cls.cursor.fetchone()
        return teacher

    # SQL Abfrage als Methode um den gesamten Schülerdatensatz eines Schülers auszugeben
    @classmethod
    def get_student(cls, email):
        cls.connect()
        query = 'SELECT id, fname, lname, email, class FROM student WHERE email = ?'
        cls.cursor.execute(query, (email,))
        student = cls.cursor.fetchone()
        return student

    # SQL Abfrage als Methode um den gesamten Schülerdatensatz aller Schüler auszugeben
    @classmethod
    def get_students(cls, schoolclass):
        cls.connect()
        query = 'SELECT fname, lname, email, class FROM student WHERE class = ?'
        cls.cursor.execute(query, (schoolclass,))
        students = cls.cursor.fetchall()
        cls.close()
        return students

    # SQL Abfrage als Methode um einen Schüler zu löschen
    # insofern die ID mit einer aus der Datenbank zustimmt wird der Schüler gelöscht, mit seinen Zertifikaten.
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
