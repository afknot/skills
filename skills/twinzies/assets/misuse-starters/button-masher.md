---
id: button-masher
name: "Sam, the Impatient Button-Masher"
kind: misuse
intent: unintentional
version: 0.1
status: hypothesis
needs: [forms, payments, slow-network]
evidence_strength: thin
archetype: "Taps again when nothing seems to happen; loses connection mid-action"
---
- Behavior: repeats taps on slow responses, refreshes during saves, switches apps and returns to a stale screen.
- What stops them: visible progress, disabled-while-working buttons, idempotency, safe retries, session recovery.
- Probe: double charge or double create, half-saved states, stale data after reconnect.
