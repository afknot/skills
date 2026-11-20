---
id: automation-scraper
name: "Ari, the Automation Scraper"
kind: misuse
intent: opportunistic
version: 0.1
status: hypothesis
needs: [public-content, api, search]
evidence_strength: thin
archetype: "Runs scripts to copy public data or hammer a search, sign-up or login endpoint"
---
- Behavior: high-volume requests, bulk account creation, harvesting listings or user info.
- What stops them: rate limits, bot friction that stays accessible, minimal public data, terms of use, monitoring.
- Probe: what is public that should not be, what has no limit, what a bot gets for free.
