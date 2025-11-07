from __future__ import annotations
from people.Person import Person

class Secretary(Person):
    def __init__(self, person_id: int, name: str, email: str):
        super().__init__(person_id, name, email)

    def issue_transfer_document(self, student, from_group, to_group):
        from documents.TransferDocument import TransferDocument
        return TransferDocument(student, from_group, to_group)

    def register_credit_result(self, credit, student) -> None:
        credit.award_credit(student)

    def notify_exam_schedule(self, exam: "Exam") -> str:
        return f"Exam {exam.course.name} scheduled on {exam.date}."
