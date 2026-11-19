#!/usr/bin/env python3
"""Build the consulting asset workbooks.

Outputs (in consulting-assets/):
  Syndicate-Benchmark.xlsx        – peer benchmark with verified pilot data and a peer view
  London-Market-Value-Model.xlsx  – plan → ratios → capital → return on capital, with levers
  Diagnostic-Scorecards.xlsx      – DA and bordereaux diagnostic, AI readiness, coverholder tiering,
                                    AI use-case prioritisation
Run: python3 tools/build_assets.py   then recalculate with LibreOffice before reading values.
"""
import pathlib

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "consulting-assets"
OUT.mkdir(exist_ok=True)

F = "Arial"
BASE = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
TITLE = Font(name=F, size=14, bold=True, color="14243A")
HEAD = Font(name=F, size=10, bold=True, color="FFFFFF")
INPUT = Font(name=F, size=10, color="0000FF")
LINK = Font(name=F, size=10, color="008000")
NOTE = Font(name=F, size=9, italic=True, color="5A6577")
HFILL = PatternFill("solid", fgColor="14243A")
YFILL = PatternFill("solid", fgColor="FFFF00")
GFILL = PatternFill("solid", fgColor="EDF0F4")
THIN = Side(style="thin", color="D8DEE6")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
PCT = "0.0%;(0.0%);-"
MONEY = "#,##0.0;(#,##0.0);-"
SCORE = "0.0"
WRAP = Alignment(wrap_text=True, vertical="top")


