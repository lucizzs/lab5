"""Book repository — in-memory storage and retrieval of Book entities."""

from typing import Dict, List, Optional

from src.models.book import Book


class BookRepository:
    """Handles persistence operations for Book entities.

    Simulates a database with an in-memory dictionary.
    """

    def __init__(self) -> None:
        self._store: Dict[int, Book] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def save(self, book: Book) -> Book:
        """Persist a book.  Assigns an ID if one is not set."""
        if book.book_id is None:
            book.book_id = self._next_id
            self._next_id += 1
        self._store[book.book_id] = book
        return book

    def delete(self, book_id: int) -> bool:
        """Remove a book by its ID.  Returns True if deletion succeeded."""
        if book_id in self._store:
            del self._store[book_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Return a book by its ID, or None if not found."""
        return self._store.get(book_id)

    def find_by_title(self, title: str) -> List[Book]:
        """Return books whose title contains the given string (case-insensitive)."""
        query = title.lower()
        return [b for b in self._store.values() if query in b.title.lower()]

    def find_by_author(self, author: str) -> List[Book]:
        """Return books whose author matches the given string (case-insensitive)."""
        query = author.lower()
        return [b for b in self._store.values() if query in b.author.lower()]

    def find_all(self) -> List[Book]:
        """Return all books in the repository."""
        return list(self._store.values())
