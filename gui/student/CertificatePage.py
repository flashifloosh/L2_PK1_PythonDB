import FreeSimpleGUI as sg

from gui.WindowManager import WindowManager


class CertificatePage:

    @classmethod
    def get_layout(cls):
        return [
            [
                sg.Button("Zurück", key='back', image_subsample=30,
                          border_width=0, size=(8, 1)),
                sg.Text(size=(30, 1), font=('Helvetica', 15), text_color='black')
            ],
            [
                # TODO Table with grades and subjects
            ],
            [
                sg.Button('Drucken', key='print', size=(10, 1)),
                sg.Button('Exportieren', key='export', size=(10, 1))
            ]
        ]

    @staticmethod
    def event_handler(event, values):
        if event == 'back':
            from gui.student.StudentStartpage import StudentStartpage
            WindowManager.update(StudentStartpage().get_layout(), StudentStartpage.event_handler)
        elif event == 'print':
            print('print button clicked')
        elif event == 'export':
            print('export button clicked')
