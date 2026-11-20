#!/usr/bin/env python3
"""WCAG contrast ratio. Usage: contrast.py FG BG [--large]   (hex such as #767676 #fff, or a basic CSS color name such as red)
Exit 0 if it passes AA (4.5:1, or 3:1 with --large), 1 otherwise. Also importable: ratio(fg, bg)."""
import sys

NAMED = {"black": "000000", "white": "ffffff", "red": "ff0000", "green": "008000", "blue": "0000ff", "gray": "808080", "grey": "808080", "silver": "c0c0c0", "yellow": "ffff00", "orange": "ffa500", "purple": "800080", "navy": "000080", "maroon": "800000", "teal": "008080", "lime": "00ff00"}

def _rgb(h):
    h = h.strip().lower()
    h = NAMED.get(h, h).lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    if len(h) != 6: raise ValueError(f"bad color {h!r}")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]

def _lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [f(v) for v in c]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(fg, bg):
    a, b = _lum(_rgb(fg)), _lum(_rgb(bg))
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    r = ratio(sys.argv[1], sys.argv[2]); need = 3.0 if "--large" in sys.argv else 4.5
    print(f"{r:.2f}:1  AA needs {need}:1  {'PASS' if r >= need else 'FAIL'}  (AAA needs {'4.5' if '--large' in sys.argv else '7'}:1)")
    sys.exit(0 if r >= need else 1)
