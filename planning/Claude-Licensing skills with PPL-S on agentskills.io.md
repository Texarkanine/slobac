# Licensing skills with PPL-S on agentskills.io

**Created:** 5/4/2026 15:01:37  
**Updated:** 5/4/2026 15:05:18  
**Exported:** 5/4/2026 15:38:41  
**Link:** [https://claude.ai/chat/b8d5aa2c-a404-4f3b-9ed0-094db76a16c9](https://claude.ai/chat/b8d5aa2c-a404-4f3b-9ed0-094db76a16c9)  

## Prompt:
5/4/2026, 3:01:37 PM

how do you include license info in agentskills.io, examples?

I have skills licensed under PPL-S, which is https://shipfail.github.io/public-prompt-license/ extending the AGPL.

in my yaml front matter, what do I put?


```

license: PPL-S
```

well there're a few ppl-s out there, and mine isn't first.


```
license: Public Prompt License (Service Variant) - PPL-S
```

still doesn't google


```
license: ./PPL-S.txt
```

and then I bundle the ppl in my skill? but ppl extends agpl; do I also need to bundle agpl? Can i put them both in `LICENSE` or just put the ppl in  there or what? why? hwat have others done?



## Response:
5/4/2026, 3:03:21 PM



````plaintext
Thought process: Clarifying license field specifications and bundling practices.

I need to look into how agentskills.io handles license metadata and what the PPL-S license format should look like in their system.
````

````plaintext
Web Search: agentskills.io skill yaml frontmatter license field
````

> **Specification - Agent Skills** [agentskills.io](https://agentskills.io/specification)
>
> **Skill validation requires 'license' in SKILL.md frontmatter (spec says optional) · Issue #894 · github/copilot-cli** [github.com](https://github.com/github/copilot-cli/issues/894)
>
> **Use Agent Skills in VS Code** [visualstudio.com](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
>
> **agentskills/docs/specification.mdx at main · agentskills/agentskills** [github.com](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx)
>
> **Building Agent Skills from Scratch - DEV Community** [dev.to](https://dev.to/onlyoneaman/building-agent-skills-from-scratch-lbl)
>
> **Agentskills** [agentskills.io](https://agentskills.io/specification.md)
>
> **Agent Skills | Microsoft Learn** [microsoft.com](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
>
> **Agent Skills | OpenCode** [opencode.ai](https://opencode.ai/docs/skills/)
>
> **Agent Skills - Claude API Docs** [claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
>
> **SKILL.md Specification | agentskills/agentskills | DeepWiki** [deepwiki.com](https://deepwiki.com/agentskills/agentskills/2.2-skill.md-specification)
>
````plaintext
Thought process

Looking at the spec, the license field is just a free-form string where I can either put the license name directly or reference a bundled file like `LICENSE.txt`. Now I'm checking how others handle custom or non-SPDX licenses, particularly around AGPL with extensions.

I need to understand two things: how GPL-extending licenses typically bundle their upstream license (since AGPL-based licenses usually include both the original and extended terms), and what conventions exist for non-SPDX licenses like the `LicenseRef-` format that SPDX uses for custom licenses.
````

````plaintext
Web Search: SPDX LicenseRef custom license identifier convention
````

> **SPDX License List | Software Package Data Exchange (SPDX)** [spdx.org](https://spdx.org/licenses/)
>
> **Annex E: Using SPDX short identifiers in Source Files - SPDX Specification 2.3.0** [github.io](https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/)
>
> **Annex D: SPDX License Expressions - SPDX Specification 2.3.0** [github.io](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/)
>
> **B. SPDX license expressions - SPDX Specification 3.0.1** [github.io](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/)
>
> **Handling License Info – SPDX** [spdx.dev](https://spdx.dev/learn/handling-license-info/)
>
> **GitHub - david-a-wheeler/spdx-tutorial: A brief tutorial on how to use Software Package Data Exchange (SPDX) · GitHub** [github.com](https://github.com/david-a-wheeler/spdx-tutorial)
>
> **Frequently Asked Questions | REUSE** [reuse.software](https://reuse.software/faq/)
>
> **Annex E: Using SPDX short identifiers in Source Files - specification v2.2.2** [github.io](https://spdx.github.io/spdx-spec/v2.2.2/using-SPDX-short-identifiers-in-source-files/)
>
> **Using SPDX License List short identifiers in source files - Using SPDX** [github.io](https://spdx.github.io/using/license-id-in-source/)
>
````plaintext
Thought process: Investigated SPDX conventions and license bundling requirements for extended GPL derivatives.

Now I'm checking how AGPL interacts with extended licenses—specifically whether the GPL/AGPL family requires underlying license text to be included when additional terms are layered on top. I should also review the PPL-S directly to see what it specifies about bundling AGPL.
````

Let me peek at the actual PPL-S text to see what *it* says about bundling, and at how AGPL-derived licenses typically handle the upstream text.

````plaintext
Web Fetch: Fetched: Public Prompt License (PPL) - Open Source for the AI Era
````

````plaintext
Thought process: Verifying PPL-S wrapper status around AGPL license.

Looking at the official documentation, PPL-S is a wrapper around AGPL, so I need to verify whether the license text requires bundling the underlying AGPL license separately or if copying the PPL-S variant into a LICENSE file is sufficient.
````

````plaintext
Web Fetch: Fetched: https://shipfail.github.io/public-prompt-license/LICENSES/PPL-S-0.2.txt
````

````plaintext
Thought process: Navigated SPDX conventions and license bundling requirements.

The PPL-S license is actually quite minimal — it just references AGPL-3.0 by linking to gnu.org rather than including the full text inline, and it only adds a definition extending what counts as "Source Code." So the bundling question really hinges on whether that external reference to AGPL satisfies the distribution requirements, or if the actual AGPL text needs to be included separately.

Looking at what PPL itself recommends, they just say to copy your chosen variant into a `LICENSE` file at the repo root — no explicit instruction to also bundle AGPL. But AGPL-3.0 § 4 is pretty clear that you need to convey the license text along with the work, so if PPL-S incorporates AGPL by reference, you're technically obligated to include it.

I'm weighing two practical approaches: either go full REUSE-compliance with a `LICENSES/` directory containing both the PPL-S and AGPL-3.0 texts plus a top-level `LICENSE` file explaining the relationship, or just bundle PPL-S and rely on the reference being sufficient.

Given that the user is already REUSE-aware and defaults to AGPL, they'd probably prefer the more rigorous approach. For the frontmatter `license:` field, the spec is flexible — it's just a free-form string and doesn't require SPDX, though some tools might try to parse it that way. I should give them a clear, unambiguous format that references the bundled file and clarifies which PPL-S version they're using.

The `LicenseRef-` prefix is the right move here because it signals to any SPDX-aware tooling that this is a custom license reference, not something to match against the standard list. I initially considered using SPDX's `WITH` syntax to express the relationship between PPL-S and AGPL, but that only works for exceptions, and PPL-S is really a scope extension rather than an exception, so that doesn't fit the model. The cleanest solution is just the `LicenseRef-` identifier pointing to the full license file.

For actually bundling these licenses, the REUSE standard approach with a dedicated `LICENSES/` directory containing both the PPL-S text and the AGPL text is the gold standard. A single `LICENSE` file works too if you concatenate them or just include PPL-S with a link to AGPL elsewhere, though AGPL's terms technically require conveying the full AGPL text. I should write this up in a way that respects the user's preference for efficiency and their familiarity with REUSE practices. I should address the user's specific questions in order: what to put in the `license:` field, how to handle the disambiguation issue, whether bundling AGPL with PPL-S makes sense, the file structure question, and what precedent exists. Let me work through a concrete answer that hits each of these points.

For the `license:` field itself, I can use a freeform string following the agentskills.io spec — the documentation even shows an example like `license: Proprietary. LICENSE.txt has complete terms`. The key insight is using SPDX's `LicenseRef-` convention as a standard way to reference custom licenses that aren't on the official SPDX list. This signals to any parser (including tools like GitHub Copilot CLI that increasingly check this field) that there's a bundled license file to consult, and it keeps the reference googleable and namespace-stable so it won't collide with other custom licenses.

I need to be careful with the syntax though — `WITH` is specifically for license exceptions (carve-outs), not scope extensions like PPL-S, so I shouldn't use that operator. And yes, I'll need to bundle the actual AGPL-3.0 text since PPL-S incorporates it by reference and only adds about 12 lines extending the definition of "Source Code" to cover prompts.

For the file structure, I'm thinking REUSE-style organization with a LICENSES directory containing both the PPL-S wrapper and the full AGPL-3.0 text, then a simple one-line LICENSE file at the root pointing to them.

If REUSE feels like overkill for a single skill, concatenating both licenses into one file with clear headers explaining how they relate works just as well—REUSE has better tooling support but the simpler approach wins on readability.

The agentskills space hasn't really settled on conventions for non-standard licenses yet, so I'm drawing on broader FLOSS precedent with REUSE as the most established pattern for handling composite licenses.

Now I'm evaluating the tone and density of the license name itself—checking whether "Patroclus' Prompt License" lands as clever wordplay or too obscure, and considering what other references or snark might strengthen the voice without overdoing it. I'm verifying all the links I included are actually live and accessible, and they check out. Now I'm double-checking that AGPL § 4 reference — that section covers conveying verbatim copies and requires distributing the license alongside the program, which matches what I claimed.

I'm reconsidering whether I'm being too strict about bundling the AGPL text with PPL-S. Since PPL-S incorporates AGPL by reference and effectively extends it, the legally safe answer is definitely yes — bundling is the right call, even if the PPL website's guidance is minimal. I should also point out that the spec itself actually validates this approach with its example showing `license: Proprietary. LICENSE.txt has complete terms`, which directly supports the pattern of naming the license and referencing a separate file.

There's a real concern the user raised about competing PPL-S implementations already existing, but I'll take their word for it rather than dig into that rabbit hole. Now I need to make sure my response is tight and direct — no wasted words or unnecessary hedging — with a clean structure of short sections that matches what they're asking for.
````

The `license:` field in agentskills.io is just a freeform string — the [spec](https://agentskills.io/specification.md) recommends "either the name of a license or the name of a bundled license file" and offers `license: Proprietary. LICENSE.txt has complete terms` as the canonical example. So you've got the right shape; the question is what string to use and what to ship.

**Frontmatter:** use SPDX's [`LicenseRef-` convention](https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/) — that's the standard escape hatch for licenses not on the SPDX list. It tells anything doing SPDX parsing "custom license, look at the bundled text" instead of failing a list-match (and an increasing number of skill consumers actually parse this — GitHub Copilot CLI [demands](https://github.com/github/copilot-cli/issues/894) a `license:` field even though the spec says it's optional):

```yaml
license: LicenseRef-PPL-S-0.2 (extends AGPL-3.0-only). See LICENSE.
```

Googleable, namespace-stable, disambiguates from any rival Patroclus' Prompt License that wants to call itself PPL-S next Tuesday. Don't be tempted to write `AGPL-3.0-only WITH LicenseRef-PPL-S-extension` — `WITH` is reserved for actual exceptions (carve-*outs*), and PPL-S is a scope *extension* (carve-*in*). Wrong operator, the SPDX validators will complain, and it lies about the relationship anyway.

**On bundling AGPL:** yes, ship it. The actual [PPL-S text](https://shipfail.github.io/public-prompt-license/LICENSES/PPL-S-0.2.txt) is only ~12 lines — it incorporates AGPL-3.0 by reference and extends "Source Code" to cover Prompt Source. AGPL-3.0 § 4 still requires you to "give all recipients a copy of this License along with the Program," and you can't satisfy that with a hyperlink to gnu.org because link rot is real and the FSF doesn't owe you uptime. The PPL site's "just copy PPL into LICENSE" instruction is technically incomplete for the -S variant for exactly this reason.

**Layout** — go [REUSE-style](https://reuse.software/faq/), since you already lean that way:

```
your-skill/
├── SKILL.md
└── LICENSES/
    ├── LicenseRef-PPL-S-0.2.txt    # the wrapper
    └── AGPL-3.0-only.txt            # the floor it stands on
```

Top-level `LICENSE` becomes a one-liner pointing at `LICENSES/`, or you skip it entirely (REUSE doesn't require a top-level file). If you find REUSE overkill for a single skill, just concatenate both texts into one `LICENSE` with a separator and a header explaining the relationship. Both are valid; REUSE wins on tooling support (linters, SBOM generators, GitHub's license detector — which will probably show your repo as "Other" either way until PPL hits the SPDX list, but at least the file structure is machine-legible) and loses on aesthetic minimalism.

**Prior art** — the agentskills ecosystem is too young to have a convention for nonstandard licenses. Published skills are overwhelmingly MIT/Apache with `license: MIT`. The REUSE pattern is the dominant prior art from broader FLOSS, and AGPL-extender precedent (Commons Clause, SSPL, the various BSL-flavored stacks) has historically shipped the upstream AGPL text alongside the modification. No perfect peer here — you're drafting the convention. Worse fates exist.



## Prompt:
5/4/2026, 3:03:59 PM

> File: 

```

```

i use resue; here's my reuse.toml: 


```

~/git/slobac (counterexamples) $ cat REUSE.toml
version = 1
SPDX-PackageName = "slobac"
SPDX-PackageSupplier = "Texarkanine <texarkanine@protonmail.com>"

# Default: application code and docs under AGPL-3.0-or-later
[[annotations]]
path = ["**/*"]
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "AGPL-3.0-or-later"

# Prompt-shaped AgentSkills content (repo skills/, the deliverables); SKILL.md etc.
[[annotations]]
path = ["skills/**"]
precedence = "override"
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "LicenseRef-PPL-S"

# Manifesto / docs site source (ProperDocs), not prompt-shaped skill payload
[[annotations]]
path = ["skills/slobac-audit/references/docs/**"]
precedence = "override"
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "CC-BY-SA-4.0"

# Agent customizations local to this repo: rules, skills, slash commands
[[annotations]]
path = [
    ".cursor/rules/**",
    ".cursor/skills/**",
    ".cursor/commands/**",
]
precedence = "override"
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "LicenseRef-PPL-S"

# Paths under **/shared/** are vendored from upstream
# with unknown or mixed licensing. No license claims are made for those files here.
[[annotations]]
path = [".cursor/**/shared/**"]
precedence = "override"
SPDX-FileCopyrightText = "NOASSERTION"
SPDX-License-Identifier = "LicenseRef-NOASSERTION"

```

it's "redundant" but when the skills distribute via cursor and claude code marketplaces, users don't get my main repo - jsut teh skill, so I need the license info to be contained, as well.



## Response:
5/4/2026, 3:05:18 PM



````plaintext
Thought process: Architected per-skill REUSE compliance for marketplace distribution.

I see the core issue now — they're using REUSE for compliance at the repo level, but individual skills need to be self-contained with their own license information since they get distributed separately through marketplaces without the parent repository structure. The REUSE standard assumes the entire repo is delivered together, so their current setup breaks down when skills are extracted and shared independently. redistributed standalone. The skill folder is the distribution unit.

Looking at their `slobac-audit/` skill:
`​`​`
skills/slobac-audit/
├── AGPL-3.0-or-later.txt
├── PPL-S.txt
├── README.md
├── SKILL.md
└── references/
`​`​`

But their other skills (slobac-batch, slobac-cross-suite, slobac-scout) don't have license files. That's an inconsistency.

What's the right answer? The skill needs to be self-contained as a distribution unit. So the skill subfolder should have:
1. License text(s) bundled in
2. Frontmatter `license:` field that points to those files
3. Ideally REUSE-compliant *within* the skill folder too, so that someone who extracts just the skill still has REUSE-valid metadata

For proper REUSE compliance at the skill level, I should organize licenses in a `LICENSES/` subdirectory with SPDX identifiers in file headers, then add a local `REUSE.toml` scoped to that skill. The `license:` field in SKILL.md frontmatter could reference the licenses with a note pointing to the LICENSES directory, and for any documentation subdirectories with different licenses like CC-BY-SA-4.0, those would need their own declarations. The license files need to move into a `LICENSES/` directory to be REUSE-compliant, and if the slobac-audit skill bundles those documentation files, it'll need the CC-BY-SA-4.0 license text included too. The frontmatter `license:` field could theoretically express the multi-licensing situation, but that risks conflating different licensing scopes and requirements.

Since skills distribute as standalone units through marketplaces rather than with the full repository, the frontmatter should declare the skill's primary license (PPL-S) as the user-facing summary, letting REUSE.toml handle the granular per-file accuracy underneath. I'd keep it simple with just the primary license in the frontmatter and note where to find the full details, then handle any mixed licensing like the CC-BY-SA content separately in the configuration.

The user clearly knows what they're doing with REUSE compliance and AGPL defaults, so they'll appreciate the per-skill REUSE.toml approach. I should also flag that their current `slobac-audit/` folder has license files scattered outside the standard `LICENSES/` directory — moving those into `LICENSES/` and adding a local `REUSE.toml` would make it fully compliant.

The other skills don't have license files yet, which is a problem for distribution. The real insight here is that REUSE was built for shipping entire repos, but when you're distributing individual skill folders, each one needs to be its own REUSE-compliant unit. The fix is straightforward: move license texts into a `LICENSES/` subdirectory within each skill and give each skill its own REUSE configuration file.

Setting up the configuration... I see the current rewritten thinking contains what looks like corrupted output with email addresses and TOML configuration. Let me rewrite both chunks naturally:

The marketplace tarball needs to be self-contained with its own license declarations, even if it duplicates the repo root — that's intentional, following the same pattern Linux distros use when packaging individual components. The frontmatter should declare the headline license cleanly, letting REUSE handle the per-file details underneath. For slobac-audit specifically, since the docs are CC-BY-SA-4.0, I could either keep the frontmatter simple with PPL-S as primary and let REUSE reveal the full picture, or be explicit about both licenses — I think the simpler approach works better here.

The frontmatter is really just a label for quick consumption; downstream users want a straightforward answer without parsing SPDX expressions, and the actual source of truth lives in the LICENSES directory and REUSE configuration. The agentskills.io spec actually encourages this exact pattern — headline plus detailed bundle. I should move the license files into the proper LICENSES subdirectory and rename them to match REUSE's identifier format.

For the other skills without license files, I need to apply the same LICENSES plus REUSE.toml structure so they're properly attributed when distributed independently. To avoid maintaining duplicate license texts across four different skill directories, I should set up a build script that syncs the canonical license files into each skill's LICENSES folder — it's extra overhead, but it's the cost of having truly self-contained distributable units instead of relying on a monorepo structure. Each package gets its own REUSE.toml at its root, and when a skill is distributed as a standalone tarball, that local file becomes authoritative for that unit—the repo-level one only matters in the repository itself. This works because REUSE tooling resolves files relative to where it's invoked, so nested configurations naturally scope to their distribution units. I should verify that skill marketplaces actually unpack to self-contained directories, but I'm pretty confident they do.

Now I'm structuring the response into 4-5 tight technical sections with one code block each, matching the tone from before—substantive paragraphs rather than bullet points. I need to make sure I link to the REUSE spec for the LICENSES/ folder requirement and any other non-obvious claims, since the user values rigor.

Actually, I notice the user already has `LicenseRef-PPL-S.txt` in their LICENSES/ directory, so they understand the REUSE convention well. I should reference their existing naming pattern when discussing how to apply it per-skill rather than explaining the basics. They also thoughtfully included `LicenseRef-NOASSERTION.txt` for vendored content, which shows they're already solid on REUSE practices—I just need to help them extend that pattern to the per-skill structure.
````

Right — the marketplace-as-distribution-unit problem is the actually interesting wrinkle. REUSE was designed for "ship the whole repo," and when your unit of distribution is a subfolder, you need REUSE-within-the-unit. Two moves get you there:

**1. Each distributed skill becomes its own REUSE-compliant package.**

Move the license texts out of the skill root into a `LICENSES/` subdir (REUSE [requires](https://reuse.software/spec-3.3/#licenses-folder) that exact name and location — your repo-root one is correct, but `slobac-audit/AGPL-3.0-or-later.txt` and `slobac-audit/PPL-S.txt` sitting at the skill root are non-compliant from a REUSE-tooling standpoint). Then give each skill its own scoped `REUSE.toml`:

```
skills/slobac-audit/
├── SKILL.md
├── README.md
├── LICENSES/
│   ├── LicenseRef-PPL-S.txt
│   ├── AGPL-3.0-or-later.txt
│   └── CC-BY-SA-4.0.txt          # only if docs ship with this skill
├── REUSE.toml                    # local, scoped to this distribution unit
└── references/
```

The local `REUSE.toml` is a trimmed mirror of the repo-root one, paths rewritten relative to the skill:

```toml
version = 1
SPDX-PackageName = "slobac-audit"
SPDX-PackageSupplier = "Texarkanine <texarkanine@protonmail.com>"

[[annotations]]
path = ["**/*"]
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "LicenseRef-PPL-S"

[[annotations]]
path = ["references/docs/**"]
precedence = "override"
SPDX-FileCopyrightText = "Texarkanine"
SPDX-License-Identifier = "CC-BY-SA-4.0"
```

Yes, it's redundant with the repo root. That's by design: in the repo, the root `REUSE.toml` is authoritative; in the marketplace tarball, the skill's own `REUSE.toml` is authoritative. They describe different distribution units, both correctly. Same pattern Linux distros use when they vendor license texts into individual packages — every `.deb` carries its own `/usr/share/doc/<pkg>/copyright` even though the source repo has one master file.

**2. Frontmatter declares the headline; REUSE handles the per-file truth.**

```yaml
license: LicenseRef-PPL-S (extends AGPL-3.0-or-later). See LICENSES/.
```

For `slobac-audit` specifically, since `references/docs/**` is CC-BY-SA-4.0, you've got a choice: keep the frontmatter clean (PPL-S as the headline, REUSE tells the full story) or be explicit:

```yaml
license: LicenseRef-PPL-S AND CC-BY-SA-4.0 (extends AGPL-3.0-or-later). See LICENSES/ and REUSE.toml.
```

I'd take the first. Frontmatter `license:` is a label, not an SPDX expression engine; downstream consumers want a fast "what is this" answer, and the `LICENSES/` + `REUSE.toml` pair is the source of truth. The spec's own example (`license: Proprietary. LICENSE.txt has complete terms`) blesses the headline-plus-see-bundle pattern explicitly.

**Cleanup checklist for what you've got:**

- `slobac-audit/{AGPL-3.0-or-later,PPL-S}.txt` → move into `slobac-audit/LICENSES/`, rename `PPL-S.txt` → `LicenseRef-PPL-S.txt` to match the REUSE identifier-as-filename convention you're already using at the repo root.
- `slobac-batch`, `slobac-cross-suite`, `slobac-scout` — currently un-licensed in-skill, so any marketplace install of those is shipping prompt content with no attribution. Same `LICENSES/` + `REUSE.toml` treatment.
- Add a pre-publish step (Makefile target, pre-commit hook, whatever fits your taste) that syncs the canonical license texts from `/LICENSES/` into each `skills/*/LICENSES/`. Otherwise the four copies of `LicenseRef-PPL-S.txt` will inevitably drift the day PPL bumps to 0.3 and you remember to update three of them.

The license-syncing-script tax is real but it's the price of ditching "monorepo with one `LICENSES/`" for "self-contained distributable units." Welcome to the npm/cargo school of license bookkeeping, where every package re-ships its dependencies' license texts and we all just sort of nod and accept it.





---
Powered by [Claude Exporter](https://www.ai-chat-exporter.net)