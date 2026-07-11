"""Runtime-emitted text oracle tests.

Fixture for the SLOBAC audit's `loose-text-oracle` scenario. Two planted
positives use underdetermined substrings on errors/logs; two negative
controls cover typed+supplementary and text-is-product goldens.
"""

from __future__ import annotations

import logging

import pytest


class NotFoundError(LookupError):
    """Typed domain error — preferred oracle target."""


def fetch(resource: str, *, fail: str | None = None) -> str:
    """SUT stand-in — fetch a resource or raise a failure."""
    if fail == "timeout":
        # Deliberately ambiguous message: opposite polarity still contains
        # the token "timeout" (e.g. "timeout disabled; proceeding").
        raise RuntimeError(f"timeout waiting for {resource}")
    if fail == "missing":
        raise NotFoundError(f"resource {resource} was not found")
    return f"payload:{resource}"


def process(item: str, logger: logging.Logger) -> str:
    """SUT stand-in — process an item and emit a log line."""
    # Deliberately ambiguous token: "operation success: false" would also match.
    logger.info("operation success for %s", item)
    return f"done:{item}"


def render_help() -> str:
    """SUT stand-in — CLI help text that *is* the product surface."""
    return (
        "Usage: demo [OPTIONS] COMMAND\n"
        "\n"
        "Options:\n"
        "  --help     Show this message and exit.\n"
        "  --version  Show the version and exit.\n"
    )


# --- positive 1: ambiguous error-message match as sole failure oracle.      -
#     `match="timeout"` underdetermines meaning — a raise whose message    -
#     says the opposite ("timeout disabled") would still pass.             -

def test_fetch_raises_on_timeout():
    # Opposite meaning that would also match: RuntimeError("timeout disabled").
    with pytest.raises(RuntimeError, match="timeout"):
        fetch("alpha", fail="timeout")


# --- positive 2: ambiguous log/stdout phrase as semantic claim.             -
#     `"success" in caplog.text` passes for "operation success: false".    -

def test_process_logs_success(caplog):
    # Opposite meaning that would also match: "operation success: false".
    with caplog.at_level(logging.INFO):
        process("beta", logging.getLogger("demo"))
    assert "success" in caplog.text


# --- negative control: typed primary oracle + supplementary datum match.    -
#     Type identifies which failure; message only checks the resource name -
#     appears (Go Wiki carve-out).                                         -

def test_fetch_raises_typed_not_found_with_optional_param_name():
    with pytest.raises(NotFoundError, match="gamma") as exc_info:
        fetch("gamma", fail="missing")
    # Primary oracle is the type; match= only checks the dynamic datum.
    assert isinstance(exc_info.value, NotFoundError)


# --- negative control: text *is* the product (full golden diagnostic).      -
#     Whole CLI help is the specified deliverable — approval-style, not a  -
#     lone underdetermined substring.                                      -

def test_cli_help_golden_matches_full_diagnostic():
    expected = (
        "Usage: demo [OPTIONS] COMMAND\n"
        "\n"
        "Options:\n"
        "  --help     Show this message and exit.\n"
        "  --version  Show the version and exit.\n"
    )
    assert render_help() == expected
