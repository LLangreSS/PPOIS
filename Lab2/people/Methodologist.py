from __future__ import annotations
from people.Person import Person

class Methodologist(Person):
    def __init__(self, person_id: int, name: str, email: str):
        super().__init__(person_id, name, email)

    def update_curriculum(self, curriculum: "Curriculum", new_content: str) -> None:
        curriculum.content = new_content

    def review_course(self, course) -> str:
        return f"Reviewed {course.name} content"

    def approve_exam(self, exam) -> bool:
        return True
