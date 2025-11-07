import pytest
from people.Accountant import Accountant
from people.Person import Person

def test_accountant_init():
    a = Accountant(1, "Alice", "a@example.com")
    assert a.name == "Alice"

def test_calculate_salary():
    a = Accountant(1, "Alice", "a@example.com")
    emp = Person(2, "Bob", "b@example.com")
    salary = a.calculate_salary(emp, 50000)
    assert salary.employee == emp
    assert salary.amount == 50000