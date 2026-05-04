"""Invoice parser tests.

Fixture for the SLOBAC audit's `vacuous-assertion` scenario. Two planted
positives where the SUT runs and returns a real structured value, but the
assertion is so weak that many interesting wrong answers would still pass.
One negative control asserts on structural equality.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Invoice:
    invoice_id: str
    customer: str
    amount_cents: int
    currency: str


def parse(line: str) -> Invoice:
    """SUT — parse a `INV-1234|ACME Corp|12550|USD` line into an Invoice."""
    parts = line.strip().split("|")
    return Invoice(
        invoice_id=parts[0],
        customer=parts[1],
        amount_cents=int(parts[2]),
        currency=parts[3],
    )


# --- positive 1: the assertion is `is not None` only.                       -
#     Wrong answers that still pass: `return Invoice("", "", 0, "")`,       -
#     `return Invoice("garbage", "anyone", 1, "XYZ")`, any constructed     -
#     Invoice at all. Many interesting wrong implementations satisfy it.   -

def test_parse_returns_an_invoice():
    result = parse("INV-1234|ACME Corp|12550|USD")
    assert result is not None


# --- positive 2: only checks that one field is "truthy".                    -
#     Wrong answers that still pass: any invoice_id at all (including      -
#     wrong ones, including the literal string "garbage"). The format     -
#     `INV-\d+` is knowable and could be checked exactly.                  -

def test_parse_extracts_an_invoice_id():
    result = parse("INV-1234|ACME Corp|12550|USD")
    assert result.invoice_id


# --- negative control: structural equality on the parsed Invoice.           -
#     The mutation kill-set is large — wrong delimiter handling, wrong   -
#     index ordering, wrong int-parsing, wrong currency truncation all   -
#     fail this assertion.                                               -

def test_parse_extracts_all_four_fields_in_order():
    assert parse("INV-1234|ACME Corp|12550|USD") == Invoice(
        invoice_id="INV-1234",
        customer="ACME Corp",
        amount_cents=12550,
        currency="USD",
    )
