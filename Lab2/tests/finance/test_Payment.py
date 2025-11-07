import pytest
from finance.Payment import Payment, InsufficientFundsException
from people.Student import Student
from academia.Group import Group

def test_payment_process():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g, 1000.0)
    p = Payment(s, 200.0, "Tuition")
    p.process()
    assert p.processed == True
    assert s.balance == 800.0

def test_payment_insufficient():
    g = Group("G1", 1)
    s = Student(1, "Alex", "a@example.com", g, 100.0)
    p = Payment(s, 200.0, "Tuition")
    with pytest.raises(InsufficientFundsException):
        p.process()