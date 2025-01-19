CREATE TABLE IF NOT EXISTS class (
classname VARCHAR(3) PRIMARY KEY 
);

INSERT OR IGNORE INTO class (classname) VALUES ('1A');
INSERT OR IGNORE INTO class (classname) VALUES ('1B');
INSERT OR IGNORE INTO class (classname) VALUES ('1C');

INSERT OR IGNORE INTO class (classname) VALUES ('2A');
INSERT OR IGNORE INTO class (classname) VALUES ('2B');
INSERT OR IGNORE INTO class (classname) VALUES ('2C');

INSERT OR IGNORE INTO class (classname) VALUES ('3A');
INSERT OR IGNORE INTO class (classname) VALUES ('3B');
INSERT OR IGNORE INTO class (classname) VALUES ('3C');

INSERT OR IGNORE INTO class (classname) VALUES ('4A');
INSERT OR IGNORE INTO class (classname) VALUES ('4B');
INSERT OR IGNORE INTO class (classname) VALUES ('4C');

CREATE TABLE IF NOT EXISTS student (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fname TEXT,
lname TEXT,
email TEXT,
secret TEXT,
class VARCHAR(3),
FOREIGN KEY (class) REFERENCES class(classname)
);

CREATE TABLE IF NOT EXISTS teacher (
id INTEGER PRIMARY KEY AUTOINCREMENT,
fname TEXT,
lname TEXT,
email TEXT,
secret TEXT,
verify VARCHAR(6)
);


CREATE TABLE IF NOT EXISTS subject (
id VARCHAR(5) PRIMARY KEY,
name TEXT
);

INSERT OR IGNORE INTO subject (id, name) VALUES ('M', 'Mathe');
INSERT OR IGNORE INTO subject (id, name) VALUES ('D', 'Deutsch');
INSERT OR IGNORE INTO subject (id, name) VALUES ('E', 'Englisch');
INSERT OR IGNORE INTO subject (id, name) VALUES ('MENUK', 'Mensch, Natur und Kultur');
INSERT OR IGNORE INTO subject (id, name) VALUES ('S', 'Sport');


CREATE TABLE IF NOT EXISTS grade (
value INTEGER PRIMARY KEY,
description TEXT
);

INSERT OR IGNORE INTO grade (value, description) VALUES (1, 'Sehr gut');
INSERT OR IGNORE INTO grade (value, description) VALUES (2, 'Gut');
INSERT OR IGNORE INTO grade (value, description) VALUES (3, 'Befriedigend');
INSERT OR IGNORE INTO grade (value, description) VALUES (4, 'Ausreichend');
INSERT OR IGNORE INTO grade (value, description) VALUES (5, 'Mangelhaft');
INSERT OR IGNORE INTO grade (value, description) VALUES (6, 'Ungenügend');

CREATE TABLE IF NOT EXISTS certificate (
grade INTEGER,
subject VARCHAR(5),
student INTEGER,
teacher INTEGER,
FOREIGN KEY (grade) REFERENCES grade(value),
FOREIGN KEY (subject) REFERENCES subject(id),
FOREIGN KEY (student) REFERENCES student(id),
FOREIGN KEY (teacher) REFERENCES teacher(id)
);