"""API client tests — WRONG LEVEL: in unit/ but uses real I/O.

Fixture for the SLOBAC audit's `wrong-level` scenario. This file lives in
unit/ but contains tests that spawn subprocesses and make real HTTP requests.
The audit must flag these as wrong-level.
"""

from __future__ import annotations

import json
import subprocess
import urllib.request
from unittest.mock import patch


class ApiClient:
    """Stub client — the audit reads imports and call patterns, not behavior."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_users(self) -> list[dict]:
        with urllib.request.urlopen(f"{self.base_url}/users") as resp:
            return json.loads(resp.read())


# --- correctly mocked test (this one IS unit-level) --------------------------

def test_get_users_with_mock():
    """Properly mocked — this test belongs in unit/."""
    mock_response = b'[{"id": 1, "name": "alice"}]'
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__ = lambda s: s
        mock_urlopen.return_value.__exit__ = lambda s, *a: None
        mock_urlopen.return_value.read.return_value = mock_response
        client = ApiClient("http://example.com")
        users = client.get_users()
        assert len(users) == 1


# --- wrong-level: real HTTP request in a "unit" test ------------------------

def test_fetch_users_from_live_endpoint():
    """Hits a real endpoint — this is integration behavior in a unit directory."""
    client = ApiClient("https://jsonplaceholder.typicode.com")
    users = client.get_users()
    assert isinstance(users, list)
    assert len(users) > 0


# --- wrong-level: subprocess spawn in a "unit" test -------------------------

def test_cli_invocation_returns_output():
    """Spawns a subprocess — this is integration behavior in a unit directory."""
    result = subprocess.run(
        ["echo", "hello"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "hello" in result.stdout
