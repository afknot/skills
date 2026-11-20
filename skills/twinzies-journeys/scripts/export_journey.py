#!/usr/bin/env python3
"""Export a journey map (journey.json) for FigJam, MURAL, Miro and spreadsheets.

  python export_journey.py --in journey.json --out-dir export/ [--blueprint] [--map N]

Writes (standard library only):
  stickies-grid.csv   one sticky per cell, laid out as lanes x stages. Paste into MURAL or Miro (each cell becomes a sticky),
                      or import into FigJam (File > Import from CSV makes a table; "Convert to Stickies" turns cells into stickies).
  journey-table.csv   compact table, one cell per lane and stage (items joined with " | "). Good for a FigJam table or Sheets.
  journey-flat.csv    one row per item: stage, lane, text, severity, confidence, evidence. For filtering, Airtable, Sheets.
  journey-map.svg     the whole map as a picture. Drop onto any board as a reference image (not editable).
  board.json          neutral board spec: sections, stickies, text and connectors with x/y/size/colour. Used to build a native
                      FigJam board through the Figma connector, or to script Miro/MURAL via their APIs.
Only the first map is exported unless --map picks another (overlays export as separate files).
"""
import argparse, csv, html, json, os, textwrap

LANES = [("Actions", "actions"), ("Thoughts", "thoughts"), ("Touchpoints", "touchpoints"), ("Pain points", "pain_points"), ("Opportunities", "opportunities")]
BLUEPRINT = [("Backstage", "backstage"), ("Systems", "systems"), ("Policies", "policies")]
COLORS = {"Emotion": "#e9e5dc", "Actions": "#fff2a8", "Thoughts": "#cfe6ff", "Touchpoints": "#e3dbf5", "Pain points": "#ffc9c9", "Opportunities": "#c9f0d2",
          "Backstage": "#ffe1b8", "Systems": "#d9d9d9", "Policies": "#d9d9d9", "Evidence": "#f4efe9"}
EMO = {-2: "very frustrated", -1: "uneasy", 0: "neutral", 1: "positive", 2: "delighted"}

def text(it):
    if isinstance(it, dict):
        s = it.get("text", ""); sev = it.get("severity")
        return f"{s} [{sev}]" if sev else s
    return str(it)

def lanes(m, bp):
    L = [("Emotion", None)] + LANES + (BLUEPRINT if bp else []) + [("Evidence", None)]
    return L

def items(st, lane, key):
    if lane == "Emotion":
        v = st.get("emotion", 0); return [f"{v:+d} {EMO.get(v, '')}" + (f": {st['emotion_note']}" if st.get("emotion_note") else "")]
    if lane == "Evidence":
        return [f"{', '.join(st.get('evidence', [])) or 'no evidence'} ({st.get('confidence', 'assumed')})"]
    return [text(x) for x in st.get(key, []) or []]

