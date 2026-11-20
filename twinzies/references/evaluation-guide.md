# Evaluation guide

## Table of contents
1. Lens checklists
2. Accessibility checks to actually run
3. Severity scale
4. Confidence labels
5. findings.json schema

## 1. Lens checklists

### Functionality
- Can the twin finish each task end to end? Where does the path dead-end?
- Is data entry efficient for bulk or repeated work (import, scan, paste, batch edit)?
- Search, filter, sort: do they match how the twin thinks about their stuff?
- Edge cases the twin's evidence mentions (duplicates, variants, missing metadata, large collections, offline).
- Anything the twin expects that doesn't exist.

### Language and content
- Labels and buttons use the twin's vocabulary, not internal terms.
- Error and empty-state messages explain what happened and what to do next.
- Jargon, abbreviations, or ambiguous verbs ("Process", "Sync").
- Tone matches the audience; no unexplained assumptions.
- Reading level and length of instructional text.

### Visual design
- Contrast, type size and weight, line length, spacing rhythm.
- Consistency of components, icons, colors, and states across screens.
- Density: does it suit a power user scanning hundreds of rows, or a newcomer?
- Color used as the only signal anywhere?
- Dark/light mode and responsive behavior if offered.

### UI and interaction
- Every control has hover, focus, active, disabled, loading, and error states.
- Controls match the product's own styling; no leftover default browser controls.
- Feedback after actions (saved, failed, in progress). Undo for destructive actions.
- Forms: labels, validation timing, input types, autofill, error recovery.
- Touch targets and spacing on mobile; keyboard path on desktop.

### Hierarchy and information architecture
- What does the eye land on first, and is it what this twin needs first?
- Primary vs. secondary actions clearly distinguished.
- Grouping and ordering of navigation, settings, and fields.
- Findability: can the twin locate a feature without being told where it is?
- Page and heading structure that matches the visual structure.

## 2. Accessibility checks to actually run

Do the ones that are possible for the access available. Report which were not run.

- **Contrast**: compute ratios for text and UI components from actual values (4.5:1 body text, 3:1 large text and UI components, WCAG 1.4.3 / 1.4.11).
- **Keyboard**: tab through each twin's task path. Everything reachable and operable, logical order, no traps, visible focus (2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11).
- **Names and labels**: every input and icon button has an accessible name; labels are programmatically associated (1.3.1, 4.1.2).
- **Headings and landmarks**: one h1, no skipped levels, main/nav regions present (1.3.1, 2.4.1, 2.4.6).
- **Images**: meaningful alt text, decorative images hidden (1.1.1).
- **Zoom and reflow**: usable at 200% zoom and 320 CSS px width without horizontal scroll (1.4.4, 1.4.10).
- **Target size**: at least 24x24 CSS px, preferably 44x44 for touch (2.5.8).
- **Motion and time**: reduced-motion respected, no content that disappears too fast (2.2.x, 2.3.3).
- **Errors and status**: errors identified in text, status messages announced (3.3.1, 3.3.3, 4.1.3).
- **Language**: page language set (3.1.1).

Reference the criterion number in each accessibility finding.

## 3. Severity scale

| Severity | Meaning |
|---|---|
| blocker | A twin cannot complete a core task, or an accessibility barrier fully excludes a group |
| major | Task completes with significant struggle, error risk, or abandonment likelihood |
| minor | Friction or inconsistency that slows people or lowers trust |
| polish | Nice-to-have refinement |

Prioritize by severity, then by how many twins are affected.

## 4. Confidence labels
- `observed`: reproduced in the live product, code, or design
- `inferred`: follows from the twin's documented behavior or vocabulary but wasn't directly reproduced
- `speculative`: plausible but not supported by evidence; flag for real-user validation

## 5. findings.json schema

```json
{
  "product": "Shelf (prototype)",
  "tested": "https://example.com (live), 2026-11-20",
  "access": ["live URL", "codebase"],
  "not_run": ["screen reader testing"],
  "summary": "Two or three sentences on the overall picture.",
  "twin_notes": [
    {
      "twin_id": "sealed-shelf-curator",
      "tasks": [
        {"task": "Add 40 discs from a haul", "outcome": "completed with difficulty", "narrative": "Expects bulk entry; finds one-at-a-time form..."}
      ]
    }
  ],
  "findings": [
    {
      "id": "F1",
      "lens": "functionality",
      "title": "No bulk add",
      "severity": "major",
      "confidence": "observed",
      "twins": ["sealed-shelf-curator", "thrift-hauler"],
      "where": "Add item screen",
      "what_happens": "Concrete description of the step and the problem.",
      "why_it_matters": "Tied to the twin's goals and evidence.",
      "recommendation": "Specific change; give 2-3 options when it's a design choice.",
      "wcag": []
    }
  ],
  "tensions": ["Dense table helps the Shelf Curator but overwhelms the Casual Gifter."],
  "what_works": ["Short list of things to keep."],
  "open_questions": [
    {"question": "Do collectors want barcode scan or manual search first?", "method": "5-person moderated test", "why": "Twins disagree"}
  ],
  "limits": "Twins reflect vocal online communities and are hypotheses, not data from real users."
}
```

`lens` is one of: functionality, language, visual, ui, hierarchy. `wcag` entries are criterion strings like `"1.4.3"`.


## Lens: misuse (optional)
Used in Mode 6. Each finding is an abuse case (see `misuse-twins.md`): what the twin tried, where, what the product does, harm, likelihood and impact, mitigation, and the effect on honest users. Confidence labels add `needs-testing`.
