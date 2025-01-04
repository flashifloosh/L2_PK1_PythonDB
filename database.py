import sqlite3 as db
import os

class database:
    def __init__(self):
        self.conn = db.connect('data.db')
        self.cursor = self.conn.cursor()
        self.create_db()


    def create_db(self):
        with open('script.sql', 'r') as f:
            self.cursor.executescript(f.read())
            self.conn.commit()
            self.conn.close()

