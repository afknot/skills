# Manual checklist (WCAG 2.2 AA focus)

Mark each item pass / fail / not tested, with evidence.

## Perceivable
- 1.1.1 Informative images have alt text that says purpose; decorative images are empty-alt; icon-only controls have names.
- 1.3.1 Headings, lists, tables and forms use real structure; reading order matches visual order.
- 1.3.4 Orientation is not locked. 1.3.5 Personal data fields have autocomplete.
- 1.4.1 Color is not the only signal (errors, status, required, links in text).
- 1.4.3 Text contrast 4.5:1 (3:1 for large text). 1.4.11 UI component and focus indicator contrast 3:1.
- 1.4.4 Text resizes to 200% without loss. 1.4.10 Reflow at 320 CSS px wide with no two-way scrolling.
- 1.4.12 Text spacing overrides do not break layout. 1.4.13 Hover/focus content can be dismissed, hovered and persists.
- Captions and transcripts for prerecorded audio and video (1.2.x).

## Operable
- 2.1.1 Everything works by keyboard; 2.1.2 no trap; 2.1.4 single-key shortcuts can be turned off or remapped.
- 2.2.1 Timeouts can be extended; 2.2.2 moving content can be paused.
- 2.3.1 Nothing flashes more than three times a second.
- 2.4.1 Skip link or landmarks; 2.4.2 page titles; 2.4.3 focus order logical; 2.4.4 link purpose clear; 2.4.6 headings and labels descriptive.
- 2.4.7 Focus is visible; 2.4.11 focus not hidden by sticky headers or cookie banners.
- 2.5.1 Path-based gestures have a simple alternative; 2.5.2 pointer cancel; 2.5.3 visible label is in the accessible name; 2.5.4 motion actuation has an alternative.
- 2.5.7 Dragging has a single-pointer alternative; 2.5.8 targets at least 24x24 CSS px (or spaced).

## Understandable
- 3.1.1 Page language; 3.1.2 language changes marked.
- 3.2.1/3.2.2 No unexpected change on focus or input; 3.2.3/3.2.4 consistent navigation and identification; 3.2.6 help in a consistent place.
- 3.3.1 Errors identified in text; 3.3.2 labels and instructions; 3.3.3 suggestions given; 3.3.4 reversible/confirmed for important data.
- 3.3.7 No redundant re-entry; 3.3.8 Authentication does not require a cognitive test (allow paste and password managers).

## Robust
- 4.1.2 Name, role, value for custom controls; 4.1.3 Status messages announced without moving focus.

## Test recipes (no special tools)
- **Keyboard**: unplug the mouse; Tab through everything, Shift+Tab back, Enter and Space on controls, Esc on dialogs. Is focus always visible and in a sensible order? Can you reach and leave everything?
- **Zoom and reflow**: browser zoom to 200% and 400%, narrow window to 320px.
- **Text spacing**: apply the WCAG text-spacing bookmarklet values.
- **Screen reader**: VoiceOver (macOS/iOS), NVDA (Windows), TalkBack (Android). Listen for names, roles, states and headings. If you cannot run one, mark "not tested".
- **Color**: grayscale view; contrast calculation on text and UI parts.
- **Motion**: honor prefers-reduced-motion; no required parallax or autoplay.
