# Exporting a journey map to FigJam, MURAL and Miro

Run `python scripts/export_journey.py --in journey.json --out-dir export/` (add `--blueprint` for backstage lanes). It writes five files. Pick by tool and by how editable you need the result.

| File | Best for | How to use |
|---|---|---|
| `stickies-grid.csv` | Editable stickies in **MURAL** or **Miro** | Open in Sheets or Excel, select all cells, copy, paste onto the board. Per each tool's help, pasting spreadsheet cells creates a sticky (or text box in MURAL) per cell. Group and colour by lane afterward. |
| `stickies-grid.csv` | **FigJam** | File > Import from CSV (or drag the file in). FigJam imports it as a table; select the table, open quick actions (Cmd/Ctrl + /), and choose Convert to Stickies. FigJam tables have a cell limit, so for a big map import one lane at a time or use `journey-table.csv`. |
| `journey-table.csv` | A compact FigJam table, Sheets or Notion | One cell per lane and stage, items joined with " | ". |
| `journey-flat.csv` | Filtering, Airtable, spreadsheets, feeding the Twinzies insight log | One row per item with stage, lane, severity, confidence, evidence. |
| `journey-map.svg` | A reference picture on any board | Drag onto the canvas. It is an image, so it is not editable; use it beside the editable stickies. |
| `board.json` | Native build and scripting | Neutral spec of sections, stickies and text with positions, sizes and colours (see below). |

## Colour convention (set it by hand after pasting; CSV cannot carry colour)
Actions yellow, thoughts blue, touchpoints purple, pain points pink, opportunities green, backstage orange, emotion and evidence grey. `board.json` carries these colours.

## Native FigJam board through the Figma connector
If the Figma connector is available in the session: load the figma skills the connector asks for, create a FigJam file, then create one section per stage and one sticky per `board.json` item (positions and colours are in the file). Confirm the file with the user before creating it, since it lands in their Figma account. If the connector is missing, use the CSV route above.

## Miro and MURAL by API (optional, user-supplied token)
`board.json` maps one-to-one to sticky notes, shapes and frames in the Miro and MURAL REST APIs. Only do this if the user supplies a board ID and a token they control, and never store or echo the token. Check each API's current docs first; the skill does not include a tested API client.

## Notes
- Keep sticky text short; the exporter keeps full text, so shorten in the JSON if a board gets cramped.
- Mark the map as hypothesis in the board title when it comes from twins.
- Re-export after edits; the JSON is the source of truth.
