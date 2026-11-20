#!/usr/bin/env python3
"""Record decisions and keep the Twinzies library consistent.

  python lib_decide.py LIB decide S1 --status accepted|backlog|dismissed|done|proposed [--note "why"]
  python lib_decide.py LIB check

`decide` updates data/solutions.json (status, decided date, note) and appends a line to changelog.md.
`check` validates ids and links across data/*.json and prints problems; exit code 1 if any.
Standard library only.
"""
import argparse, json, sys, datetime
from pathlib import Path

STATUSES = {"proposed", "accepted", "backlog", "dismissed", "done"}


def load(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def decide(lib, sid, status, note):
    f = lib / "data/solutions.json"
    sols = load(f, [])
    for s in sols:
        if s["id"] == sid:
            s["status"], s["note"] = status, note or s.get("note", "")
            s["decided"] = datetime.date.today().isoformat() if status != "proposed" else None
            f.write_text(json.dumps(sols, indent=1), encoding="utf-8")
            with (lib / "changelog.md").open("a", encoding="utf-8") as c:
                c.write(f"- {datetime.date.today().isoformat()} | {sid} | {s['title']}: {status}" + (f" ({note})" if note else "") + "\n")
            print(f"{sid} -> {status}")
            return 0
    print(f"No solution {sid}", file=sys.stderr)
    return 1


def check(lib):
    ev = {e["id"] for e in load(lib / "data/evidence.json", [])}
    ins = load(lib / "data/insights.json", [])
    sol = load(lib / "data/solutions.json", [])
    st = {s["id"] for s in load(lib / "data/studies.json", [])}
    twins = {p.stem for p in (lib / "twins").glob("*.md")}
    iid = {i["id"] for i in ins}
    bad = []
    for i in ins:
        bad += [f"{i['id']}: missing evidence {e}" for e in i.get("evidence", []) if e not in ev]
        bad += [f"{i['id']}: unknown twin {t}" for t in i.get("twins", []) if t not in twins]
        if i.get("study") and i["study"] not in st:
            bad.append(f"{i['id']}: unknown study {i['study']}")
    for s in sol:
        bad += [f"{s['id']}: unknown insight {x}" for x in s.get("insights", []) if x not in iid]
        if s.get("status") not in STATUSES:
            bad.append(f"{s['id']}: bad status {s.get('status')}")
    orphan = iid - {x for s in sol for x in s.get("insights", [])}
    for o in sorted(orphan):
        bad.append(f"{o}: insight feeds no solution (propose one or mark it noted)")
    print("\n".join(bad) or "OK")
    return 1 if [b for b in bad if "feeds no solution" not in b] else 0


ap = argparse.ArgumentParser()
ap.add_argument("library")
sp = ap.add_subparsers(dest="cmd", required=True)
d = sp.add_parser("decide"); d.add_argument("id"); d.add_argument("--status", required=True, choices=sorted(STATUSES)); d.add_argument("--note", default="")
sp.add_parser("check")
a = ap.parse_args()
lib = Path(a.library)
sys.exit(decide(lib, a.id, a.status, a.note) if a.cmd == "decide" else check(lib))
