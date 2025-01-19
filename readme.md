# Schule

## Aufgabenstellung 

Die Aufgabe ist alleine oder in einer Gruppe ein Projekt zu erstellen oder eine Vorlage zu verwenden. Inhalt des Projektes ist es, ein Datenbankmodell zu erstellen sowohl in der ERD Schreibweise als auch als Relationship Modell, das mindestens 3 Entitätstypen hat in der 3. Normalform zu generieren. Dieses Modell soll umgesetzt werden und mit ein paar Datensätzen befült werden. 
Dazu soll ein Programm in Python geschrieben werden, dass auf die Datenbanken zugreift, dadurch sollte es möglich sein Daten hinzuzufügen, daten zu löschen und zu suchen. Es sollte auch möglich sein Daten zu importieren als auch zu exportieren mit verschiedenen Dateientypen (JSON oder CSV).

## Kurzbeschreibung Unternehmen

Wir haben uns überlegt ein kleines Schulverwaltungstool aufzubauen. Ziel sollte es sein für Lehrer die Noten der Schüler über eine Grafische Oberfläche zu verändern, dazu müssen sich Lehrer einmalig registrieren. Um das Projekt nicht zu komplex zu gestalten kann nur ein Lehrer (der Klassenlehrer) pro Klasse die Noten eintragen. Schüler sind nur in der Lage ihre eigenen Noten auszulesen nicht aber zu verändern und diese Herunterzuladen. Sowohl Lehrer als auch Schüler müssen sich anmelden und können daraufhin Änderungen vornehmen oder nur auslesen. 

## Datenbankmodell

Wir haben uns für eine SQL Datenbank entschieden, die mithilfe von Code generiert und befüllt wird. Bei unserem System sind dafür 6 Entitätstypen erforderlich. Zu einen haben wir die Klasse die nur in Relation zum Schüler liegt dabei können mehrere Schüler nur in einer Klasse sein. In der Klasse selber gibt es nur einen Namen der gleichzeitig als ID dient, da der Name einzigartig ist. Die Schülerentität besteht aus einer ID einem Vor- und Nachnamen, einem Passwort dem secret und der Mailadresse des Schülers. Die Klasse wird als Fremdschlüssel dem Schüler hinzugefügt. In der Mitte steht das Zeugnis als Entität, dieses verbindet vier andere Entitäten darunter der Schüler der Lehrer die Note und das Fach. Das Zeugnis spielt deshlab eine elementare Rolle und ist der Kern der Datenbank. Das Zeugnis beinhaltet die anderen Entitäten als Fremdschlüssel und hat somit einen Zusammengefügten Primärschlüssel. Logischerweise besitzt das zeugnis alle n Beziehungen, damit das Produkt einfacher gestaltet wird gibt es nur n - 1 Beziehungen, da ssonst der Rahmen gesprengt wird und die Komplexität zu immens wird. Bei den Fächern haben wir eine ID und einen Namen, der Name ist dabei die volle Bezeichnung des Faches und die ID die Abkürzung des Faches wie man es aus der Schule kennt. Hier haben wir vordefinierte Datensätze, die auf alle Schüler zutreffen, hierbei haben wir uns auf Fächer die normal für eine Grundschule sind bezogen. Darunter zählen Mathe, Englisch, Deutsch, Sport und Mensch und Kultur. Die Noten sind auch ein Fremdschlüssel des Zeugnisses und auch schon vordefiniert. Wir benutzen den normalen Notenschlüssel aus Deutschland, der in ganzen Zahlen definiert ist. Die Notenzahl ist dabei der Primärschlüssel. Neben dem Primärschlüssel gibt es nur noch eine Bezeichnung der Note. Der Letzte Fremdschlüssel der Zeugnis Entität ist der Lehrer. Bei der Lehrer Entität gibt es neben einer ID als Primärschlüssel den Vor und Nachnamen, eine Mail Adresse, ein Passwort und ein Verification Code, dieser wird einmalig gebraucht um zu verifizieren, dass es ein Lehrer ist und dieser dann die entsprechenden Rechte bekommt die Noten der Schüler anzupasen. Unsere Datenbank ist die `schule.db`. Bei unserer Schule gilt, dass jede Klasse die gleichen Fächer hat. 

---

## Features

Im folgenden Text bekommt ihr einen Überblick, über die Funktionen unseres Produkts. Im Kern haben wir mehrere einzelne Fenster die einzeln eine Funktion besitzen. Darunter fallen der CSV Export und Import, unser Ziel hierbei ist es, dass Schüler ihre Noten als CSV Datei herunterladen können. Lehrer hingegen sollen die Möglichkeit haben eine Notenliste eines Schülers hochzuladen, hierbei ist immer der Klassenlehrer gemeint. Unsere Datenbank ist auf der Basis von SQLite, sie wird komplett über einen Code generiert und über die importfunktion oder das Registrieren eines Benutzers befüllt. Die Registrierung spielt eine große Rolle, da sie benötigt wird, dass sich Schüler oder Lehrer überhaupt erst anmelden können. Dabei gibt es für jede Rolle ein eigenes Fenster. Die Registrierung wird benötigt um Passwörter für die einzelnen Benutzer zu setzen, dabei muss wie üblich das Passwort zwei mal angegeben werden. Insofern die Registrierung abgeschlossen ist kann sich der Benutzer anmelden und hat seine zugeschriebenen Funktionen. Das besondere ist, dass die Passwörter verschlüsselt sind, sodass man die Passwörter nicht aus der Datenbank auslesen kann. Dies ist nur möglich, da die Passwörter bei der Anmeldung auch gehasht werden und die beiden gehashten Werte dann verglichen werden, wenn diese gleich sind ist das Passwort richtig und der Benutzer kann sich anmelden. Wie man sieht sind sehr viele verschiedene Fenster im Einsatz. Damit das erstellen einfacher ist haben wir eine separate Klasse namens Windowmaker. Die Kernfunktion ist es ein Standartfenster zu generieren, mit Werten die Global angewendet werden. Dies Vereinfacht die Nutzung von mehreren Verschiedenen Fenstern erheblich, da man nur eine Funktion aufrufen muss. Möglich ist das durch ein eventmaker, der dann über Klassen hinaus verwendbar ist. Die einzelnen Buttons werden dann in der separaten Klasse des Fensters generiert und überschreiben den Ursrünglichen eventmaker. 

- CSV import and export
- SQLite database
- GUI
- Windowmaker
- Anmeldung mit passwortverschlüsselung
- Registrierung


## Datenbank
`schule.db`


> see [script.sql](https://github.com/flashifloosh/L2_PK1_PythonDB/blob/main/script.sql) for more information