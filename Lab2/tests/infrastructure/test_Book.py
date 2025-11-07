import pytest
from infrastructure.Book import Book, BookNotAvailableException

def test_book_init():
    b = Book("Title", "Author", "123")
    assert b.title == "Title"
    assert b.author == "Author"
    assert b.isbn == "123"

def test_checkout():
    b = Book("Title", "Author", "123")
    b.checkout()
    assert b.checked_out == True
    with pytest.raises(BookNotAvailableException):
        b.checkout()