# Expected findings — `semantic-redundancy` scenario

**Target suite root:** `tests/fixtures/audit/semantic-redundancy/`
**In-scope smells:** `semantic-redundancy`
**Expected finding count:** 1 (covering a cross-file redundancy group)

Shape mirrors the audit report template. Each finding below must appear in the emitted `slobac-audit.md` with equivalent content; phrasing need not be byte-identical, but the test location, smell slug, remediation path, and rationale anchor must match.

## Findings

### 1. Token-validation behavior tested redundantly across two files

- **Location:** `test_auth_tokens.py` → `test_expired_token_is_rejected` (line ~28) AND `test_session_auth.py` → `test_session_rejects_expired_credentials` (line ~30)
- **Smell:** `semantic-redundancy`
- **Rationale:** Both tests verify the same observable behavior: a token whose expiry timestamp is in the past causes rejection. `test_auth_tokens.py` does it via a direct `validate_token()` call; `test_session_auth.py` does it via `SessionManager.authenticate()` which internally calls `validate_token()`. Different call paths, same behavioral claim — "expired credentials are rejected." See [semantic-redundancy](https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/) signals — "two tests exercise the same observable behavior with different names, fixtures, or mock styles."
- **Prescribed remediation:** The canonical location is `test_auth_tokens.py` (more direct, thinner fixture surface, stronger assertion — tests the validation function at its natural layer). The `test_session_rejects_expired_credentials` test in `test_session_auth.py` should either be deleted (with a named absorber comment explaining that `test_expired_token_is_rejected` in `test_auth_tokens.py` covers this) or refactored to test a session-level behavior that the token-level test does not cover (e.g., that the session manager returns a specific error type, logs the rejection, or cleans up session state).
- **Why this isn't a false positive:** Both tests construct an expired token/credential (different fixture shapes, same semantic content), pass it through a validation path, and assert rejection. The observable being guarded is identical; only the indirection level differs.

## Tests that must NOT be flagged

### `test_contract_keys.py` — intentional duplication as contract guard

- **Location:** `test_contract_keys.py` → `test_api_response_contains_required_keys` (line ~18) and `test_contract_keys.py` → `test_token_payload_contains_required_claims` (line ~27)
- **Why not redundant:** These tests both assert that a data structure contains certain required keys. A naive detector might cluster them as "checks required keys." But they protect *different knowledge*: one guards the API response contract (what the external consumer sees), the other guards the token payload contract (what the auth system signs). Folding them would lose the independent contract assertion — if one schema changes, the other's test must still guard its own shape.
- **False-positive guard:** See the [semantic-redundancy](https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/) canonical entry's False-positive guards section — "similar-looking tests that guard different knowledge" are intentional duplication, not the smell. The key question is whether folding them would lose information, and here it would.

## Notes

- This is a multi-file scenario exercising cross-suite detection scope. The assessor must compare behavior descriptions across files to detect the overlap.
- The finding covers a 2-test redundancy group spanning 2 files. The expected remediation names a canonical location and explains why it's canonical (more direct, thinner fixture, stronger assertion).
- `test_contract_keys.py` is the negative example: structurally similar pattern (key-checking assertions) but semantically distinct knowledge being protected.
