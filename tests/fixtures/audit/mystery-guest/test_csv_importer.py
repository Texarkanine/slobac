"""CSV importer tests.

Fixture for the SLOBAC audit's `mystery-guest` scenario. Two planted positives
load the external `orders.csv` file and assert on magic counts/values whose
derivation is invisible inline. One negative control uses inline fixture
data with a derived expectation.
"""

from __future__ import annotations

import csv
from pathlib import Path

FIXTURE_FILE = Path(__file__).parent / "orders.csv"


def import_orders(path: Path) -> list[dict]:
    """SUT — read a CSV of orders into a list of dicts."""
    with path.open() as f:
        return list(csv.DictReader(f))


def count_paid(orders: list[dict]) -> int:
    return sum(1 for o in orders if o["status"] == "paid")


# --- positive 1: classical mystery guest.                                   -
#     Reads `orders.csv` (an external fixture file) and asserts a magic   -
#     count of 6. The reader cannot tell from the test why 6 is the     -
#     right answer without opening the CSV. No inline summary, no      -
#     derived constant.                                                  -

def test_import_orders_returns_all_rows():
    orders = import_orders(FIXTURE_FILE)
    assert len(orders) == 6


# --- positive 2: fixture-coupled magic-number variant.                      -
#     Asserts `count_paid(...) == 4` — a magic number tied to the exact -
#     order-status distribution in `orders.csv`. Editing the fixture  -
#     to rebalance statuses (e.g. one more pending, one less paid)   -
#     silently breaks this test with no signal of what went wrong.   -

def test_count_paid_returns_four():
    orders = import_orders(FIXTURE_FILE)
    assert count_paid(orders) == 4


# --- negative control: inline fixture with derived expectation.             -
#     The fixture data is inline; the relevant shape is named with a     -
#     local constant and the expectation is derived from it             -
#     symbolically rather than as a magic number.                       -

def test_count_paid_counts_only_paid_status():
    inline_orders = [
        {"order_id": "1", "customer": "alice", "status": "paid", "amount": "10"},
        {"order_id": "2", "customer": "alice", "status": "paid", "amount": "20"},
        {"order_id": "3", "customer": "bob", "status": "pending", "amount": "30"},
        {"order_id": "4", "customer": "carol", "status": "refunded", "amount": "40"},
    ]
    EXPECTED_PAID_ROWS = sum(1 for o in inline_orders if o["status"] == "paid")
    assert count_paid(inline_orders) == EXPECTED_PAID_ROWS
