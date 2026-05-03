"""Session authentication tests.

Fixture for the SLOBAC audit's `semantic-redundancy` scenario. This file tests
session-level auth — but one test redundantly re-verifies the same expired-token
behavior that test_auth_tokens.py already covers at a more direct layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Credentials:
    username: str
    token_expires_at: datetime


class SessionManager:
    def authenticate(self, creds: Credentials) -> bool:
        if creds.token_expires_at <= datetime.now():
            return False
        return True

    def create_session(self, creds: Credentials) -> str | None:
        if not self.authenticate(creds):
            return None
        return f"session-{creds.username}"


def test_session_rejects_expired_credentials():
    """Redundant with test_expired_token_is_rejected in test_auth_tokens.py —
    same observable (expired = rejected), different indirection level."""
    mgr = SessionManager()
    creds = Credentials(
        username="user-1",
        token_expires_at=datetime.now() - timedelta(hours=1),
    )
    assert mgr.authenticate(creds) is False


def test_session_creates_token_for_valid_credentials():
    mgr = SessionManager()
    creds = Credentials(
        username="user-1",
        token_expires_at=datetime.now() + timedelta(hours=1),
    )
    session_id = mgr.create_session(creds)
    assert session_id is not None
    assert "user-1" in session_id


def test_session_returns_none_for_invalid_credentials():
    mgr = SessionManager()
    creds = Credentials(
        username="user-1",
        token_expires_at=datetime.now() - timedelta(hours=1),
    )
    assert mgr.create_session(creds) is None
