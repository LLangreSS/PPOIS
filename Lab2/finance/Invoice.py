from __future__ import annotations

class Invoice:
    def __init__(self, recipient: "Person", amount: float):
        self.recipient = recipient
        self.amount = amount
        self.paid = False

    def is_overdue(self, days: int) -> bool:
        return days > 30 and not self.paid

    def mark_paid(self) -> None:
        self.paid = True
