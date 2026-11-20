# Pairing twins with real-user qualitative research

Twins are hypotheses. The fastest way to make them trustworthy is to pair every evaluation with a small amount of qualitative research with real users, and to use the twins to make that research sharper and cheaper. Neither replaces the other: twins find likely problems before anyone is recruited; real users confirm which are real and correct the twins.

## The pairing: twin-led hypothesis testing
1. **Predict.** Before any research, list the twin-based predictions as falsifiable statements: "Marcus-type users will abandon manual add when they have more than ~20 items to enter", "Walt-type users won't find Export because it is labeled 'Insurance Report'". Take them from the findings, flagging the ones that rest on `inferred` or `speculative` evidence.
2. **Test with real people** using one of the methods below, with tasks and questions written from the twins' own jobs and vocabulary, not from the product's feature names.
3. **Compare.** Mark each prediction confirmed, contradicted, or unclear, and note surprises the twins did not predict. Surprises are the most valuable output: they are what the twins are missing.
4. **Update the twins** through the improvement loop in `library.md` (version bump, changelog, status).

## Choosing a method (offer these as options)
| Method | Best for | Effort | Where it runs |
|---|---|---|---|
| **A. Unmoderated in-product task prompts + micro-surveys** (recommended default) | Checking many predictions cheaply; ongoing signal | Low: copy and a few triggers | Inside the app or website |
| **B. Moderated remote think-aloud sessions** | Understanding *why* a prediction held or failed; twins that disagree | Medium: 3-5 sessions of 30 minutes | Video call or in person |
| **C. Intercept screener plus short interviews** | Matching real users to twins and recruiting for B | Low-medium | Feedback widget, email, community posts |

A good default for a solo builder: use **C** to find and tag real users, **A** to collect task and satisfaction signal continuously, and **B** only for the two or three predictions where twins disagreed or the stakes are high. Five moderated sessions per round is enough to confirm or refute the biggest usability problems; don't aim for statistics.

Ground rules for all methods: say what the research is for, collect the minimum personal data, get an explicit opt-in before storing a name or email, never ask for sensitive details, and keep it short. Keep the participant's own words in the log; avoid reading twin traits into answers.

## 1. Twin-match screener (3-6 questions)
Purpose: place a real person near a twin so their feedback updates the right twin. Ask about behavior, not demographics. Replace the bracketed parts with the product's domain. The questions below are tuned to physical media and are meant as a pattern.

1. "Which best describes what you do with your [collection]?" (single choice, include an "other" box)
   - I keep a list so I don't buy duplicates
   - I need to know the exact edition, pressing or version I own
   - I mostly want to scan or enter lots of items quickly
   - I want my shelf and my digital library (Plex, Jellyfin) to match
   - I'm sorting or downsizing and need a record someone else can use
   - None of these
