import pytest
from people.Person import Person

def test_person_init():
    p = Person(1, "Alex", "a@example.com")
    assert p.person_id == 1
    assert p.name == "Alex"
    assert p.email == "a@example.com"

def test_change_email():
    p = Person(1, "Alex", "old@example.com")
    p.change_email("new@example.com")
    assert p.email == "new@example.com"

def test_get_full_info():
    p = Person(1, "Alex", "a@example.com")
    assert p.get_full_info() == "Alex <a@example.com>"