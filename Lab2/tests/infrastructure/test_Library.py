import pytest
from infrastructure.Library import Library, BookNotAvailableException
from infrastructure.Book import Book

def test_library_init():
    lib = Library("Main Library")
    assert lib.name == "Main Library"

def test_add_and_find_book():
    lib = Library("Main")
    book = Book("Title", "Author", "123")
    lib.add_book(book)
    found = lib.find_book("Title")
    assert found == book

def test_reserve_book():
    lib = Library("Main")
    book = Book("Title", "Author", "123")
    lib.add_book(book)
    student = type('S', (), {})()
    lib.reserve_book(student, "Title")
    assert book.checked_out == True