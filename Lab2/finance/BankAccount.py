from __future__ import annotations
from exceptions.InsufficientFundsException import InsufficientFundsException

class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0):
        self.account_number = account_number
        self.balance = balance

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise InsufficientFundsException("Not enough funds to withdraw.")
        self.balance -= amount

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def get_balance(self) -> float:
        return self.balance
