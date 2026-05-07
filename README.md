# Library System — Lab 5

Бібліотечна система реалізована мовою Python з використанням архітектурного шаблону
**Controller → Service → Repository**.

---

## Структура проєкту

```
lab5/
├── src/
│   ├── controllers/
│   │   └── library_controller.py   # Точка входу (CLI), без бізнес-логіки
│   ├── services/
│   │   └── library_service.py      # Вся бізнес-логіка
│   ├── repositories/
│   │   ├── book_repository.py      # CRUD для книг
│   │   └── user_repository.py      # CRUD для користувачів
│   ├── models/
│   │   ├── book.py                 # Модель книги
│   │   └── user.py                 # Модель користувача
│   └── dto/
│       ├── book_dto.py             # DTO книги
│       └── user_dto.py             # DTO користувача
└── tests/
    └── test_library_service.py     # 17 юніт-тестів
```

---

## Бізнес-сценарії

| № | Сценарій | Метод сервісу |
|---|----------|---------------|
| 1 | Видача книги читачу | `LibraryService.issue_book()` |
| 2 | Повернення книги | `LibraryService.return_book()` |
| 3 | Пошук книги за назвою/автором | `LibraryService.find_book()` |
| 4 | Реєстрація нового користувача | `LibraryService.register_user()` |

---

## Встановлення та запуск тестів

### 1. Встановіть залежності

```bash
pip3 install pytest
```

### 2. Запустіть тести

```bash
cd lab5
python3 -m pytest tests/ -v
```

### Очікуваний вивід

```
============================= test session starts ==============================
collected 17 items

tests/test_library_service.py::TestIssueBook::test_issue_book_success PASSED
tests/test_library_service.py::TestIssueBook::test_issue_book_updates_user_borrow_list PASSED
tests/test_library_service.py::TestIssueBook::test_issue_book_already_issued_raises PASSED
tests/test_library_service.py::TestIssueBook::test_issue_book_nonexistent_book_raises PASSED
tests/test_library_service.py::TestIssueBook::test_issue_book_nonexistent_user_raises PASSED
tests/test_library_service.py::TestReturnBook::test_return_book_success PASSED
tests/test_library_service.py::TestReturnBook::test_return_book_removes_from_user_list PASSED
tests/test_library_service.py::TestReturnBook::test_return_book_not_issued_raises PASSED
tests/test_library_service.py::TestReturnBook::test_return_book_wrong_user_raises PASSED
tests/test_library_service.py::TestFindBook::test_find_book_by_title_success PASSED
tests/test_library_service.py::TestFindBook::test_find_book_by_author_success PASSED
tests/test_library_service.py::TestFindBook::test_find_book_no_match_returns_empty PASSED
tests/test_library_service.py::TestFindBook::test_find_book_no_criteria_raises PASSED
tests/test_library_service.py::TestRegisterUser::test_register_user_success PASSED
tests/test_library_service.py::TestRegisterUser::test_register_user_duplicate_email_raises PASSED
tests/test_library_service.py::TestRegisterUser::test_register_user_empty_name_raises PASSED
tests/test_library_service.py::TestRegisterUser::test_register_user_empty_email_raises PASSED

============================== 17 passed in 0.05s ==============================
```

---

## Лінтинг (flake8)

```bash
pip3 install flake8
python3 flake8 src/ tests/ --max-line-length=100
```
