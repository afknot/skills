# Misuse twins: unexpected and malicious use

Ordinary twins ask "can my users do their job?". Misuse twins ask "what happens when someone uses this in ways I did not plan for, carelessly, cleverly or in bad faith?". The output is a list of **abuse cases with mitigations**, so the builder can harden the product and write clearer errors. It is a design and threat-modelling aid, not a penetration test.

## Ground rules (read first)
1. **Defensive purpose only.** Work on products the user owns or is authorized to assess. If ownership is unclear, ask once.
2. **Reason, do not attack.** Read code, specs, screens and flows and describe how a misuse could play out and what the product would do. Do not write working exploits, payloads, credential-stuffing or scraping scripts, or step-by-step intrusion instructions, even if asked. Name the weakness class (for example "no rate limit on login", "client-side-only price check", "IDs guessable in URLs") and the fix.
3. **Only run things safely.** Anything executed goes against a local or dev copy with fake data, no real accounts and no outbound calls to third parties. Never probe a live site that is not the user's. Never use real credentials; mark such checks "not run".
4. **No private data.** Twins are archetypes of behavior. Never build one around a named person or a real group of victims, and never store personal data.
5. **Security findings are leads, not verdicts.** Label each `observed` (shown in code or a safe local run), `inferred` (reasoned), or `needs-testing`. Recommend a real security review for anything handling money, health data, children or authentication.

## Two kinds of misuse
- **Unintentional**: confused, rushed, careless, or working around the product. Common, and usually a design problem.
- **Intentional**: boundary-testing, abusing features, scraping, fraud, harassment, or insider overreach. Rarer, and usually a trust-and-safety or security problem.

## Evidence for misuse twins
Same rule as other twins: traceable evidence, paraphrased. Good sources: public security advisories and write-ups of incidents in similar products, OWASP guidance (Top 10, API Top 10, ASVS), app-store and forum complaints about scams or harassment on similar platforms, trust-and-safety transparency reports, support-ticket themes from the builder. Record the source and the *behavior pattern*, not exploit detail. Starter archetypes are in `assets/misuse-starters/`; they count as hypotheses with `evidence_strength: thin` until backed.

Twin files add two frontmatter fields: `kind: misuse` and `intent: unintentional | opportunistic | malicious`. Add a `goal_of_misuse` and `what_stops_them` section.

## Workflow
1. **Match** against the library (`kind: misuse` twins are reusable across products; match by `needs` like `forms`, `accounts`, `payments`, `uploads`, `messaging`, `public-content`, `api`).
2. **Scope the surface**: list the product's inputs (forms, URLs, uploads, API calls, links, settings, notifications), accounts and roles, money or data it holds, and anything public or shared.
3. **Walk each misuse twin** through the surface and write abuse cases in this shape:
   - *Abuse case*: what the twin tries, in one sentence
   - *Where*: screen, field, endpoint or file
   - *What the product does*: observed or inferred
   - *Harm*: to users, the business, or third parties
   - *Likelihood* (low / medium / high) and *impact* (low / medium / high), giving a severity
   - *Mitigation*: concrete and proportionate (validation, rate limits, confirmations, undo, permissions, logging, clearer copy)
   - *Experience check*: does the mitigation hurt honest users? (A CAPTCHA that blocks a screen-reader user is a failure; see the a11y companion skill.)
4. **Separate the honest-user fixes** (clearer errors, undo, safer defaults) from **security work** (needs an owner and a real review).
5. **Log** as a study with `method: misuse walkthrough`, insights per abuse case, and solutions grouped by mitigation, exactly as in `references/studies-and-insights.md`. Then run the decision flow (do it / backlog / dismiss).

## Output
`abuse-cases.json` plus an HTML report from `scripts/build_report.py` (use `lens: misuse` in findings; the severity scale is unchanged). Always include: what was not tested, that twins are not attackers, and a recommendation for professional review where stakes are high.

## Keep it humane
Misuse twins describe *behaviors*, never groups of people. Avoid stereotyping who "the attacker" is. Pair every adversarial case with the vulnerable user it affects; the goal is to protect them.
