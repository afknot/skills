# Studies, insights, solutions and decisions

The library keeps one trail from raw evidence to a decision, so the user can see why any change is proposed and what supports it:

    evidence  ->  insight  ->  solution  ->  decision
    (what was seen/said)  (what it means)  (what to change)  (do / dismiss / backlog)

Many evidence items can support one insight, and **many insights can feed one solution**. Everything is stored as JSON in `twinzies-library/data/` so the dashboard can be rebuilt at any time. Twins stay as markdown in `twins/`.

## Files in `data/`

**evidence.json**: list of
`{id, type, source, community, date, point, twins[], study?, where?}`
- `type`: `public` (forum, review, article), `first-party` (the builder's own feedback, support, interviews, analytics), `product-observed` (seen in the product during an evaluation, id `O-<finding>`), `study` (said or done by a real participant).
- `point` is a paraphrase, never a long quote. No usernames, no names of participants.

**studies.json**: list of
`{id, title, product, method, date, status, twins[], participants[], real_participants, insights[], report, not_run[], notes}`
- `participants`: `{id: "P01", twin: "<id of nearest twin>", source: "feedback widget | community post | email list", notes: "<role or context, no name>"}`. Pseudonymous IDs only. Keep names, emails and recordings outside the library (and outside any repo), and record consent where they are kept.
- `real_participants` is the count of real people; a twins-only evaluation has 0 and the dashboard says so.

**insights.json**: list of
`{id, statement, lens, severity, confidence, twins[], evidence[], study, where, finding?}`
- An insight is a claim about users that the evidence supports: "Collectors can't tell they already own a title when adding." It is not a design change.
- `evidence` lists evidence ids. Prefer at least one `product-observed` or `study` item plus any `public` or `first-party` items that corroborate it. An insight with only `inferred` support keeps `confidence: inferred`.

**solutions.json**: list of
`{id, title, detail, insights[], effort (S/M/L), impact (high/medium/low), status, product, decided, note}`
- A solution is a change to the product. Group insights that one change would resolve into one solution, rather than one solution per insight. Give each solution an impact based on how many twins and insights it serves, and an honest effort size.
- `status`: `proposed`, `accepted` (the user chose "Do it"), `backlog`, `dismissed`, `done`.

## Logging a study (after an evaluation or research round)
1. Add or update the study record (method, date, participants as pseudonymous IDs matched to twins, not-run list).
2. Add new evidence items from the study (paraphrased, tagged with the twins they speak for).
3. Add insights, each linked to evidence ids. Reuse an existing insight id when the new evidence supports it, and add the evidence to it, rather than duplicating.
4. Add or update solutions and link the insights that feed them. Note what the evidence contradicts.
5. Run the improvement loop from `library.md` for the twins involved.
6. Run `python scripts/lib_decide.py <library> check` and fix any broken links.
7. Rebuild the dashboard and give the user the link.

## Review and decide (in the Claude session)
When the user asks to review (or right after an evaluation or study), walk through the open solutions, most-supported first (most insights, then highest impact):
1. Show the solution in two or three lines: what it is, which insights feed it and how strongly they are evidenced, which twins it serves, impact and effort.
2. Ask with AskUserQuestion, up to four solutions per call, one question each with these options: **Do it**, **Backlog**, **Dismiss**. Put the recommended one first with "(Recommended)" only when the evidence clearly points that way. The user can always type a note or a different answer, so invite a reason for a dismissal; it prevents the same idea resurfacing.
3. Record each answer with `lib_decide.py` (`accepted` for Do it). Save the note.
4. For anything accepted, offer the next step in one line (draft the change, make a task list, or hand off to a build session). Do not start changing the product's code unless the user asks.
5. Rebuild the dashboard. Dismissed solutions keep their insights, which still count as evidence for the twins.

If the user dismisses a solution but agrees the insight is real, keep the insight; if they dispute the insight itself, mark it `contested` in its statement and note what would settle it.

## The dashboard
`python scripts/build_dashboard.py --library <lib> --out <lib>/dashboard.html` creates one self-contained page with: Overview (what needs a decision), Twins (evidence, studies, validation log, changelog for each), Studies (who took part, key insights, what was not run), Insight map (a matrix of insights, their evidence and the solutions they feed), Decisions (proposed, do it, backlog, dismissed, done), Changelog, and the Research prompts. It is read-only; decisions are made in the Claude session and the page is rebuilt. Publish it as an artifact when an artifact tool is available, since the user will revisit it.
