# Journey mapping guide

## Stage design
- 4 to 8 stages, each a verb phrase from the person's side: "Notice a problem", "Look for options", "Set up", "Do the task", "Get a result", "Keep using or leave".
- Start before the product (what triggers the need) and end after it (what happens next). A map that begins at the home page misses why people came.
- One goal per map. If the goal changes, make another map.

## Fields per stage
| Field | Meaning |
|---|---|
| name | Stage, as a goal |
| actions | What the person does (observable) |
| thoughts | What they think or say, paraphrased |
| emotion | -2 very frustrated, -1 uneasy, 0 neutral, 1 positive, 2 delighted |
| emotion_note | Why, in a line |
| touchpoints | Screens, messages, people, places, devices |
| pain_points | Obstacles, with severity (low/med/high) |
| opportunities | Specific improvements |
| backstage | (blueprint) staff actions, handoffs, systems, policies |
| evidence | IDs or short source labels |
| confidence | observed / reported / inferred / assumed |

## Rules of thumb
- Emotion is a judgment: justify each score with evidence or label it inferred.
- Pain points are specific ("the scanner closes after every code") not vague ("hard to use").
- Opportunities must connect to a pain point; unconnected ideas go in a parking lot.
- Rank opportunities by the number of pain points and personas they help.
- Moment of truth: the stage where the person is most likely to continue or quit.
- Include accessibility and context (noisy store, one hand, small screen, low vision) in actions and touchpoints when the twin has it.

## journey.json
```json
{
  "title": "Adding a disc collection",
  "product": "Shelf",
  "persona": {"id": "barcode-blitz-cataloger", "name": "Marcus", "status": "hypothesis"},
  "scenario": "Marcus wants 300 discs in a database this weekend.",
  "goal": "Catalogue everything with minimal typing",
  "scope": "current state",
  "stages": [
    {"name": "Decide to start", "actions": ["..."], "thoughts": ["..."], "emotion": 1,
     "emotion_note": "...", "touchpoints": ["..."], "pain_points": [{"text":"...", "severity":"med"}],
     "opportunities": ["..."], "backstage": [], "evidence": ["E01"], "confidence": "reported"}
  ],
  "moments_of_truth": ["Stage 3: after the fifth manual entry he decides whether to continue"],
  "not_validated": ["Whether scanning is available on his device"],
  "next_research": "Five 30-minute sessions with people who own 200+ discs"
}
```
A list of maps (same stage names) renders as an overlay.

## Service blueprint additions
Add `backstage` (staff and system actions), `systems`, and `policies` per stage. Look for failure points where a pain point meets a handoff.

## Failure checklist
Fantasy happy path; screens not goals; no evidence; emotions all positive; no stage before or after the product; mapping an "average" user; a map nobody acts on (always end with solutions and a decision).
