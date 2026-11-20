---
name: twinzies-journeys
description: Create customer and user journey maps (and optional service blueprints) grounded in evidence, from Twinzies personas, research notes, support tickets, analytics, forum discussion or a described flow. Use whenever the user asks for a journey map, experience map, user flow with emotions, service blueprint, "map the experience", touchpoints and pain points, moments of truth, or wants to see where a persona struggles across a whole process (not just one screen), even if they never say "journey". Produces a self-contained HTML map with an emotion curve, a structured JSON file, exports for FigJam, MURAL and Miro, and insights ready to log in the Twinzies library.
---

# Twinzies Journeys

Turn evidence about what a person does, thinks and feels over time into a journey map the team can act on. This is a companion to the **twinzies** skill: it reads twins from the library, and writes its insights back into the same evidence → insight → solution trail.

A journey map shows one person's path through one goal. It is only as good as its evidence, so every stage must say where its claims came from and how sure we are. Twin-based maps are **hypotheses**; the output says so and lists what real users should confirm.

## When to use which map
- **Journey map**: one persona, one scenario, stages with actions, thoughts, emotions, touchpoints, pain points and opportunities. Default.
- **Experience map**: broader than the product ("getting a passport", "building a collection"); use when the product is one step in a larger life task.
- **Service blueprint**: a journey map plus frontstage/backstage actions, systems and policies, used to find where the organization causes the pain. Offer it when pain points trace to staff, handoffs or back-end systems.
- **Multi-persona overlay**: two to four twins on the same stages, to see where they diverge. Do this instead of an "average user".

Read `references/journey-guide.md` for the method, the field definitions, the emotion scale, and how to avoid common failures (fantasy happy paths, mapping features instead of goals, no evidence, too many stages).

## Workflow
1. **Frame.** Ask or infer: who (twin or segment), what goal, scenario and starting/ending point, scope (map of today vs a future state), and what decision the map must inform. If the request is clear, start; ask at most one question.
2. **Find the twin(s).** Look for the Twinzies library (`twinzies-library/`, see the twinzies skill) and reuse twins by `needs` and domain. If none fit, offer to build them with the twinzies skill, or map from the evidence the user supplies. Never invent a person. If a supplied twin file does not match the persona the user named, say so in one line and use the matching twin from the library (or ask which to use). Cite evidence by the IDs in the twin or evidence log (for example E01), and use `sample` only for illustrative maps.
3. **Gather evidence** per stage: twin files, the evidence log, findings from earlier studies, user notes or transcripts, support tickets, analytics, and the product itself (walk it, read code). Record where each claim came from.
4. **Draft the stages** (4 to 8). Name them by what the person is trying to do, not by the product's screens. For each stage fill actions, thoughts (paraphrased, in the person's words), emotion (-2 to +2), touchpoints, pain points, opportunities and evidence IDs. Mark any cell without evidence `assumed`.
5. **Find the moments**: the lowest emotional point, the moment of truth (where the person decides to continue or quit), and the biggest gap between expectation and reality.
6. **Write `journey.json`** (schema in `references/journey-guide.md`; example in `assets/journey-example.json`).
7. **Render** with `python scripts/build_journey.py --in journey.json --out journey.html` (accepts one map or a list for an overlay; add `--blueprint` to show backstage rows). Deliver the HTML and the JSON.
8. **Export** for whiteboards when asked (or offer it): `python scripts/export_journey.py --in journey.json --out-dir export/` writes editable sticky grids for FigJam, MURAL and Miro, a table, a flat CSV, an SVG picture and a `board.json` spec. Read `references/export-guide.md` for the import steps per tool and for building a native FigJam board through the Figma connector.
9. **Log it** (Mode 5 of twinzies): each pain point becomes an insight with its evidence, grouped opportunities become solutions, and the user decides do / backlog / dismiss. Offer a validation plan using the twinzies research-pairing prompts.

## Honesty rules
- Label confidence per stage: `observed` (seen in the product or real data), `reported` (stated in evidence), `inferred`, `assumed`.
- Do not smooth the curve. If the evidence shows a rough stage, show it.
- Do not put quotes from real people in the map. Paraphrase, and cite the source.
- State that twin-built maps are hypotheses and list what to confirm with real users.

## Output checklist
Title, persona, scenario and scope; the stage grid; emotion curve with a text alternative; moments of truth; opportunities ranked by how many pain points they address; evidence list; not-validated list; next research step.
