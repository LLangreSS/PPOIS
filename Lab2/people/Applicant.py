from __future__ import annotations
from people.Person import Person

class Applicant(Person):
    def __init__(self, person_id: int, name: str, email: str, application: "Application"):
        super().__init__(person_id, name, email)
        self.application = application

    def submit_application(self) -> None:
        self.application.submitted = True

    def withdraw(self) -> None:
        self.application.submitted = False

    def is_complete(self) -> bool:
        return bool(getattr(self.application, 'program', None))
