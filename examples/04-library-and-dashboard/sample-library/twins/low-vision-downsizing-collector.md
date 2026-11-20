---
id: low-vision-downsizing-collector
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [large-text, printable-record, shared-access]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Walt, the Low-Vision Legacy Collector"
archetype: "Older collector with decades of discs and records who needs large text, a simple list, and a record someone else can use"
evidence_strength: moderate
evidence_count: 7
communities: ["CLZ support club", "CLZ release notes", "Sound & Vision magazine", "AVNirvana forum", "Criterion Forum", "Naim Audio community", "DVD Talk forum"]
tech_comfort: low
primary_device: older Windows desktop or tablet, scaled up (browser zoom or OS display scaling)
accessibility_context: "low vision / small-text difficulty, supported by 2 sources (one older poster, one DPI-scaling release note); the rest of his profile is inferred, not stated"
goals:
  - Read and edit every screen without squinting, including edit dialogs
  - Keep a plain, printable list of what he owns, with condition and approximate value, for downsizing, insurance or heirs
  - Have a family member help enter titles
  - Decide what to cull and what to keep
pain_points:
  - Font size controls miss some screens (e.g., the edit card), and layouts break when OS scaling is raised
  - Entering thousands of titles is too much work
  - Apps change business model (subscription) without warning
  - Barcode scanning needs a camera or extra hardware he may not have
vocabulary: ["list", "inventory", "insurance", "print", "sort", "collection", "LaserDisc", "LP", "DVD"]
tasks:
  - "Increase text size and enter a new title using the edit form at 200% zoom"
  - "Print or export an inventory for insurance or heirs"
  - "Mark which discs to sell/donate and see the remainder"
  - "Let a family member add titles from a shared list"
---

## Who they are
A long-time collector who may be moving, downsizing, or planning for the collection's future. Owns multiple formats (LPs, DVDs, LaserDiscs). Moderately wary of subscriptions and cloud tools.

## What they want and why
Evidence shows an older user losing readability in an edit card after moving to a new PC, DPI scaling issues in a major cataloging app, a collector logging everything before a costly move, and a household using a spreadsheet with a relative reading titles aloud. The pattern: plain, legible, exportable lists that other people can use.

## How they approach software
Patient but easily lost by dense screens. Falls back to a spreadsheet when the app is hard to read. Trusts printouts. Will not read long onboarding.

## Language they use
"List", "inventory", "print". Avoids tech jargon like "sync", "database" or "cloud".

## Evidence
- [CLZ support club, undated] An elderly user could not enlarge text in the add/edit card; staff suggested DPI scaling or the browser version -> supports: goal 1, pain point 1 (E14)
- [CLZ release notes, 2018] Large-text and 125/150% scaling broke layouts and blurred text until fixed -> supports: pain point 1 (E15)
- [Sound & Vision, approx. 2020] Reviewer culling about 2,000 discs and 1,000 LPs before a move logged what remained; cost, findability and selling the house drove it -> supports: goals 2, 4 (E25)
- [AVNirvana forum, undated] Household used a spreadsheet with a family member reading titles; manual entry felt like too much work; subscriptions confusing -> supports: goal 3, pain points 2-3 (E01)
- [Criterion Forum, older] Insurance-style photo records of storage bins; print/export reports -> supports: goal 2 (E09)
- [Naim Audio community, undated] Grade condition as you add so it saves time if you sell or someone else handles the collection -> supports: goal 2 (E20)
- [DVD Talk forum, older] Entering 10,000+ titles by hand felt impractical -> supports: pain point 2 (E02)

## Assumptions (thin spots)
Low-vision need is directly evidenced only in a single support post and a scaling release note. Low tech comfort, tablet use and age-related planning are inferred from those plus the downsizing article, not stated by posters. Treat this twin as a hypothesis about accessibility and legacy needs, not a measured segment.

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
