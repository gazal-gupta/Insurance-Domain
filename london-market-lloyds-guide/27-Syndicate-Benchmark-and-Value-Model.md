# Module 27 – Your Own Data: Syndicate Benchmark and Value Model

| | |
|---|---|
| **Level** | Champion – owned consulting assets |
| **Assets** | `consulting-assets/Syndicate-Benchmark.xlsx`, `consulting-assets/London-Market-Value-Model.xlsx`, `tools/extract_syndicate_metrics.py` |
| **Time** | 2 hours to learn; 6–8 weeks to build the full benchmark (about 100 syndicates × 5 years) |
| **You will be able to** | Build and maintain a peer benchmark from public syndicate accounts; walk into a meeting with the client's numbers next to its peers'; size any recommendation in combined ratio points, profit, capital and return on capital |

---

## 1. Why owned data makes you a leader

Top-tier firms win London market work by arriving with **facts the client has not assembled about itself**: how its ratios compare with peers, where the gap is, and what closing it is worth. Public syndicate accounts make this possible for anyone willing to do the work – most consultants are not. At 31 December 2025 there were **103 syndicates managed by 57 managing agents**, and 2026 started with record stamp capacity of about **£58.2bn** **[likely]**. A benchmark of all of them is a durable, defensible asset.

---

## 2. The benchmark workbook

### 2.1 Structure

| Sheet | Purpose |
|---|---|
| **Read me** | Purpose, method, caveats, legend |
| **Data** | One row per syndicate per year: GWP, net earned premium, claims ratio, acquisition, admin, total expense ratio, reported and calculated combined ratio, check, profit, underwriting result, source document and location, verified flag |
| **Peer view** | Type a syndicate number and year: see its ratios against the average of the other syndicates in the dataset and the Lloyd's market, the gap in points, and the value of the gap |
| **Definitions** | What each field means and what to watch for |

### 2.2 Pilot data (verified by hand against the published reports)

| Syndicate | Managing agent | Year | Combined ratio | Claims ratio | Expense ratio | Notes |
|---|---|---|---|---|---|---|
| 4444 | Canopius | 2025 | 86.1% | 51.6% | 34.5% (acquisition 29.9% + admin 4.6%) | GWP $3,870m; profit $479.5m |
| 4444 | Canopius | 2024 | 86.3% | 51.3% | 35.0% | |
| 1084 | Chaucer | 2025 | 88.2% | 52.2% | 36.0% | GWP $2,455.5m |
| 1084 | Chaucer | 2024 | 85.6% | 51.4% | 34.2% | |
| 3000 | Markel | 2021–2025 | 95.1% → 84.9% | 54.5% → 38.7% | 40.6% → 46.2% | Presented in £m |
| Lloyd's market | — | 2024 / 2025 | 86.9% / 87.6% | — | — | Market benchmark |

Sources are recorded row by row in the workbook. Every pilot combined ratio equals its claims ratio plus expense ratio, which is the first quality check **[certain]** for these rows.

**Early insight from the pilot [likely]:** the three syndicates reach similar combined ratios through very different structures. Markel's Syndicate 3000 runs a low claims ratio with a high expense ratio (46%); Canopius 4444 runs a higher claims ratio with a lower expense ratio (35%). Benchmarking only the combined ratio would hide this – **always benchmark the parts**.

### 2.3 How to build the full benchmark

| Step | Action | Tool |
|---|---|---|
| 1 | List syndicates from Lloyd's syndicate reports and accounts pages; prioritise your target accounts ([Module 29](29-Account-Profiles-Top-25.md)) | lloyds.com |
| 2 | Download annual reports (calendar-year basis) for the last five years | Browser; managing agents' websites |
| 3 | Run the extractor on the folder | `python3 tools/extract_syndicate_metrics.py <folder> <out.csv>` |
| 4 | Review every figure against its captured source line and the PDF; watch for five-year tables (oldest year first), $000 vs $m, gross vs net ratios | Manual review |
| 5 | Enter rows into the Data sheet; set Verified = Y only after review | Excel |
| 6 | Add Lloyd's market rows for each year | Lloyd's results |
| 7 | Refresh each spring when new accounts are published | Annual cycle |

**Extractor behaviour (tested on four real reports):** it captured GWP, earned premium, claims, expense, acquisition and admin ratios, combined ratio and profit with source lines for Syndicates 4444, 1084 and 3000, flagged Syndicate 3000's five-year table, and correctly found little on an underwriting-year account (Syndicate 2525), which is a different basis and should not enter the calendar-year benchmark.

### 2.4 Analyses the benchmark unlocks

