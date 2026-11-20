# Physical media collectors: twin set

Domain: people who organize physical media (DVDs, Blu-rays, vinyl, games). Built 2026-11-20. Target product: an app for organizing physical media.

| Twin | Archetype | Top need | Evidence |
|---|---|---|---|
| [Marcus, Barcode-Blitz Cataloger](barcode-blitz-cataloger.md) | Big disc collection, wants fast scanning and export | Bulk intake by barcode, in-store duplicate check | strong (6) |
| [Priya, Edition Completionist](edition-and-spine-completionist.md) | Boutique-label and special-edition film buyer | Edition-level fields, sort/filter by label and spine | moderate (4) |
| [Dale, Pressing-Obsessed Digger](pressing-obsessed-vinyl-digger.md) | Vinyl collector who needs the exact pressing | Right pressing, condition, usable in a shop | strong (5) |
| [Kenji, Regional-Variant Game Hunter](regional-variant-game-hunter.md) | Retro and import game collector | Region/variant/completeness, sane value data | strong (6) |
| [Rosa, Rip-and-Shelf Homelabber](rip-and-shelf-homelabber.md) | Rips discs to Plex/Jellyfin | Shelf and digital library in one view, shelf location | strong (5) |
| [Walt, Low-Vision Legacy Collector](low-vision-downsizing-collector.md) | Older collector, downsizing, needs large text | Legible UI, printable inventory, family can help | moderate; accessibility need directly evidenced by 2 sources, rest inferred |

Full audit trail: [evidence-log.md](evidence-log.md)

## Sources
25 pages were read (E01-E25) across forums, a Plex/Jellyfin/MakeMKV set, game communities, a vinyl blog, a magazine and vendor support/release notes.

## Unreachable
reddit.com (blocked; two public mirrors used), one Lemmy thread and one AudioKarma thread (errors), Facebook groups (login-gated), X and Threads (blocked). Paste exports of those if they matter.

## Limits
Synthetic twins skew toward vocal forum posters and toward complaints, and many threads are old. Evidence is thinner for video games on consoles other than retro/import, for streaming-era casuals, and for Priya (steelbook details assumed) and Walt (low-vision need rests on two sources). Use them to sharpen hypotheses and test plans, then confirm with real people.

## Ways to split or merge
- Merge Priya into Marcus if edition-level data is not a priority; split Marcus into "in-store checker" and "bulk archivist" if mobile lookup is the core use case.
- Add a casual gift-receiver / small-shelf owner twin if you expect non-hobbyists; no evidence collected for that group.
- Add a seller/reseller twin if marketplace features are in scope.