def style_all(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font == Font():  # untouched default
                c.font = BASE


def header(ws, row, labels, widths=None):
    for i, lab in enumerate(labels, start=1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font, c.fill, c.alignment, c.border = HEAD, HFILL, Alignment(wrap_text=True, vertical="center"), BOX
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w


def readme(ws, title, lines):
    ws["A1"] = title
    ws["A1"].font = TITLE
    ws.column_dimensions["A"].width = 120
    r = 3
    for ln in lines:
        c = ws.cell(row=r, column=1, value=ln)
        c.font = BOLD if ln and ln.isupper() else BASE
        c.alignment = Alignment(wrap_text=True)
        r += 1
    return r


LEGEND = [
    "LEGEND",
    "Blue text = hard-coded input or lever. Black text = formula. Green text = link to another sheet.",
    "Yellow fill = cells you should fill in or change. Do not overwrite black formula cells.",
    "Percentages are stored as fractions (0.876 shows as 87.6%).",
]

# ---------------------------------------------------------------- 1. Benchmark
def build_benchmark():
    wb = Workbook()
    ws = wb.active
    ws.title = "Read me"
    readme(ws, "Lloyd's Syndicate Benchmark", [
        "PURPOSE",
        "A peer benchmark of Lloyd's syndicates built from public syndicate annual reports and accounts, used to put a client's "
        "performance next to its peers before the first meeting (see guide Module 27).",
        "",
        "HOW TO EXTEND",
        "1. Download syndicate reports from lloyds.com (Syndicate reports and accounts) or managing agents' websites.",
        "2. Run: python3 tools/extract_syndicate_metrics.py <pdf-folder> <output.csv>",
        "3. Check every figure against its source line and the PDF, then add one row per syndicate per year on the Data sheet.",
        "4. Set Verified = Y only after a person has checked the figures against the report.",
        "",
        "PILOT DATA",
        "Pilot rows (Syndicates 4444, 1084, 3000 and the Lloyd's market) were taken from published 2025 reports and Lloyd's "
        "full-year results, and checked by hand: each combined ratio equals claims ratio plus expense ratio.",
        "",
        "CAVEATS",
        "Ratios are comparable across syndicates only on the same basis (annual accounts, net of reinsurance). Definitions differ: "
        "some reports show gross claims ratios or exclude acquisition costs. Amounts are in each syndicate's presentation currency – "
        "compare ratios, not amounts, across currencies. Underwriting-year (closed year) accounts are a different basis.",
        "",
    ] + LEGEND)

    d = wb.create_sheet("Data")
    cols = ["Key", "Syndicate", "Managing agent", "Owner group", "Year", "Basis", "Currency", "Units", "GWP", "Net earned premium",
            "Claims ratio (net)", "Acquisition ratio", "Admin / other expense ratio", "Total expense ratio",
            "Combined ratio (reported)", "Combined ratio (calc)", "Check: reported – calc", "Profit for year",
            "Underwriting result", "Source document", "Source location", "Verified", "Notes"]
    header(d, 1, cols, [14, 10, 26, 30, 7, 18, 9, 7, 11, 11, 10, 10, 10, 10, 11, 11, 10, 10, 11, 48, 30, 8, 40])
    d.freeze_panes = "B2"
    src4444 = "Syndicate 4444 Annual Report and Accounts 2025 – https://www.canopius.com/wp-content/uploads/25_S4444_Accounts_-_EY_Signed.pdf"
    src1084 = "Chaucer Syndicate 1084 Annual Report 2025 – https://media.chaucergroup.com/documents/Chaucer_Syndicate_1084-2025.pdf"
    src3000 = "Syndicate 3000 Report and Accounts 2025 – https://content.markel.com/api/public/content/syndicate-3000-reports-accounts-signed"
    srcLLY = "Lloyd's full-year results 2025 – https://www.lloyds.com/insights/media-centre/press-releases/lloyds-announces-full-year-results-2025"
    own4444 = "Samsung Fire & Marine (majority; KKR and KIC minority) – change of control reported Nov 2026"
    rows = [
        ["4444", "Canopius Managing Agents Ltd", own4444, "2025", "Annual accounts", "USD", "m", 3870.0, 2390.8, 0.516, 0.299, 0.046, 0.345, 0.861, 479.5, None, src4444, "KPI table, Report of the Directors", "Y", "Total expense = acquisition + admin"],
        ["4444", "Canopius Managing Agents Ltd", own4444, "2024", "Annual accounts", "USD", "m", 3159.4, 1948.0, 0.513, 0.295, 0.055, 0.350, 0.863, 387.0, None, src4444, "KPI table, prior-year column", "Y", ""],
        ["1084", "Chaucer Syndicates Ltd", "China Re (verify)", "2025", "Annual accounts", "USD", "m", 2455.5, 1754.2, 0.522, None, None, 0.360, 0.882, 366.8, 207.9, src1084, "KPI table, Managing Agent's Report", "Y", "Profit = technical profit; reported in $000, converted to $m"],
        ["1084", "Chaucer Syndicates Ltd", "China Re (verify)", "2024", "Annual accounts", "USD", "m", 2384.8, 1722.5, 0.514, None, None, 0.342, 0.856, 351.3, 248.9, src1084, "KPI table, prior-year column", "Y", ""],
    ]
    m3000 = [("2021", 482.6, 409.0, .545, .406, .951, None, 20.0), ("2022", 623.6, 465.3, .616, .387, 1.003, None, -1.6),
             ("2023", 701.5, 452.6, .400, .484, .884, None, 52.5), ("2024", 785.5, 580.5, .349, .457, .806, 145.7, 113.4),
             ("2025", 927.5, 665.1, .387, .462, .849, 153.6, 100.6)]
    for y, g, n, c, e, cr, p, u in m3000:
        rows.append(["3000", "Markel Syndicate Management Ltd", "Markel Group", y, "Annual accounts", "GBP", "m", g, n, c, None, None, e, cr, p, u,
                     src3000, "Five-year KPI table (oldest year first)", "Y", "Presented in £m; functional currency USD"])
    rows += [["Lloyd's market", "All managing agents", "Society of Lloyd's", "2024", "Lloyd's aggregate", "GBP", "m", 55500, None, None, None, None, None, 0.869, None, None, srcLLY, "Results release", "Y", "Market benchmark row"],
             ["Lloyd's market", "All managing agents", "Society of Lloyd's", "2025", "Lloyd's aggregate", "GBP", "m", 57900, None, None, None, None, None, 0.876, 10600, None, srcLLY, "Results release", "Y", "Profit = profit before tax"]]
    r = 2
    for row in rows:
        (syn, ma, own, yr, basis, cur, units, gwp, nep, clm, acq, adm, exp, cr, prof, uw, src, loc, ver, note) = row
        vals = {2: syn, 3: ma, 4: own, 5: yr, 6: basis, 7: cur, 8: units, 9: gwp, 10: nep, 11: clm, 12: acq, 13: adm, 14: exp,
                15: cr, 18: prof, 19: uw, 20: src, 21: loc, 22: ver, 23: note}
        d.cell(row=r, column=1, value=f'=B{r}&"|"&E{r}').font = BASE
        for col, v in vals.items():
            c = d.cell(row=r, column=col, value=v)
            c.font = INPUT if col in (9, 10, 11, 12, 13, 14, 15, 18, 19) else BASE
        d.cell(row=r, column=16, value=f'=IF(AND(K{r}<>"",N{r}<>""),K{r}+N{r},"")').font = BASE
        d.cell(row=r, column=17, value=f'=IF(AND(O{r}<>"",P{r}<>""),O{r}-P{r},"")').font = BASE
        for col in (11, 12, 13, 14, 15, 16, 17):
            d.cell(row=r, column=col).number_format = PCT
        for col in (9, 10, 18, 19):
            d.cell(row=r, column=col).number_format = MONEY
        r += 1
    # empty input rows for extension
    for rr in range(r, r + 40):
        d.cell(row=rr, column=1, value=f'=IF(B{rr}="","",B{rr}&"|"&E{rr})').font = BASE
        d.cell(row=rr, column=16, value=f'=IF(AND(K{rr}<>"",N{rr}<>""),K{rr}+N{rr},"")').font = BASE
        d.cell(row=rr, column=17, value=f'=IF(AND(O{rr}<>"",P{rr}<>""),O{rr}-P{rr},"")').font = BASE
        for col in range(2, 24):
            if col not in (16, 17):
                d.cell(row=rr, column=col).fill = YFILL
        for col in (11, 12, 13, 14, 15, 16, 17):
            d.cell(row=rr, column=col).number_format = PCT
        for col in (9, 10, 18, 19):
            d.cell(row=rr, column=col).number_format = MONEY
    last = r + 39
    d.cell(row=last + 2, column=2, value="Add new syndicates in the yellow rows. Year must be text (e.g. 2025). Ratios as fractions.").font = NOTE

    p = wb.create_sheet("Peer view")
    p["A1"] = "Peer view – one syndicate against the dataset and the Lloyd's market"
    p["A1"].font = TITLE
    p.column_dimensions["A"].width = 38
    for col in "BCDE":
        p.column_dimensions[col].width = 18
    p["A3"], p["B3"] = "Syndicate (type number)", "4444"
    p["A4"], p["B4"] = "Year (text)", "2025"
    for a in ("B3", "B4"):
        p[a].fill, p[a].font = YFILL, INPUT
    p["A3"].font = p["A4"].font = BOLD
    header(p, 6, ["Metric", "Selected syndicate", "Peer average (others in dataset, same year)", "Lloyd's market", "Gap vs peers (pts)"])
    rng = f"$2:${last}"
    metrics = [("Combined ratio (reported)", "O"), ("Claims ratio (net)", "K"), ("Total expense ratio", "N")]
    rr = 7
    for name, col in metrics:
        p.cell(row=rr, column=1, value=name)
        p.cell(row=rr, column=2, value=f'=IFERROR(INDEX(Data!{col}:{col},MATCH($B$3&"|"&$B$4,Data!A:A,0)),"")').font = LINK
        p.cell(row=rr, column=3, value=(
            f'=IFERROR((SUMIFS(Data!{col}:{col},Data!E:E,$B$4,Data!F:F,"Annual accounts")-N(B{rr}))/'
            f'(COUNTIFS(Data!E:E,$B$4,Data!F:F,"Annual accounts",Data!{col}:{col},"<>")-IF(B{rr}="",0,1)),"")')).font = LINK
        p.cell(row=rr, column=4, value=(f'=IFERROR(INDEX(Data!{col}:{col},MATCH("Lloyd\'s market|"&$B$4,Data!A:A,0)),"")' if col == "O" else "")).font = LINK
        p.cell(row=rr, column=5, value=f'=IF(AND(ISNUMBER(B{rr}),ISNUMBER(C{rr})),(B{rr}-C{rr})*100,"")')
        for c in (2, 3, 4):
            p.cell(row=rr, column=c).number_format = PCT
        p.cell(row=rr, column=5).number_format = "0.0;(0.0);-"
        rr += 1
    p.cell(row=rr + 1, column=1, value="Net earned premium (presentation currency, m)")
    p.cell(row=rr + 1, column=2, value='=IFERROR(INDEX(Data!J:J,MATCH($B$3&"|"&$B$4,Data!A:A,0)),"")').font = LINK
    p.cell(row=rr + 1, column=2).number_format = MONEY
    p.cell(row=rr + 2, column=1, value="Combined ratio gap vs Lloyd's market (pts)")
    p.cell(row=rr + 2, column=2, value='=IF(AND(ISNUMBER(B7),ISNUMBER(D7)),(B7-D7)*100,"")').number_format = "0.0;(0.0);-"
    p.cell(row=rr + 3, column=1, value="Value of the gap vs peers (m a year; positive = profit at stake)")
    p.cell(row=rr + 3, column=2, value=f'=IF(AND(ISNUMBER(E7),ISNUMBER(B{rr+1})),E7/100*B{rr+1},"")').number_format = MONEY
    p.cell(row=rr + 5, column=1, value="Positive gap = worse than peers (higher ratio). Value = gap × net earned premium, in the syndicate's own currency. "
                                       "Peer average excludes the selected syndicate. With a small pilot dataset, treat peer averages as indicative only.").font = NOTE

    df = wb.create_sheet("Definitions")
    header(df, 1, ["Field", "Definition", "Watch out for"], [28, 70, 60])
    defs = [
        ("GWP", "Gross written premium for the calendar year", "Growth from rate vs volume; currency movements"),
        ("Net earned premium", "Premium earned in the year, net of reinsurance", "Some reports show gross earned only"),
        ("Claims ratio (net)", "Net claims incurred ÷ net earned premium", "Gross vs net; includes prior-year development"),
        ("Acquisition ratio", "Brokerage and commission ÷ net earned premium", "Not always disclosed separately"),
        ("Admin / other expense ratio", "Operating expenses ÷ net earned premium", "Allocation of group costs differs"),
        ("Total expense ratio", "Acquisition + administrative expense ratio", "Some reports exclude certain costs"),
        ("Combined ratio", "Claims ratio + total expense ratio", "Check reported vs calculated (Check column)"),
        ("Profit for year", "Total result including investment return", "Technical vs total profit; currency"),
        ("Basis", "Annual accounts (calendar year) vs underwriting-year accounts (closed YOA)", "Do not mix bases in peer averages"),
    ]
    for i, (a, b, c) in enumerate(defs, start=2):
        df.cell(row=i, column=1, value=a).font = BOLD
        df.cell(row=i, column=2, value=b).alignment = WRAP
        df.cell(row=i, column=3, value=c).alignment = WRAP
    for s in wb.worksheets:
        style_all(s)
    wb.save(OUT / "Syndicate-Benchmark.xlsx")


# ---------------------------------------------------------------- 2. Value model
def build_value_model():
    wb = Workbook()
    ws = wb.active
    ws.title = "Read me"
    readme(ws, "London Market Value Model", [
        "PURPOSE",
        "Links a syndicate's plan to its combined ratio, profit, capital (uSCR → ECA) and return on capital, and shows the value "
        "of operating and underwriting levers. Use it to size recommendations in board language (see guide Module 27).",
        "",
        "HOW TO USE",
        "1. Inputs: replace the example classes, premiums and ratios with the client's figures (yellow cells).",
        "2. Levers: set the changes you want to test (growth, rate change, selection, acquisition, expenses, class exits, reinsurance).",
        "3. Model: read base vs scenario – combined ratio, profit, ECA, return on capital, capital released, economic profit.",
        "4. Lever value: approximate standalone value of each lever. Sensitivity: profit change for loss and expense ratio moves.",
        "",
        "EXAMPLE DATA",
        "All starting numbers are an illustrative mid-size syndicate (about £1bn net earned premium). They are not any real syndicate.",
        "",
        "SIMPLIFICATIONS",
        "Rate change affects loss ratio by price only (expected loss unchanged). Capital is approximated as uSCR % of NEP by class "
        "with a diversification credit; real capital comes from the syndicate's internal model. ECA = uSCR × (1 + uplift) – Lloyd's "
        "uplift is 35%. Investment income = NEP × investable assets multiple × yield.",
        "",
    ] + LEGEND)

    i = wb.create_sheet("Inputs")
    i["A1"] = "Inputs – base plan (£m unless stated)"
    i["A1"].font = TITLE
    header(i, 4, ["Class", "Net earned premium (£m)", "Attritional loss ratio", "Large loss ratio", "Cat loss ratio (normalised)",
                  "Acquisition ratio", "uSCR as % of NEP"], [30, 16, 14, 14, 16, 14, 14])
    classes = [("Property D&F", 250, .48, .07, .10, .22, .75), ("US casualty binders", 200, .66, .06, 0, .30, .90),
               ("Marine and energy", 150, .45, .10, .04, .20, .70), ("Specialty", 150, .50, .05, .02, .24, .65),
               ("Property treaty reinsurance", 250, .38, .03, .18, .12, 1.10)]
    for k, row in enumerate(classes):
        r = 5 + k
        for j, v in enumerate(row, start=1):
            c = i.cell(row=r, column=j, value=v)
            c.font, c.fill = INPUT, YFILL
            if j >= 3:
                c.number_format = PCT
            elif j == 2:
                c.number_format = MONEY
    i["A10"], i["B10"] = "Total", "=SUM(B5:B9)"
    i["A10"].font = BOLD
    i["B10"].number_format = MONEY
    glob = [("Operating expense ratio", .09, PCT), ("Prior-year development (negative = release, as % of NEP)", -.02, PCT),
            ("Investment yield", .035, PCT), ("Investable assets as multiple of NEP", 1.5, "0.00x"), ("ECA uplift on uSCR (Lloyd's: 35%)", .35, PCT),
            ("Cost of capital", .12, PCT), ("Diversification credit on summed uSCR", .15, PCT), ("Tax rate", .25, PCT)]
    i["A12"] = "Global assumptions"
    i["A12"].font = BOLD
    for k, (lab, v, fmt) in enumerate(glob):
        r = 13 + k
        i.cell(row=r, column=1, value=lab)
        c = i.cell(row=r, column=2, value=v)
        c.font, c.fill, c.number_format = INPUT, YFILL, fmt
    i["A22"] = "Example values: illustrative mid-size syndicate, not a real company. Replace with client data."
    i["A22"].font = NOTE

    lv = wb.create_sheet("Levers")
    lv["A1"] = "Levers – scenario changes"
    lv["A1"].font = TITLE
    header(lv, 4, ["Class", "Include (1 = keep, 0 = exit)", "Volume growth", "Risk-adjusted rate change", "Selection improvement (loss ratio pts)",
                   "Acquisition ratio change (pts)"], [30, 14, 14, 16, 18, 16])
    levers = [(1, .00, -.05, .01, 0), (0, 0, 0, 0, 0), (1, .05, -.03, .01, 0), (1, .05, -.04, .005, 0), (1, -.10, -.07, 0, 0)]
    for k, row in enumerate(levers):
        r = 5 + k
        lv.cell(row=r, column=1, value=f"=Inputs!A{r}").font = LINK
        for j, v in enumerate(row, start=2):
            c = lv.cell(row=r, column=j, value=v)
            c.font, c.fill = INPUT, YFILL
            c.number_format = "0" if j == 2 else PCT
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="1", allow_blank=False)
    lv.add_data_validation(dv)
    dv.add("B5:B9")
    gl = [("Operating expense ratio change (pts)", -.015), ("Reinsurance: uSCR relief", .05), ("Reinsurance: additional cost (£m)", 6.0),
          ("Prior-year development in scenario (as % of NEP)", 0.0)]
    lv["A11"] = "Global levers"
    lv["A11"].font = BOLD
    for k, (lab, v) in enumerate(gl):
        r = 12 + k
        lv.cell(row=r, column=1, value=lab)
        c = lv.cell(row=r, column=2, value=v)
        c.font, c.fill = INPUT, YFILL
        c.number_format = MONEY if "£m" in lab else PCT
    lv["A17"] = "Example scenario: exit US casualty binders, modest growth in marine and specialty, rates falling, 1.5 pts expense reduction, extra reinsurance."
    lv["A17"].font = NOTE

    m = wb.create_sheet("Model")
    m["A1"] = "Model – base vs scenario (£m)"
    m["A1"].font = TITLE
    header(m, 3, ["Class", "Base NEP", "Base loss ratio", "Base acquisition ratio", "Scenario NEP", "Scenario loss ratio",
                  "Scenario acquisition ratio", "Base claims", "Scenario claims", "Base acquisition cost", "Scenario acquisition cost",
                  "Base uSCR (pre-diversification)", "Scenario uSCR (pre-diversification)"], [28] + [14] * 12)
    for k in range(5):
        r, s = 4 + k, 5 + k
        f = {1: f"=Inputs!A{s}", 2: f"=Inputs!B{s}", 3: f"=Inputs!C{s}+Inputs!D{s}+Inputs!E{s}", 4: f"=Inputs!F{s}",
             5: f"=B{r}*Levers!B{s}*(1+Levers!C{s})*(1+Levers!D{s})", 6: f"=IF(1+Levers!D{s}=0,0,C{r}/(1+Levers!D{s}))-Levers!E{s}",
             7: f"=D{r}+Levers!F{s}", 8: f"=B{r}*C{r}", 9: f"=E{r}*F{r}", 10: f"=B{r}*D{r}", 11: f"=E{r}*G{r}",
             12: f"=B{r}*Inputs!G{s}", 13: f"=E{r}*Inputs!G{s}"}
        for col, fx in f.items():
            c = m.cell(row=r, column=col, value=fx)
            c.font = LINK if fx.startswith("=Inputs") and col in (1, 2, 4) else BASE
            c.number_format = PCT if col in (3, 4, 6, 7) else MONEY
    m["A9"] = "Total"
    m["A9"].font = BOLD
    for col in (2, 5, 8, 9, 10, 11, 12, 13):
        L = get_column_letter(col)
        c = m.cell(row=9, column=col, value=f"=SUM({L}4:{L}8)")
        c.number_format, c.font = MONEY, BOLD

    header(m, 11, ["Summary", "Base", "Scenario", "Change"], None)
    summary = [
        ("Net earned premium", "=B9", "=E9", MONEY),
        ("Claims incl. prior-year development", "=H9+Inputs!B14*B9", "=I9+Levers!B15*E9", MONEY),
        ("Acquisition costs", "=J9", "=K9", MONEY),
        ("Operating expenses", "=Inputs!B13*B9", "=(Inputs!B13+Levers!B12)*E9", MONEY),
        ("Underwriting result", "=B12-B13-B14-B15", "=C12-C13-C14-C15", MONEY),
        ("Combined ratio", "=IF(B12=0,0,(B13+B14+B15)/B12)", "=IF(C12=0,0,(C13+C14+C15)/C12)", PCT),
        ("Investment income", "=B12*Inputs!B16*Inputs!B15", "=C12*Inputs!B16*Inputs!B15", MONEY),
        ("Additional reinsurance cost", "0", "=Levers!B14", MONEY),
        ("Profit before tax", "=B16+B18-B19", "=C16+C18-C19", MONEY),
        ("Profit after tax", "=B20*(1-Inputs!B20)", "=C20*(1-Inputs!B20)", MONEY),
        ("uSCR after diversification", "=L9*(1-Inputs!B19)", "=M9*(1-Inputs!B19)*(1-Levers!B13)", MONEY),
        ("ECA (Funds at Lloyd's)", "=B22*(1+Inputs!B17)", "=C22*(1+Inputs!B17)", MONEY),
        ("Return on capital (after tax ÷ ECA)", "=IF(B23=0,0,B21/B23)", "=IF(C23=0,0,C21/C23)", PCT),
        ("Economic profit (after tax – cost of capital × ECA)", "=B21-Inputs!B18*B23", "=C21-Inputs!B18*C23", MONEY),
    ]
    for k, (lab, b, s, fmt) in enumerate(summary):
        r = 12 + k
        m.cell(row=r, column=1, value=lab).font = BOLD if lab in ("Underwriting result", "Combined ratio", "Profit after tax", "Return on capital (after tax ÷ ECA)") else BASE
        for col, fx in ((2, b), (3, s)):
            c = m.cell(row=r, column=col, value=fx if fx != "0" else 0)
            c.number_format = fmt
        c = m.cell(row=r, column=4, value=f"=C{r}-B{r}")
        c.number_format = "0.0%;(0.0%);-" if fmt == PCT else MONEY
    m["A27"] = "Capital released (base ECA – scenario ECA)"
    m["B27"] = "=B23-C23"
    m["B27"].number_format = MONEY
    m["A28"] = "Value of one combined ratio point on base NEP"
    m["B28"] = "=B12/100"
    m["B28"].number_format = MONEY
    m["A30"] = ("Notes: scenario loss ratio = base loss ratio ÷ (1 + rate change) – selection improvement. Exiting a class (Include = 0) removes its "
                "premium, claims, costs and capital. Operating expenses scale with NEP – in reality part is fixed, so exits may raise the expense ratio.")
    m["A30"].font = NOTE

    v = wb.create_sheet("Lever value")
    v["A1"] = "Approximate standalone value of each lever (£m a year, before tax)"
    v["A1"].font = TITLE
    header(v, 3, ["Lever", "Estimate", "Method"], [44, 14, 80])
    lv_rows = [
        ("Selection improvement", "=SUMPRODUCT(Levers!E5:E9,Model!E4:E8)", "Loss ratio points × scenario NEP by class"),
        ("Acquisition cost change", "=-SUMPRODUCT(Levers!F5:F9,Model!E4:E8)", "– acquisition points × scenario NEP"),
        ("Operating expense change", "=-Levers!B12*Model!C12", "– expense points × scenario NEP"),
        ("Rate change (price effect on margin)", "=SUMPRODUCT(Model!E4:E8,Levers!D5:D9/(1+Levers!D5:D9))", "Approximate: premium change at constant expected loss"),
        ("Reinsurance: capital cost saved less extra premium", "=Model!B23*Levers!B13*Inputs!B18-Levers!B14", "Capital relief × cost of capital – additional reinsurance cost"),
        ("Total change in economic profit (from model)", "=Model!D25", "Full interaction of all levers (after tax)"),
    ]
    for k, (a, b, c) in enumerate(lv_rows):
        r = 4 + k
        v.cell(row=r, column=1, value=a)
        x = v.cell(row=r, column=2, value=b)
        x.number_format = MONEY
        v.cell(row=r, column=3, value=c).alignment = WRAP
    v["A11"] = "Standalone estimates do not add up exactly to the model total because levers interact (and the total is after tax)."
    v["A11"].font = NOTE

    sv = wb.create_sheet("Sensitivity")
    sv["A1"] = "Change in base underwriting result (£m) for loss ratio and expense ratio moves"
    sv["A1"].font = TITLE
    sv["A3"] = "Rows: loss ratio change (pts). Columns: expense ratio change (pts). Negative = improvement."
    sv["A3"].font = NOTE
    sv.column_dimensions["A"].width = 22
    moves = [-3, -2, -1, 0, 1, 2, 3]
    sv.cell(row=5, column=1, value="LR \\ ER").font = BOLD
    for j, e in enumerate(moves):
        c = sv.cell(row=5, column=2 + j, value=e)
        c.font, c.fill = INPUT, GFILL
        sv.column_dimensions[get_column_letter(2 + j)].width = 12
    for k, lr in enumerate(moves):
        r = 6 + k
        c = sv.cell(row=r, column=1, value=lr)
        c.font, c.fill = INPUT, GFILL
        for j in range(len(moves)):
            col = get_column_letter(2 + j)
            x = sv.cell(row=r, column=2 + j, value=f"=-($A{r}+{col}$5)/100*Model!$B$12")
            x.number_format = MONEY

    for s in wb.worksheets:
        style_all(s)
    wb.save(OUT / "London-Market-Value-Model.xlsx")


# ---------------------------------------------------------------- 3. Diagnostic scorecards
def scorecard(ws, title, dims):
    ws["A1"] = title
    ws["A1"].font = TITLE
    header(ws, 3, ["Dimension", "Level 1 – weak", "Level 5 – leading practice", "Weight", "Score (1–5)", "Weighted", "Evidence / notes"],
           [30, 48, 52, 9, 11, 10, 40])
    for k, (dim, lo, hi, w) in enumerate(dims):
        r = 4 + k
        ws.cell(row=r, column=1, value=dim).font = BOLD
        ws.cell(row=r, column=2, value=lo).alignment = WRAP
        ws.cell(row=r, column=3, value=hi).alignment = WRAP
        c = ws.cell(row=r, column=4, value=w)
        c.font, c.number_format = INPUT, "0%"
        c = ws.cell(row=r, column=5, value=3)
        c.font, c.fill = INPUT, YFILL
        ws.cell(row=r, column=6, value=f"=D{r}*E{r}").number_format = "0.00"
        ws.cell(row=r, column=7).fill = YFILL
    n = 4 + len(dims)
    ws.cell(row=n, column=1, value="Overall maturity (weighted, 1–5)").font = BOLD
    c = ws.cell(row=n, column=5, value=f"=IF(SUM(D4:D{n-1})=0,0,SUMPRODUCT(D4:D{n-1},E4:E{n-1})/SUM(D4:D{n-1}))")
    c.number_format, c.font = SCORE, BOLD
    ws.cell(row=n + 1, column=1, value="Maturity label").font = BOLD
    ws.cell(row=n + 1, column=5, value=f'=IF(E{n}>=4.5,"Leading",IF(E{n}>=3.5,"Advanced",IF(E{n}>=2.5,"Developing",IF(E{n}>=1.5,"Basic","Weak"))))')
    ws.cell(row=n + 1, column=4, value=f"=SUM(D4:D{n-1})").number_format = "0%"
    ws.cell(row=n + 3, column=1, value="Scores of 3 are placeholders – replace with assessed scores (yellow). Weights should total 100%.").font = NOTE
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5")
    ws.add_data_validation(dv)
    dv.add(f"E4:E{n-1}")


def build_diagnostics():
    wb = Workbook()
    ws = wb.active
    ws.title = "Read me"
    readme(ws, "London Market Diagnostic Scorecards", [
        "CONTENTS",
        "DA diagnostic – delegated authority and bordereaux maturity (10 dimensions).",
        "AI readiness – readiness to scale AI in a London market firm (9 dimensions).",
        "Coverholder tiering – risk-based oversight tiers from six factors.",
        "AI use-case prioritisation – value, feasibility and risk scoring of use cases from guide Module 26.",
        "",
        "HOW TO USE",
        "Score each dimension 1–5 from interviews, documents and data (method in guide Module 28). Record evidence for every score. "
        "Weights reflect typical importance and can be changed. Example values are placeholders, not assessments of any firm.",
        "",
    ] + LEGEND)

    da = wb.create_sheet("DA diagnostic")
    scorecard(da, "Delegated authority and bordereaux diagnostic", [
        ("Strategy and appetite", "DA growth by opportunity; no DA-specific appetite", "Clear DA strategy by class and territory, linked to plan and oversight capacity", .08),
        ("Partner selection and due diligence", "Checklist due diligence; data capability not tested", "Risk-rated due diligence including data and systems tests; partner economics reviewed", .10),
        ("Contract and authority", "Binder terms only in PDF; non-standard wordings", "Structured contract register for all binders; standard wordings; registered before inception", .12),
        ("Bordereaux timeliness and quality", "Late and incomplete; quality not measured", "On time >95%; mandatory field validity >98%; measured monthly by coverholder", .12),
        ("Validation and controls", "Manual spot checks after loading", "Automated validation against binder terms at ingestion; exceptions workflow with service levels", .12),
        ("Premium and credit control", "DA premium reconciled late; high aged debt", "Cash matched by binder monthly; aged debt >90 days <3% of DA premium", .08),
        ("Claims oversight (DCA/TPA)", "Claims seen only in bordereaux", "Authority levels enforced; loss funds reconciled; leakage reviews; claims data linked to policies", .10),
        ("Performance management and exits", "Binders renewed by default", "Coverholder league table; profit-linked commission; documented exits", .12),
        ("Governance and Lloyd's compliance", "ATLAS records out of date; findings repeat", "Risk-based tiering; coordinated audits; findings closed on time; board MI", .08),
        ("Technology and automation", "Spreadsheets per coverholder", "Single DA data platform; reusable mappings; AI-assisted ingestion; API with top coverholders", .08),
    ])
    ai = wb.create_sheet("AI readiness")
    scorecard(ai, "AI readiness diagnostic", [
        ("Strategy and value", "AI ambition without value targets", "Board-approved AI ambition with sized value pools and owners", .12),
        ("Use-case portfolio", "Scattered pilots", "Prioritised portfolio across the lifecycle; scale criteria agreed before pilots", .10),
        ("Data foundations", "Unstructured data; weak master data", "Golden records for party, contract, exposure, finance, claims; CDR-aligned", .16),
        ("Workflow integration", "AI tools outside daily systems", "AI embedded in workbench, DA platform and claims system with clear human gates", .12),
        ("Governance and risk", "No inventory; no accountable senior manager", "Policy, inventory, risk tiers, SM&CR accountability; aligned to LMA toolkit", .14),
        ("Evaluation and monitoring", "Demos instead of measurement", "Test sets per use case; accuracy by segment; drift and override monitoring", .12),
        ("Skills and change", "Few trained staff; resistance", "AI literacy across roles; product owners in the business; adoption tracked", .10),
        ("Technology and vendors", "Point tools; no gateway; vendor lock-in", "AI gateway; approved models; vendor due diligence and exit plans", .08),
        ("Broker and market alignment", "Carrier cannot receive structured data", "Structured intake from platforms and brokers; fast, consistent responses", .06),
    ])

    ct = wb.create_sheet("Coverholder tiering")
    ct["A1"] = "Coverholder risk tiering (1 = low risk, 5 = high risk)"
    ct["A1"].font = TITLE
    factors = ["Premium size", "Class risk", "Loss ratio vs plan", "Data quality and timeliness", "Audit findings open", "Conduct exposure"]
    header(ct, 3, ["Coverholder"] + factors + ["Weighted score", "Tier"], [26] + [14] * 6 + [14, 10])
    weights = [.20, .20, .20, .15, .15, .10]
    ct.cell(row=4, column=1, value="Weights").font = BOLD
    for j, w in enumerate(weights):
        c = ct.cell(row=4, column=2 + j, value=w)
        c.font, c.number_format = INPUT, "0%"
    examples = [("Example – Florida property MGA", 4, 5, 3, 4, 2, 3), ("Example – UK SME package MGA", 3, 2, 2, 2, 1, 4),
                ("Example – Canadian liability coverholder", 2, 3, 4, 3, 3, 2), ("Example – A&H affinity scheme", 2, 2, 2, 3, 1, 5)]
    for k, ex in enumerate(examples):
        r = 5 + k
        ct.cell(row=r, column=1, value=ex[0])
        for j, v in enumerate(ex[1:]):
            c = ct.cell(row=r, column=2 + j, value=v)
            c.font, c.fill = INPUT, YFILL
        ct.cell(row=r, column=8, value=f"=SUMPRODUCT($B$4:$G$4,B{r}:G{r})").number_format = "0.00"
        ct.cell(row=r, column=9, value=f'=IF(H{r}>=3.5,"Tier 1",IF(H{r}>=2.5,"Tier 2","Tier 3"))')
    for r in range(9, 39):
        for col in range(1, 8):
            ct.cell(row=r, column=col).fill = YFILL
        ct.cell(row=r, column=8, value=f'=IF(A{r}="","",SUMPRODUCT($B$4:$G$4,B{r}:G{r}))').number_format = "0.00"
        ct.cell(row=r, column=9, value=f'=IF(A{r}="","",IF(H{r}>=3.5,"Tier 1",IF(H{r}>=2.5,"Tier 2","Tier 3")))')
    ct["A40"] = "Tier 1 = monthly review and annual full audit; Tier 2 = quarterly review, audit every 18–24 months; Tier 3 = semi-annual review, desk audit."
    ct["A40"].font = NOTE

    uc = wb.create_sheet("AI use-case priority")
    uc["A1"] = "AI use-case prioritisation (value and feasibility 1–5 high is good; risk 1–5 high is bad)"
    uc["A1"].font = TITLE
    header(uc, 3, ["ID", "Use case", "Value", "Feasibility", "Risk", "Priority score", "Rank"], [8, 52, 10, 12, 10, 14, 8])
    uc["A2"], uc["C2"], uc["D2"], uc["E2"] = "Weights", .5, .3, .2
    for a in ("C2", "D2", "E2"):
        uc[a].font, uc[a].number_format = INPUT, "0%"
    cases = [("U03", "Submission intake and extraction", 4, 5, 1), ("U04", "Appetite triage and prioritisation", 4, 3, 3),
             ("U09", "Lead quote generation with underwriter approval", 4, 2, 4), ("U10", "Smart follow decisions", 4, 2, 5),
             ("U11", "Wording comparison and contract certainty", 4, 3, 3), ("U16", "Cash matching", 3, 4, 1),
             ("U17", "Reconciliation break classification", 3, 4, 1), ("U19", "Binder contract digitisation", 4, 4, 2),
             ("U21", "Bordereaux mapping and cleansing", 5, 4, 1), ("U22", "Bordereaux validation against binder terms", 5, 4, 2),
             ("U24", "Coverholder performance analytics", 5, 3, 3), ("U28", "Claims file summarisation", 4, 4, 3),
             ("U31", "Leakage and fraud detection", 4, 3, 4), ("U33", "Catastrophe event loss estimation", 4, 3, 3),
             ("U34", "Reinsurance recovery matching", 4, 4, 2)]
    for k, (cid, name, val, fea, risk) in enumerate(cases):
        r = 4 + k
        uc.cell(row=r, column=1, value=cid)
        uc.cell(row=r, column=2, value=name)
        for col, v in ((3, val), (4, fea), (5, risk)):
            c = uc.cell(row=r, column=col, value=v)
            c.font, c.fill = INPUT, YFILL
        uc.cell(row=r, column=6, value=f"=$C$2*C{r}+$D$2*D{r}+$E$2*(6-E{r})").number_format = "0.00"
        uc.cell(row=r, column=7, value=f"=RANK(F{r},$F$4:$F${3+len(cases)})")
    uc.cell(row=5 + len(cases), column=1, value="Example scores reflect typical London market conditions [guessing]; rescore for each client.").font = NOTE
    for s in wb.worksheets:
        style_all(s)
    wb.save(OUT / "Diagnostic-Scorecards.xlsx")


if __name__ == "__main__":
    build_benchmark()
    build_value_model()
    build_diagnostics()
    print("Built:", ", ".join(p.name for p in sorted(OUT.glob("*.xlsx"))))
