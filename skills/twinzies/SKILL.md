---
name: twinzies
description: Build, reuse and keep improving a library of research-grounded "digital twin" user personas, drawn from public online discussion (Reddit, forums, reviews, blogs, pasted/exported threads from Facebook, X, Threads) and the builder's own feedback data. Use the twins to run usability walkthroughs, accessibility checks and lightweight user research on any app, site, codebase or design, and pair them with real-user qualitative research (screeners, in-product prompts, think-aloud scripts). Use whenever the user mentions twinzies, digital twins, synthetic users, forum-based personas, simulated usability tests, "test my app with realistic users", or wants feedback on functionality, language and content, visual design, UI, or hierarchy from the point of view of a specific community, even if they never say "digital twin". Also use for misuse and abuse-case testing (twins that use an app carelessly, unexpectedly or maliciously) to harden a product.
---

# Twinzies: Digital Twin Research

Turn what real communities say about a topic into 4-12 evidence-backed personas ("twins"), then walk those twins through a product and report what breaks, confuses, or delights them.

A twin is a **synthetic stand-in built from public discourse**. It is a fast, cheap way to surface likely problems and sharpen hypotheses. It is not a replacement for sessions with real users, and the report should say so plainly. The value comes from traceability: every trait on a twin should point back to evidence, so the user can tell signal from invention.

Twins live in a **library** that outlasts any one product. Each time the builder starts a new app or site, Twinzies first looks for twins that already fit, adapts the near-fits, and builds only the missing ones. Each evaluation and each round of real-user research then corrects the twins, so they get more accurate with use. Read `references/library.md` before starting any work; it defines where the library lives, how matching works, the naming rules, status ladder, and the improvement loop.

The lifecycle, and the modes that cover it (any can run alone):
1. **Match** the new product against the library: reuse, adapt, or find gaps.
2. **Build** twins for the gaps only.
3. **Evaluate** the product with the twins.
4. **Validate** the twins' predictions with real users, using a qualitative method paired to the twins.
5. **Improve** the twins from what was learned, and record it.
6. **Stress** the product with misuse twins that use it carelessly, unexpectedly or maliciously (Mode 6).

## Mode 0: Match against the library
Run this first for every new product, site, or domain.
1. Find or create the library (`references/library.md`, "Where it lives").
2. Describe the product by the jobs, contexts and audience it serves; search the registry and twin files; sort candidates into reuse / adapt / skip; list the gaps.
3. Show the user the plan as a short table (reuse, adapt, new, with one line of reasoning each) and offer options where the choice changes how many twins they maintain. If the library is empty, say so and go to Mode 1 for everything.

## Mode 1: Build twins
Build only what Mode 0 found missing, scoped to the gap, rather than a full set from scratch.

### 1. Frame the domain
Confirm in one or two lines: the topic (e.g. "physical media collectors who organize DVDs, Blu-rays, vinyl, games"), the product category the twins will be testing, and how many twins (default 6 in total for the product, range 4-12, counting reused ones). If the user already stated these, don't re-ask.

### 2. Gather evidence
Evidence comes from three kinds of source, and the first is the strongest, so ask for it up front: **the builder's own first-party data** (feedback-widget messages, support email, interview notes, analytics summaries, app-store or community comments about their product); **public discourse** (below); and **material the user pastes or exports**. Weight first-party evidence highest when clustering and mark it as such in the evidence log.
Use WebSearch and WebFetch for public sources, and read anything the user pastes or attaches. App store reviews (Apple App Store and Google Play) are a core public source for the builder's own app and for competitors; read `references/app-store-reviews.md` for how to get them legitimately, how to weight them and how to log them (`scripts/parse_reviews.py` cleans pasted or exported reviews). Facebook groups are login-gated and X/Threads are mostly blocked to crawlers, so say so up front and invite the user to paste or export threads from those if they matter. Don't try to bypass login walls or blocks.

Aim for breadth before depth: several communities, and both complaint-heavy threads ("how do you track your collection?", "I gave up on my spreadsheet") and enthusiasm-heavy threads (show-and-tell, recommendations). Look especially for:
- Jobs people are trying to do, and the workarounds they use today
- Complaints about existing tools, with the exact feature or moment that failed
- Vocabulary: what they call things (a "backlog", "sealed", "variants", "region lock")
- Device, skill, and accessibility context mentioned in passing
- Disagreements between sub-groups, because those become separate twins
- Store-review patterns: the moment a task failed, the app version and date, and whether Android and iOS users differ

