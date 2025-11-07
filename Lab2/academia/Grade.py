from __future__ import annotations
from exceptions.InvalidGradeException import InvalidGradeException

class Grade:
    def __init__(self, student: "Student", course: "Course", value: float):
        self.validate(value)
        self.student = student
        self.course = course
        self.value = value
        record = getattr(student, 'academic_record', None)
        if record:
            record.add_grade(self)

    @staticmethod
    def validate(value: float) -> None:
        if not (0 <= value <= 100):
            raise InvalidGradeException("Grade must be between 0 and 100.")
