"""Data Transfer Objects for users."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    """DTO used when creating or returning user data to the controller layer."""

    name: str
    email: str
    user_id: Optional[int] = None
