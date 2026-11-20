#!/usr/bin/env python3
"""Render a Twinzies evaluation report (single self-contained HTML file).

Usage:
  python build_report.py --twins twins/<slug> --findings findings.json --out report.html [--title "..."]

Twin files are markdown with simple YAML frontmatter (see references/persona-schema.md).
Only the standard library is used. Every interactive control is styled explicitly.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

SEV_ORDER = ["blocker", "major", "minor", "polish"]
LENS_LABEL = {
    "functionality": "Functionality",
    "language": "Language & content",
    "visual": "Visual design",
    "ui": "UI & interaction",
    "hierarchy": "Hierarchy & IA",
    "misuse": "Misuse & abuse cases",
    "accessibility": "Accessibility",
    "journey": "Journey",
}


def esc(x):
    return html.escape(str(x if x is not None else ""))


def parse_frontmatter(text):
    """Tiny YAML subset: scalars, inline lists, and '- item' block lists."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    data, key = {}, None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or line.lstrip().startswith("- "):
            item = line.strip()
            if item.startswith("- ") and key:
                data.setdefault(key, []).append(item[2:].strip().strip('"'))
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            key, v = k.strip(), v.strip()
            v = re.sub(r"\s+#.*$", "", v)
            if v == "":
                data[key] = []
            elif v.startswith("[") and v.endswith("]"):
                data[key] = [s.strip().strip('"') for s in v[1:-1].split(",") if s.strip()]
            else:
                data[key] = v.strip('"')
    return data, body


def load_twins(folder):
    twins = []
    for p in sorted(Path(folder).glob("*.md")):
        if p.name in ("index.md", "evidence-log.md"):
            continue
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"))
        if fm.get("id"):
            fm["_body"] = body
            twins.append(fm)
    return twins


def render_list(items):
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def render_twin(t, notes):
    strength = esc(t.get("evidence_strength", ""))
    tasks_html = ""
    for tn in (notes or {}).get("tasks", []):
        tasks_html += (
            f"<li><strong>{esc(tn.get('task'))}</strong> "
            f"<span class='pill'>{esc(tn.get('outcome'))}</span>"
            f"<p>{esc(tn.get('narrative'))}</p></li>"
        )
    return f"""
<article class="card twin" id="twin-{esc(t['id'])}">
  <header>
    <h3>{esc(t.get('name'))}</h3>
    <span class="pill strength-{strength}">{strength} evidence ({esc(t.get('evidence_count', '?'))})</span>
    {'<span class="pill">' + esc(t.get('status')) + (' v' + esc(t.get('version')) if t.get('version') else '') + '</span>' if t.get('status') else ''}
  </header>
  <p class="muted">{esc(t.get('archetype'))}</p>
  <dl>
    <dt>Tech comfort</dt><dd>{esc(t.get('tech_comfort'))}</dd>
    <dt>Device</dt><dd>{esc(t.get('primary_device'))}</dd>
    <dt>Accessibility context</dt><dd>{esc(t.get('accessibility_context'))}</dd>
  </dl>
  <h4>Goals</h4>{render_list(t.get('goals'))}
  <h4>Pain points</h4>{render_list(t.get('pain_points'))}
  {'<h4>Walkthrough</h4><ul class="tasks">' + tasks_html + '</ul>' if tasks_html else ''}
</article>"""


def render_finding(f, twin_names):
    sev = esc(f.get("severity"))
    who = ", ".join(twin_names.get(i, i) for i in f.get("twins", []))
    wcag = ", ".join(f.get("wcag", []))
    return f"""
<article class="card finding sev-{sev}" data-sev="{sev}" data-lens="{esc(f.get('lens'))}">
  <header>
    <h4><span class="fid">{esc(f.get('id'))}</span> {esc(f.get('title'))}</h4>
    <span class="pill sev-{sev}">{sev}</span>
    <span class="pill">{esc(f.get('confidence'))}</span>
  </header>
  <p class="muted">{esc(LENS_LABEL.get(f.get('lens'), f.get('lens')))} &middot; {esc(f.get('where'))}{' &middot; WCAG ' + esc(wcag) if wcag else ''}</p>
  <p>{esc(f.get('what_happens'))}</p>
  <p><strong>Why it matters.</strong> {esc(f.get('why_it_matters'))}</p>
  <p><strong>Suggested change.</strong> {esc(f.get('recommendation'))}</p>
  {'<p class="muted">Affects: ' + esc(who) + '</p>' if who else ''}
</article>"""


