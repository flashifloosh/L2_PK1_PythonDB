# Schulverwaltungstool

# Requirements

- Python 3.13
- ```pip install freesimplegui```

# Installation

### Releases
1. In [Releases](https://github.com/flashifloosh/L2_PK1_PythonDB/releases) die neuste Version herunterladen
2. ZIP entpacken
3. Schulverwaltungstool.exe ausführen


### Source Code

1. Code herunterladen (als ZIP oder mit git clone)
2. Command Line öffnen im Ordner
3. ```python Start.py```



---

# Dokumentation

## Aufgabenstellung

Die Aufgabe besteht darin, alleine oder in einer Gruppe ein Projekt zu erstellen oder eine Vorlage zu verwenden. Ziel
des Projektes ist es, ein Datenbankmodell zu erstellen, sowohl in der ERD-Schreibweise als auch als Relationship-Modell,
das mindestens drei Entitätstypen in der dritten Normalform umfasst. Dieses Modell soll umgesetzt und mit einigen
Datensätzen befüllt werden.

Zusätzlich soll ein Programm in Python geschrieben werden, das auf die Datenbank zugreift. Dadurch soll es möglich sein,
Daten hinzuzufügen, zu löschen und zu suchen. Es sollte auch möglich sein, Daten zu importieren und zu exportieren, und
zwar in verschiedenen Dateiformaten (JSON oder CSV).

## Kurzbeschreibung Unternehmen

Wir haben uns entschieden, ein kleines Schulverwaltungstool zu entwickeln. Ziel ist es, Lehrern die Möglichkeit zu
geben, die Noten der Schüler über eine grafische Oberfläche zu ändern. Dazu müssen sich Lehrer einmalig registrieren. Um
das Projekt nicht zu komplex zu gestalten, kann jeder Lehrer in jeder Klasse die Noten eintragen.

Schüler sind nur in der Lage, ihre eigenen Noten einzusehen, aber nicht zu verändern, und diese herunterzuladen. Sowohl
Lehrer als auch Schüler müssen sich anmelden, um Änderungen vorzunehmen oder Daten auszulesen.

## Datenbankmodell

Wir haben uns für eine SQL-Datenbank entschieden, die mithilfe von Code generiert und befüllt wird. Unser System
erfordert sechs Entitätstypen. Zum einen haben wir die Klasse, die nur in Relation zum Schüler steht. Mehrere Schüler
können nur in einer Klasse sein. In der Klasse gibt es nur einen Namen, der gleichzeitig als ID dient, da der Name
einzigartig ist. Die Schülerentität besteht aus einer ID, einem Vor- und Nachnamen, einem Passwort, dem Secret und der
E-Mail-Adresse des Schülers. Die Klasse wird als Fremdschlüssel dem Schüler hinzugefügt.

Im Zentrum steht das Zeugnis als Entität, das vier andere Entitäten verbindet: den Schüler, den Lehrer, die Note und das
Fach. Das Zeugnis spielt eine elementare Rolle und ist der Kern der Datenbank. Es beinhaltet die anderen Entitäten als
Fremdschlüssel und hat somit einen zusammengesetzten Primärschlüssel. Logischerweise besitzt das Zeugnis alle
n-Beziehungen. Um das Produkt einfacher zu gestalten, gibt es nur n-1-Beziehungen, da sonst der Rahmen gesprengt wird
und die Komplexität zu hoch wäre.

Bei den Fächern haben wir eine ID und einen Namen. Der Name ist die volle Bezeichnung des Faches und die ID die
Abkürzung des Faches, wie man es aus der Schule kennt. Hier haben wir vordefinierte Datensätze, die auf alle Schüler
zutreffen. Dazu zählen Mathematik, Englisch, Deutsch, Sport und Mensch und Kultur. Die Noten sind ebenfalls ein
Fremdschlüssel des Zeugnisses und auch schon vordefiniert. Wir benutzen den normalen Notenschlüssel aus Deutschland, der
in ganzen Zahlen definiert ist. Die Notenzahl ist dabei der Primärschlüssel. Neben dem Primärschlüssel gibt es nur noch
eine Bezeichnung der Note.

Der letzte Fremdschlüssel der Zeugnisentität ist der Lehrer. Bei der Lehrerentität gibt es neben einer ID als
Primärschlüssel den Vor- und Nachnamen, eine E-Mail-Adresse, ein Passwort und einen Verifizierungscode. Dieser wird
einmalig benötigt, um zu verifizieren, dass es sich um einen Lehrer handelt, der dann die entsprechenden Rechte erhält,
die Noten der Schüler anzupassen. Unsere Datenbank ist die `schule.db`. In unserer Schule gilt, dass jede Klasse die
gleichen Fächer hat.

---

## Features

Im folgenden Text erhalten Sie einen Überblick über die Funktionen unseres Produkts. Im Kern haben wir mehrere einzelne
Fenster, die jeweils eine Funktion besitzen. Dazu gehören der CSV-Export und -Import. Unser Ziel hierbei ist es, dass
Schüler ihre Noten als CSV-Datei herunterladen können. Lehrer hingegen sollen die Möglichkeit haben, eine Notenliste
eines Schülers hochzuladen (wobei immer der Klassenlehrer gemeint ist).

Unsere Datenbank basiert auf SQLite. Sie wird komplett über Code generiert und über die Importfunktion oder die
Registrierung eines Benutzers befüllt. Die Registrierung spielt eine große Rolle, da sie benötigt wird, damit sich
Schüler oder Lehrer überhaupt erst anmelden können. Dabei gibt es für jede Rolle ein eigenes Fenster. Die Registrierung
wird benötigt, um Passwörter für die einzelnen Benutzer zu setzen. Dabei muss, wie üblich, das Passwort zweimal
angegeben werden. Sobald die Registrierung abgeschlossen ist, kann sich der Benutzer anmelden und seine zugewiesenen
Funktionen nutzen.

Das Besondere ist, dass die Passwörter verschlüsselt sind, sodass man die Passwörter nicht aus der Datenbank auslesen
kann. Dies ist nur möglich, da die Passwörter bei der Anmeldung ebenfalls gehasht werden und die beiden gehashten Werte
dann verglichen werden. Wenn diese gleich sind, ist das Passwort richtig und der Benutzer kann sich anmelden.

Wie man sieht, sind sehr viele verschiedene Fenster im Einsatz. Um die Erstellung zu vereinfachen, haben wir eine
separate Klasse namens `WindowManager`. Die Kernfunktion ist es, ein Standardfenster zu generieren, mit Werten, die
global
angewendet werden. Dies vereinfacht die Nutzung von mehreren verschiedenen Fenstern erheblich, da man nur eine Funktion
aufrufen muss. Möglich ist das durch einen `event_manager`, der dann klassenübergreifend verwendet werden kann. Die
einzelnen Buttons werden dann in der separaten Klasse des Fensters generiert und überschreiben den ursprünglichen
`event_manager`.

- CSV-Import und -Export
- SQLite-Datenbank
- GUI
- `WindowManager`
- Anmeldung mit Passwortverschlüsselung
- Registrierung

## Datenbank

`data.db`

> siehe [script.sql](https://github.com/flashifloosh/L2_PK1_PythonDB/blob/main/database_util/script.sql) für weitere
> Informationen
