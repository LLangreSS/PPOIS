from __future__ import annotations
from people.Teacher import Teacher
from academia.Department import Department

class HeadOfDepartment(Teacher):
    def __init__(self, person_id: int, name: str, email: str, department: Department):
        super().__init__(person_id, name, email, department)
        self.department.head = self

    def conduct_staff_meeting(self) -> list[str]:
        return [t.name for t in self.department.teachers]
