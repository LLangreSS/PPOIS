from __future__ import annotations

class Faculty:
    def __init__(self, name: str, dean=None):
        self.name = name
        self.dean = dean
        self.departments: list["Department"] = []

    def add_department(self, department: "Department") -> None:
        self.departments.append(department)
        department.faculty = self

    def get_total_students(self) -> int:
        total = 0
        for dept in self.departments:
            for teacher in dept.teachers:
                for course in getattr(teacher, 'courses', []):
                    total += len(getattr(course, 'students', []))
        return total
