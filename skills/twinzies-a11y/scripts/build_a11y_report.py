#!/usr/bin/env python3
"""Render an accessibility audit report (self-contained HTML) from findings JSON.

  python build_a11y_report.py --in findings.json --out report.html [--title "..."]

findings.json: {"product","scope","standard":"WCAG 2.2 AA","methods_run":[...],"not_run":[...],"twins":[...],
                "summary": "...", "solutions":[{title,detail,effort,findings:[ids]}], "what_works":[...], "findings":[{id,sc,level,severity,title,detail,values,fix,confidence,method,twin,where,line,element}]}
Never states that a product "conforms"; it reports what was and was not tested.
"""
import argparse, html, json
e = lambda x: html.escape(str(x), quote=True)
SC = {"1.1.1": "Non-text Content", "1.3.1": "Info and Relationships", "1.3.5": "Identify Input Purpose", "1.4.1": "Use of Color", "1.4.2": "Audio Control", "1.4.3": "Contrast (Minimum)",
      "1.4.4": "Resize Text", "1.4.10": "Reflow", "1.4.11": "Non-text Contrast", "1.4.12": "Text Spacing", "1.4.13": "Content on Hover or Focus", "2.1.1": "Keyboard", "2.1.2": "No Keyboard Trap",
      "2.2.1": "Timing Adjustable", "2.2.2": "Pause, Stop, Hide", "2.3.1": "Three Flashes", "2.4.1": "Bypass Blocks", "2.4.2": "Page Titled", "2.4.3": "Focus Order", "2.4.4": "Link Purpose (In Context)",
      "2.4.6": "Headings and Labels", "2.4.7": "Focus Visible", "2.4.11": "Focus Not Obscured (Minimum)", "2.5.3": "Label in Name", "2.5.7": "Dragging Movements", "2.5.8": "Target Size (Minimum)",
      "3.1.1": "Language of Page", "3.2.1": "On Focus", "3.2.2": "On Input", "3.2.6": "Consistent Help", "3.3.1": "Error Identification", "3.3.2": "Labels or Instructions", "3.3.3": "Error Suggestion",
      "3.3.7": "Redundant Entry", "3.3.8": "Accessible Authentication (Minimum)", "4.1.2": "Name, Role, Value", "4.1.3": "Status Messages"}
POUR = {"1": "Perceivable", "2": "Operable", "3": "Understandable", "4": "Robust"}
SEV = ["blocker", "major", "minor", "polish"]

def build(d, title):
    fs = d.get("findings", []); fs.sort(key=lambda f: (SEV.index(f.get("severity", "minor")) if f.get("severity") in SEV else 9, f.get("sc", "")))
    cnt = {s: sum(1 for f in fs if f.get("severity") == s) for s in SEV}
    h = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{CSS}</style></head><body><main>',
         f'<p class="eyebrow">Accessibility audit · {e(d.get("standard","WCAG 2.2 AA"))}</p><h1>{e(title)}</h1><p class="muted">{e(d.get("product",""))} · {e(d.get("scope",""))}</p>']
    h.append('<p class="note" role="note"><strong>This is an audit, not a conformance claim.</strong> Passing every check here would not prove the product is accessible. Automated checks cover a minority of issues; the sections below list what was and was not tested, and disabled users should confirm the result.</p>')
    if d.get("summary"): h.append(f'<section><h2>Summary</h2><p>{e(d["summary"])}</p></section>')
    h.append('<section><h2>Counts</h2><ul class="counts">' + "".join(f'<li><strong>{cnt[s]}</strong> {s}</li>' for s in SEV) + "</ul>")
    h.append('<table><caption class="sr">Findings by principle</caption><thead><tr><th scope="col">Principle</th><th scope="col">Findings</th></tr></thead><tbody>' +
             "".join(f'<tr><th scope="row">{n}</th><td>{sum(1 for f in fs if str(f.get("sc","")).startswith(k))}</td></tr>' for k, n in POUR.items()) + "</tbody></table></section>")
    h.append("<section><h2>Findings</h2>")
    for f in fs:
        sc = f.get("sc", ""); h.append(f'<article class="f sev-{e(f.get("severity","minor"))}"><h3><span class="pill">{e(f.get("severity",""))}</span> {e(f.get("title",""))}</h3>')
        h.append(f'<p class="meta">WCAG {e(sc)} {e(SC.get(sc,""))} · Level {e(f.get("level",""))} · {e(f.get("confidence",""))} · Method: {e(f.get("method","automated scan"))}' + (f' · Twin: {e(f["twin"])}' if f.get("twin") else "") + "</p>")
        h.append(f'<p>{e(f.get("detail",""))}</p>')
        if f.get("values"): h.append(f'<p class="meta">Measured: {e(f["values"])}</p>')
        if f.get("where") or f.get("line") or f.get("element"):
            h.append(f'<p class="muted small">Where: {e(f.get("where",""))} {("line " + str(f["line"])) if f.get("line") else ""} <code>{e(f.get("element",""))}</code></p>')
        h.append(f'<p><strong>Fix:</strong> {e(f.get("fix",""))}</p></article>')
    h.append("</section>")
    if d.get("solutions"):
        h.append("<section><h2>Fix first: solutions that clear the most findings</h2><ol>" + "".join(
            f'<li><strong>{e(x.get("title",""))}</strong> ({e(x.get("effort",""))} effort) clears {e(", ".join(x.get("findings", [])))}<br><span class="muted small">{e(x.get("detail",""))}</span></li>' for x in d["solutions"]) + "</ol></section>")
    for key, lab in (("what_works", "What works"), ("methods_run", "Methods run"), ("not_run", "Not run (needs testing)")):
        if d.get(key): h.append(f'<section><h2>{lab}</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in d[key]) + "</ul></section>")
    return "".join(h) + "</main></body></html>"

CSS = """:root{--bg:#faf8f4;--panel:#fff;--fg:#1d1b18;--muted:#5d5851;--line:#ddd7cc;--accent:#1b6b5a}
@media (prefers-color-scheme:dark){:root{--bg:#161513;--panel:#201f1c;--fg:#efece6;--muted:#aaa59b;--line:#38352f;--accent:#7fc0ad}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}main{max-width:900px;margin:0 auto;padding:24px 20px 60px}h1{font-size:28px;margin:4px 0}h2{font-size:20px;margin:28px 0 10px}h3{font-size:16px;margin:0 0 4px}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:12px;color:var(--muted);margin:0}.muted{color:var(--muted)}.small{font-size:13px}.sr{position:absolute;left:-9999px}
.note{border:1px solid var(--line);border-left:4px solid var(--accent);background:var(--panel);padding:10px 14px;border-radius:8px}
.counts{display:flex;gap:18px;list-style:none;padding:0}table{border-collapse:collapse;background:var(--panel)}th,td{border:1px solid var(--line);padding:6px 12px;text-align:left}
.f{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--line);border-radius:10px;padding:12px 16px;margin:12px 0}.sev-blocker{border-left-color:#b3261e}.sev-major{border-left-color:#c2570c}.sev-minor{border-left-color:#8a6d12}
.pill{font-size:11px;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:1px 8px}.meta{font-size:13px;color:var(--muted);margin:2px 0 8px}code{font-size:12px;word-break:break-all}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}"""
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="i", required=True); ap.add_argument("--out", required=True); ap.add_argument("--title", default="Accessibility audit")
    a = ap.parse_args(); open(a.out, "w").write(build(json.load(open(a.i)), a.title)); print("Wrote", a.out)
