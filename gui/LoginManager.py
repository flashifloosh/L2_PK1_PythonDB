
class LoginManager:
    teacher = None
    student = None
    class_selection = None

    @classmethod
    def set_student(cls, student):
        cls.student = student

    @classmethod
    def get_student(cls):
        return cls.student

    @classmethod
    def set_teacher(cls, teacher):
        cls.teacher = teacher

    @classmethod
    def get_teacher(cls):
        return cls.teacher

    @classmethod
    def get_class(cls):
        return cls.class_selection

    @classmethod
    def set_class(cls, schoolclass):
        cls.class_selection = schoolclass