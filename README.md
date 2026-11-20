# Skills

A collection of Claude skills. Each skill is a self-contained folder with a `SKILL.md` (instructions plus frontmatter) and optional `references/`, `scripts/`, `assets/` and `evals/`.

## Skills

| Skill | What it does |
| --- | --- |
| [`twinzies`](twinzies/) | Builds and maintains a library of research-grounded "digital twin" personas from public online discussion, then walks them through an app, site or design for usability, accessibility and misuse-case feedback. |
| [`twinzies-a11y`](twinzies-a11y/) | WCAG 2.2 accessibility audits that combine a static scan, a manual checklist and accessibility-focused personas. Works alone or with `twinzies`. |
| [`twinzies-journeys`](twinzies-journeys/) | Evidence-based customer and user journey maps and service blueprints, with exports for FigJam, MURAL and Miro. |

## Layout

```
.
├── README.md
├── <skill-name>/
│   ├── SKILL.md        # required: name, description, instructions
│   ├── references/     # docs the skill loads on demand
│   ├── scripts/        # helpers the skill runs
│   ├── assets/         # templates, starter data
│   └── evals/          # test cases for the skill
```

## Adding a skill

1. Create a folder named after the skill (lowercase, hyphenated).
2. Add a `SKILL.md` with `name` and `description` frontmatter. The description decides when the skill triggers, so say what it does and when to use it.
3. Add a row to the table above.

## Notes

- `twinzies-a11y` and `twinzies-journeys` can log into the same insight trail as `twinzies`, so keep them together.
- No license is set yet. Add a `LICENSE` file before making the repo public.
