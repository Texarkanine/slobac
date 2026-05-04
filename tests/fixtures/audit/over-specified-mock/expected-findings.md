# Expected findings — `over-specified-mock` scenario

**Target suite root:** `tests/fixtures/audit/over-specified-mock/`
**In-scope smells:** `over-specified-mock`
**Expected finding count:** 2

The two findings exercise both canonical shapes from the [`over-specified-mock`](https://texarkanine.github.io/slobac/taxonomy/over-specified-mock/) entry: **over-specified interactions** (exact call counts, ordering, baked production constants) and **testing internal details** (deep argument capture, log-level pinning). Distinct from `tautology-theatre` — here the SUT runs end-to-end; the issue is that the test asserts on *how* it works rather than *what* it produces.

## Findings

### 1. `test_dispatch_sends_email_with_default_timeout` — shape: over-specified interactions

- **Location:** `test_email_dispatcher.py` → module level
- **Smell:** `over-specified-mock`
- **Rationale:** The test pins `smtp.send.call_count == 1`, uses `assert_called_once_with` with the production-constant `timeout=30` baked in, asserts `logger.info.call_count == 2`, and pins exact ordering via `assert_has_calls`. An internal refactor that, for example, split `dispatch` into a helper which logs at a different cardinality (one combined log line instead of two), or that read the timeout from a constructor argument instead of a class constant, would break this test without breaking the public dispatch contract (which is "sends the email; returns a result with sent/message_id/to").
- **Prescribed remediation:** Reduce to outcome-based assertion. Per the canonical fix steps: (1) identify whether the collaboration is contract-relevant — for `smtp.send`, "is called with the recipient" *is* the contract; for the timeout constant and the log-call cardinality, those are incidental. (2) Keep one focused matcher-based assertion: `smtp.send.assert_called_once_with(to="alice@example.com", subject=ANY, body=ANY, timeout=ANY)`. (3) Delete the `logger.info` assertions entirely. (4) The post-fix test must survive a SUT refactor that reorders internal calls — verify by mentally applying such a refactor.
- **Why this isn't a false positive:** Multiple canonical signals fire at once: pinned call count, pinned ordering via `assert_has_calls`, and a production-constant (`timeout=30`) baked into the assertion. The test name suggests the contract is "sends with default timeout," but the contract is whether the email gets dispatched — not which timeout value the SUT happens to choose internally.

### 2. `test_dispatch_logs_dispatch_event_at_info_level` — shape: testing internal details

- **Location:** `test_email_dispatcher.py` → module level
- **Smell:** `over-specified-mock`
- **Rationale:** The test inspects `logger.info.call_args_list[0].args` field-by-field (canonical "ArgumentCaptor followed by field-by-field assertions on the captured argument" signal), and asserts that *no* other log level was used (`logger.debug.call_count == 0`, `.warning == 0`, `.error == 0`). Whether `dispatch` logs at info, debug, or not at all is an internal observability choice — not part of the public dispatch contract. A refactor that switches to structured logging via a different method name would break the test without breaking the dispatch behavior.
- **Prescribed remediation:** Delete the entire test. The "logs dispatch event at info level" claim is not a contract the SUT publicly commits to; if observability *is* a contract (e.g. structured event emission for downstream consumers), encode that contract via a separate `EventEmitter` collaborator that the test can drive observably — do not assert on log-call shape.
- **Why this isn't a false positive:** Field-by-field inspection of `call_args_list[0].args` is the textbook canonical signal. The negation assertions on debug/warning/error are a `verifyNoMoreInteractions`-equivalent — pinning what the SUT must *not* do internally.

## Tests that must NOT be flagged

### `test_dispatch_returns_message_id_and_recipient`

- **Location:** `test_email_dispatcher.py` → module level
- **Why not over-specified:** The primary assertion is `result == {...}` — full structural equality on the SUT's observable return value. The single mock-call assertion uses matcher-based `ANY` for subject/body/timeout — so an internal refactor that changes the timeout default, or reads subject/body from a different source, leaves this test green so long as the recipient is passed through.
- **False-positive guard:** Naive detectors that flag any test using `assert_called_once_with` or any test inspecting mock calls will trip here. The semantic question per the canonical entry is *"would this test still pass if the SUT refactored to call the collaborator differently but produced the same external outcome?"* — yes, because all collaborator-call args except `to` are wildcarded.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `over-specified-mock`, 1 must not be flagged.
- The remediation for finding 1 is **reduce to outcome-based**; for finding 2 is **delete** (because the asserted contract is not a contract). The audit is correct only when the remediation distinguishes these two paths.
- Sibling smells (`tautology-theatre`, `implementation-coupled`) are not in scope; cross-pollution shape, if incidentally present, must be scoped out by the audit.
