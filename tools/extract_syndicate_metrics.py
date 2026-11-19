#!/usr/bin/env python3
"""Extract headline KPIs from Lloyd's syndicate annual report PDFs into a CSV for review.

Usage:
    python3 tools/extract_syndicate_metrics.py <folder-with-pdfs> <output.csv>

Requirements: pdftotext (poppler-utils) on PATH.

What it does:
  - Converts each PDF to text (layout mode).
  - Finds the first KPI-style lines for gross written premium, net earned premium,
    claims/loss ratio, expense ratio, acquisition ratio, administrative expense ratio,
    combined ratio and profit for the year.
  - Captures the first two numbers on each line (normally current year, prior year)
    and the exact source line so a person can verify every figure.
  - Detects the units header ($m, $000, £m, £'m) and presentation currency where stated.

Important: report layouts differ. Always review the output against the source line
(and the PDF) before loading figures into the benchmark. Some reports show five-year
tables (oldest first) – the script flags these so you pick the right column.
"""
import csv
import pathlib
import re
import subprocess
import sys

PATTERNS = {
    "gwp": r"^\s*gross (premiums )?written( premiums)?\b",
    "nep": r"^\s*(net (premiums )?earned( premiums)?|earned premiums, net of reinsurance)\b",
    "claims_ratio": r"^\s*(net claims ratio|claims (loss )?ratio|loss ratio)\b",
    "expense_ratio": r"^\s*(expense ratio|expenses ratio)\b",
    "acquisition_ratio": r"^\s*-?\s*acquisition( cost)? ratio\b",
    "admin_ratio": r"^\s*-?\s*administrative expense ratio\b",
    "combined_ratio": r"^\s*combined (operating )?ratio\b",
    "profit": r"^\s*(profit|result) for the (financial )?year\b|^\s*technical profit for the financial year\b",
}
NUM = r"\(?-?[\d,]+(?:\.\d+)?\)?%?"


def to_number(tok):
    neg = tok.startswith("(") and tok.endswith(")") or tok.startswith("-")
    t = tok.strip("()%-").replace(",", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def extract(pdf):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    lines = txt.splitlines()
    out = {"file": pdf.name}
    m = re.search(r"Syndicate\s+(\d{3,4})", txt)
    out["syndicate"] = m.group(1) if m else ""
    cur = re.search(r"present(ation|ed)[^.\n]{0,60}(US dollars?|USD|sterling|GBP|euro)", txt, re.I)
    out["currency_note"] = cur.group(2) if cur else ""
    for key, pat in PATTERNS.items():
        out[key + "_cy"] = out[key + "_py"] = out[key + "_line"] = ""
        for i, line in enumerate(lines):
            if re.search(pat, line, re.I):
                nums = re.findall(NUM, line[len(re.match(r"^\s*[^\d(]*", line).group(0)):])
                nums = [n for n in nums if to_number(n) is not None]
                if not nums:
                    continue
                # units: look upward up to 25 lines for a units header
                units = ""
                for j in range(i, max(0, i - 25), -1):
                    u = re.search(r"(\$m|\$000|£m|£'m|£000|\$'m|USD ?m|GBP ?m)", lines[j])
                    if u:
                        units = u.group(1)
                        break
                out[key + "_cy"] = to_number(nums[0])
                out[key + "_py"] = to_number(nums[1]) if len(nums) > 1 else ""
                out[key + "_line"] = f"L{i+1}: {line.strip()[:160]}"
                if key == "gwp":
                    out["units"] = units
                    out["multi_year_table"] = "YES – check column order" if len(nums) > 2 else ""
                break
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    folder, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    rows = [extract(p) for p in sorted(folder.glob("*.pdf"))]
    keys = ["file", "syndicate", "currency_note", "units", "multi_year_table"]
    for k in PATTERNS:
        keys += [k + "_cy", k + "_py", k + "_line"]
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Extracted {len(rows)} reports to {dest}. Review every figure against its source line before use.")


if __name__ == "__main__":
    main()
