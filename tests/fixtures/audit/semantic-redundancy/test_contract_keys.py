"""Contract key tests — intentional duplication (negative example).

Fixture for the SLOBAC audit's `semantic-redundancy` scenario. These tests both
check "required keys present" but guard DIFFERENT contracts (API response shape
vs. token payload shape). The audit must not flag them as semantically redundant.
"""

from __future__ import annotations


def _build_api_response() -> dict:
    return {
        "status": "ok",
        "data": {"id": 1, "name": "alice"},
        "pagination": {"page": 1, "total": 10},
    }


def _build_token_payload() -> dict:
    return {
        "sub": "user-1",
        "iat": 1700000000,
        "exp": 1700003600,
        "aud": "api.example.com",
    }


def test_api_response_contains_required_keys():
    """Guards the external API contract — consumers depend on these keys."""
    response = _build_api_response()
    required = {"status", "data", "pagination"}
    assert required.issubset(response.keys())


def test_token_payload_contains_required_claims():
    """Guards the JWT contract — auth infrastructure depends on these claims."""
    payload = _build_token_payload()
    required = {"sub", "iat", "exp", "aud"}
    assert required.issubset(payload.keys())
