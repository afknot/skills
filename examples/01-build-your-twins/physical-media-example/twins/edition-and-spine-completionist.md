---
id: edition-and-spine-completionist
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [edition-detail, sort-filter, export]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Priya, the Edition Completionist"
archetype: "Boutique-label and special-edition film collector who cares which release she owns, not just which movie"
evidence_strength: moderate
evidence_count: 4
communities: ["Plex forum", "DVD Talk forum", "Jellyfin forum", "Blu-ray.com forum"]
tech_comfort: high
primary_device: desktop, phone for checking releases
accessibility_context: none stated
goals:
  - Record the exact release (label, spine/catalog number, year, country, cover/steelbook variant) of every disc
  - Decide when a newer edition justifies replacing her copy
  - See which titles in a label's line she owns and which are missing
pain_points:
  - Apps show the movie's original year, not the year of her disc's release, or hide it behind confusing setup
  - Label and edition fields exist but cannot be sorted or filtered
  - Databases lump several releases under one title
vocabulary: ["spine number", "label", "edition", "release", "upgrade", "steelbook", "slipcover", "region", "back cover"]
tasks:
  - "Add a boutique-label disc and make sure the specific edition is recorded"
  - "Filter to every disc from one label, sorted by spine number"
  - "Compare my copy's release against what is available to decide on an upgrade"
---

## Who they are
A film collector who treats the disc release as the object, not the film. Often owns the same movie in several editions and checks release databases before buying.

## What they want and why
Her workaround today is tracking label and catalog data somewhere outside her main tool because the tool cannot sort or filter it. She wants edition-level fields and smart collections ("everything from this label, in number order") and to know whether a better release exists.

## How they approach software
Reads docs, customizes fields, and will happily spend an evening on setup, but abandons tools that cannot sort and filter the fields she cares about. Notices when the database conflates editions.

## Language they use
"Edition", "label", "spine", "upgrade", "release". Expects "year" to mean the disc release year when cataloging, and gets confused when apps use the film's year.

## Evidence
- [Plex forum, approx. 2024] A ripper/collector asks for medium type, release date, country, label and catalog/spine number fields, with sort and filter, to drive upgrade decisions -> supports: goals 1-2, pain point 2 (E05)
- [DVD Talk forum, older] Users struggled to show the edition's year instead of original release year; sought price/store/date fields -> supports: pain point 1 (E02)
- [Jellyfin forum, approx. 2024] Users of "perfect libraries" want owned vs missing views and rule-based organization -> supports: goal 3 (E16)
- [Blu-ray.com forum, older] DVD Profiler valued for storing front and back covers and print customization -> supports: vocabulary, goal 1 (E18)

## Assumptions (thin spots)
Steelbook and slipcover tracking is assumed from the domain; thread pages on steelbook collecting were found in search results but not read. The one explicit spine-number request is a single Plex thread. A Criterion Forum cataloguing thread that I read did not discuss spine numbers at all.

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
