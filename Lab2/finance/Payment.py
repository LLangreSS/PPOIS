from __future__ import annotations
from exceptions.InsufficientFundsException import InsufficientFundsException

class Payment:
    def __init__(self, payer: "Student", amount: float, description: str = ""):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.payer = payer
        self.amount = amount
        self.description = description
        self.processed = False
        self.refunded = False

    def process(self) -> None:
        if self.processed:
            raise ValueError("Payment already processed.")
        if self.payer.balance < self.amount:
            raise InsufficientFundsException("Insufficient funds.")
        self.payer.balance -= self.amount
        self.processed = True

    def refund(self) -> None:
        if not self.processed:
            raise ValueError("Cannot refund unprocessed payment.")
        if self.refunded:
            raise ValueError("Already refunded.")
        self.payer.balance += self.amount
        self.refunded = True

    def get_receipt(self) -> str:
        return f"Receipt: {self.amount} RUB for {self.description}"

    def cancel(self) -> None:
        if not self.processed:
            self.amount = 0

    def is_refundable(self) -> bool:
        return self.processed and not self.refunded
