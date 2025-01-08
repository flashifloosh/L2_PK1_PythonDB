import os.path
import sqlite3 as db


class Database:
    def __init__(self):
        import sqlite3 as db
        import os
        self.cursor = None
        self.conn = None
        self.create_db()

    def create_db(self):
        if not os.path.exists('data.db'):
            with open('script.sql', 'r') as f:
                self.cursor.executescript(f.read())
                self.conn.commit()
                self.conn.close()

    def connect(self):
        self.conn = db.connect('data.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

