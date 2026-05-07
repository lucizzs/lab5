"""Library controller — CLI entry point for the library system.

Delegates all work to LibraryService; contains NO business logic.
"""

from src.dto.user_dto import UserDTO
from src.services.library_service import LibraryService


class LibraryController:
    """Provides a simple command-line interface to the library system."""

    def __init__(self, service: LibraryService) -> None:
        self._service = service

    def handle_issue_book(self, book_id: int, user_id: int) -> None:
        """Handle the 'issue book' command."""
        try:
            book = self._service.issue_book(book_id, user_id)
            print(f"[OK] Book '{book.title}' issued to user #{user_id}.")
        except ValueError as exc:
            print(f"[ERROR] {exc}")

    def handle_return_book(self, book_id: int, user_id: int) -> None:
        """Handle the 'return book' command."""
        try:
            book = self._service.return_book(book_id, user_id)
            print(f"[OK] Book '{book.title}' returned successfully.")
        except ValueError as exc:
            print(f"[ERROR] {exc}")

    def handle_find_book(self, title: str = None, author: str = None) -> None:
        """Handle the 'find book' command."""
        try:
            results = self._service.find_book(title=title, author=author)
            if results:
                for book in results:
                    status = "ISSUED" if book.is_issued else "AVAILABLE"
                    print(f"  [{status}] {book.title} — {book.author}")
            else:
                print("[INFO] No books found matching the criteria.")
        except ValueError as exc:
            print(f"[ERROR] {exc}")

    def handle_register_user(self, name: str, email: str) -> None:
        """Handle the 'register user' command."""
        try:
            user = self._service.register_user(UserDTO(name=name, email=email))
            print(f"[OK] User '{user.name}' registered with id={user.user_id}.")
        except ValueError as exc:
            print(f"[ERROR] {exc}")
