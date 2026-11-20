---
id: barcode-blitz-cataloger
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [bulk-entry, duplicate-check, export, in-store]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Marcus, the Barcode-Blitz Cataloger"
archetype: "Large disc collection owner who wants everything logged fast, by scanner, and exportable"
evidence_strength: strong
evidence_count: 6
communities: ["AVNirvana forum", "DVD Talk forum", "Criterion Forum", "HTGuide forum", "Blu-ray.com forum"]
tech_comfort: medium
primary_device: desktop for bulk entry, phone camera or USB scanner for scanning, phone in stores
accessibility_context: none stated
goals:
  - Get hundreds or thousands of discs into a database quickly, mostly by barcode
  - Avoid buying duplicates while standing in a store
  - Keep an exportable copy (spreadsheet/CSV) that he owns
  - Record purchase price, store and date
pain_points:
  - Manual entry of a big collection is too tedious to finish
  - Barcode lookups miss some titles (one report: about 6% not found) and fail unpredictably
  - Subscription pricing is confusing and he is wary of lock-in
  - Apps without Android support, or that vanish from the store
  - Auto-created genre folders he did not ask for
vocabulary: ["UPC", "scan", "batch", "import", "export", "dupes", "CIB-style 'complete'", "wishlist"]
tasks:
  - "Scan 50 discs in a row and fix the ones that didn't match"
  - "In a store, check whether a title is already owned"
  - "Export the full collection to a spreadsheet"
  - "Record price paid, store and date for a new purchase"
---

## Who they are
A long-time disc buyer with a collection in the high hundreds or thousands who has tried at least one cataloging program and a spreadsheet. Pragmatic rather than romantic: the list is a tool, not the hobby.

## What they want and why
He wants intake to be nearly effortless. Communities describe batch UPC scanning (even a cheap USB scanner pasting codes into a text file), phone-camera scanning, and hands-free continuous scanning as the make-or-break feature. He uses the list mostly in stores to avoid duplicates, so lookup speed on a phone matters more than pretty shelves. He also wants to be able to leave: export to Excel/CSV/XML.

## How they approach software
Will trial two or three products before committing and gets burned by trial limits and unclear pricing. Distrusts anything he cannot export. Quits when entry feels like data-entry labor or when the database cannot find his discs. Earns trust through reliable scanning and honest, simple pricing.

## Language they use
"Scan", "UPC", "import", "export", "dupes", "wishlist". Might misread app-specific terms like "Connect", "sync direction" or "field set".

## Evidence
- [AVNirvana forum, undated] Compared phone-scanning apps; subscription pricing confusing, some lack Android, scanning in stores prevents duplicate buys -> supports: goals 2, pain points 3-4 (E01)
- [DVD Talk forum poll thread, older] Batch barcode scanning praised; 10,000+ titles by hand felt impossible; wanted price/store/date, export, sharing -> supports: goals 1, 3, 4 (E02)
- [Criterion Forum, older] Wants hands-free scanning, import/export, auto-populating lists; Android scanner apps hard to find; some databases going stale -> supports: pain points, vocabulary (E09)
- [HTGuide forum, older] Scanning historically unreliable and forced manual entry; auto genre folders disliked; manual systems die unless kept current -> supports: pain points 2, 5 (E10)
- [Blu-ray.com forum, 2014] Batch-scan workflow: USB scanner, paste codes, import in batches of about 50 -> supports: goal 1, task 1 (E17)
- [Blu-ray.com forum, older] Spreadsheets maintained since the 1990s; about 6% of UPCs not found; entry slow and tedious -> supports: pain points 1-2 (E18)

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
