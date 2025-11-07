from __future__ import annotations
from exceptions.BookNotAvailableException import BookNotAvailableException

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: list["Book"] = []

    def add_book(self, book: "Book") -> None:
        self.books.append(book)
        book.library = self

    def find_book(self, title: str) -> "Book":
        for book in self.books:
            if book.title == title:
                return book
        raise BookNotAvailableException(f"Book '{title}' not found.")

    def reserve_book(self, student, title: str) -> bool:
        book = self.find_book(title)
        if book.checked_out:
            raise BookNotAvailableException("Book is already checked out.")
        book.checkout()
        return True

    def return_book(self, title: str) -> None:
        book = self.find_book(title)
        book.return_book()
