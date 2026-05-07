"""Book model — represents a single book in the library."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Book:
    """Represents a library book.

    Attributes:
        book_id: Unique identifier.
        title: Title of the book.
        author: Author's full name.
        is_issued: Whether the book is currently borrowed.
        issued_to_user_id: ID of the user who borrowed the book (or None).
    """

    book_id: int
    title: str
    author: str
    is_issued: bool = False
    issued_to_user_id: Optional[int] = field(default=None)

    def __repr__(self) -> str:
        status = f"issued to user #{self.issued_to_user_id}" if self.is_issued else "available"
        return f"Book(id={self.book_id}, title='{self.title}', author='{self.author}', {status})"