def stickies_grid(m, bp, path):
    st = m["stages"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow([""] + [f"{i+1}. {s['name']}" for i, s in enumerate(st)])
        for lane, key in lanes(m, bp):
            cols = [items(s, lane, key) for s in st]; n = max(1, max(len(c) for c in cols))
            for r in range(n): w.writerow([lane if r == 0 else ""] + [c[r] if r < len(c) else "" for c in cols])

def table(m, bp, path):
    st = m["stages"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow([""] + [f"{i+1}. {s['name']}" for i, s in enumerate(st)])
        for lane, key in lanes(m, bp): w.writerow([lane] + [" | ".join(items(s, lane, key)) for s in st])

def flat(m, bp, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["map", "persona", "stage_no", "stage", "lane", "text", "severity", "emotion", "confidence", "evidence"])
        for i, s in enumerate(m["stages"], 1):
            for lane, key in lanes(m, bp):
                if lane == "Evidence": continue
                for it in (items(s, lane, key) if lane == "Emotion" else s.get(key, []) or []):
                    sev = it.get("severity", "") if isinstance(it, dict) else ""
                    w.writerow([m.get("title", ""), m.get("persona", {}).get("name", ""), i, s["name"], lane, (it if lane == "Emotion" else text(it).replace(f" [{sev}]", "") if sev else text(it)),
                                sev, s.get("emotion", ""), s.get("confidence", ""), "; ".join(s.get("evidence", []))])

# ---- layout shared by SVG and board.json ----
COLW, GAP, LABW, PAD, LH, CH = 240, 16, 120, 24, 15, 12  # col width, gap, label width, padding, line height, chars factor

def wrap(s, width_px): return textwrap.wrap(s, max(12, int(width_px / 6.6))) or [""]

def layout(m, bp):
    st = m["stages"]; y = PAD + 88; cards = []; lane_boxes = []
    for lane, key in lanes(m, bp):
        cols = [items(s, lane, key) for s in st]; n = max(1, max(len(c) for c in cols))
        heights = [[len(wrap(t, COLW - 24)) * LH + 18 for t in c] for c in cols]
        lane_h = max(sum(h) + GAP * max(0, len(h) - 1) for h in heights) + 2 * 12 if any(cols) else 40
        lane_boxes.append((lane, y, lane_h))
        for ci, c in enumerate(cols):
            yy = y + 12
            for t, h in zip(c, heights[ci]):
                cards.append({"lane": lane, "stage": ci, "text": t, "x": LABW + PAD + ci * (COLW + GAP) + 6, "y": yy, "w": COLW - 12, "h": h, "color": COLORS.get(lane, "#fff")}); yy += h + GAP
        y += lane_h + 10
    return cards, lane_boxes, y

def svg(m, bp, path):
    cards, boxes, H = layout(m, bp); n = len(m["stages"]); W = LABW + PAD * 2 + n * (COLW + GAP)
    e = lambda s: html.escape(s, quote=True)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H+20}" width="{W}" height="{H+20}" font-family="Helvetica,Arial,sans-serif" role="img" aria-label="{e(m.get("title","Journey map"))}">',
         f'<rect width="{W}" height="{H+20}" fill="#faf8f4"/><text x="{PAD}" y="34" font-size="22" font-weight="700" fill="#1d1b18">{e(m.get("title",""))}</text>',
         f'<text x="{PAD}" y="56" font-size="12" fill="#5d5851">{e(m.get("persona",{}).get("name",""))} · hypothesis · {e(m.get("scenario",""))[:120]}</text>']
    for i, s in enumerate(m["stages"]):
        x = LABW + PAD + i * (COLW + GAP)
        o.append(f'<rect x="{x}" y="{PAD+50}" width="{COLW}" height="26" rx="6" fill="#1d1b18"/><text x="{x+10}" y="{PAD+68}" font-size="13" font-weight="600" fill="#fff">{i+1}. {e(s["name"])[:28]}</text>')
    for lane, y, h in boxes:
        o.append(f'<rect x="{PAD}" y="{y}" width="{W-2*PAD}" height="{h}" rx="8" fill="#fff" stroke="#ddd7cc"/><text x="{PAD+10}" y="{y+22}" font-size="12" font-weight="700" fill="#5d5851">{e(lane)}</text>')
    for c in cards:
        o.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="4" fill="{c["color"]}" stroke="#00000022"/>')
        for k, ln in enumerate(wrap(c["text"], COLW - 24)): o.append(f'<text x="{c["x"]+8}" y="{c["y"]+16+k*LH}" font-size="11.5" fill="#1d1b18">{e(ln)}</text>')
    return open(path, "w", encoding="utf-8").write("".join(o) + "</svg>")

def board(m, bp, path):
    cards, boxes, H = layout(m, bp); n = len(m["stages"])
    items_ = [{"type": "text", "text": m.get("title", ""), "x": PAD, "y": 10, "w": 800, "h": 40, "style": "title"}]
    for i, s in enumerate(m["stages"]):
        items_.append({"type": "section", "text": f"{i+1}. {s['name']}", "x": LABW + PAD + i * (COLW + GAP), "y": PAD + 50, "w": COLW, "h": H - PAD - 50, "color": "#f4efe9"})
    for lane, y, h in boxes: items_.append({"type": "text", "text": lane, "x": PAD, "y": y + 8, "w": LABW - 10, "h": 24, "style": "lane-label"})
    for c in cards: items_.append({"type": "sticky", "text": c["text"], "x": c["x"], "y": c["y"], "w": c["w"], "h": c["h"], "color": c["color"], "lane": c["lane"], "stage": c["stage"] + 1})
    for i in range(n - 1): items_.append({"type": "connector", "from_stage": i + 1, "to_stage": i + 2, "note": "optional arrow between stage headers"})
    json.dump({"title": m.get("title", ""), "units": "px", "source": "twinzies-journeys", "legend": {k: v for k, v in COLORS.items()}, "items": items_}, open(path, "w"), indent=1)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="i", required=True); ap.add_argument("--out-dir", required=True)
    ap.add_argument("--blueprint", action="store_true"); ap.add_argument("--map", type=int, default=1)
    a = ap.parse_args(); d = json.load(open(a.i)); maps = d if isinstance(d, list) else [d]; m = maps[a.map - 1]; os.makedirs(a.out_dir, exist_ok=True)
    stickies_grid(m, a.blueprint, f"{a.out_dir}/stickies-grid.csv"); table(m, a.blueprint, f"{a.out_dir}/journey-table.csv"); flat(m, a.blueprint, f"{a.out_dir}/journey-flat.csv")
    svg(m, a.blueprint, f"{a.out_dir}/journey-map.svg"); board(m, a.blueprint, f"{a.out_dir}/board.json")
    print("Wrote 5 files to", a.out_dir)
