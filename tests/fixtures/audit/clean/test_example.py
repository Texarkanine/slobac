"""Clean-suite tests.

Fixture for the SLOBAC audit's false-positive gate. Every test here has a
behavior-encoded name and a body that verifies exactly the claim the title
makes. The audit must emit zero findings at any scope.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str


def add(a: Money, b: Money) -> Money:
    if a.currency != b.currency:
        raise ValueError("cannot add mixed currencies")
    return Money(amount=a.amount + b.amount, currency=a.currency)


class TestMoneyAddition:
    def test_sums_amounts_when_currencies_match(self):
        result = add(Money(100, "USD"), Money(250, "USD"))
        assert result == Money(350, "USD")

    def test_rejects_mixed_currencies_with_value_error(self):
        try:
            add(Money(100, "USD"), Money(100, "EUR"))
        except ValueError as exc:
            assert "mixed currencies" in str(exc)
        else:
            raise AssertionError("expected ValueError for mixed currencies")

    def test_preserves_currency_of_operands_in_result(self):
        result = add(Money(1, "JPY"), Money(2, "JPY"))
        assert result.currency == "JPY"
