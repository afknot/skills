#!/usr/bin/env python3
"""Build the Twinzies dashboard (one self-contained HTML file) from a twin library folder.

Usage: python build_dashboard.py --library twinzies-library --out dashboard.html [--title "Twinzies"]

Reads: twins/*.md, data/{evidence,studies,insights,solutions}.json, changelog.md.
Missing data files are treated as empty. Standard library only.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    data, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or line.lstrip().startswith("- "):
            it = line.strip()
            if it.startswith("- ") and key:
                data.setdefault(key, []).append(it[2:].strip().strip('"'))
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            key, v = k.strip(), re.sub(r"\s+#.*$", "", v.strip())
            if v == "":
                data[key] = []
            elif v.startswith("[") and v.endswith("]"):
                data[key] = [s.strip().strip('"') for s in v[1:-1].split(",") if s.strip()]
            else:
                data[key] = v.strip('"')
    return data, m.group(2)


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def bullets(txt):
    return [l[2:].strip() for l in (txt or "").splitlines() if l.startswith("- ")]


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--library", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Twinzies")
    a = ap.parse_args()
    lib = Path(a.library)
    twins = []
    for p in sorted((lib / "twins").glob("*.md")):
        meta, body = fm(p.read_text(encoding="utf-8"))
        if not meta.get("id"):
            continue
        sec = sections(body)
        meta["who"] = sec.get("Who they are", "")
        meta["validation_log"] = bullets(sec.get("Validation log"))
        meta["changelog"] = bullets(sec.get("Changelog"))
        av = lib / "avatars" / f"{meta['id']}.svg"
        meta["avatar"] = av.read_text(encoding="utf-8") if av.exists() else ""
        twins.append(meta)
    log = []
    cl = lib / "changelog.md"
    if cl.exists():
        for l in cl.read_text(encoding="utf-8").splitlines():
            if l.startswith("- "):
                parts = [x.strip() for x in l[2:].split("|", 2)]
                log.append({"date": parts[0], "scope": parts[1] if len(parts) > 2 else "", "text": parts[-1]})
    data = {
        "title": a.title,
        "twins": twins,
        "evidence": load_json(lib / "data/evidence.json"),
        "studies": load_json(lib / "data/studies.json"),
        "insights": load_json(lib / "data/insights.json"),
        "solutions": load_json(lib / "data/solutions.json"),
        "log": log,
        "playbook": load_json(HERE.parent / "assets/playbook.json"),
    }
    tpl = (HERE / "dashboard_template.html").read_text(encoding="utf-8")
    html = tpl.replace("__TITLE__", a.title).replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
    Path(a.out).write_text(html, encoding="utf-8")
    print(f"Wrote {a.out}: {len(twins)} twins, {len(data['studies'])} studies, {len(data['insights'])} insights, {len(data['solutions'])} solutions")


if __name__ == "__main__":
    main()
