import subprocess
import sys

try:
    # https://freesimplegui.readthedocs.io/
    import FreeSimpleGUI
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'FreeSimpleGUI'])
    import FreeSimpleGUI

from Core import Core


# initialisiert das Programm insofern eine Datenbank vorhanden ist.
# Ansonsten wartet er darauf bis diese angelegt wurde und startet dann das Programm.
def main():
    try:
        Core()
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"An error occurred: {e}")


# Startet das Programm
if __name__ == "__main__":
    main()
