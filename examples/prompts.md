# Research prompts, broad to specific

Paste these into a Claude session where the Twinzies skill is installed. Fill in the `[brackets]`. They follow the order of a real research project: set up, plan, build, explore, evaluate, validate, decide, maintain. The same prompts appear on the dashboard's *Research prompts* tab with copy buttons.

## 1 · Set up: Find or create my library

*Scope: broad. Use when: first time, or at the start of any new session.*

```text
Use Twinzies. Find or create my twin library. Tell me where it lives, how many twins, studies, insights and open solutions it holds, and rebuild the dashboard.
```

**You get:** Library location, a one-line status, and a dashboard link.

## 2 · Landscape: Plan the twin set for a new product

*Scope: broad. Use when: starting a new app or site, before gathering anything.*

```text
Use Twinzies. I'm starting a new [product type] for [audience and what they're trying to do]. Check my library for twins that already fit and show me a reuse / adapt / new plan, one line of reasoning each, plus the needs no twin covers yet. Don't build anything yet.
```

**You get:** A table of reused, adapted and new twins and the gaps, so you decide how many twins you maintain.

## 3 · Audience: Build the missing twins

*Scope: broad → mid. Use when: after you approve the plan.*

```text
Use Twinzies to build the missing twins from the plan. Gather evidence from public sources and from the first-party material I'm attaching [feedback exports, support emails, interview notes]. Aim for [N] twins in total for this product. Show me the set, with options for splitting or merging, before saving.
```

**You get:** New twins saved as hypotheses (v0.1) with an evidence log; unreachable sources listed.

## 4 · Jobs & journeys: Map journeys for each twin

*Scope: mid. Use when: you want to know where each audience stalls before you test anything.*

```text
Use Twinzies. Map the end-to-end journey for [the job, e.g. 'getting 40 new items into my library'] for each of [twins]: steps, what they expect, their vocabulary, and where they are most likely to stall. Mark each point evidenced, inferred or speculative.
```

**You get:** Journey table per twin, with the riskiest moments ranked.

## 5 · Evaluation: Evaluate a product across all five lenses

*Scope: mid → specific. Use when: you have a URL, repo, Figma file or screenshots.*

```text
Use Twinzies. Evaluate [URL / repo path / Figma link / screenshots] with [twins, or 'all relevant twins']. Cover functionality, language and content, visual design, UI and hierarchy, and accessibility against WCAG 2.2. Treat the repo as read-only and keep secrets and real data out of any copy. Give me insights mapped to their evidence, then proposed solutions grouped by how many insights feed them.
```

**You get:** findings.json, an HTML report, insights and solutions added to the library, dashboard rebuilt.

## 6 · Flow: Walk one twin through one flow

*Scope: specific. Use when: a single flow is under suspicion: onboarding, checkout, search, import.*

```text
Use Twinzies. Walk [twin] through [flow] in [product], step by step: what they expect, what they try first, where they hesitate, and which words they don't understand. Give me the three highest-impact changes, with two or three options for any design change.
```

**You get:** Step-by-step narration and three prioritized changes.

## 7 · Component: Review one screen, component or piece of copy

*Scope: most specific. Use when: you're about to ship or rewrite something small.*

```text
Use Twinzies. Review [screen / component / copy] for [twins]: hierarchy, labels, empty, error and loading states, and keyboard and screen-reader behavior. Offer two or three options for any change, written in the product's own voice.
```

**You get:** Specific issues and rewrite options, with WCAG references.

## 8 · Comparison: Compare two versions

*Scope: specific. Use when: you have two designs or two copy options.*

```text
Use Twinzies. Compare [version A] and [version B] of [screen or flow] through [twins]. For [task], which would each twin prefer and why? Where do they disagree, and what would settle it?
```

**You get:** Per-twin preference, tensions, and the real-user check that would settle it.

## 9 · Validation plan: Turn predictions into a research plan

*Scope: specific. Use when: after an evaluation, before recruiting real people.*

```text
Use Twinzies. Turn the top predictions from [study] into a validation plan for [product]. Offer me method options, then write a twin-match screener, task scenarios, in-product prompts with triggers, and a think-aloud script in [product]'s tone. State where and when each one is deployed.
```

**You get:** A ready-to-deploy kit for the method you choose.

## 10 · Log results: Log a study and map insights

*Scope: specific. Use when: you have sessions, survey answers or feedback to record.*

```text
Use Twinzies. Log this study. Method and dates: [..]. Participants: [pseudonymous IDs, matched twin, recruiting source, no names or emails]. Results: [notes, transcripts or responses]. Confirm or contradict each prediction, list surprises, add insights with their evidence, and propose solutions. Update the dashboard.
```

**You get:** Study record with participants, validated predictions, insights linked to evidence and solutions.

## 11 · Decide: Review and decide on solutions

*Scope: decision. Use when: insights and proposed solutions are waiting.*

```text
Use Twinzies. Show me the proposed solutions for [product], most-supported first. For each, let me choose Do it, Dismiss or Backlog, one at a time, and record my choice and a note.
```

**You get:** Each solution marked accepted, dismissed or backlog, with the date, then the dashboard rebuilt.

## 12 · Improve twins: Update twins from what we learned

*Scope: decision. Use when: after any study.*

```text
Use Twinzies. Propose revisions to the twins from [study]: what changes, the new version and status, and the evidence behind each. Don't apply anything until I approve.
```

**You get:** Proposed changes per twin; on approval, version bumps and changelog entries.

## 13 · Maintenance: Audit the library

*Scope: ongoing. Use when: monthly.*

```text
Use Twinzies. Audit my library: stale evidence, near-duplicate twins, twins never validated with real users, and solutions that have been proposed or backlogged for more than 30 days. Recommend what to refresh, merge or retire.
```

**You get:** A short audit with recommended actions.

## Companion skills

**Journey map (twinzies-journeys)**
```text
Use Twinzies Journeys. Map [twin name]'s journey for [goal] in [product], current state. Label confidence per stage, show the emotion curve, and export editable stickies for [FigJam / MURAL / Miro].
```

**Accessibility audit (twinzies-a11y)**
```text
Use Twinzies A11y. Audit [file, URL I own, or codebase] against WCAG 2.2 AA for [core flows]. Use the static scan, the manual checklist and the keyboard, screen reader and low-vision twins. List what you did not test, and group fixes by what clears the most findings.
```
