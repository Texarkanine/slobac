"""Payment processor tests.

Fixture for the SLOBAC audit's `tautology-theatre` scenario. Two planted
positives (one per canonical shape: mock-tautology and mock-of-SUT) plus a
negative control where the real SUT runs and a mock stands in only for an
external collaborator.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class PaymentProcessor:
    """Minimal SUT — exists so tests have something real to import."""

    def __init__(self, http_client):
        self._http = http_client

    def validate(self, amount: int) -> bool:
        return amount > 0

    def charge(self, amount: int) -> dict:
        response = self._http.post("/charge", json={"amount": amount})
        return {"ok": response["status"] == 200, "amount": amount}


# --- positive 1: mock tautology.                                            -
#     The mock is configured to return True; the assertion checks the mock  -
#     returned True. The real PaymentProcessor.charge is never called.      -
#     Logically `x = True; assert x == True`.                               -

def test_charge_returns_true_when_successful():
    mock_charger = MagicMock()
    mock_charger.charge.return_value = True
    result = mock_charger.charge(amount=1000)
    assert result is True


# --- positive 2: mock-of-SUT.                                               -
#     PaymentProcessor IS the unit under test, but its `validate` method is -
#     replaced by a patch. The assertion verifies the patch's return value, -
#     not the real validation logic.                                        -

def test_validate_accepts_positive_amount():
    with patch.object(PaymentProcessor, "validate", return_value=True):
        processor = PaymentProcessor(http_client=MagicMock())
        result = processor.validate(amount=42)
        assert result is True


# --- negative control: real SUT runs; mock stands in for an external HTTP  -
#     collaborator only. Asserts on the SUT's observable output, not on the -
#     mock's configured return value.                                       -

def test_charge_marks_response_ok_when_http_returns_200():
    http = MagicMock()
    http.post.return_value = {"status": 200}
    processor = PaymentProcessor(http_client=http)
    result = processor.charge(amount=100)
    assert result == {"ok": True, "amount": 100}
