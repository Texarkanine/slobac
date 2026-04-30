"""Auth token validation tests.

Fixture for the SLOBAC audit's `semantic-redundancy` scenario. This file tests
token validation directly — it's the more natural home for token-behavior tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Token:
    subject: str
    expires_at: datetime


def validate_token(token: Token) -> bool:
    return token.expires_at > datetime.now()


def test_valid_token_is_accepted():
    token = Token(subject="user-1", expires_at=datetime.now() + timedelta(hours=1))
    assert validate_token(token) is True


def test_expired_token_is_rejected():
    """The canonical test for expired-token rejection behavior."""
    token = Token(subject="user-1", expires_at=datetime.now() - timedelta(hours=1))
    assert validate_token(token) is False


def test_token_expiring_exactly_now_is_rejected():
    token = Token(subject="user-1", expires_at=datetime.now())
    assert validate_token(token) is False