| Analysis | Question it answers |
|---|---|
| Combined ratio decomposition vs peers | Is the gap claims or expenses? |
| Expense ratio vs size | Is the client sub-scale? |
| Acquisition ratio vs channel mix | Is distribution cost the problem? |
| Five-year trend vs market | Is performance improving faster or slower than the market? |
| Volatility of results | Is the client taking more risk for its return? |
| Peer clusters (lead-heavy, DA-heavy, reinsurance, follow) | Who are the right peers? |

---

## 3. The value model

### 3.1 Structure

| Sheet | What it does |
|---|---|
| **Inputs** | Five classes with net earned premium, attritional, large and normalised catastrophe loss ratios, acquisition ratio and uSCR as % of NEP; global assumptions (operating expense ratio, prior-year development, investment yield, investable assets multiple, ECA uplift 35%, cost of capital, diversification, tax) |
| **Levers** | By class: keep or exit, volume growth, risk-adjusted rate change, selection improvement, acquisition change. Global: operating expense change, reinsurance capital relief and cost, scenario prior-year development |
| **Model** | Base vs scenario: premium, claims, acquisition, expenses, underwriting result, combined ratio, investment income, profit, uSCR, ECA, return on capital, economic profit, capital released |
| **Lever value** | Approximate standalone value of each lever |
| **Sensitivity** | Change in underwriting result for loss and expense ratio moves of ±3 points |

### 3.2 Example result (illustrative syndicate, not a real company)

| Measure | Base | Scenario | Change |
|---|---|---|---|
| Net earned premium | £1,000m | £751m | exit US casualty binders, rates falling |
| Combined ratio | 90.9% | 89.8% | −1.1 pts |
| Profit after tax | £107.6m | £82.8m | −£24.9m |
| ECA (Funds at Lloyd's) | £970m | £669m | £301m capital released |
| Return on capital | 11.1% | 12.4% | +1.3 pts |
| Economic profit | −£8.7m | +£2.5m | +£11.2m |

**The board insight:** the scenario makes **less profit but more value** – it releases £301m of capital and lifts return on capital above a 12% cost of capital. This is the conversation Lloyd's 2026–2030 strategy (return on capital above 12% across the cycle) invites **[likely]**, and the kind of insight that separates a partner from an analyst.

### 3.3 How to use it with a client

1. Load the client's plan by class from its SBF or management accounts.
2. Calibrate uSCR % by class to the client's capital model output.
3. Agree levers in a workshop with the CUO and CFO.
4. Present base vs scenario, lever value and the sensitivity grid.
5. Feed the outcome into the business plan and capital discussion with Lloyd's.

### 3.4 Model limits (say them out loud)

- Rate change affects loss ratio by price only; real rate changes also shift mix and terms.
- Capital is a simple % of premium with diversification; the real number comes from the internal model.
- Operating expenses scale with premium; in reality much is fixed, so class exits can raise the expense ratio.
- Investment income uses a single yield and asset multiple.

---

## 4. Partner's lens

1. **Lead every first meeting with the client's own numbers against peers.** One page: combined ratio parts vs peers and market, five-year trend, value of the gap.
2. **Never quote a benchmark you have not verified.** The Verified flag exists for a reason; one wrong peer number destroys trust.
3. **Show value, not just profit.** Return on capital and economic profit change the discussion from "how do we grow?" to "where do we earn our cost of capital?"
4. **Refresh annually and publish.** A yearly benchmark summary (anonymised and aggregated) becomes your signature research.

---

## 5. Practice tasks

1. Add five syndicates to the benchmark using the extractor and review process.
2. Run the Peer view for each target account and write a one-paragraph "so what".
3. Rebuild the value model for one real syndicate using public figures; test two scenarios.

---

## 6. Sources

- [Canopius – Syndicate 4444 Report and Accounts 2025](https://www.canopius.com/wp-content/uploads/25_S4444_Accounts_-_EY_Signed.pdf)
- [Chaucer – Syndicate 1084 Annual Report 2025](https://media.chaucergroup.com/documents/Chaucer_Syndicate_1084-2025.pdf)
- [Markel – Syndicate 3000 Report and Accounts 2025](https://content.markel.com/api/public/content/syndicate-3000-reports-accounts-signed)
- [Lloyd's full year results 2025](https://www.lloyds.com/insights/media-centre/press-releases/lloyds-announces-full-year-results-2025)
- [LMA – Lloyd's 2026 Insights Report (market structure)](https://lmalloyds.com/lloyds-investor-appeal-stays-high-backed-by-strong-syndicate-performance-reveals-lloyds-2026-insights-report/)
- [Lloyd's – syndicate reports and accounts](https://www.lloyds.com/about-lloyds/investor-relations/financial-performance/syndicate-reports-and-accounts)
