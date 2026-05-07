"""Data Transfer Objects for books."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BookDTO:
    """DTO used when creating or returning book data to the controller layer."""

    title: str
    author: str
    book_id: Optional[int] = None
    is_issued: bool = False
    issued_to_user_id: Optional[int] = None
