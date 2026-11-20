#!/usr/bin/env python3
"""Normalize and summarize app store reviews for Twinzies evidence. Standard library only.

  python parse_reviews.py --in reviews.csv|reviews.json [--store play|apple|auto] [--out-dir reviews/] [--themes themes.json] [--app "Name"]

Accepts: Google Play Console review export (CSV), a saved Apple customer-reviews JSON feed,
or any CSV/TSV with rating and text columns (columns found by name). Drops reviewer names and contact
fields, redacts emails/phones/@handles in text, de-duplicates, and writes reviews.json, summary.json and evidence-draft.md.
It does not fetch anything from the network.
"""
import argparse, collections, csv, io, json, os, re, sys

DROP = re.compile(r"(author|reviewer ?name|user ?name|email|device|reviewer id|review id|link|url)", re.I)
STOP = set("the a an and or but to of in on for with is are was were it this that i my me we you they be have has had not no so if as at by from can will just do does did app apps get got use used using one all out up its im ive dont cant doesnt very really also more than then when what which there their them would could should".split())
THEMES = {"crash_or_bug": ["crash", "bug", "freez", "glitch", "stuck", "error"], "sync_or_data_loss": ["sync", "lost", "disappear", "backup", "data"],
          "slow": ["slow", "lag", "loading", "wait"], "price_or_paywall": ["subscription", "paywall", "price", "pay", "premium", "free"],
          "ads": ["ads", "advert"], "login_or_account": ["login", "log in", "sign in", "password", "account"], "search_or_find": ["search", "find"],
          "import_export": ["import", "export", "csv", "backup"], "scan_or_camera": ["scan", "barcode", "camera"], "accessibility": ["font", "text size", "contrast", "screen reader", "voiceover", "talkback", "zoom", "small"],
          "ui_confusing": ["confus", "can't find", "cannot find", "hard to", "unintuitive", "clunky"], "support": ["support", "developer", "response"]}

def redact(t):
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", t); t = re.sub(r"(?<!\w)@\w{2,}", "[handle]", t)
    t = re.sub(r"(?<!\d)(\+?\d[\d\s().-]{8,}\d)(?!\d)", "[number]", t); return t.strip()

def pick(row, *names):
    low = {k.lower().strip(): v for k, v in row.items()}
    for n in names:                      # names are in priority order: exact match first, then substring
        if n in low: return low[n]
    for n in names:
        for k, v in low.items():
            if n in k and not re.search(r"reviewer|language", k): return v
    return ""

def load(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    if raw.lstrip().startswith("{") or raw.lstrip().startswith("["):
        d = json.loads(raw); ent = d.get("feed", {}).get("entry", d) if isinstance(d, dict) else d
        if isinstance(ent, dict): ent = [ent]
        out = []
        for e in ent:
            if "im:rating" not in e and "rating" not in e: continue
            g = lambda k: (e.get(k, {}).get("label") if isinstance(e.get(k), dict) else e.get(k, ""))
            out.append({"store": "apple", "rating": g("im:rating") or g("rating"), "title": g("title"), "text": g("content") or g("text"), "date": g("updated") or g("date"), "version": g("im:version") or g("version"), "reply": ""})
        return out
    dialect = csv.excel_tab if raw.split("\n", 1)[0].count("\t") > raw.split("\n", 1)[0].count(",") else csv.excel
    rows = []
    for r in csv.DictReader(io.StringIO(raw), dialect=dialect):
        rows.append({"store": "", "rating": pick(r, "star rating", "rating", "stars", "score"), "title": pick(r, "review title", "title"),
                     "text": pick(r, "review text", "text", "body", "content", "review"), "date": pick(r, "review submit date", "review last update date", "date", "updated", "created"),
                     "version": pick(r, "app version name", "version", "app version"), "reply": pick(r, "developer reply text", "reply", "response")})
    return rows

def month(d):
    m = re.search(r"(\d{4})[-/](\d{2})", d or ""); return f"{m.group(1)}-{m.group(2)}" if m else "unknown"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="i", required=True); ap.add_argument("--store", default="auto"); ap.add_argument("--out-dir", default="reviews")
    ap.add_argument("--themes"); ap.add_argument("--app", default=""); a = ap.parse_args()
    themes = json.load(open(a.themes)) if a.themes else THEMES
    rows = load(a.i); seen = set(); rv = []
    for r in rows:
        txt = redact(" ".join(x for x in [r["title"], r["text"]] if x).strip())
        try: rating = int(float(str(r["rating"]).strip()))
        except ValueError: continue
        if not txt: continue
        k = (rating, txt.lower()[:160])
        if k in seen: continue
        seen.add(k); st = r["store"] or (a.store if a.store != "auto" else "unknown")
        rv.append({"store": st, "rating": rating, "date": (r["date"] or "")[:10], "month": month(r["date"]), "version": r["version"] or "", "text": txt, "developer_replied": bool(r["reply"])})
    os.makedirs(a.out_dir, exist_ok=True); json.dump(rv, open(f"{a.out_dir}/reviews.json", "w"), indent=1)
    cnt = lambda f: dict(collections.Counter(f(x) for x in rv).most_common())
    words = collections.Counter(w for x in rv for w in re.findall(r"[a-z']{3,}", x["text"].lower()) if w not in STOP)
    tally = {}
    for t, kws in themes.items():
        hit = [x for x in rv if any(k in x["text"].lower() for k in kws)]
        if hit: tally[t] = {"n": len(hit), "avg_rating": round(sum(x["rating"] for x in hit) / len(hit), 2), "by_store": dict(collections.Counter(x["store"] for x in hit)), "versions": sorted({x["version"] for x in hit if x["version"]})[:8]}
    summ = {"n_reviews": len(rv), "by_store": cnt(lambda x: x["store"]), "by_rating": dict(sorted(cnt(lambda x: x["rating"]).items())), "by_month": dict(sorted(cnt(lambda x: x["month"]).items())),
            "by_version": cnt(lambda x: x["version"] or "unknown"), "top_terms": words.most_common(25), "themes": dict(sorted(tally.items(), key=lambda kv: -kv[1]["n"]))}
    json.dump(summ, open(f"{a.out_dir}/summary.json", "w"), indent=1)
    lines = [f"# Evidence draft: store reviews{(' for ' + a.app) if a.app else ''}", "", f"{len(rv)} reviews after de-duplication. Reviewer names and contact details were dropped. Paraphrase before use; a sample, not the whole store.", ""]
    for t, v in summ["themes"].items():
        lines.append(f"- store-review | {', '.join(v['by_store']) or 'unknown'} | theme: {t} | n: {v['n']} of {len(rv)} | avg rating {v['avg_rating']} | versions: {', '.join(v['versions']) or 'n/a'} | paraphrase: TODO")
    open(f"{a.out_dir}/evidence-draft.md", "w").write("\n".join(lines) + "\n")
    print(f"{len(rv)} reviews -> {a.out_dir}/ (reviews.json, summary.json, evidence-draft.md); themes found: {len(tally)}")

if __name__ == "__main__": main()
