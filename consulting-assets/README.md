# Consulting Assets

Owned assets that turn the learning guide into client-ready work. Percentages are stored as fractions; blue text = inputs, black = formulas, green = links, yellow = cells to fill.

| File | What it is | Guide |
|---|---|---|
| `Syndicate-Benchmark.xlsx` | Peer benchmark of Lloyd's syndicates from public accounts, with verified pilot data (Syndicates 4444, 1084, 3000 and the Lloyd's market) and a peer view | Module 27 |
| `London-Market-Value-Model.xlsx` | Plan → combined ratio → profit → uSCR/ECA → return on capital, with levers, lever value and sensitivity | Module 27 |
| `Diagnostic-Scorecards.xlsx` | Delegated authority diagnostic, AI readiness diagnostic, coverholder tiering, AI use-case prioritisation | Module 28 |

Rebuild from source: `python3 tools/build_assets.py` (then open in Excel or recalculate with LibreOffice).
Extend the benchmark: `python3 tools/extract_syndicate_metrics.py <folder-of-syndicate-pdfs> <output.csv>`, then verify every figure before adding it.
