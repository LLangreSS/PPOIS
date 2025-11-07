import pytest
from documents.TransferDocument import TransferDocument
from people.Student import Student
from academia.Group import Group

def test_transfer_document_init():
    g1 = Group("G1", 1)
    g2 = Group("G2", 1)
    s = Student(1, "Alex", "a@example.com", g1)
    doc = TransferDocument(s, g1, g2)
    assert doc.from_group == g1
    assert doc.to_group == g2
    assert doc.processed == False

def test_process():
    g1 = Group("G1", 1)
    g2 = Group("G2", 1)
    s = Student(1, "Alex", "a@example.com", g1)
    doc = TransferDocument(s, g1, g2)
    doc.approve()
    doc.process()
    assert s.group == g2
    assert doc.processed == True