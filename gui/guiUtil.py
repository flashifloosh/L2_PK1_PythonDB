import FreeSimpleGUI as sg

class guiUtil:

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
                self.student_startpage()
            if event == 'teacher':
                print('Exit button clicked')
            if event == sg.WIN_CLOSED:
                break

    def student_startpage(self):
        self.layout = [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0, button_color=('white', self.window.BackgroundColor)),
                sg.Text('Schüler Startseite', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1)), 
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]
        self.window = sg.Window('Schüler Startseite', self.layout, size=(300, 100), element_justification='c', finalize=True)
        while True:
            event, values = self.window.read()
            if event == 'back':
                self.window.close()
                self.__init__()
            if event == 'register':
                print('Register button clicked')
            if event == 'login':
                print('Login button clicked')
            if event == sg.WIN_CLOSED:
                break

        