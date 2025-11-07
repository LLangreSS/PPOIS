from __future__ import annotations

class AcademicRecord:
    def __init__(self, student: "Student"):
        self.student = student
        self.grades: list["Grade"] = []

    def add_grade(self, grade: "Grade") -> None:
        self.grades.append(grade)

    def get_gpa(self) -> float:
        return sum(g.value for g in self.grades) / len(self.grades) if self.grades else 0.0
