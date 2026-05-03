"""Calculator tests — correctly placed in unit/.

Fixture for the SLOBAC audit's `wrong-level` scenario (negative example). This
file lives in unit/ and contains only pure-function tests. The audit must NOT
flag it despite the imports of math and decimal (standard library, no I/O).
"""

from __future__ import annotations

import math
from decimal import Decimal


class Calculator:
    """Minimal stub — the audit reads structure, not behavior."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def sqrt(self, x: float) -> float:
        return math.sqrt(x)

    def precise_add(self, a: str, b: str) -> Decimal:
        return Decimal(a) + Decimal(b)


def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_add_negative():
    calc = Calculator()
    assert calc.add(-1, -2) == -3


def test_divide():
    calc = Calculator()
    assert calc.divide(10, 2) == 5.0


def test_divide_by_zero():
    calc = Calculator()
    try:
        calc.divide(1, 0)
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        pass


def test_sqrt():
    calc = Calculator()
    assert calc.sqrt(16) == 4.0


def test_sqrt_of_zero():
    calc = Calculator()
    assert calc.sqrt(0) == 0.0


def test_precise_add():
    calc = Calculator()
    result = calc.precise_add("0.1", "0.2")
    assert result == Decimal("0.3")


def test_precise_add_large():
    calc = Calculator()
    result = calc.precise_add("999999999.999", "0.001")
    assert result == Decimal("1000000000.000")
