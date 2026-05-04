"""Promo calculator tests.

Fixture for the SLOBAC audit's `conditional-logic` scenario. Two planted
positives exercise the canonical `if`-shape and `try/except`-shape signals.
One negative control uses parameterized inputs to express the same intent
without branching inside the test body.
"""

from __future__ import annotations

import pytest


def apply_promo(price: float, code: str | None) -> float:
    """SUT — apply a known promo code to a price; raise on unknown code."""
    if code is None:
        return price
    if code == "SAVE10":
        return round(price * 0.9, 2)
    if code == "FREESHIP":
        return price
    raise ValueError(f"unknown promo code: {code}")


# --- positive 1: `if cond: assert(...)` shape.                              -
#     The `if code is not None` path has an assertion; the `else` path    -
#     (when `code is None`) is silently passing — vacuous by omission. -

def test_apply_promo_with_save10_reduces_price():
    code = "SAVE10"
    result = apply_promo(100.00, code)
    if code:
        assert result == 90.00


# --- positive 2: `try { sut() } except: assert(...)` without trailing      -
#     `pytest.fail("should have raised")`. If `apply_promo` ever         -
#     stopped raising on unknown codes (e.g. silently returned the     -
#     original price), the except block would never be entered and    -
#     the test would pass without ever asserting anything.            -

def test_apply_promo_with_unknown_code_raises_value_error():
    try:
        apply_promo(100.00, "MYSTERY")
    except ValueError as e:
        assert "MYSTERY" in str(e)


# --- negative control: parameterized inputs, no branching.                  -
#     Same intent as positive 1 (apply_promo with a code reduces price)  -
#     expressed without an `if` inside the body. Each parameterized   -
#     case has an unconditional assertion.                              -

@pytest.mark.parametrize(
    "code,expected",
    [
        ("SAVE10", 90.00),
        ("FREESHIP", 100.00),
        (None, 100.00),
    ],
)
def test_apply_promo_returns_expected_price(code, expected):
    assert apply_promo(100.00, code) == expected
