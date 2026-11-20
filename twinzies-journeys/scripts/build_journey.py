#!/usr/bin/env python3
"""Render journey map(s) from JSON into one self-contained, accessible HTML file.

  python build_journey.py --in journey.json --out journey.html [--blueprint]

--in may hold one map (object) or several (list, same stage names) for an overlay.
Standard library only. No external requests.
"""
import argparse, html, json, sys

def e(x): return html.escape(str(x), quote=True)
COLORS = ["#1b6b5a", "#a6492b", "#5b4a9a", "#8a6d12"]
CONF = {"observed": "Observed", "reported": "Reported", "inferred": "Inferred", "assumed": "Assumed"}
EMO = {-2: "very frustrated", -1: "uneasy", 0: "neutral", 1: "positive", 2: "delighted"}

def curve(maps):
    n = len(maps[0]["stages"]); W = max(640, 150 * n); H = 200; pad = 60
    xs = [pad + i * (W - 2 * pad) / max(1, n - 1) for i in range(n)]
    y = lambda v: 20 + (2 - v) * (H - 40) / 4
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="ct cd" class="curve"><title id="ct">Emotion curve</title>']
    desc = []
    for gi, v in enumerate([-2, -1, 0, 1, 2]):
        s.append(f'<line x1="{pad-20}" x2="{W-pad+20}" y1="{y(v)}" y2="{y(v)}" class="grid{" zero" if v==0 else ""}"/>')
        s.append(f'<text x="8" y="{y(v)+4}" class="ax">{v:+d}</text>')
    for mi, m in enumerate(maps):
        c = COLORS[mi % len(COLORS)]
        pts = [(xs[i], y(st.get("emotion", 0))) for i, st in enumerate(m["stages"])]
        d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts)
        s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, (a, b) in enumerate(pts):
            s.append(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="5.5" fill="{c}" stroke="var(--panel)" stroke-width="2"/>')
        name = m.get("persona", {}).get("name", f"Map {mi+1}")
        desc.append(name + ": " + "; ".join(f'{st["name"]} {EMO.get(st.get("emotion",0),"")}' for st in m["stages"]))
    s.append(f'<desc id="cd">{e(" | ".join(desc))}</desc></svg>')
    return "".join(s)

def ul(items, key=None):
    if not items: return '<p class="muted">None recorded</p>'
    out = "<ul>"
    for it in items:
        if isinstance(it, dict):
            sev = it.get("severity")
            out += f'<li>{e(it.get("text",""))}' + (f' <span class="pill sev-{e(sev)}">{e(sev)}</span>' if sev else "") + "</li>"
        else: out += f"<li>{e(it)}</li>"
    return out + "</ul>"

def grid(m, blueprint):
    rows = [("Actions", "actions"), ("Thoughts", "thoughts"), ("Touchpoints", "touchpoints"), ("Pain points", "pain_points"), ("Opportunities", "opportunities")]
    if blueprint: rows += [("Backstage", "backstage"), ("Systems", "systems"), ("Policies", "policies")]
    t = '<div class="scroll"><table><thead><tr><th scope="col"><span class="sr">Row</span></th>'
    for i, st in enumerate(m["stages"]): t += f'<th scope="col">{i+1}. {e(st["name"])}</th>'
    t += "</tr></thead><tbody>"
    t += '<tr><th scope="row">Emotion</th>' + "".join(
        f'<td><strong>{st.get("emotion",0):+d}</strong> {e(EMO.get(st.get("emotion",0),""))}<br><span class="muted small">{e(st.get("emotion_note",""))}</span></td>' for st in m["stages"]) + "</tr>"
    for label, key in rows:
        t += f'<tr><th scope="row">{label}</th>' + "".join(f"<td>{ul(st.get(key))}</td>" for st in m["stages"]) + "</tr>"
    t += '<tr><th scope="row">Evidence</th>' + "".join(
        f'<td>{e(", ".join(st.get("evidence", [])) or "none")}<br><span class="pill conf-{e(st.get("confidence","assumed"))}">{e(CONF.get(st.get("confidence","assumed"),"Assumed"))}</span></td>' for st in m["stages"]) + "</tr>"
    return t + "</tbody></table></div>"

def opp_rank(maps):
    c = {}
    for m in maps:
        for st in m["stages"]:
            n = len(st.get("pain_points", []))
            for o in st.get("opportunities", []): c.setdefault(o, 0); c[o] += max(1, n)
    return sorted(c.items(), key=lambda kv: -kv[1])

def build(maps, blueprint):
    m0 = maps[0]
    h = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(m0.get("title","Journey map"))}</title><style>{CSS}</style></head><body><main>']
    h.append(f'<header><p class="eyebrow">Journey map{" with blueprint" if blueprint else ""}</p><h1>{e(m0.get("title",""))}</h1>')
    h.append(f'<p class="muted">Product: {e(m0.get("product","-"))} · Scope: {e(m0.get("scope","-"))}</p></header>')
    h.append('<p class="note" role="note"><strong>Hypothesis, not research.</strong> Maps built from personas, forum evidence or inference should be confirmed with real users before big decisions.</p>')
    h.append('<section aria-labelledby="who"><h2 id="who">Who and why</h2><ul class="legend">')
    for i, m in enumerate(maps):
        p = m.get("persona", {})
        h.append(f'<li><span class="swatch" style="background:{COLORS[i%len(COLORS)]}"></span><strong>{e(p.get("name","Persona"))}</strong> <span class="pill">{e(p.get("status","hypothesis"))}</span> · {e(m.get("scenario",""))} <em>Goal: {e(m.get("goal",""))}</em></li>')
    h.append("</ul></section>")
    h.append(f'<section aria-labelledby="ec"><h2 id="ec">Emotion curve</h2>{curve(maps)}<p class="muted small">Scale: +2 delighted to -2 very frustrated. A table below gives the same values in text.</p></section>')
    for i, m in enumerate(maps):
        h.append(f'<section aria-labelledby="g{i}"><h2 id="g{i}">{e(m.get("persona",{}).get("name","Map"))}: stage by stage</h2>{grid(m, blueprint)}</section>')
    mot = [x for m in maps for x in m.get("moments_of_truth", [])]
    h.append('<section aria-labelledby="mt"><h2 id="mt">Moments of truth</h2>' + ul(mot) + "</section>")
    rk = opp_rank(maps)
    h.append('<section aria-labelledby="op"><h2 id="op">Opportunities, most pain points addressed first</h2><ol>' + "".join(f"<li>{e(o)} <span class='muted small'>({n} pain point{'s' if n!=1 else ''})</span></li>" for o, n in rk) + "</ol></section>")
    nv = [x for m in maps for x in m.get("not_validated", [])]
    h.append('<section aria-labelledby="nv"><h2 id="nv">Not validated</h2>' + ul(nv) + f'<p><strong>Next research:</strong> {e(m0.get("next_research","define a validation step"))}</p></section>')
    h.append("</main></body></html>")
    return "".join(h)

