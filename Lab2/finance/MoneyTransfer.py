from __future__ import annotations

class MoneyTransfer:
    FEE_PERCENT = 0.01

    def __init__(self, from_account: "BankAccount", to_account: "BankAccount", amount: float):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.fee = amount * self.FEE_PERCENT

    def execute(self) -> None:
        total = self.amount + self.fee
        self.from_account.withdraw(total)
        self.to_account.deposit(self.amount)

    def get_total_cost(self) -> float:
        return self.amount + self.fee
