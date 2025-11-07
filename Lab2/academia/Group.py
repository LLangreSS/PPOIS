from __future__ import annotations

class Group:
    def __init__(self, group_id: str, course_year: int):
        self.group_id = group_id
        self.course_year = course_year
        self.students: list["Student"] = []

    def add_student(self, student: "Student") -> None:
        if student not in self.students:
            self.students.append(student)
            student.group = self

    def remove_student(self, student: "Student") -> None:
        if student in self.students:
            self.students.remove(student)

    def promote_to_next_year(self) -> None:
        self.course_year += 1