CSS = """
:root{--bg:#f7f6f3;--fg:#1d1c1a;--muted:#5f5b55;--card:#fff;--line:#e3dfd8;--accent:#2f5d50;--accent-fg:#fff;
--blocker:#a3281f;--major:#b25e09;--minor:#7a6a00;--polish:#46606b}
@media (prefers-color-scheme:dark){:root{--bg:#171614;--fg:#efece6;--muted:#aaa59b;--card:#211f1c;--line:#37342f;--accent:#7fc0ad;--accent-fg:#10201b;
--blocker:#f08a80;--major:#f0b066;--minor:#e0cf6a;--polish:#9bb8c4}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:980px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:30px;margin:0 0 4px}h2{font-size:22px;margin:40px 0 12px}h3{font-size:18px;margin:0}h4{font-size:15px;margin:14px 0 4px}
.muted{color:var(--muted);margin:2px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:12px 0}
.card header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.card header h3,.card header h4{flex:1 1 60%}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 10px;font-size:13px;color:var(--muted)}
.pill.sev-blocker{color:var(--blocker);border-color:var(--blocker)}.pill.sev-major{color:var(--major);border-color:var(--major)}
.pill.sev-minor{color:var(--minor);border-color:var(--minor)}.pill.sev-polish{color:var(--polish);border-color:var(--polish)}
.finding{border-left:5px solid var(--line)}
.finding.sev-blocker{border-left-color:var(--blocker)}.finding.sev-major{border-left-color:var(--major)}
.finding.sev-minor{border-left-color:var(--minor)}.finding.sev-polish{border-left-color:var(--polish)}
.fid{font-variant-numeric:tabular-nums;color:var(--muted);margin-right:6px}
dl{display:grid;grid-template-columns:max-content 1fr;gap:2px 14px;margin:8px 0;font-size:14px}dt{color:var(--muted)}dd{margin:0}
ul{margin:4px 0 4px 20px;padding:0}
.tasks{list-style:none;margin:0;padding:0}.tasks li{border-top:1px solid var(--line);padding:8px 0}.tasks p{margin:4px 0 0;font-size:14px}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 12px}
.filters button{appearance:none;-webkit-appearance:none;font:inherit;font-size:14px;color:var(--fg);background:var(--card);
border:1px solid var(--line);border-radius:999px;padding:6px 14px;cursor:pointer;min-height:36px}
.filters button:hover{border-color:var(--accent)}
.filters button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.filters button[aria-pressed=true]{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}
.limits{border-left:5px solid var(--polish)}
a{color:var(--accent)}
"""

JS = """
const state={sev:'all',lens:'all'};
function apply(){document.querySelectorAll('.finding').forEach(el=>{
 const ok=(state.sev==='all'||el.dataset.sev===state.sev)&&(state.lens==='all'||el.dataset.lens===state.lens);
 el.hidden=!ok;});}
document.querySelectorAll('.filters').forEach(group=>{
 group.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  state[group.dataset.kind]=b.dataset.value;
  group.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));apply();});});
"""


def build(twins, data, title):
    names = {t["id"]: t.get("name", t["id"]) for t in twins}
    notes = {n["twin_id"]: n for n in data.get("twin_notes", [])}
    findings = sorted(
        data.get("findings", []),
        key=lambda f: (SEV_ORDER.index(f.get("severity", "polish")) if f.get("severity") in SEV_ORDER else 9,
                       -len(f.get("twins", []))),
    )
    counts = {s: sum(1 for f in findings if f.get("severity") == s) for s in SEV_ORDER}
    sev_buttons = "<button type='button' data-value='all' aria-pressed='true'>All severities</button>" + "".join(
        f"<button type='button' data-value='{s}' aria-pressed='false'>{s} ({counts[s]})</button>" for s in SEV_ORDER)
    lens_buttons = "<button type='button' data-value='all' aria-pressed='true'>All lenses</button>" + "".join(
        f"<button type='button' data-value='{k}' aria-pressed='false'>{esc(v)}</button>" for k, v in LENS_LABEL.items())

    parts = [f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>{esc(title)}</title><style>{CSS}</style></head><body><main>"]
    parts.append(f"<h1>{esc(title)}</h1><p class='muted'>{esc(data.get('product'))} &middot; {esc(data.get('tested'))}</p>")
    parts.append(f"<p>{esc(data.get('summary'))}</p>")
    parts.append("<p class='muted'>" + " &middot; ".join(f"{counts[s]} {s}" for s in SEV_ORDER) + "</p>")
    if data.get("not_run"):
        parts.append(f"<p class='muted'>Not run: {esc(', '.join(data['not_run']))}</p>")

    parts.append("<h2>The twins</h2><div class='grid'>" + "".join(render_twin(t, notes.get(t["id"])) for t in twins) + "</div>")

    parts.append("<h2>Findings</h2>")
    parts.append(f"<div class='filters' data-kind='sev' role='group' aria-label='Filter by severity'>{sev_buttons}</div>")
    parts.append(f"<div class='filters' data-kind='lens' role='group' aria-label='Filter by lens'>{lens_buttons}</div>")
    parts.append("".join(render_finding(f, names) for f in findings) or "<p class='muted'>No findings recorded.</p>")

    if data.get("tensions"):
        parts.append("<h2>Tensions between twins</h2>" + render_list(data["tensions"]))
    if data.get("what_works"):
        parts.append("<h2>What works</h2>" + render_list(data["what_works"]))
    if data.get("open_questions"):
        parts.append("<h2>Questions for real users</h2>" + "".join(
            f"<article class='card'><strong>{esc(q.get('question'))}</strong>"
            f"<p class='muted'>{esc(q.get('method'))} &middot; {esc(q.get('why'))}</p></article>"
            for q in data["open_questions"]))
    parts.append(f"<h2>Limits</h2><article class='card limits'><p>{esc(data.get('limits', 'Twins are synthetic and built from public online discussion. Treat findings as hypotheses to confirm with real users.'))}</p></article>")
    parts.append(f"</main><script>{JS}</script></body></html>")
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--twins", required=True, help="folder of twin .md files")
    ap.add_argument("--findings", required=True, help="findings.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Twinzies evaluation")
    a = ap.parse_args()
    twins = load_twins(a.twins)
    if not twins:
        sys.exit(f"No twin files with an 'id' found in {a.twins}")
    data = json.loads(Path(a.findings).read_text(encoding="utf-8"))
    Path(a.out).write_text(build(twins, data, a.title), encoding="utf-8")
    print(f"Wrote {a.out} ({len(twins)} twins, {len(data.get('findings', []))} findings)")


if __name__ == "__main__":
    main()
