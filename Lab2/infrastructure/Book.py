from __future__ import annotations
from exceptions.BookNotAvailableException import BookNotAvailableException

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.library = None
        self.checked_out = False

    def checkout(self) -> None:
        if self.checked_out:
            raise BookNotAvailableException("Book is already checked out.")
        self.checked_out = True

    def return_book(self) -> None:
        self.checked_out = False

    def is_available(self) -> bool:
        return not self.checked_out
