CREATE TABLE noten (
    sUID INTEGER,
    kuerzelFach TEXT,
    note REAL,
    PRIMARY KEY (sUID, KürzelFach)
);

CREATE TABLE schueler (
    sUID INTEGER PRIMARY KEY,
    benutzername TEXT,
    vorname TEXT,
    nachname TEXT,
    geburtsdatum TEXT,
    geschlecht TEXT
);

CREATE TABLE lehrer (
    kuerzel_lehrer TEXT PRIMARY KEY,
    vorname TEXT,
    nachname TEXT,
    geburtsdatum TEXT,
    geschlecht TEXT
);


CREATE TABLE lehrer_faecher (
    kuerzelLehrer TEXT,
    kuerzelFach TEXT,
    PRIMARY KEY (KürzelLehrer, KürzelFach)
);

Create TABLE faecher (
    kuerzel_fach TEXT PRIMARY KEY,
    fach TEXT
);