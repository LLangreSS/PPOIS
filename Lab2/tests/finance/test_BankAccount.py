import pytest
from finance.BankAccount import BankAccount, InsufficientFundsException

def test_bank_account_init():
    acc = BankAccount("12345", 1000.0)
    assert acc.account_number == "12345"
    assert acc.balance == 1000.0

def test_withdraw():
    acc = BankAccount("12345", 1000.0)
    acc.withdraw(200.0)
    assert acc.balance == 800.0

def test_withdraw_insufficient():
    acc = BankAccount("12345", 100.0)
    with pytest.raises(InsufficientFundsException):
        acc.withdraw(200.0)