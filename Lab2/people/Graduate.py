from __future__ import annotations
from people.Student import Student

class Graduate(Student):
    def __init__(self, person_id: int, name: str, email: str, group, diploma, balance: float = 0.0):
        super().__init__(person_id, name, email, group, balance)
        self.diploma = diploma

    def request_diploma_copy(self):
        from documents.Diploma import Diploma
        return Diploma(self, self.diploma.degree)

    def verify_diploma(self) -> bool:
        return self.diploma.approved
