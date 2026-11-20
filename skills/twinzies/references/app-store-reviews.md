# App store reviews as evidence (Apple App Store and Google Play)

Store reviews are some of the best public evidence about real use: they are written at the moment of frustration or delight, they name the feature that failed, and they carry a version and date. Use them for the builder's own app and for competitors and neighbors in the domain.

## How you can legitimately get them
| Store | Your own app | Someone else's app |
|---|---|---|
| **Apple App Store** | App Store Connect (customer reviews, with export or the App Store Connect API using the builder's own keys). | Reviews visible on the public App Store page (a small sample, copied by hand). Apple's public customer-reviews feed (`itunes.apple.com/{country}/rss/customerreviews/...`) is widely used and capped at about 500 recent reviews per app per country, but fetching it was refused by robots rules when tried from this skill's tools, so do not assume the agent can read it. |
| **Google Play** | Play Console: the review export (CSV) holds the full history; the Play Developer API reviews endpoint returns only recent (about a week) written reviews and only for apps you publish. | Reviews visible on the public listing, copied by hand. Google offers no public API for other people's apps. Third-party scrapers exist; whether using one is permitted is a terms-of-service decision for the user, so do not run or recommend one on your own. |

Rules:
- **Do not bypass robots rules, login walls or rate limits**, and say plainly when a store page or feed is blocked. Ask the user to paste, attach or export instead. Treat a paste of 20-200 reviews as a good sample.
- For competitor apps, ask for reviews by **recency window and rating spread**: roughly 20 each of 1-2 star, 3 star and 4-5 star from the last 12 months, plus the "most helpful" ones, in each store the audience uses.
- Collect from **both stores** when the product is on both: Android and iOS users, devices and complaints differ. Note the country or language storefront.
- Store, rating, date, app version, device or OS if shown, and whether the developer replied are useful fields. **Reviewer names, emails and any account details are not.** Drop them on intake.

## Intake helper
`python scripts/parse_reviews.py --in reviews.csv --store play|apple|auto --out-dir reviews/` reads a Play Console CSV, an Apple-style JSON feed someone saved, or any CSV/TSV with rating and text columns. It removes author and contact fields, redacts emails, phone numbers and @handles inside the text, de-duplicates, and writes `reviews.json` (normalized, no author), `summary.json` (counts by store, rating, version and month, plus frequent terms and a keyword-theme tally) and `evidence-draft.md` (one evidence line per theme with counts and rating spread, in paraphrase-ready form). Use `--themes themes.json` to supply your own theme keywords (for example `{"scanner": ["scan", "barcode"], "sync": ["sync", "lost data"]}`).

## Reading reviews well
- **Cluster by need, then by moment**: what job were they doing and where did it break (onboarding, import, search, sync, paywall, crash)?
- **Weight carefully.** Reviews skew negative and toward people who hit a problem, include fake and incentivized reviews and review bombs after a bad release, and many complaints are about the store, price or support rather than the product. Look for the same point from several different people, across versions.
- **Version and date matter.** A complaint fixed two releases ago is history; a cluster after one release is a regression.
- **Developer replies** show known issues and what the team said; they are evidence of the company's side, not the user's.
- Ratings summarize mood, not importance. Do not average them into a score for a twin.
- Short reviews ("great app") add little; skip them for need-finding but keep them in the counts.
- Non-English reviews: note the language, translate for yourself, and flag as translated.

## Putting them in the evidence log
One log entry per theme per store, not per review:
`store: Google Play | app: <name> | window: 2025-12 to 2026-11 | n: 38 | ratings: mostly 1-2 | theme: scanner closes after each code | versions: 4.2, 4.3 | twins: marcus | paraphrase: ...`
Evidence `type` is `store-review` (or `first-party-store-review` for the builder's own app, which ranks with other first-party data). Record the app and store listing URL, not individual reviewers. Paraphrase; a verbatim quote must be under 15 words and carry no identity.

## Twin building with reviews
Reviews rarely give identity or context, so use them for **needs, pain points, vocabulary and moments**, and combine with forum threads and first-party data for who the person is. A twin supported only by store reviews is `evidence_strength: thin` unless many independent reviews across both stores agree.
