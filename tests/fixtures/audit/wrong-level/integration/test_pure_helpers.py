"""Pure helper tests — WRONG LEVEL: in integration/ but pure-function unit tests.

Fixture for the SLOBAC audit's `wrong-level` scenario. This file lives in
integration/ but every test is a pure-function unit test with zero external
dependencies. The audit must flag these as wrong-level.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    return a + b


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").strip("-")


def parse_bool(text: str) -> bool:
    return text.lower() in ("true", "1", "yes", "on")


# --- all pure-function tests — no I/O, no fixtures, no mocks ----------------

def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 0) == 0


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_minimum():
    assert clamp(-5, 0, 10) == 0


def test_clamp_above_maximum():
    assert clamp(15, 0, 10) == 10


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"


def test_slugify_already_slug():
    assert slugify("hello-world") == "hello-world"


def test_slugify_leading_trailing_spaces():
    assert slugify(" Hello World ") == "hello-world"


def test_parse_bool_true_variants():
    for val in ("true", "True", "TRUE", "1", "yes", "on"):
        assert parse_bool(val) is True


def test_parse_bool_false_variants():
    for val in ("false", "False", "0", "no", "off", "maybe"):
        assert parse_bool(val) is False