Keep an evidence log as you go: source URL, community, rough date, and a one-line paraphrase of the point. Collect enough that each twin can cite at least 3 distinct pieces of evidence. If searches come back thin, say so and build fewer, better-supported twins rather than padding.

### 3. Cluster into twins
Group the evidence by *need and behavior*, not demographics. Two collectors of the same age can want opposite things; a casual and a completionist with the same hobby usually do. Make the twins different enough that a finding which affects one wouldn't automatically affect the rest. Include at least one twin with an accessibility need or constrained context (low vision, one-handed mobile use, slow connection, dyslexia, older device) when the evidence supports it, because accessibility problems are easy to miss with only "typical" users. Mark that support level honestly.

Read `references/persona-schema.md` for the fields every twin carries and the file format.

### 4. Name and save the twins
Give each twin a stable id and a display name (invented first name plus a nickname for what they do; rules in `references/library.md`, "Naming"). Write one markdown file per twin into `twinzies-library/twins/`, add the evidence to `twinzies-library/evidence/<domain>.md`, add a row to `registry.md`, and add a changelog entry. New twins start at version 0.1 with status `hypothesis`. Reusable files matter: the user will re-run tests on the same twins after changing their product, and on other products.

Show the user a short summary table of the working set (name, one-line archetype, top need, status and evidence strength, and whether it was reused, adapted or new) and invite adjustments before testing starts. A few options for how to split or merge twins is better than a single take-it-or-leave-it set.

### Privacy and quoting
Describe people in aggregate. Never include usernames, profile links, or anything that could identify a specific poster, and don't build a twin around one individual. Paraphrase rather than quote; if a short phrase is truly characteristic, keep it under 15 words and cite only the community, not the author. Skip content from private groups unless the user pasted it themselves, and tell them to remove names first.

## Mode 2: Evaluate with the twins

### 1. Identify what is being tested and how to reach it
Ask what to test if it isn't clear, and use whichever access the user has:
- **Live URL**: drive the browser (the built-in browser is the default; check the browser skills available) and actually perform each twin's task. Read pages as text and take screenshots at key moments. Test at a narrow mobile width too if any twin is mobile-first.
- **Local codebase**: read the source for structure, labels, ARIA, focus handling, color tokens, and copy; run the app if feasible and test it as for a live URL. Treat the repo as read-only. If you run it, copy only what the app needs into a scratch folder outside the repo, and leave out secrets and private data: `.env*`, key and credential files, `data/`, databases, logs and feedback files, `node_modules` and `.git`. Run it with an empty data folder and a clean environment (no real API keys), on a spare port. If something needs a real credential to work, mark that check "not run" rather than borrowing the user's.
- **Screenshots or Figma**: review the static design. Say which findings are about the design only and can't be confirmed without a working build (focus order, error states, loading behavior).

### 2. Define tasks per twin
Give each twin 2-4 realistic tasks drawn from its goals (for example, "add 40 discs from a haul quickly", "find out whether you already own a title while standing in a store"). Tasks come from the twin, not from the feature list. A feature nobody's twin reaches for is itself a finding.

### 3. Walk each twin through the product
For every task, narrate as that twin: what they expect to see, what they try first, where they hesitate, what words they don't understand, what they give up on. Record the concrete step and screen, so every issue is reproducible. Ground reactions in the twin's evidence and vocabulary rather than generic "users might be confused" statements.

Then judge the product across five lenses. Read `references/evaluation-guide.md` for the checklist, severity scale, and the accessibility checks to run:
1. **Functionality**: can the twin complete the task, and is anything missing or broken
2. **Language and content**: labels, microcopy, error messages, jargon, tone
3. **Visual design**: contrast, type, spacing, consistency, density
4. **UI and interaction**: controls, states, feedback, forms, navigation, keyboard and touch
5. **Hierarchy and information architecture**: what draws attention first, grouping, findability

Accessibility cuts across all five. Run real checks where you can (contrast ratios computed, not eyeballed; keyboard-only path; labels, alt text, headings, focus visibility, touch target size, zoom/reflow). Map issues to WCAG 2.2 criteria. If a `design-skills:accessibility-audit` or `a11y-enforcer` skill is available, use it for that part.

