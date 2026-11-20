---
id: careless-multitasker
name: "Chris, the Careless Multitasker"
kind: misuse
intent: unintentional
version: 0.1
status: hypothesis
needs: [forms, destructive-actions, undo]
evidence_strength: thin
archetype: "Distracted user who double-submits, goes back, pastes the wrong thing and taps through confirmations"
---
- Behavior: submits twice, edits in two tabs, pastes long or odd text, dismisses dialogs without reading.
- Goal of misuse: none; wants to get on with their day.
- What stops them: idempotent actions, clear confirmations naming what will be lost, undo, autosave, and plain error text.
- Probe: double-submit, back button mid-flow, two tabs editing one item, paste of 10,000 characters or emoji, deleting by mistake.
