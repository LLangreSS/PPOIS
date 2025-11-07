from __future__ import annotations
from people.Person import Person

class Accountant(Person):
    def __init__(self, person_id: int, name: str, email: str):
        super().__init__(person_id, name, email)

    def process_payment(self, payment) -> None:
        from finance.Payment import Payment
        assert isinstance(payment, Payment)
        payment.process()

    def calculate_salary(self, employee, base: float = 50000):
        from finance.Salary import Salary
        return Salary(employee, base)

    def issue_invoice(self, recipient, amount: float):
        from finance.Invoice import Invoice
        return Invoice(recipient, amount)

    def award_scholarship(self, student):
        from finance.Scholarship import Scholarship
        scholarship = Scholarship(student, 10000)
        if scholarship.evaluate_eligibility():
            student.balance += scholarship.amount
            return scholarship
        return None
