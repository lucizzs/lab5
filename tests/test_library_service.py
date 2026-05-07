"""Unit tests for LibraryService.

Covers all four business scenarios:
    - issue_book   (positive + negative)
    - return_book  (positive + negative)
    - find_book    (positive + negative)
    - register_user (positive + negative)
"""

import pytest

from src.dto.book_dto import BookDTO
from src.dto.user_dto import UserDTO
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.services.library_service import LibraryService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def service() -> LibraryService:
    """Return a fresh LibraryService backed by empty in-memory repositories."""
    return LibraryService(
        book_repository=BookRepository(),
        user_repository=UserRepository(),
    )


@pytest.fixture()
def seeded_service(service: LibraryService):
    """Return a service with one book and one user already persisted."""
    service.add_book(BookDTO(title="Kobzar", author="Taras Shevchenko"))
    service.register_user(UserDTO(name="Ivan Franko", email="ivan@example.com"))
    return service


# ---------------------------------------------------------------------------
# Scenario 1: issue_book
# ---------------------------------------------------------------------------


class TestIssueBook:
    def test_issue_book_success(self, seeded_service):
        """Valid user can borrow an available book."""
        book = seeded_service.issue_book(book_id=1, user_id=1)

        assert book.is_issued is True
        assert book.issued_to_user_id == 1

    def test_issue_book_updates_user_borrow_list(self, seeded_service):
        """Borrowing a book adds it to the user's borrowed list."""
        seeded_service.issue_book(book_id=1, user_id=1)
        user = seeded_service._users.find_by_id(1)

        assert 1 in user.borrowed_book_ids

    def test_issue_book_already_issued_raises(self, seeded_service):
        """Attempting to borrow an already-issued book raises ValueError."""
        seeded_service.issue_book(book_id=1, user_id=1)

        with pytest.raises(ValueError, match="already issued"):
            seeded_service.issue_book(book_id=1, user_id=1)

    def test_issue_book_nonexistent_book_raises(self, seeded_service):
        """Issuing a book that does not exist raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            seeded_service.issue_book(book_id=999, user_id=1)

    def test_issue_book_nonexistent_user_raises(self, seeded_service):
        """Issuing a book to a user that does not exist raises ValueError."""
        with pytest.raises(ValueError, match="does not exist"):
            seeded_service.issue_book(book_id=1, user_id=999)


# ---------------------------------------------------------------------------
# Scenario 2: return_book
# ---------------------------------------------------------------------------


class TestReturnBook:
    def test_return_book_success(self, seeded_service):
        """A properly issued book can be returned and becomes available again."""
        seeded_service.issue_book(book_id=1, user_id=1)
        book = seeded_service.return_book(book_id=1, user_id=1)

        assert book.is_issued is False
        assert book.issued_to_user_id is None

    def test_return_book_removes_from_user_list(self, seeded_service):
        """Returning a book removes it from the user's borrowed list."""
        seeded_service.issue_book(book_id=1, user_id=1)
        seeded_service.return_book(book_id=1, user_id=1)
        user = seeded_service._users.find_by_id(1)

        assert 1 not in user.borrowed_book_ids

    def test_return_book_not_issued_raises(self, seeded_service):
        """Returning a book that was never issued raises ValueError."""
        with pytest.raises(ValueError, match="was not issued"):
            seeded_service.return_book(book_id=1, user_id=1)

    def test_return_book_wrong_user_raises(self, seeded_service):
        """Returning a book as the wrong user raises ValueError."""
        seeded_service.register_user(UserDTO(name="Lesya Ukrainka", email="lesya@example.com"))
        seeded_service.issue_book(book_id=1, user_id=1)

        with pytest.raises(ValueError, match="was not issued to user"):
            seeded_service.return_book(book_id=1, user_id=2)


# ---------------------------------------------------------------------------
# Scenario 3: find_book
# ---------------------------------------------------------------------------


class TestFindBook:
    def test_find_book_by_title_success(self, seeded_service):
        """Searching by a known title substring returns the matching book."""
        results = seeded_service.find_book(title="kobzar")

        assert len(results) == 1
        assert results[0].title == "Kobzar"

    def test_find_book_by_author_success(self, seeded_service):
        """Searching by a known author substring returns the matching book."""
        results = seeded_service.find_book(author="Shevchenko")

        assert len(results) == 1
        assert results[0].author == "Taras Shevchenko"

    def test_find_book_no_match_returns_empty(self, seeded_service):
        """Searching for a non-existent title returns an empty list."""
        results = seeded_service.find_book(title="nonexistent title xyz")

        assert results == []

    def test_find_book_no_criteria_raises(self, seeded_service):
        """Calling find_book with no criteria raises ValueError."""
        with pytest.raises(ValueError, match="At least one"):
            seeded_service.find_book()


# ---------------------------------------------------------------------------
# Scenario 4: register_user
# ---------------------------------------------------------------------------


class TestRegisterUser:
    def test_register_user_success(self, service):
        """A new user is saved and assigned an ID."""
        user = service.register_user(UserDTO(name="Mykola Gogol", email="gogol@example.com"))

        assert user.user_id is not None
        assert user.name == "Mykola Gogol"
        assert user.email == "gogol@example.com"

    def test_register_user_duplicate_email_raises(self, service):
        """Registering with an already-used email raises ValueError."""
        service.register_user(UserDTO(name="User One", email="shared@example.com"))

        with pytest.raises(ValueError, match="already exists"):
            service.register_user(UserDTO(name="User Two", email="shared@example.com"))

    def test_register_user_empty_name_raises(self, service):
        """Registering with an empty name raises ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            service.register_user(UserDTO(name="   ", email="valid@example.com"))

    def test_register_user_empty_email_raises(self, service):
        """Registering with an empty email raises ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            service.register_user(UserDTO(name="Valid Name", email=""))
