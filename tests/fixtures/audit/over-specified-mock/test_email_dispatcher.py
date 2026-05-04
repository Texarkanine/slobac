"""Email dispatcher tests.

Fixture for the SLOBAC audit's `over-specified-mock` scenario. Two planted
positives exercise both canonical shapes (over-specified interactions and
testing internal details). One negative control asserts only on the
observable outcome.
"""

from __future__ import annotations

from unittest.mock import ANY, MagicMock, call


class EmailDispatcher:
    """SUT — sends an email by calling smtp_client.send and logger.info."""

    DEFAULT_TIMEOUT = 30

    def __init__(self, smtp_client, logger):
        self._smtp = smtp_client
        self._logger = logger

    def dispatch(self, to: str, subject: str, body: str) -> dict:
        self._logger.info("dispatching to %s", to)
        message_id = self._smtp.send(
            to=to, subject=subject, body=body, timeout=self.DEFAULT_TIMEOUT
        )
        self._logger.info("dispatched %s", message_id)
        return {"sent": True, "message_id": message_id, "to": to}


# --- positive 1: over-specified interactions.                               -
#     Pins exact call count, exact ordering, exact constant (the timeout   -
#     production constant baked into the test), and `assert_no_other_calls`-
#     style strictness via `assert_has_calls` with extra checks. An       -
#     internal refactor (e.g. splitting `dispatch` into helper methods    -
#     that call `logger.info` differently) would break this without      -
#     breaking the observable contract.                                   -

def test_dispatch_sends_email_with_default_timeout():
    smtp = MagicMock()
    smtp.send.return_value = "msg-001"
    logger = MagicMock()

    dispatcher = EmailDispatcher(smtp, logger)
    dispatcher.dispatch(
        to="alice@example.com", subject="Hi", body="Hello"
    )

    assert smtp.send.call_count == 1
    smtp.send.assert_called_once_with(
        to="alice@example.com",
        subject="Hi",
        body="Hello",
        timeout=30,
    )
    assert logger.info.call_count == 2
    logger.info.assert_has_calls([
        call("dispatching to %s", "alice@example.com"),
        call("dispatched %s", "msg-001"),
    ])


# --- positive 2: testing internal details.                                  -
#     `ArgumentCaptor`-style deep inspection of the captured argument and -
#     a redundant `verify_no_other_interactions` shape. Even the choice  -
#     of which logger level (`info` vs `debug`) is incidental, but this  -
#     test pins it.                                                       -

def test_dispatch_logs_dispatch_event_at_info_level():
    smtp = MagicMock()
    smtp.send.return_value = "msg-002"
    logger = MagicMock()

    EmailDispatcher(smtp, logger).dispatch(
        to="bob@example.com", subject="Hello", body="Body"
    )

    
    captured_args = logger.info.call_args_list[0].args
    assert captured_args[0] == "dispatching to %s"
    assert captured_args[1] == "bob@example.com"
    
    assert logger.debug.call_count == 0
    assert logger.warning.call_count == 0
    assert logger.error.call_count == 0


# --- negative control: outcome-based assertion.                             -
#     Mocks stand in for collaborators; the assertion checks only the SUT's-
#     observable return value. Internal refactors (renaming helpers,       -
#     reordering log lines, changing the timeout default) are tolerated -
#     so long as the public dispatch contract is preserved.              -

def test_dispatch_returns_message_id_and_recipient():
    smtp = MagicMock()
    smtp.send.return_value = "msg-003"
    logger = MagicMock()

    result = EmailDispatcher(smtp, logger).dispatch(
        to="carol@example.com", subject="X", body="Y"
    )

    assert result == {
        "sent": True,
        "message_id": "msg-003",
        "to": "carol@example.com",
    }
    
    smtp.send.assert_called_once_with(
        to="carol@example.com", subject=ANY, body=ANY, timeout=ANY
    )
