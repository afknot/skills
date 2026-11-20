---
id: boundary-tester
name: "Jo, the Boundary Tester"
kind: misuse
intent: opportunistic
version: 0.1
status: hypothesis
needs: [forms, urls, uploads, accounts]
evidence_strength: thin
archetype: "Curious or mischievous user who edits URLs, enters extremes and tries things they should not be allowed to do"
---
- Behavior: changes IDs in URLs, enters negative, huge or malformed values, uploads unexpected file types, tries admin pages, uses someone else's link.
- Goal of misuse: curiosity, free stuff, seeing what breaks.
- What stops them: server-side validation and authorization on every request, guess-resistant IDs, upload checks, safe error messages that reveal nothing internal.
- Probe class: broken access control, input validation, error-message leakage (name the class; do not craft payloads).
