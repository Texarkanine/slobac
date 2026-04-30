# SLOBAC audit report template

The audit skill emits its report as markdown in this shape. Fill every angle-bracketed placeholder. Do not reorder top-level sections, do not add new top-level sections, do not skip the `Why this isn't a false positive` field on any finding — it is the reader's guard against trusting a finding blindly.

The shape is deliberately regular so a future JSON extraction is mechanical. That future is not Phase 1's problem; stability of the shape today is.

## Default emission path

Write to `./slobac-audit.md` in the operator's current working directory. If the operator names a different path in their invocation, use that path. If a file already exists at the chosen path, append a `-2`, `-3`, … suffix to avoid clobbering prior reports — do not overwrite.

## Template

~~~markdown
# SLOBAC audit report

- **Scope invoked:** <comma-separated smell slugs the operator requested, or `all` if unscoped>
- **Target suite root:** <path to the audited directory, as given to the skill>
- **Audit date:** <ISO-8601 date, e.g. 2026-04-23>

## Summary

<One paragraph. Total finding count, broken down per smell. Any in-scope smell
with zero findings gets an explicit "No findings for scope <slug>" line — the
audit does not silently skip a requested smell.>

## Findings

### <N>. `<test location — file path + test identifier>` — <smell slug>

- **Location:** <file relative to target suite root> → <test identifier: function name, or class.method>
- **Smell:** `<slug>`
- **Rationale:** <One or two sentences. State what the title/grouping claims vs. what the body actually verifies. Cite the specific signal from references/docs/taxonomy/<slug>.md (the skill's canonical smell definition) that matched. Include a link to the published manifesto URL (https://texarkanine.github.io/slobac/taxonomy/<slug>/) so the reader can audit the auditor.>
- **Prescribed remediation:** <Concrete next action. For naming-lies, name the fix arm explicitly (rename / strengthen / investigate). For deliverable-fossils, name the phase (rename-only, or rename + regroup). Encode the *behavior* in any rename suggestion, not the fossil label.>
- **Why this isn't a false positive:** <One sentence. The guard against the specific over-trigger this finding could be mistaken for. If no principled guard applies, the finding itself is suspect — reconsider before emitting.>

<Repeat the finding block for every flagged test. If a test exhibits more than
one in-scope smell, emit one finding block per smell — do not collapse. Each
finding has its own remediation because each smell prescribes a different fix.>

## Tests considered but not flagged

<Always include this section. If the audit examined tests that looked
smell-adjacent but were verified clean on closer reading, record one line per
test: test location + one-sentence reason the audit decided not to flag. If no
tests were considered and cleared, write `None.` This section is how the audit
shows its work; it is how a future reviewer can disagree with the auditor
without re-running it.>

## Out-of-scope requests

<Always include this section. If the operator named a smell slug the audit
does not support (anything other than `deliverable-fossils`, `naming-lies`,
`shared-state`, `monolithic-test-file`, `semantic-redundancy`, or
`wrong-level`), name it here and state explicitly that it was not audited. Do
not silently drop it; do not audit it anyway. If no out-of-scope slugs were
requested, write `None.`>
~~~

## Field-level contracts

- **Every finding carries all five fields** (location, smell, rationale, remediation, false-positive guard). A finding missing any field is structurally invalid — do not emit.
- **Rationale cites a specific signal** from the canonical docs entry, not a generic "this looks like a fossil." A reader must be able to walk from the finding to the signal to the principle.
- **Remediation encodes the product behavior**, not the fossil label. A rename recommendation that recycles the ticket ID is not a remediation; it's a relabel.
- **False-positive guard is the reader's audit lever.** If the audit cannot articulate why the finding isn't the common over-trigger for that smell, the finding is weak — reconsider.

## Shape stability

The top-level sections (`Summary`, `Findings`, `Tests considered but not flagged`, `Out-of-scope requests`) and the per-finding field names (`Location`, `Smell`, `Rationale`, `Prescribed remediation`, `Why this isn't a false positive`) are the shape contract. Phrasing is free. Adding new top-level sections, renaming field labels, or omitting a section is a shape break — downstream consumers (today: human readers; Phase 3+: the apply layer) rely on this shape.
