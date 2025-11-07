import pytest
from finance.Invoice import Invoice
from people.Person import Person

def test_invoice_init():
    p = Person(1, "Client", "c@example.com")
    inv = Invoice(p, 1000.0)
    assert inv.recipient == p
    assert inv.amount == 1000.0
    assert inv.paid == False

def test_mark_paid():
    p = Person(1, "Client", "c@example.com")
    inv = Invoice(p, 1000.0)
    inv.mark_paid()
    assert inv.paid == True