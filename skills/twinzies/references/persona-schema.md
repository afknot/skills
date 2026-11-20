# Twin schema

Each twin is one markdown file: `twins/<domain-slug>/<twin-slug>.md`. YAML frontmatter holds the structured fields (the report builder reads it); the body holds the narrative.

```markdown
---
id: sealed-shelf-curator               # stable kebab-case id; never changes
name: "Dana, the Shelf Curator"        # invented first name + archetype; never a real poster
version: 0.1                           # patch: wording/evidence; minor: goals or pain points; major: archetype
kind: user                             # user (default) | misuse (see misuse-twins.md)
intent:                                # misuse twins only: unintentional | opportunistic | malicious
status: hypothesis                     # hypothesis | corroborated | validated | retired (see library.md)
forked_from:                           # id of the parent twin if this is an adapted variant, else empty
domains: [physical-media, collecting]  # topics where the twin has been used or built
needs: [bulk-entry, duplicate-check, edition-detail, offline]   # reusable need tags used for matching across products
products_tested: []                    # products evaluated with this twin
last_validated:                        # date of last real-user validation, empty if never
evidence_newest: 2026-11               # month of the newest evidence, to flag staleness
archetype: "Completionist who values condition and edition details"
evidence_strength: strong               # strong (5+ sources, multiple communities) | moderate (3-4) | thin (<3)
evidence_count: 7
communities: ["r/Fuckthisdisc-style forums (paraphrase only)", "collector forums"]
tech_comfort: high                      # low | medium | high
primary_device: desktop + phone in stores
accessibility_context: none stated      # or e.g. "low vision, uses browser zoom to 200%"
goals:
  - Know exactly which editions and variants they own
  - Avoid buying duplicates while out shopping
pain_points:
  - Spreadsheets break when the collection passes a few hundred items
  - Existing apps get edition/variant data wrong
vocabulary: ["sealed", "variant", "steelbook", "region", "backlog"]
tasks:
  - "Add 40 discs from a thrift haul, fixing wrong edition matches"
  - "Check in a store whether a title is already owned"
---

## Who they are
2-4 sentences of narrative, in aggregate. No identifying details from any one poster.

## What they want and why
Behavior and motivation, tied to the evidence.

## How they approach software
Patience, willingness to read docs, what makes them quit, what earns trust.

## Language they use
How they describe the domain in their own words, and terms they'd misread.

## Evidence
- [community, approx. date] one-line paraphrase of the point -> supports: <goal/pain point/vocabulary>
- ...
```

## Rules of thumb
- 4-12 twins; default 6. Prefer fewer well-supported twins over many thin ones.
- Each twin cites at least 3 distinct evidence items. If it can't, set `evidence_strength: thin` and say what is assumed.
- Name twins with an invented first name and an archetype. Never reuse a real poster's handle or story.
- `accessibility_context` is only filled from evidence or an explicit user request. If a twin is added to cover an accessibility gap without evidence, label it `assumed` in the field and in the report.
- Keep `tasks` realistic for the product being tested. They can be updated per evaluation run without rebuilding the twin.

Add two sections at the end of each twin file, which the improvement loop maintains:

```markdown
## Validation log
- 2026-12-02, moderated think-aloud (3 participants matched): predicted "won't find Export" -> confirmed 3/3; surprise: expects export in the item list, not settings

## Changelog
- 0.2 (2026-12-02): added "expects export from the list view" to goals; status hypothesis -> validated for the export trait. Cause: study products/shelf/validation-2026-12-02.md
```

## Library files
Twins live in `twinzies-library/` (layout and rules in `library.md`): `twins/<id>.md`, a `registry.md` table of every twin, `evidence/<domain>.md` logs, `products/<product>/` studies and a `changelog.md`.
- `registry.md`: one row per twin (id, name, status, version, domains, needs, last validated, products tested).
- `evidence/<domain>.md`: every collected item with source URL (or "first-party" and the channel), community, rough date, a paraphrased point, and which twin(s) it supports. This is what lets the user audit the twins. The source list should call out what was unreachable (login-gated, blocked).