2. "How do you usually check what you own?" (notebook, spreadsheet, another app, memory, I don't)
3. "Where are you when you most need that answer?" (at home at a computer / in a shop on my phone / both)
4. "Is there anything that makes apps harder for you to use?" (optional; large text, screen reader, keyboard only, slow connection, other, prefer not to say)
5. "What's the last app you gave up on for this, and why?" (open text, optional)

Mapping: keep a table from answers to twin ids in the product's study folder. If a respondent fits no twin, record them as a candidate gap. Question 4 is optional and never required to continue.

## 2. In-product micro-surveys (method A)
Short, one question each, shown at the moment of the experience and dismissible. Triggers in brackets. Keep wording plain and short.

- First run finished: "That's setup done. How easy was it to get started?" 1-5 scale + "What almost stopped you?" (optional text)
- After a core task succeeds [e.g., first item added, first export, first scan]: "Did that go the way you expected?" Yes / Not quite / No, then "What did you expect instead?" (shown only on Not quite / No)
- After an abandoned task [left a form with unsaved data, or 3 errors in a row]: "Looks like that didn't finish. What were you trying to do?" (open text) with "Not now"
- Empty state, after 30 seconds idle: "Not sure where to start? What are you hoping to do here?" with 3-4 buttons drawn from the twins' jobs plus "Something else"
- After an error: "Was this message clear about what to do next?" Yes / No + optional text
- Search with no results: "We didn't find that. What were you looking for?"
- Settings or help page: "What were you trying to find?"
- Periodic (once per 30 days, only for active users): "What's one thing that would make this more useful for you?"
- Accessibility check, in settings or help: "Is anything hard to see, read or use? Tell us what and where." (open text, optional)

Rules: one prompt per session at most; never interrupt a task in progress; wait at least a week between prompts to the same person; always provide a way to dismiss; tag each response with page, task, app version and (if known) matched twin.

## 3. Unmoderated task prompts (method A or B)
Write tasks as short scenarios that describe a goal and a reason, without naming screens or buttons. Use the twin's vocabulary. Ask the participant to think aloud (in B) or write what they expected before and after (in A).

Template: "Imagine [situation in the twin's world]. Using [product], [goal in the twin's words]. Tell us when you think you're done, or if you give up."

Examples for a collection app:
- Marcus-type: "You come home with a box of about 40 discs from a sale and want them all in your library by tonight. Add them."
- Dale-type: "You're in a record shop and spot an album. Find out whether you already own that exact pressing."
- Rosa-type: "You want to see which discs on your shelf you've already ripped and which you haven't."
- Priya-type: "Find every special-edition release from one label and sort them by spine number."
- Kenji-type: "Record that you own an import copy of a game, complete in box, and note its region."
- Walt-type: "Make a printed list of everything you own that a family member could use."

After each task, ask three things: "How did that go?" (very easy to very hard), "What did you expect to happen at the point you hesitated?" and "What would you call this feature?" (vocabulary check).

## 4. Moderated think-aloud script (method B)
Plan 30 minutes. Recruit through the screener, aiming for one to two real users per twin you most want to check.

1. **Welcome (2 min).** "We're testing the product, not you. There are no wrong answers. Please think out loud, including when something confuses you. I may not answer questions right away; I'm curious what you would do." Ask permission to record.
2. **Warm-up (3 min).** "Tell me about your collection and how you keep track of it today." Listen for the twin's goals and words.
3. **Tasks (15-18 min).** Give one task from section 3 at a time. Stay quiet. If they stall for more than a minute, ask the least leading probe that works.
4. **Probes, when needed.**
   - "What are you looking for right now?"
   - "What did you expect that to do?"
   - "What would you try next?"
   - "You paused there. What was going through your mind?"
   - "How would you describe this screen to a friend?"
   - Avoid: "Do you like it?", "Is that confusing?", or naming the button.
5. **Wrap-up (5 min).** "What was the easiest part? The hardest? What's missing for how you actually collect?" Then: "If you could change one thing, what would it be?"
6. **Close (1 min).** Thank them and say what happens next.

Capture for each task: success, time stuck, quote in the participant's words, and the matching prediction.

## 5. Recruitment and opt-in copy
For a feedback widget or footer link:
- Prompt: "Help improve [Product]. Want to join a short research chat? About 30 minutes, no prep."
- Opt-in form fields: first name, email, and one screener question. Consent line: "We'll use your answers only to improve [Product]. We'll email you to schedule a time, and you can leave anytime." Explicit checkbox styled to match the product, never left in the browser default.
- For community posts: "I'm building [Product] for people who [job in the twin's words]. If you'd like to try it and talk for 30 minutes about how you collect, comment or message me." Do not recruit by quoting or identifying people from forum threads.

## 6. Validation log (write to `products/<product>/validation-<date>.md`)
```markdown
# Validation: <product>, <date>
Method: A/B/C | Participants: n (matched twins: ids) | Tools: ...

| Prediction (from findings F#) | Twin(s) | Result | Evidence (participant words, paraphrased) |
|---|---|---|---|
| Walt-type users won't find Export | walt | confirmed (3 of 3) | "I looked under Settings, then gave up" |

## Surprises (not predicted by any twin)
- ...

## Twin updates proposed
- twin id: change, reason, new status/version
```
Feed this into the improvement loop in `library.md`.
