---
id: rip-and-shelf-homelabber
version: 0.1
status: hypothesis
forked_from:
domains: [physical-media]
needs: [rip-status, shelf-location, media-server-link]
products_tested: [shelf]
last_validated:
evidence_newest: 2026-11
name: "Rosa, the Rip-and-Shelf Homelabber"
archetype: "Owns discs, rips them to Plex/Jellyfin, and needs the physical shelf and the digital library to agree"
evidence_strength: strong
evidence_count: 5
communities: ["Plex forum", "Jellyfin forum", "MakeMKV forum"]
tech_comfort: high
primary_device: desktop and home server; phone for browsing the library
accessibility_context: none stated
goals:
  - Know which physical discs are ripped, which are not, and which are only on the shelf
  - See the whole collection (playable and not) in one place
  - Find a specific disc fast when stored in boxes
  - Track upgrades (low-bitrate rip vs better disc) and missing items
pain_points:
  - Media servers have no concept of "owned but not ripped"; workarounds are placeholders and fake files
  - Labels/edition fields cannot be sorted or filtered
  - Few clients display format information on placeholders
  - Discs stored in boxes are hard to locate; drives fill up
  - Wants lending and storage-location tracking but separate tools do not integrate
vocabulary: ["rip", "remux", "ISO", "metadata", "library", "extras", "bitrate", "NAS", "agent", "placeholder"]
tasks:
  - "Mark 30 discs as ripped and link them to library entries"
  - "Add unripped discs as 'owned, not playable' entries"
  - "Record shelf or box location and who has a disc on loan"
  - "List discs whose rips are lower quality than the disc"
---

## Who they are
Runs a home server, rips with MakeMKV-style tools, and keeps the discs as backups. Some have thousands of discs ripped over many years.

## What they want and why
One source of truth. Without it she keeps a separate catalog app beside the media server and still cannot answer "is this on the shelf, on the NAS, or both?" or "where is this box?".

## How they approach software
Comfortable with self-hosted tooling, filenames, scripts and APIs. Wants import/export and integration, not another silo. Distrusts closed formats.

## Language they use
"Rip", "remux", "ISO", "library", "extras", "bitrate", "metadata". "Collection" in Plex means a grouping of films, not a physical collection, so the word can mislead.

## Evidence
- [Plex forum, approx. 2024] Owner of about 120 Blu-rays uses a separate catalog; "dumb entries" as checklist; asks about storage location and lending -> supports: goals 1-2, pain point 5 (E07)
- [Plex forum, approx. 2024] Source medium/label/catalog fields wanted because existing fields cannot be sorted or filtered -> supports: pain point 2, goal 4 (E05)
- [Jellyfin forum, approx. 2024] Wants physical titles shown unplayable; placeholder ".disc" files; few clients show format -> supports: goal 2, pain points 1, 3 (E06)
- [Jellyfin forum, approx. 2024] Owned-vs-missing views, quality scoring for upgrades, rule-based organization, XML export -> supports: goal 4 (E16)
- [MakeMKV forum, older] About 5,000 discs ripped over 13 years; discs in boxes hard to locate; drive capacity -> supports: goal 3, pain point 4 (E23)

## Validation log
- none yet (no real-user study)

## Changelog
- 0.1 (2026-11-20): created from public sources in evidence/physical-media.md; evaluated against the Shelf prototype in study-001
