import pytest
from documents.Contract import Contract
from people.Person import Person

def test_contract_init():
    p1 = Person(1, "A", "a@example.com")
    p2 = Person(2, "B", "b@example.com")
    contract = Contract(p1, p2, "Employment")
    assert contract.party_b == p2
    assert contract.terms == "Employment"

def test_renew():
    p1 = Person(1, "A", "a@example.com")
    p2 = Person(2, "B", "b@example.com")
    contract = Contract(p1, p2, "Old")
    contract.renew("New")
    assert contract.terms == "New"
    assert contract.approved == True