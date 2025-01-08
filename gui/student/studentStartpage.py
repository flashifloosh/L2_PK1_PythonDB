import FreeSimpleGUI as sg


class StudentStartpage:

    def __init__(self):
        self.window = sg.Window('Schüler Startseite')
        self.layout = [
            [
                sg.Button(key='back', image_filename='./images/back.png', image_subsample=30, border_width=0,
                          button_color=('white', self.window.BackgroundColor)),
                sg.Text('Schüler Startseite', size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                sg.Button('Registrieren', key='register', size=(10, 1)),
                sg.Button('Anmelden', key='login', size=(10, 1))
            ]
        ]
        self.window = sg.Window('Schüler Startseite', self.layout, size=(300, 100), element_justification='c',
                                finalize=True)
        while True:
            event, values = self.window.read()
            if event == 'back':
                self.window.close()
                from gui.startpage import Startpage
                Startpage()
                break
            if event == 'register':
                self.window.close()
                from gui.student.studentRegister import StudentRegister
                StudentRegister()
                break
            if event == 'login':
                self.window.close()
                from gui.student.studentLogin import StudentLogin
                StudentLogin()
                break
            if event == sg.WIN_CLOSED:
                break
