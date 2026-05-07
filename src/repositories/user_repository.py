"""User repository — in-memory storage and retrieval of User entities."""

from typing import Dict, List, Optional

from src.models.user import User


class UserRepository:
    """Handles persistence operations for User entities.

    Simulates a database with an in-memory dictionary.
    """

    def __init__(self) -> None:
        self._store: Dict[int, User] = {}
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def save(self, user: User) -> User:
        """Persist a user.  Assigns an ID if one is not set."""
        if user.user_id is None:
            user.user_id = self._next_id
            self._next_id += 1
        self._store[user.user_id] = user
        return user

    def delete(self, user_id: int) -> bool:
        """Remove a user by their ID.  Returns True if deletion succeeded."""
        if user_id in self._store:
            del self._store[user_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Return a user by their ID, or None if not found."""
        return self._store.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """Return a user with the given email address, or None."""
        for user in self._store.values():
            if user.email.lower() == email.lower():
                return user
        return None

    def find_all(self) -> List[User]:
        """Return all users in the repository."""
        return list(self._store.values())