CSS = """:root{--bg:#faf8f4;--panel:#fff;--fg:#1d1b18;--muted:#5d5851;--line:#ddd7cc;--accent:#1b6b5a}
@media (prefers-color-scheme:dark){:root{--bg:#161513;--panel:#201f1c;--fg:#efece6;--muted:#aaa59b;--line:#38352f;--accent:#7fc0ad}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 20px 60px}h1{font-size:28px;margin:4px 0}h2{font-size:19px;margin:30px 0 10px}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:12px;color:var(--muted);margin:0}.muted{color:var(--muted)}.small{font-size:13px}
.note{border:1px solid var(--line);border-left:4px solid var(--accent);background:var(--panel);padding:10px 14px;border-radius:8px}
.curve{width:100%;height:auto;background:var(--panel);border:1px solid var(--line);border-radius:12px}.grid{stroke:var(--line)}.grid.zero{stroke:var(--muted);stroke-dasharray:4 4}.ax{fill:var(--muted);font-size:11px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--panel)}table{border-collapse:collapse;min-width:900px;width:100%}
th,td{border:1px solid var(--line);padding:10px;vertical-align:top;text-align:left;font-size:14px}thead th{background:var(--bg);position:sticky;top:0}tbody th{background:var(--bg);width:110px}
td ul{margin:0;padding-left:18px}.sr{position:absolute;left:-9999px}
.pill{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;border:1px solid var(--line);background:var(--bg)}
.sev-high{border-color:#b3261e;color:#b3261e}.sev-med{border-color:#8a6d12;color:#8a6d12}.conf-observed{border-color:var(--accent);color:var(--accent)}
.legend{list-style:none;padding:0}.legend li{margin:6px 0}.swatch{display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:8px;vertical-align:-2px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
@media print{.scroll{overflow:visible}body{background:#fff;color:#000}}"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="inp", required=True); ap.add_argument("--out", required=True); ap.add_argument("--blueprint", action="store_true")
    a = ap.parse_args(); d = json.load(open(a.inp)); maps = d if isinstance(d, list) else [d]
    names = [[s["name"] for s in m["stages"]] for m in maps]
    if any(n != names[0] for n in names): sys.exit("Overlay maps must share the same stage names")
    open(a.out, "w").write(build(maps, a.blueprint)); print("Wrote", a.out)
