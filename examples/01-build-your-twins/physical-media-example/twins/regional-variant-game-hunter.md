---
id: regional-variant-game-hunter
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [region-variant, completeness, want-list]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Kenji, the Regional-Variant Game Hunter"
archetype: "Retro and import game collector who tracks region, completeness and variants, and has mixed feelings about price tracking"
evidence_strength: strong
evidence_count: 6
communities: ["InsertCredit forum", "NeoGAF", "Giant Bomb forums", "Collectors Edition forums", "LaunchBox feedback board", "Nintendo Life forums"]
tech_comfort: high
primary_device: phone (scanning at shops, conventions), desktop for the real database
accessibility_context: none stated
goals:
  - Record region (NTSC-U, NTSC-J, PAL), product code, language and variant for each game
  - Track completeness (loose, boxed, complete, sealed) and where/how each copy is owned
  - Add a game once and record several platform versions
  - Keep a wanted list and avoid duplicate buys across physical and digital libraries
pain_points:
  - Price tools value games by US rarity, distorting UK and Japanese copies
  - Trackers lack tools for large physical collections (how/where owned)
  - Fixed databases cannot hold obscure or import titles; free-form naming is prized
  - No structured fields for game codes, so people stash them in filenames or spreadsheets
  - Value tracking causes anxiety and reluctance to open sealed games for some
  - Backlog-style apps that nag feel like chores
vocabulary: ["CIB", "loose", "sealed", "NTSC-J", "PAL", "variant", "backlog", "import", "reprint", "Greatest Hits"]
tasks:
  - "Add an import game that is not in the database"
  - "Record a boxed copy with missing manual, and a second copy sealed"
  - "See all Japanese releases I own for one platform"
  - "Check in a shop if I already own the PAL version"
---

## Who they are
A collector for whom region and packaging are the point. Keeps physical games alongside Steam/Switch libraries and does not want to mix the two up.

## What they want and why
Variant-level truth: product codes, region, languages, cover finishes, double-packs. Wants value only if it is regionally correct, and a minority want no value at all. Wants to log "how I own it", not just "have/want".

## How they approach software
Tolerates rough UI if data is flexible; will use a spreadsheet or a free-form tracker rather than a rigid database. Responds to developers who listen. Distrusts gamified nagging.

## Language they use
"CIB", "loose", "sealed", "variant", "import", "backlog". Might read "edition" and "platform" in ways that conflict with how databases use them (a game released on several platforms).

## Evidence
- [InsertCredit forum, approx. 2024] Valuations use US rarity so UK/JP copies are mispriced; Backloggd lacks physical-management; wants add-once multi-platform and "how owned" tracking -> supports: goals 2-3, pain points 1-3 (E12)
- [NeoGAF, approx. 2025] Duplicate buys across stores; ownership type tracking (physical/digital/subscription); nagging backlog apps feel like chores; wants durable categories -> supports: goal 4, pain point 6 (E13)
- [Giant Bomb forums, older] Grouvee shelves, Backloggery needs manual entry; wants import, custom shelves, filtering -> supports: goal 4, tasks (E11)
- [Collectors Edition forums, older] Checklist by platform and region; cover finishes and double-packs treated as variants; wanted lists -> supports: goal 1, vocabulary (E21)
- [LaunchBox feedback board, Apr-May 2025] Request for region, localized title, disc, variant, language and game-code fields; people use filenames/spreadsheets today -> supports: goal 1, pain point 4 (E22)
- [Nintendo Life forums, older] PriceCharting and scanning apps used as catalogs; some do not care about value; value tracking brings anxiety; sealed copies feel too valuable to open -> supports: pain point 5 (E24)

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
