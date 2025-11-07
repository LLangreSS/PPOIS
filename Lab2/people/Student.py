from __future__ import annotations
from people.Person import Person
from academia.Group import Group
from documents.Transcript import Transcript
from academia.AcademicRecord import AcademicRecord

class Student(Person):
    def __init__(self, person_id: int, name: str, email: str, group: Group, balance: float = 0.0):
        super().__init__(person_id, name, email)
        self.group = group
        self.balance = balance
        self.transcript = Transcript(self)
        self.academic_record = AcademicRecord(self)
        group.add_student(self)

    def enroll_in_course(self, course) -> None:
        course.enroll_student(self)

    def pay_tuition(self, amount: float):
        from finance.Payment import Payment
        payment = Payment(self, amount, "Tuition fee")
        payment.process()
        return payment

    def request_transcript(self) -> Transcript:
        return self.transcript

    def take_exam(self, exam) -> bool:
        try:
            exam.register_student(self)
            return True
        except Exception:
            return False

    def transfer_to_group(self, new_group: Group) -> None:
        self.group.remove_student(self)
        new_group.add_student(self)
        self.group = new_group
