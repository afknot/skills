# Library and dashboard

`sample-library/` shows the layout Twinzies keeps in your own folder: `twins/`, `evidence/`, `data/*.json` (evidence → insights → solutions → decisions), `avatars/`, `changelog.md`. Decisions and statuses here are **sample data**.

Open `dashboard.html` in a browser (works offline). Rebuild it any time:

```bash
python skills/twinzies/scripts/build_dashboard.py --library examples/04-library-and-dashboard/sample-library --out dashboard.html
```

Record a decision: `python skills/twinzies/scripts/lib_decide.py decide S3 --status backlog --note "after launch"`.
