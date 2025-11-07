import pytest
from documents.Document import Document
from people.Person import Person

def test_document_init():
    owner = Person(1, "Alex", "a@example.com")
    doc = Document("DOC-1", owner, "2025-01-01")
    assert doc.doc_id == "DOC-1"
    assert doc.owner == owner
    assert doc.issue_date == "2025-01-01"
    assert doc.approved == False

def test_approve():
    owner = Person(1, "Alex", "a@example.com")
    doc = Document("DOC-1", owner, "2025-01-01")
    doc.approve()
    assert doc.approved == True