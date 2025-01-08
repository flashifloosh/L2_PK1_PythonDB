import FreeSimpleGUI as sg

from gui.student.studentStartpage import StudentStartpage


class Startpage:

    def __init__(self):
        self.layout = [
            [
                sg.Text('Schulsystem', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Schüler', key='student', size=(10, 1)),
                sg.Button('Lehrer', key='teacher', size=(10, 1))
            ]
        ]
        self.window = sg.Window('Schulsystem', self.layout, size=(300, 100), element_justification='c', finalize=True)
        while True:
            event, values = self.window.read()
            if event == 'student':
                self.window.close()
                StudentStartpage()
                break
            if event == 'teacher':
                print('Exit button clicked')
                break
            if event == sg.WIN_CLOSED:
                break
