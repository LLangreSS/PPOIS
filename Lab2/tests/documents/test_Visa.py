import pytest
from documents.Visa import Visa
from people.Person import Person

def test_visa_init():
    p = Person(1, "Ali", "ali@example.com")
    v = Visa(p, "2026-01-01")
    assert v.expiry_date == "2026-01-01"

def test_is_expired():
    p = Person(1, "Ali", "ali@example.com")
    v = Visa(p, "2020-01-01")
    assert v.is_expired() == True