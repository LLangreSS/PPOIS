import pytest
from finance.Salary import Salary
from people.Person import Person

def test_salary_init():
    p = Person(1, "Alice", "a@example.com")
    salary = Salary(p, 50000.0)
    assert salary.employee == p
    assert salary.amount == 50000.0
    assert salary.paid == False

def test_generate_payslip():
    p = Person(1, "Alice", "a@example.com")
    salary = Salary(p, 50000.0)
    slip = salary.generate_payslip()
    assert "Alice" in slip
    assert "50000.0" in slip