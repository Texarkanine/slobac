"""User repository tests.

Fixture for the SLOBAC audit's `implementation-coupled` scenario. Two planted
positives reach into private state and call private helpers respectively.
One negative control drives only the public API.
"""

from __future__ import annotations


class UserRepository:
    """SUT — stores users in an in-memory dict; exposes get/save publicly."""

    def __init__(self):
        self._users: dict[str, dict] = {}

    def save(self, user_id: str, name: str, email: str) -> None:
        normalized = self._normalize_email(email)
        self._users[user_id] = {
            "id": user_id,
            "name": name,
            "email": normalized,
        }

    def get(self, user_id: str) -> dict | None:
        return self._users.get(user_id)

    def _normalize_email(self, email: str) -> str:
        return email.strip().lower()


# --- positive 1: reaches into _private state.                               -
#     Asserts on `repo._users` — a private dict whose existence and shape -
#     are implementation details. Renaming `_users` to `_records` or     -
#     swapping it for an external KV store breaks this test even though -
#     the public save/get contract is preserved.                         -

def test_save_persists_user_in_internal_dict():
    repo = UserRepository()
    repo.save(user_id="u1", name="Alice", email="alice@example.com")
    assert "u1" in repo._users
    assert repo._users["u1"]["name"] == "Alice"


# --- positive 2: calls a _private helper directly.                          -
#     `_normalize_email` is a private convention (leading underscore).    -
#     A refactor that inlines the normalization, moves it to a free      -
#     function, or replaces it with a third-party library call breaks  -
#     this test even though the observable behavior of `save` is        -
#     unchanged.                                                         -

def test_normalize_email_lowercases_and_strips_whitespace():
    repo = UserRepository()
    assert repo._normalize_email("  Alice@Example.COM  ") == "alice@example.com"


# --- negative control: drives only the public surface.                      -
#     `save(...)` then `get(...)` — both public. No private accessor.    -
#     Asserts on the observable transform (email lowercased) without    -
#     coupling to whether normalization happens via `_normalize_email`, -
#     a free function, or a third-party library.                        -

def test_save_then_get_returns_user_with_lowercased_email():
    repo = UserRepository()
    repo.save(user_id="u2", name="Bob", email="  Bob@Example.COM  ")
    assert repo.get("u2") == {
        "id": "u2",
        "name": "Bob",
        "email": "bob@example.com",
    }
