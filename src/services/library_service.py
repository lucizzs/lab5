"""Library service — business logic for the library system.

Business scenarios implemented:
    1. issue_book    — lend a book to a registered user
    2. return_book   — accept a returned book from a user
    3. find_book     — search books by title or author keyword
    4. register_user — create a new library user account
"""

from typing import List, Optional

from src.dto.book_dto import BookDTO
from src.dto.user_dto import UserDTO
from src.models.book import Book
from src.models.user import User
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository


class LibraryService:
    """Provides core library operations.

    Depends on BookRepository and UserRepository for data access.
    All public methods raise ValueError with descriptive messages on rule violations.
    """

    def __init__(
        self,
        book_repository: BookRepository,
        user_repository: UserRepository,
    ) -> None:
        self._books = book_repository
        self._users = user_repository

    # ------------------------------------------------------------------
    # Scenario 1: Issue a book
    # ------------------------------------------------------------------

    def issue_book(self, book_id: int, user_id: int) -> Book:
        """Lend *book_id* to *user_id*.

        Business rules:
            - The book must exist.
            - The user must exist.
            - The book must not already be issued.

        Returns:
            The updated Book with ``is_issued=True``.

        Raises:
            ValueError: if any business rule is violated.
        """
        book = self._books.find_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with id={book_id} does not exist.")

        user = self._users.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with id={user_id} does not exist.")

        if book.is_issued:
            raise ValueError(
                f"Book '{book.title}' is already issued to user #{book.issued_to_user_id}."
            )

        book.is_issued = True
        book.issued_to_user_id = user_id
        user.borrowed_book_ids.append(book_id)

        self._books.save(book)
        self._users.save(user)
        return book

    # ------------------------------------------------------------------
    # Scenario 2: Return a book
    # ------------------------------------------------------------------

    def return_book(self, book_id: int, user_id: int) -> Book:
        """Accept the return of *book_id* from *user_id*.

        Business rules:
            - The book must exist.
            - The user must exist.
            - The book must currently be issued to *user_id*.

        Returns:
            The updated Book with ``is_issued=False``.

        Raises:
            ValueError: if any business rule is violated.
        """
        book = self._books.find_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with id={book_id} does not exist.")

        user = self._users.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with id={user_id} does not exist.")

        if not book.is_issued:
            raise ValueError(f"Book '{book.title}' was not issued and cannot be returned.")

        if book.issued_to_user_id != user_id:
            raise ValueError(
                f"Book '{book.title}' was not issued to user #{user_id}."
            )

        book.is_issued = False
        book.issued_to_user_id = None
        if book_id in user.borrowed_book_ids:
            user.borrowed_book_ids.remove(book_id)

        self._books.save(book)
        self._users.save(user)
        return book

    # ------------------------------------------------------------------
    # Scenario 3: Search for a book
    # ------------------------------------------------------------------

    def find_book(
        self,
        *,
        title: Optional[str] = None,
        author: Optional[str] = None,
    ) -> List[Book]:
        """Search books by *title* substring and/or *author* substring.

        At least one of *title* or *author* must be provided.

        Returns:
            A list of matching Book objects (may be empty).

        Raises:
            ValueError: if neither *title* nor *author* is given.
        """
        if title is None and author is None:
            raise ValueError("At least one of 'title' or 'author' must be provided.")

        if title is not None and author is not None:
            by_title = set(b.book_id for b in self._books.find_by_title(title))
            return [b for b in self._books.find_by_author(author) if b.book_id in by_title]

        if title is not None:
            return self._books.find_by_title(title)

        return self._books.find_by_author(author)  # type: ignore[arg-type]

    # ------------------------------------------------------------------
    # Scenario 4: Register a new user
    # ------------------------------------------------------------------

    def register_user(self, dto: UserDTO) -> User:
        """Create a new library user from *dto*.

        Business rules:
            - Email must be unique — no two users share the same address.
            - Name and email must not be empty.

        Returns:
            The newly created User entity.

        Raises:
            ValueError: if any business rule is violated.
        """
        if not dto.name or not dto.name.strip():
            raise ValueError("User name must not be empty.")

        if not dto.email or not dto.email.strip():
            raise ValueError("User email must not be empty.")

        if self._users.find_by_email(dto.email) is not None:
            raise ValueError(f"A user with email '{dto.email}' already exists.")

        new_user = User(user_id=0, name=dto.name.strip(), email=dto.email.strip())
        new_user.user_id = None  # let repository assign
        return self._users.save(new_user)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def add_book(self, dto: BookDTO) -> Book:
        """Add a new book to the catalogue (helper for seeding data)."""
        book = Book(book_id=0, title=dto.title, author=dto.author)
        book.book_id = None  # type: ignore[assignment]
        return self._books.save(book)
