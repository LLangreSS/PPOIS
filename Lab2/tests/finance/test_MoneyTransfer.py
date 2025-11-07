import pytest
from finance.MoneyTransfer import MoneyTransfer
from finance.BankAccount import BankAccount

def test_money_transfer_execute():
    acc1 = BankAccount("1", 1000.0)
    acc2 = BankAccount("2", 0.0)
    transfer = MoneyTransfer(acc1, acc2, 100.0)
    transfer.execute()
    assert acc1.balance == 1000.0 - 100.0 - 1.0  # 1% fee
    assert acc2.balance == 100.0