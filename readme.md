# Schule

## Aufgabenstellung 

Die Aufgabe ist alleine oder in einer Gruppe ein Projekt zu erstellen oder eine Vorlage zu verwenden. Inhalt des Projektes ist es, ein Datenbankmodell zu erstellen sowohl in der ERD Schreibweise als auch als Relationship Modell, das mindestens 3 Entitätstypen hat in der 3. Normalform zu generieren. Dieses Modell soll umgesetzt werden und mit ein paar Datensätzen befült werden. 
Dazu soll ein Programm in Python geschrieben werden, dass auf die Datenbanken zugreift, dadurch sollte es möglich sein Daten hinzuzufügen, daten zu löschen und zu suchen. Es sollte auch möglich sein Daten zu importieren als auch zu exportieren mit verschiedenen Dateientypen (JSON oder CSV).

## Kurzbeschreibung Unternehmen

Wir haben uns überlegt ein kleines Schulverwaltungstool aufzubauen. Ziel sollte es sein für Lehrer die Noten der Schüler über eine Grafische Oberfläche zu verändern, dazu müssen sich Lehrer einmalig registrieren. Um das Projekt nicht zu komplex zu gestalten kann nur ein Lehrer (der Klassenlehrer) pro Klasse die Noten eintragen. Schüler sind nur in der Lage ihre eigenen Noten auszulesen nicht aber zu verändern und diese Herunterzuladen. Sowohl Lehrer als auch Schüler müssen sich anmelden und können daraufhin Änderungen vornehmen oder nur auslesen. 

## Datenbankmodell

Wir haben uns für eine SQL Datenbank entschieden, die mithilfe von Code generiert und befüllt wird. Bei unserem System sind dafür 6 Entitätstypen erforderlich. Zu einen haben wir die Klasse die nur in Relation zum Schüler liegt dabei können mehrere Schüler nur in einer Klasse sein. In der Klasse selber gibt es nur einen Namen der gleichzeitig als ID dient, da der Name einzigartig ist. Die Schülerentität besteht aus einer ID einem Vor- und Nachnamen, einem Passwort dem secret und der Mailadresse des Schülers. Die Klasse wird als Fremdschlüssel dem Schüler hinzugefügt. In der Mitte steht das Zeugnis als Entität, dieses verbindet vier andere Entitäten darunter der Schüler der Lehrer die Note und das Fach. Das Zeugnis spielt deshlab eine elementare Rolle und ist der Kern der Datenbank. Das Zeugnis beinhaltet die anderen Entitäten als Fremdschlüssel und hat somit einen Zusammengefügten Primärschlüssel. Logischerweise besitzt das zeugnis alle n Beziehungen, damit das Produkt einfacher gestaltet wird gibt es nur n - 1 Beziehungen, da ssonst der Rahmen gesprengt wird und die Komplexität zu immens wird. Bei den Fächern haben wir eine ID und einen Namen, der Name ist dabei die volle Bezeichnung des Faches und die ID die Abkürzung des Faches wie man es aus der Schule kennt. Hier haben wir vordefinierte Datensätze, die auf alle Schüler zutreffen, hierbei haben wir uns auf Fächer die normal für eine Grundschule sind bezogen. Darunter zählen Mathe, Englisch, Deutsch, Sport und Mensch und Kultur. Die Noten sind auch ein Fremdschlüssel des Zeugnisses und auch schon vordefiniert. Wir benutzen den normalen Notenschlüssel aus Deutschland, der in ganzen Zahlen definiert ist. Die Notenzahl ist dabei der Primärschlüssel. Neben dem Primärschlüssel gibt es nur noch eine Bezeichnung der Note. Der Letzte Fremdschlüssel der Zeugnis Entität ist der Lehrer. Bei der Lehrer Entität gibt es neben einer ID als Primärschlüssel den Vor und Nachnamen, eine Mail Adresse, ein Passwort und ein Verification Code, dieser wird einmalig gebraucht um zu verifizieren, dass es ein Lehrer ist und dieser dann die entsprechenden Rechte bekommt die Noten der Schüler anzupasen. 

---

## Features
- CSV import and export
- SQLite database
- GUI
- 


## Datenbank
`schule.db`


> see [script.sql](https://github.com/flashifloosh/L2_PK1_PythonDB/blob/main/script.sql) for more information