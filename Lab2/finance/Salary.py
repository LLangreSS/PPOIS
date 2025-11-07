from __future__ import annotations

class Salary:
    def __init__(self, employee: "Person", amount: float):
        self.employee = employee
        self.amount = amount
        self.paid = False

    def mark_as_paid(self) -> None:
        self.paid = True

    def generate_payslip(self) -> str:
        return f"Payslip for {self.employee.name}: {self.amount} RUB"
