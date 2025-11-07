from __future__ import annotations
from people.Student import Student
from exceptions.VisaExpiredException import VisaExpiredException

class ForeignStudent(Student):
    def __init__(self, person_id: int, name: str, email: str, group, visa, balance: float = 0.0):
        super().__init__(person_id, name, email, group, balance)
        self.visa = visa

    def renew_visa(self) -> None:
        if self.visa.is_expired():
            raise VisaExpiredException("Visa is expired and must be renewed.")
