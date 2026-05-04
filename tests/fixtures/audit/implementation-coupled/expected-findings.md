# Expected findings — `implementation-coupled` scenario

**Target suite root:** `tests/fixtures/audit/implementation-coupled/`
**In-scope smells:** `implementation-coupled`
**Expected finding count:** 2

The two findings exercise the canonical signals from the [`implementation-coupled`](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/) entry: reaching into a `_private` field and calling a `_private` helper directly. Distinct from `over-specified-mock` — that's about over-asserting *interactions* with collaborators; this is about reaching into *state* or *visibility* of the SUT itself.

## Findings

### 1. `test_save_persists_user_in_internal_dict` — public-API substitute

- **Location:** `test_user_repository.py` → module level
- **Smell:** `implementation-coupled`
- **Rationale:** The assertion accesses `repo._users` — a private attribute by Python convention (leading underscore). The canonical signal "Python: `sut._internal_dict['some_key']` instead of a public getter" applies directly. A refactor that renames `_users` to `_records`, replaces it with an external KV store, or makes the dict lazy-loaded breaks this test even though the public `save`/`get` contract is preserved.
- **Prescribed remediation:** Drive the public API instead. Replace `assert "u1" in repo._users` with `assert repo.get("u1") is not None` and the field assertion with `assert repo.get("u1")["name"] == "Alice"`. Per the canonical fix step (1), "drive the library's public API instead of reaching for internals." Apply the [`semantic-redundancy`](https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/) check after the fix — the resulting test may now duplicate the negative-control test (`test_save_then_get_returns_user_with_lowercased_email`); fold them if so.
- **Why this isn't a false positive:** `_users` is unambiguously private by convention. There is no scenario where production code outside `UserRepository` should read `_users` directly; therefore the test is asserting on a non-contract.

### 2. `test_normalize_email_lowercases_and_strips_whitespace` — extract-or-delete

- **Location:** `test_user_repository.py` → module level
- **Smell:** `implementation-coupled`
- **Rationale:** The test calls `repo._normalize_email(...)` — a private helper. The canonical signal "`_private_method(` in the test body (Python convention)" fires. The test claims to verify normalization behavior, but does so by binding to a private implementation detail. A refactor that inlines `_normalize_email` into `save`, moves it to a module-level function, or replaces it with a `email_validator` library call breaks this test even though `save("...", email=" Alice@Example.COM  ")` would still produce the same lowercased stored value.
- **Prescribed remediation:** Apply canonical fix step (2). Ask: is `_normalize_email` cohesive enough to extract as a pure public function? Email normalization is small, pure, and reusable — yes. Extract `normalize_email` to module level (or a `user_repository.normalization` submodule), make it public, and rewrite this test to call the public function. Otherwise, cover the behavior through `save`/`get` and delete this test (folding into the negative-control test which already verifies the lowercase transform via the public surface). Per the [no-extract-for-testability governor rule](https://texarkanine.github.io/slobac/principles/#no-extract-for-testability), extraction is only justified when it clarifies architecture — extraction here is justified iff the helper is reused outside `UserRepository`.
- **Why this isn't a false positive:** The leading-underscore convention is the canonical Python signal for "private." The alternative reading — that `_normalize_email` is part of a stable but underscore-prefixed-by-style-only API — is rejected by the SUT's own structure (no other module imports or calls it).

## Tests that must NOT be flagged

### `test_save_then_get_returns_user_with_lowercased_email`

- **Location:** `test_user_repository.py` → module level
- **Why not implementation-coupled:** Drives only public methods (`save`, `get`). Asserts on the observable result of the public `get` call — a fully public contract. A refactor that replaces `_normalize_email` with an inlined transform or a third-party library leaves this test green so long as the lowercasing semantic is preserved.
- **False-positive guard:** Naive detectors that flag any test asserting on dict shape will trip here. The semantic question per the canonical entry is *"is the accessed field part of the SUT's stable public API?"* — for `repo.get(...)`, yes; the dict shape `{id, name, email}` is the public return contract.

## Notes

- Scenario contains 3 tests total: 2 must be flagged with `implementation-coupled`, 1 must not be flagged.
- The two findings have *different* prescribed remediations — finding 1 is **public-API substitute**, finding 2 is **extract or delete**. The audit must distinguish; a uniform "drive public API" prescription for both is a build-phase bug per the canonical entry's branching fix logic.
- Sibling smells (`over-specified-mock`, `semantic-redundancy`) are not in scope; the canonical entry notes the `semantic-redundancy` follow-up after fixing implementation coupling, but that is a *future* pass, not a finding for this audit.