### 4. Basic research outputs
Beyond issue-finding, synthesize like a researcher:
- **Cross-twin patterns**: issues hit by several twins vs. issues only one twin cares about
- **Tension points**: where fixing it for one twin would hurt another
- **Open questions**: things the twins can't answer and a real study should (suggest 3-5, each with a method and sample)
- **A confidence note** per finding: *observed* (reproduced in the product), *inferred* (from the twin's evidence), or *speculative*

### 5. Deliver
Produce a findings file and an HTML report. Save findings as `findings.json` (schema in `references/evaluation-guide.md`) and render with:

```bash
python <skill-path>/scripts/build_report.py --twins twins/<slug> --findings findings.json --out report.html --title "<Product> twin evaluation"
```

The report has a summary, a per-twin section, prioritized findings grouped by lens with severity and confidence, and the open-questions list. Publish it as an artifact when an artifact tool is available, since it's meant to be shared and revisited; otherwise deliver the file.

In the chat reply, give the 3-5 highest-impact fixes and where the twins disagreed. Don't recap the method. Then offer the next step: validating the biggest predictions with real users (Mode 3). Save the study (tasks, findings, report) in `twinzies-library/products/<product>/` and record the product on each twin's `products_tested`.

## Mode 3: Validate with real users
Pair the evaluation with a small round of qualitative research so real behavior can confirm or correct the twins. Read `references/research-pairing.md`; it defines the pairing, three methods to offer as options (in-product task prompts and micro-surveys, moderated think-aloud sessions, and an intercept screener with short interviews), and ready-to-use prompts: a twin-match screener, micro-survey copy with triggers, task scenarios, a think-aloud script, opt-in copy and a validation log.

Tailor the prompts to the product and the twins' own vocabulary, label each with where and when to deploy it, and match its styling and tone to the product (plain, short, no jargon; any form controls styled like the product's own). When results come back, fill in the validation log, then move to Mode 4.

## Mode 4: Improve the twins
After an evaluation or a study, run the improvement loop in `references/library.md`: compare predictions with what was observed, revise the twin files only where the evidence supports it, bump versions, update status, write the changelog, update the registry, and tell the user in two or three lines what changed. Real-user evidence outranks forum evidence, which outranks inference. Propose merging or splitting twins when the evidence says so, and ask before doing it.

## Mode 5: Studies, insights and decisions
Every evaluation and study ends by writing a trail in the library from evidence to insight to solution, and by offering the user a decision on each solution. Read `references/studies-and-insights.md` for the data files, how to log a study (participants as pseudonymous IDs only), and the review flow: walk the open solutions most-supported first, ask Do it / Backlog / Dismiss with AskUserQuestion, record each answer with `scripts/lib_decide.py`, then rebuild the dashboard with `scripts/build_dashboard.py` and publish it. Many insights can feed one solution; group them so the user decides once per change, not once per symptom.

The user can also paste prompts from the broad-to-specific research ladder in `assets/playbook.json` (also shown on the dashboard's Research prompts tab). Treat those prompts as the entry points to the modes above.

## Mode 6: Misuse and abuse-case testing
Use twins whose intent is unintentional, opportunistic or malicious to find what happens when the product is used in ways nobody planned. Read `references/misuse-twins.md` first: it holds the ground rules (defensive purpose, authorized products only, reason about weaknesses instead of writing exploits, safe local runs only, no private data), the workflow and the abuse-case format. Starter archetypes are in `assets/misuse-starters/`; copy the ones that fit into the library as `kind: misuse` twins, evidence them, and reuse them across products. Findings use `lens: misuse`, feed Mode 5, and always pair each abuse case with the honest user it protects. Decline requests for working exploits, attack scripts or targeting a specific person or live system, and offer the abuse-case and mitigation version instead.

## Principles
- **Evidence before invention.** If the sources don't support a trait, leave it out or mark it as assumed.
- **Specific over plausible.** "Taps the tiny barcode icon three times because it looks like a decoration" beats "may struggle with iconography."
- **Don't flatter the product.** Report what the twins couldn't do. Note what worked too, so the user knows what to keep.
- **Be honest about limits.** Synthetic twins skew toward vocal forum users, over-represent complaints, and under-represent people who don't post online. Say this in the report.
- **Make fixes concrete.** Each finding should have a suggested change specific enough to act on, and when design direction is involved, offer two or three options rather than one.
