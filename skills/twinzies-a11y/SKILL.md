---
name: twinzies-a11y
description: Conduct accessibility (a11y) audits against WCAG 2.2 for websites, web apps, HTML, codebases, screenshots and designs, combining a static scan, a manual checklist and accessibility-focused personas (keyboard-only, screen reader, low vision and zoom, color blindness, motor and tremor, cognitive and attention, deaf and hard of hearing, vestibular). Use whenever the user asks for an accessibility audit, a11y review, WCAG check, VPAT-style findings, "is this accessible", contrast, keyboard or screen reader testing, or wants prioritized accessibility fixes, even if they do not say "WCAG". Works standalone or with the twinzies skill, and logs findings into the same insight and solution trail.
---

# Twinzies A11y

Audit a product for accessibility barriers, say honestly what was and was not tested, and hand back prioritized fixes. Companion to **twinzies** (personas and the library) and **twinzies-journeys** (journey maps).

An audit finds barriers. It does not certify conformance. Automated tools see only some problems, and no desk review replaces disabled people using the product. The report says so every time, and never declares a product "accessible", "compliant" or "WCAG conformant".

## Workflow
1. **Scope.** What is being audited (URL, file, codebase, screenshots, Figma), which flows matter most (sign-up, checkout, search, the core task), target standard (default WCAG 2.2 AA), and any legal context (ADA, Section 508, EN 301 549, AODA). If clear, start; ask at most one question.
2. **Access.** Prefer the real thing: local files and codebases first, then a live URL the user owns or may test. For HTML files run `python scripts/a11y_scan.py page.html --out scan.json`. If a browser or headless Chrome is available, also check computed styles, zoom, reflow and focus order. Never run tests against live sites the user does not own, never use real credentials, never copy `.env` or secrets into scratch space.
3. **Static scan.** `scripts/a11y_scan.py` flags missing language, labels, names, alt text, heading and landmark problems, positive tabindex, click handlers on non-interactive elements, disabled zoom, autoplay and low-contrast color pairs it can read from CSS. Treat results as leads and verify the important ones.
4. **Manual checks.** Walk `references/wcag-checklist.md` for what tools cannot decide: keyboard order and traps, focus visibility, meaningful names and alt text, error handling, reflow at 320px and 200% zoom, text spacing, target size, motion, time limits, authentication, consistent help, cognitive load. Compute contrast with `scripts/contrast.py` (hex or basic CSS color names) for any color you can read, and put the measured ratio in the finding's `values` field.
5. **Persona lenses.** Use accessibility twins (`references/a11y-twins.md`) to walk the core flows: keyboard-only, screen reader, low vision with zoom, color blind, motor and tremor, cognitive and attention, deaf and hard of hearing, vestibular. If the twinzies library exists, reuse its twins that have an `accessibility_context` and add the a11y archetypes as `kind: user` twins. Twins are hypotheses; lived experience outranks them.
6. **Write `findings.json`.** For each finding: WCAG success criterion, level, severity (blocker / major / minor / polish), where, what happens, who is affected, concrete fix, and confidence (`observed` / `inferred` / `needs-testing`). Add `what_works`, `methods_run` and a candid `not_run` list (screen reader, real devices, voice control, user testing, anything you could not reach).
7. **Report.** `python scripts/build_a11y_report.py --in findings.json --out report.html --title "..."`. Deliver the HTML and JSON.
8. **Decide.** Group findings into solutions (one fix often clears many findings) and list them under `solutions` in `findings.json` (title, detail, effort, finding IDs); the report shows them first. If the twinzies skill is installed, also log them with its studies-and-insights flow (Mode 5: evidence, insights, solutions, decisions) and ask do / backlog / dismiss for each. Without it, ask the same question in chat and record the answers in the JSON. Offer a retest plan and a short list of questions for real assistive-technology users.

## Severity guide
- **Blocker**: a user cannot complete a core task (keyboard trap, unlabeled primary control, no way to submit).
- **Major**: task possible with real difficulty or workaround; affects many users or a required step.
- **Minor**: friction or inconsistency; workaround is easy.
- **Polish**: best practice beyond the standard.

## Honesty and care
- Say which findings were observed, inferred or need testing. Say what was not run.
- Do not use disability as a metaphor or stereotype; describe barriers, not people.
- Prefer native HTML over ARIA, and name the simplest fix first. ARIA added wrongly makes things worse.
- Fixes must not create new barriers (an "accessible" CAPTCHA that blocks screen readers is a failure). Any new control must match the product's existing styles.
- Recommend a specialist or user review for regulated or high-stakes products. This is not legal advice.
