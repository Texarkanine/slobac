"""Text normalizer tests.

Fixture for the SLOBAC audit's `pseudo-tested` scenario. Two planted positives
exercise the canonical signal: the SUT runs, an assertion fires, but a no-op
replacement of the SUT body would still pass. One negative control asserts on
a derived value that a no-op replacement would break.
"""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    """SUT — collapse whitespace, lowercase, strip leading/trailing punctuation."""
    if text is None:
        return ""
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed.lower().strip(".,!?;:")


# --- positive 1: structural-shape pseudo-tested.                            -
#     `def normalize(s): return s` (no-op) survives — the input "Hello"     -
#     is non-empty, so `len(result) > 0` passes against the no-op too.      -

def test_normalize_returns_non_empty_string():
    result = normalize("Hello, World!  ")
    assert isinstance(result, str)
    assert len(result) > 0


# --- positive 2: identity-pseudo-tested.                                    -
#     `def normalize(s): return s` (no-op) survives — input contains the   -
#     letters "hello", and so does any plausible passthrough. The "in"     -
#     check accepts identity transforms.                                   -

def test_normalize_preserves_some_letters():
    result = normalize("HELLO WORLD")
    assert "h" in result.lower() or "H" in result


# --- negative control: derived-value assertion.                             -
#     A no-op `def normalize(s): return s` returns "  Hello, World!  " —   -
#     not equal to "hello world" — so this test would fail under the      -
#     no-op mutation. Mutation kill-set delta is strictly positive.        -

def test_normalize_lowercases_and_strips_trailing_punctuation():
    assert normalize("  Hello, World!  ") == "hello world"
