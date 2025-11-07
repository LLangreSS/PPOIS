from __future__ import annotations
from people.Person import Person
from academia.Faculty import Faculty

class Dean(Person):
    def __init__(self, person_id: int, name: str, email: str, faculty: Faculty):
        super().__init__(person_id, name, email)
        self.faculty = faculty
        faculty.dean = self

    def approve_study_plan(self, study_plan) -> None:
        study_plan.approved = True

    def review_department(self, department) -> str:
        return f"Reviewed {department.name}"

    def sign_diploma(self, graduate) -> None:
        graduate.diploma.approved = True
