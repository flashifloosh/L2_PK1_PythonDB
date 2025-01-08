# Schule

## Aufgabenstellung 

Die Aufgabe ist alleine oder in einer Gruppe ein Projekt zu erstellen oder eine Vorlage zu verwenden. Inhalt des Projektes ist es, ein Datenbankmodell zu erstellen sowohl in der ERD Schreibweise als auch als Relationship Modell, das mindestens 3 Entitätstypen hat in der 3. Normalform zu generieren. Dieses Modell soll umgesetzt werden und mit ein paar Datensätzen befült werden. 
Dazu soll ein Programm in Python geschrieben werden, dass auf die Datenbanken zugreift, dadurch sollte es möglich sein Daten hinzuzufügen, daten zu löschen und zu suchen. Es sollte auch möglich sein Daten zu importieren als auch zu exportieren mit verschiedenen Dateientypen (JSON oder CSV).

## Kurzbeschreibung Unternehmen

Wir haben uns überlegt ein kleines Schulverwaltungstool aufzubauen. Ziel sollte es sein für Lehrer die Noten der Schüler über eine Grafische Oberfläche zu verändern, dazu müssen sich Lehrer einmalig registrieren. Um das Projekt nicht zu komplex zu gestalten kann nur ein Lehrer (der Klassenlehrer) pro Klasse die Noten eintragen. Schüler sind nur in der Lage ihre eigenen Noten auszulesen nicht aber zu verändern und diese Herunterzuladen. Sowohl Lehrer als auch Schüler müssen sich anmelden und können daraufhin Änderungen vornehmen oder nur auslesen. 

## Datenbankmodell

Wir haben uns für eine SQL Datenbank entschieden, die mithilfe von Code generiert und befüllt wird. Bei unserem System sind dafür 6 Entitätstypen erforderlich. Zu einen haben wir die Klasse die nur in Relation zum Schüler liegt dabei können mehrere Schüler nur in einer Klasse sein. In der Klasse selber gibt es nur einen Namen und eine ID. Die Schülerentität besteht aus 

## Features
- CSV import and export
- SQLite database
- GUI
- 


## Datenbank
`schule.db`


> see [script.sql](https://github.com/flashifloosh/L2_PK1_PythonDB/blob/main/script.sql) for more information