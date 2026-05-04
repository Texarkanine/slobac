# Shared State / Order Dependence

| Slug | Severity | Detection Scope | Protects |
|---|---|---|---|
| `shared-state` | Medium | per-file | [Atomic](../principles.md#atomic), [Repeatable](../principles.md#repeatable) |

## Summary

Tests leak state across one another via module-level mutables, fixture side effects retained between tests, `before(:suite)` blocks that install globals without restoration, or lazy-initialized module variables populated by the first test to run. Results depend on execution order.

## Aliases

- "shared state"
- "order dependence"
- "order-dependent"
- "leaked state"
- "module-level mutables"
- "test isolation"
- "state leaking between tests"

## Description

The semantic judgment is reachability analysis over the file's mutable bindings: trace writes and reads of each shared container across test bodies and setup hooks. A reader with the imports plus the hook blocks can build this graph quickly; a linter has to do scope-aware data flow.

Includes unused shared setup (dead `@temp_dir`, unused `let(:doc)`) — syntactically not a bug, but a signal that the author lost track of what's shared.

## Signals

- File-level `let` / `const` bound to a mutable object (`new SUT()`, `new Engine()`, `createClient()`) used by many tests without a `beforeEach` factory.
- `let css = ''` written in one `describe`, read in another, with lazy-init (`if (!css) rebuild`).
- `before(:suite)` / `beforeAll` creates a resource; individual tests mutate it.
- `sys.path.insert(0, ...)` / `NODE_PATH` mutation in `conftest` that a sibling test file *also* performs.
- Global mutable stubs (`console.warn = ...`, `Date.now = ...`) installed without restore.
- Temp directories created at suite-level and never cleaned.
- Test passes in isolation but fails under randomized ordering (`pytest-randomly`,[^pyrandomly] `jest --testSequencer=random`, `--shuffle`).

## False-positive guards

Module-level binding signals over-trigger in three classes the audit must not flag:

- **Read-only shared bindings.** Module-level constants (`const FIXTURES_DIR = ...`, `const FROZEN = Object.freeze({...})`, `FIXTURE_PATH = pathlib.Path(...)`) and `let`s bound to immutable values are not shared *state* — they're shared *data*. There is no order-coupling risk because no test can mutate them. The smell fires on mutable bindings only; immutable shared bindings are a normal optimization.
- **`beforeAll` / `before(:suite)` for genuinely expensive immutable setup.** A parsed grammar, a compiled regex, an HTTP-client connection pool, a once-loaded ML model — created once and never mutated by tests — is legitimate cross-test sharing. Per-test recreation would burn CI time with zero isolation gain. The smell fires when (a) tests mutate the suite-level resource, or (b) the setup installs *globals* (monkey-patches, env-var changes, DOM patches) without a paired restore in `afterAll` / `after(:suite)`.
- **Genuinely-unused shared setup is [`rotten-green`](./rotten-green.md), not shared-state.** A `before(:suite)` block whose product is read by no test (a `@temp_dir` created and never referenced, a `let(:doc)` bound and never used) is dead scaffolding, not state leakage. Distinguish: shared-state requires both write and read across tests with order coupling; orphan setup with zero reads belongs to a different smell entirely. Routing such cases to rotten-green is the correct disposition.

## Prescribed Fix

1. Move setup into `beforeEach` or a per-test factory; accept the small perf cost.
2. Delete genuinely unused shared setup (dead `@temp_dir`, unused `let(:doc)`).
3. Use install-and-restore patterns (`jest.spyOn(console, 'warn')` with `afterEach`) instead of permanent global mutation.
4. Consolidate duplicate `sys.path` / env-var mutations into one conftest.
5. Optional: enable order randomization in CI to prevent regression.
6. Gate: [preservation of regression-detection power](../principles.md#preservation-of-regression-detection-power) plus the file must pass shuffled runs N times.

## Example

### Before

```python
# tests/test_engine.py
engine = Engine()  # module-level

def test_adds_rule():
    engine.add('rule-a')
    assert 'rule-a' in engine.rules

def test_empty_on_init():
    assert engine.rules == []  # fails if test_adds_rule ran first
```

### After

```python
@pytest.fixture
def engine():
    return Engine()

def test_adds_rule(engine):
    engine.add('rule-a')
    assert 'rule-a' in engine.rules

def test_empty_on_init(engine):
    assert engine.rules == []
```

The module-level `engine` leaked state. Both tests now get a fresh instance via fixture. Passes under randomized ordering.

## Related modes

- [`wrong-level`](./wrong-level.md) — integration-tier tests often legitimately share expensive state; the fix is to mark the tier, not eliminate sharing.
- [`mystery-guest`](./mystery-guest.md) — shared fixtures with undocumented shapes.
- [`rotten-green`](./rotten-green.md) — dead shared setup.

## Polyglot notes

Universal. Every runner has a per-test lifecycle hook (`beforeEach`, `@BeforeEach`, `Setup`, fixture). Detection of reachability is a per-language AST walk; the fix recipe is language-agnostic.

[^pyrandomly]: `pytest-randomly` — randomizes test order per session; failures under randomization are reproducible via the printed seed. <https://github.com/pytest-dev/pytest-randomly>.
