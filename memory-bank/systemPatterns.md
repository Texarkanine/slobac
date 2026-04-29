# System Patterns

## How This System Works

SLOBAC's canonical artifact is the per-smell manifesto, with `planning/VISION.md` as the product brief and `planning/research/` as the prior-art survey that justifies the positioning. Since Phase 1 shipped, the repo carries the first runtime artifact: the audit skill at `skills/slobac-audit/`. The skill bundle at `skills/slobac-audit/references/docs/` contains the **full manifesto** — principles, glossary, workflows, taxonomy entries, and site navigation. There is one document per smell; forking is structurally impossible. Manifesto-independence is enforced **structurally** — the skill bundle *is* the manifesto's home. The rendered site (properdocs) builds directly from this directory; no wrappers, no snippet indirection. Architectural judgment at this stage is still predominantly about the *shape of the documents and how they couple* — module boundaries matter only inside `skills/slobac-audit/` (ur-SKILL.md + per-smell canonical entries + report template).

A contributor who wants to modify SLOBAC safely needs to hold three load-bearing facts in mind:

**1. The three deliverables layer; later layers depend on earlier ones for correctness.**

- **Manifesto** is the opinion. The full manifesto lives at `skills/slobac-audit/references/docs/` — principles, glossary, workflows, and all 15 taxonomy entries. The reader-facing site is built directly from this directory by properdocs.
- **Audit** is a portable report of manifesto violations in a specific suite. Its recommendations are only valid if the manifesto they cite is coherent.
- **Apply** mechanically executes audit recommendations. It has almost no independent judgment; it inherits its correctness from the audit's correctness.

If a change would weaken the manifesto, it transitively weakens everything downstream. If a change would couple audit or apply to implementation details the manifesto hasn't blessed, it has broken the layering. This is the chief integrity constraint of the project.

**2. The `docs/` tree is a tightly cross-linked web. Treat renames and anchor changes as ripple events.**

- Taxonomy entries cross-link to [`principles.md`](../skills/slobac-audit/references/docs/principles.md) anchors (e.g., `#maintainable`, `#preservation-of-regression-detection-power`) and [`glossary.md`](../skills/slobac-audit/references/docs/glossary.md) anchors. Renaming an anchor breaks every citation of it.
- [`taxonomy/README.md`](../skills/slobac-audit/references/docs/taxonomy/README.md) defines the uniform entry shape (header table, summary, description, signals, false-positive guards, prescribed fix, example, related, polyglot notes). **That file is the source of truth for taxonomy file shape** — don't restate it elsewhere. Changes to the shape require updating every existing entry.
- [`workflows.md`](../skills/slobac-audit/references/docs/workflows.md) codifies the RED-GREEN-MUTATE-KILL-REFACTOR cycle that the taxonomy *assumes* when it talks about transform safety. A new taxonomy entry whose prescribed fix does not fit this workflow is suspect and needs its rationale spelled out.

Before changing any manifesto file, re-read the cross-links it receives and sends. `grep` for the anchor or filename across `skills/slobac-audit/references/docs/` and `planning/` before renaming. CI runs `properdocs build --strict` with `validation.anchors: warn` as a secondary mechanical gate — it will fail the PR build on any broken internal link or missing anchor — but CI is slower feedback than grep; grep discipline stays primary. The CI gate is guaranteed to catch drift within the manifesto tree; it does **not** catch manifesto → `planning/` links (those would need to be absolute URLs anyway) or external-URL rot.

**3. Scope exclusions are load-bearing, not decorative.**

The "what SLOBAC is not" list in [`planning/VISION.md`](../planning/VISION.md) §2 (not a SaaS, not a linter, not a mutation engine, not a test generator, not a smell-count scoreboard, not harness-specific) is explicit because the adjacent spaces are crowded with mature tooling. Any proposal that would pull SLOBAC into any of those spaces should be rejected or require an explicit, documented reversal of the exclusion. The **anti-smell-count** constraint in particular is backed by a specific research finding (EMSE 2023 *Test Smells 20 Years Later*) — it is not a style preference.

## Taxonomy entry uniformity is the primary invariant

Every canonical taxonomy entry under `skills/slobac-audit/references/docs/taxonomy/` follows the shape defined in [`taxonomy/README.md`](../skills/slobac-audit/references/docs/taxonomy/README.md). When adding or editing an entry, the invariant to preserve is that a reader can skim any two entries and know exactly where to look for signals vs false-positive guards vs fix vs example. Drift in this shape is the single most damaging thing that can happen to the manifesto's usability. Evidence: all 15 existing entries follow the pattern.

## Principles and taxonomy are bidirectionally coupled by design

Taxonomy entries cite principles (`**Protects:** [Maintainable](../principles.md#maintainable)`), and principles are only useful insofar as taxonomy entries reference them. Adding a principle that no taxonomy entry cites is a code smell in the docs; so is adding a taxonomy entry that protects no named principle. When editing either side, check the other.

## Phased-delivery order is not a free choice

[`planning/VISION.md`](../planning/VISION.md) §4 specifies `deliverable-fossils` as Phase 1 (audit MVP) and Phase 3 (apply MVP) for specific reasons: highest reader value, most syntactic detection signals, and (for apply) the safest transform class (rename-only, call graph unchanged). Proposing a different first smell requires re-arguing those tradeoffs; don't pick a first smell on aesthetic grounds.

## Skill-root self-containment (invariant #11)

An AgentSkills.io skill's runtime root is its own install directory (`~/.claude/skills/slobac-audit/`, a user-level Cursor install, a marketplace-dropped copy, etc.). Every file the skill reads at agent-runtime must be reachable via a path anchored inside that root. No `../` escapes, no assumed co-location with the source repo's layout, no harness-cwd dependency, no runtime network dependency.

Under the full-manifesto-in-bundle architecture, this invariant is satisfied **structurally**: the skill's canonical content — including the full manifesto (principles, glossary, workflows, all taxonomy entries) — lives inside the skill root by architectural construction. The skill reads `references/docs/taxonomy/<slug>.md` — a path rooted in its own `references/` tree. No generator, no copy-with-sync discipline, no procedural enforcement needed.

Relative links inside the canonical files (e.g. `[Understandable](../principles.md#understandable)`) resolve at their actual filesystem location — properdocs builds directly from the directory where these files live, so links work both at build-time and for raw-GitHub rendering.

This invariant applies to every skill SLOBAC ships, not just `slobac-audit`. When Phase-2 additions land, the same self-containment rule holds.

### Full-manifesto-in-bundle authoring model

The skill bundle at `skills/slobac-audit/references/docs/` contains the full manifesto. `properdocs.yml` `docs_dir` points directly at this directory; the rendered site is built from it with no indirection. Contributors edit files in `skills/slobac-audit/references/docs/` — that is both the skill's runtime content and the site source. The properdocs "Edit this page" link points at the actual file (not a wrapper), landing the contributor directly at the canonical content.

## Vocabulary discipline: "describe-before-edit"

The manifesto's [behavior-articulation principle](../skills/slobac-audit/references/docs/principles.md#behavior-articulation-before-change) applies to SLOBAC's own authorship: before proposing any change to a taxonomy entry or principle, state in one sentence what the entry is supposed to claim about testing. Drift in this document tends to happen when contributors preserve shape without restating intent.
