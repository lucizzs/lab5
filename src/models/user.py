"""User model — represents a registered library user."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    """Represents a library user.

    Attributes:
        user_id: Unique identifier.
        name: Full name of the user.
        email: Contact email address.
        borrowed_book_ids: List of IDs of currently borrowed books.
    """

    user_id: int
    name: str
    email: str
    borrowed_book_ids: List[int] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"User(id={self.user_id}, name='{self.name}', "
            f"email='{self.email}', borrowed={self.borrowed_book_ids})"
        )
