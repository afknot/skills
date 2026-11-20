---
id: pressing-obsessed-vinyl-digger
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [exact-pressing, in-store, offline, want-list]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Dale, the Pressing-Obsessed Digger"
archetype: "Record collector who needs the exact pressing, condition and a want list that works in a shop with bad signal"
evidence_strength: strong
evidence_count: 5
communities: ["r/discogs (via a public mirror)", "r/vinyl wiki (via a public mirror)", "MacRumors forum", "Naim Audio community", "vinyl app review blog"]
tech_comfort: medium
primary_device: phone in record stores and at record fairs, desktop browser at home
accessibility_context: none stated; hands often full (crate digging), unreliable signal at fairs
goals:
  - Match each record to its exact pressing (label, catalog number, matrix/runout, country)
  - Grade record and sleeve condition as items are added
  - Keep a wantlist and know instantly if a find is a duplicate or a reissue
  - Split the collection into sub-collections (e.g., household members, or keepers vs for sale)
pain_points:
  - Barcode scan returns a list of releases, not the pressing; many older records have no barcode
  - Scanning picks the wrong reissue and there is no easy way to switch
  - Changing a record to a more accurate version resets its date added
  - The mobile app is awkward on small screens and flaky at fairs
  - Subscription changes in paid tools; no desktop app for his computer
vocabulary: ["pressing", "reissue", "first press", "matrix", "runout", "dead wax", "wantlist", "VG+", "sleeve", "RSD"]
tasks:
  - "Identify an unbarcoded 1970s LP's exact pressing"
  - "Scan 20 records in a row, fixing a wrong reissue match without losing the added date"
  - "Check in a shop (poor signal) whether a record is a duplicate"
  - "Grade condition for record and sleeve on add"
---

## Who they are
A hobbyist who thinks in pressings. Two copies of one album can differ in sound and value to him, so "album" is the wrong unit of ownership.

## What they want and why
Collection value, selling, and bragging rights all hang on the exact pressing. He wants intake that gets to the right pressing quickly, tolerates imperfect barcode data, and remembers condition. Reviewers of vinyl apps say none of them yet gets fast intake, exact edition and deep classification together.

## How they approach software
Uses Discogs as the reference but often uses its website over its app for precision. Willing to compare matrix numbers by hand, so the tool should help rather than guess silently. Loses trust the first time an app files a reissue as an original.

## Language they use
"Pressing", "reissue", "first press", "matrix/runout", "wantlist", Goldmine-style grades. "Version" in Discogs means pressing; he may find "edition" ambiguous.

## Evidence
- [Vinyl app review blog, approx. 2023] Apps differ in edition choice; scanning returned the wrong reissue with no switch; no sub-collections; long logging sessions make UI quality important -> supports: goals 1, 4, pain point 2 (E03)
- [MacRumors forum, older] Most records lack barcodes; spreadsheets cannot hold pressing/condition/promo; CLZ subscription change; Discogs lacks Mac app -> supports: pain points 1, 5 (E04)
- [r/discogs mirror, approx. Jan 2025] Switching release version loses date added; no sign of which items already scanned after interruption; iOS scanner black screen; confusion about reissues -> supports: pain points 2-3, goal 3 (E08)
- [r/vinyl wiki via mirror, undated] Match by label, catalog number and matrix; grade record and sleeve; barcodes unreliable for older records -> supports: goals 1-2 (E19)
- [Naim Audio community, undated] Barcode gives generic list not pressing; app awkward and unreliable at a record fair; grade as you add; use website -> supports: pain points 1, 4, task 3 (E20)

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
