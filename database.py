import sqlite3 as db
import os

class database:
    def __init__(self):
        self.conn = db.connect('data.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        if os.path.exists('data.db'):
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS student(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fname TEXT,
                    lname TEXT,
                    class VARCHAR(2),
                )
