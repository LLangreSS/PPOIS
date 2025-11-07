from __future__ import annotations
from exceptions.CourseFullException import CourseFullException
from exceptions.DuplicateEnrollmentException import DuplicateEnrollmentException

class Course:
    MAX_STUDENTS = 30

    def __init__(self, name: str, credits: int):
        self.name = name
        self.credits = credits
        self.teacher = None
        self.students: list["Student"] = []

    def is_full(self) -> bool:
        return len(self.students) >= self.MAX_STUDENTS

    def enroll_student(self, student: "Student") -> None:
        if student in self.students:
            raise DuplicateEnrollmentException(f"{student.name} already enrolled.")
        if self.is_full():
            raise CourseFullException(f"Course {self.name} is full.")
        self.students.append(student)

    def drop_student(self, student: "Student") -> None:
        if student in self.students:
            self.students.remove(student)

    def get_average_grade(self) -> float:
        grades = []
        for s in self.students:
            for g in getattr(s, 'academic_record', getattr(s, 'grades', [])):
                if hasattr(g, 'course') and g.course is self:
                    grades.append(g.value)
                elif hasattr(g, 'value'):
                    grades.append(g.value)
        return sum(grades) / len(grades) if grades else 0.0
