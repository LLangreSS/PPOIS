from __future__ import annotations

class Department:
    def __init__(self, name: str, faculty=None):
        self.name = name
        self.faculty = faculty
        self.teachers: list["Teacher"] = []
        self.head = None

    def assign_teacher(self, teacher: "Teacher") -> None:
        if teacher not in self.teachers:
            self.teachers.append(teacher)
            teacher.department = self

    def get_head_name(self) -> str:
        return self.head.name if self.head else "None"
