"""Shared pytest helpers for the taxonomy-index generator tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Path to the static markdown fixtures used by the parser tests."""
    return Path(__file__).parent / "fixtures"
