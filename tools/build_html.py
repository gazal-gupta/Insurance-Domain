#!/usr/bin/env python3
"""Build the interactive London Market Field Guide HTML from the Markdown modules.

Usage: python3 tools/build_html.py
Outputs:
  london-market-lloyds-guide/interactive/London-Market-Field-Guide.html  (standalone, open locally)
  london-market-lloyds-guide/interactive/publish-body.html                (same page without document skeleton)
"""
import html
import json
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "london-market-lloyds-guide"
OUT = SRC / "interactive"

GROUPS = [
    ("Start here", ["00", "18"]),
    ("Beginner", ["01", "02", "03"]),
    ("Intermediate", ["04", "05", "06"]),
    ("Advanced", ["07", "08", "09", "26"]),
    ("Lloyd's master reference", ["21", "23", "24", "25"]),
    ("Strategy and outlook", ["20", "22"]),
    ("Consulting", ["11", "10", "19"]),
    ("Owned consulting assets", ["27", "28", "29", "30"]),
    ("Reference", ["12", "13", "31"]),
    ("CII syllabus notes (optional)", ["14", "15", "16", "17"]),
]
LABELS = {
    "00": "Strategy and learning path", "18": "Path to world-class consultant",
    "01": "Foundations", "02": "Actors and entities", "03": "Lines of business",
    "04": "Placement and underwriting", "05": "Delegated authority",
    "06": "Accounting, claims, reinsurance", "07": "Capital, finance, regulation",
    "08": "Modernisation, data, technology", "09": "AI in the London market", "26": "AI use cases and live examples",
    "21": "Lloyd's end to end", "23": "Process catalogue (L0–L3)", "24": "Systems, documents and data", "25": "IT landscape swimlanes", "20": "Outlook 2027–2030", "22": "New strategies",
    "11": "Consulting playbook", "10": "Case studies", "19": "Practice toolkit",
    "27": "Benchmark and value model", "28": "Diagnostic toolkits", "29": "Account profiles (top 25)", "30": "Flagship POV fact base", "12": "Glossary", "13": "Self-assessment and sources", "31": "Master Guide integration map",
    "14": "CII LM1–LM3 overview", "15": "LM1 notes", "16": "LM2 notes", "17": "LM3 notes",
}

MINDMAP = [
    {"t": "Market and players", "m": "02", "hook": "Lloyd's is the exchange; syndicates are the traders.",
     "leaves": [["Lloyd's is not an insurer", "02"], ["Syndicates and year of account", "21"], ["Managing agents", "02"],
                ["Members and capital", "02"], ["Brokers act for the client", "02"], ["Company market", "02"]]},
    {"t": "Risk lifecycle", "m": "21", "hook": "Submit, lead, follow, sign down, certain, settle, claim, recover.",
     "leaves": [["MRC and UMR", "04"], ["Lead, follow, signing down", "04"], ["GUA for changes", "04"],
                ["Underwriting controls", "04"], ["Claims – LCLA", "06"], ["Reinsurance", "03"]]},
    {"t": "Delegated authority", "m": "05", "hook": "Approve, register, bind, report, remit, oversee.",
     "leaves": [["Coverholders and ATLAS", "21"], ["Binding authority terms", "05"], ["Bordereaux", "05"],
                ["Risk-based oversight", "05"], ["DCA and TPA claims", "05"], ["DA economics", "05"]]},
    {"t": "Money and capital", "m": "07", "hook": "Premium in trust; capital in three links; years close by RITC.",
     "leaves": [["Bureau and SND", "06"], ["Premium trust funds", "06"], ["Chain of security", "07"],
                ["ECA = uSCR × 1.35", "07"], ["RITC and open years", "07"], ["Combined ratio", "01"]]},
    {"t": "Regulation", "m": "07", "hook": "PRA for soundness, FCA for conduct, Lloyd's for the market.",
     "leaves": [["PRA priorities 2026", "07"], ["FCA PS25/21", "07"], ["Lloyd's oversight", "21"],
                ["Insurance Act 2015", "15"], ["Sanctions", "15"], ["Climate SS5/25", "07"]]},
    {"t": "Data, tech and AI", "m": "08", "hook": "Standards first, workflow second, model last.",
     "leaves": [["Blueprint Two retired", "08"], ["CDR and standards", "08"], ["Target architecture", "08"],
                ["AI use cases and live examples", "26"], ["Evaluating AI", "09"], ["AI governance", "09"]]},
    {"t": "Strategy and outlook", "m": "20", "hook": "Soft cycle, more capital, fewer bigger players.",
     "leaves": [["Soft market 2026", "20"], ["Consolidation", "20"], ["Facilities and follow", "22"],
                ["MGA partnerships", "22"], ["New risk classes", "22"], ["Scenarios 2027–2030", "20"]]},
    {"t": "Consulting craft", "m": "11", "hook": "Answer first; one point on £1bn is £10m.",
     "leaves": [["Problem statement", "11"], ["Issue trees", "11"], ["Day-one hypothesis", "11"],
                ["Value sizing", "11"], ["Pyramid storyline", "11"], ["14 case studies", "10"]]},
]


def fix_blank_lines(text):
    out = []
    lines = text.split("\n")
    in_code = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_code = not in_code
        prev = out[-1] if out else ""
        if not in_code and prev.strip():
            is_list = re.match(r"^(\d+\.|-|\*) ", line)
            prev_list = re.match(r"^\s*(\d+\.|-|\*) ", prev)
            is_table = line.startswith("|")
            prev_table = prev.startswith("|")
            if (is_list and not prev_list and not prev_table) or (is_table and not prev_table):
                out.append("")
        out.append(line)
    return "\n".join(out)


def slug(s):
    s = re.sub(r"<[^>]+>", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "s"


INIT = ('%%{init: {"theme": "base", "themeVariables": {'
        '"fontFamily": "Arial, Helvetica, sans-serif", "fontSize": "16px", '
        '"primaryColor": "#FFF4DA", "primaryTextColor": "#14243A", "primaryBorderColor": "#9C7218", '
        '"secondaryColor": "#DDEFF1", "tertiaryColor": "#F3F5F8", "lineColor": "#4E5A6B", '
        '"edgeLabelBackground": "#FFFFFF", "clusterBkg": "#F6F8FB", "clusterBorder": "#9AA5B4", '
        '"actorBkg": "#14243A", "actorTextColor": "#FFFFFF", "actorBorder": "#14243A", "actorLineColor": "#9AA5B4", '
        '"signalColor": "#1C6A73", "signalTextColor": "#14243A", "labelBoxBkgColor": "#DDEFF1", '
        '"noteBkgColor": "#FFF4DA", "noteTextColor": "#14243A", "noteBorderColor": "#9C7218", '
        '"sequenceNumberColor": "#FFFFFF"}, '
        '"flowchart": {"nodeSpacing": 45, "rankSpacing": 55, "padding": 14, "useMaxWidth": false}, '
        '"sequence": {"actorFontSize": 15, "messageFontSize": 15, "noteFontSize": 14, "useMaxWidth": false, "mirrorActors": true}}}%%')

CLASSDEFS = [
    "classDef startc fill:#2B7A4B,stroke:#1E5A37,color:#FFFFFF,stroke-width:2px",
    "classDef stepc fill:#FFF4DA,stroke:#9C7218,color:#14243A,stroke-width:1.5px",
    "classDef decc fill:#FDE7C4,stroke:#A86400,color:#14243A,stroke-width:2px",
    "classDef endc fill:#1C6A73,stroke:#124A50,color:#FFFFFF,stroke-width:2px",
]

LEGENDS = {
    "flow-numbered": ('<span class="dleg"><i class="sw s-start"></i>Start <i class="sw s-step"></i>Step '
                      '<i class="sw s-dec"></i>Decision <i class="sw s-end"></i>End · numbers show the step sequence</span>'),
    "sequence": ('<span class="dleg"><i class="sw s-actor"></i>Party and system (lane) '
                 '<i class="num">1</i>Numbered hand-offs show the step sequence</span>'),
    "flow": '<span class="dleg">Map view · use Enlarge to zoom</span>',
    "other": '<span class="dleg">Use Enlarge to zoom</span>',
}

NODE_DEF = re.compile(r"(\b[A-Za-z][\w]*)\s*(\[\[.*?\]\]|\[.*?\]|\{.*?\}|\(\(.*?\)\)|\(.*?\))")
ARROW = re.compile(r"\s*(?:<-->|-->|-\.->|==>|---)\s*")


def enhance_mermaid(code):
    """Add theme, numbering and colour coding. Returns (code, kind)."""
    lines = code.strip("\n").split("\n")
    first = lines[0].strip()
    if first.startswith("sequenceDiagram"):
        if not any(l.strip() == "autonumber" for l in lines):
            lines.insert(1, "  autonumber")
        return INIT + "\n" + "\n".join(lines) + "\n", "sequence"
    if not (first.startswith("flowchart") or first.startswith("graph")):
        return INIT + "\n" + "\n".join(lines) + "\n", "other"
    if any(l.strip().startswith("subgraph") for l in lines):
        return INIT + "\n" + "\n".join(lines) + "\n", "flow"
    # parse nodes, labels, shapes and edges
    order, shape, edges = [], {}, []
    for l in lines[1:]:
        s = l.strip()
        if not s or s.startswith(("classDef", "class ", "style ", "linkStyle", "%%", "direction", "click")):
            continue
        for mo in NODE_DEF.finditer(s):
            nid, lab = mo.group(1), mo.group(2)
            if nid not in shape:
                shape[nid] = lab[0]
            if nid not in order:
                order.append(nid)
        bare = NODE_DEF.sub(r"\1", s)
        bare = re.sub(r"--\s[^>]*?-->", "-->", bare)
        bare = re.sub(r"-\.\s[^>]*?\.->", "-.->", bare)
        bare = re.sub(r"\|[^|]*\|", "", bare)
        parts = [p.strip() for p in ARROW.split(bare) if p.strip()]
        ids = [p for p in parts if re.fullmatch(r"[A-Za-z]\w*", p)]
        for nid in ids:
            if nid not in order:
                order.append(nid)
        if len(ids) == len(parts):
            edges += list(zip(ids, ids[1:]))
    outdeg = {n: 0 for n in order}
    indeg = {n: 0 for n in order}
    for a, b in edges:
        outdeg[a] = outdeg.get(a, 0) + 1
        indeg[b] = indeg.get(b, 0) + 1
    if not order or len(order) > 18 or max(outdeg.values() or [0]) > 4 or not edges:
        return INIT + "\n" + "\n".join(lines) + "\n", "flow"
    # sequence: breadth-first from roots in appearance order
    adj = {n: [] for n in order}
    for a, b in edges:
        if b not in adj[a]:
            adj[a].append(b)
    roots = [n for n in order if indeg.get(n, 0) == 0] or [order[0]]
    seq, queue = [], list(roots)
    while queue:
        n = queue.pop(0)
        if n in seq:
            continue
        seq.append(n)
        queue += [m for m in adj.get(n, []) if m not in seq]
    seq += [n for n in order if n not in seq]
    num = {n: i + 1 for i, n in enumerate(seq)}
    labels_text = [m.group(2) for l in lines[1:] for m in NODE_DEF.finditer(l)]
    if labels_text and all(re.match(r"^[\[\{\(]+\"?\d", t) for t in labels_text):
        num = {}  # diagram already carries its own step numbers – keep them
    done = set()

    def label(mo):
        nid, lab = mo.group(1), mo.group(2)
        if nid in done or nid not in num:
            return mo.group(0)
        done.add(nid)
        op = 2 if lab[:2] in ("[[", "((") else 1
        inner = lab[op:-op].strip().strip('"')
        return f'{nid}{lab[:op]}"{num[nid]}. {inner}"{lab[-op:]}'

    out = [lines[0]]
    for l in lines[1:]:
        out.append(NODE_DEF.sub(label, l))
    cls = {"startc": [], "stepc": [], "decc": [], "endc": []}
    for n in order:
        if shape.get(n) == "{":
            cls["decc"].append(n)
        elif indeg.get(n, 0) == 0:
            cls["startc"].append(n)
        elif outdeg.get(n, 0) == 0:
            cls["endc"].append(n)
        else:
            cls["stepc"].append(n)
    out += ["  " + c for c in CLASSDEFS]
    out += [f"  class {','.join(v)} {k}" for k, v in cls.items() if v]
    return INIT + "\n" + "\n".join(out) + "\n", "flow-numbered"


def convert(mid, text):
    # title
    m = re.match(r"#\s+(.+)\n", text)
    title = m.group(1).strip() if m else LABELS[mid]
    body = text[m.end():] if m else text
    title = re.sub(r"^Module\s+\d+\s+–\s+", "", title)

    mermaids = []

    def mer(mo):
        mermaids.append(mo.group(1))
        return f"\n\nMERMAIDBLOCK{len(mermaids)-1}\n\n"

    body = re.sub(r"```mermaid\n(.*?)```", mer, body, flags=re.S)
    body = fix_blank_lines(body)
    # internal links
    body = re.sub(r"\]\((?:\.\./)?(?:london-market-lloyds-guide/)?(\d\d)-[A-Za-z0-9\-]+\.md(#[^)]*)?\)", r"](#m\1)", body)
    # checkboxes
    cnt = {"n": 0}

    def chk(mo):
        cnt["n"] += 1
        return f'{mo.group(1)}<input type="checkbox" class="persist" id="chk-{mid}-{cnt["n"]}"> '

    body = re.sub(r"^(\s*- )\[ \] ", chk, body, flags=re.M)
    # confidence tags
    body = re.sub(r"\*\*\[(certain|likely|guessing)\]\*\*", r'<span class="tag tag-\1">\1</span>', body)
    body = re.sub(r"(?<![\(\w])\[(certain|likely|guessing)\](?!\()", r'<span class="tag tag-\1">\1</span>', body)

    h = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    for i, code in enumerate(mermaids):
        code, kind = enhance_mermaid(code)
        legend = LEGENDS.get(kind, "")
        block = (f'<div class="diagram" data-kind="{kind}"><div class="dbar">{legend}'
                 f'<button type="button" class="btn small enlarge">Enlarge</button></div>'
                 f'<div class="dwrap"><pre class="mermaid">{html.escape(code, quote=False)}</pre></div></div>')
        h = h.replace(f"<p>MERMAIDBLOCK{i}</p>", block)
    h = h.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    h = re.sub(r'<a href="(https?://)', r'<a target="_blank" rel="noopener" href="\1', h)
    seen = set()

    def hid(mo):
        lvl, inner = mo.group(1), mo.group(2)
        base = f"m{mid}-{slug(inner)}"
        hid_ = base
        k = 2
        while hid_ in seen:
            hid_ = f"{base}-{k}"
            k += 1
        seen.add(hid_)
        return f'<h{lvl} id="{hid_}">{inner}</h{lvl}>'

    h = re.sub(r"<h([234])>(.*?)</h\1>", hid, h)
    return title, h


def flashcards(mid, text):
    cards = []
    for tbl in re.finditer(r"((?:^\|.*\|\s*\n)+)", text, flags=re.M):
        rows = [r.strip() for r in tbl.group(1).strip().split("\n")]
        if len(rows) < 3:
            continue
        head = [c.strip() for c in rows[0].strip("|").split("|")]
        qi = next((i for i, c in enumerate(head) if c.lower() == "question"), None)
        ai = next((i for i, c in enumerate(head) if "answer" in c.lower()), None)
        if qi is None or ai is None:
            continue
        for r in rows[2:]:
            cells = [c.strip() for c in r.strip("|").split("|")]
            if len(cells) <= max(qi, ai):
                continue
            q, a = cells[qi], cells[ai]
            strip = lambda s: re.sub(r"\*\*|`", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s))
            cards.append({"m": mid, "q": strip(q), "a": strip(a)})
    return cards


def main():
    files = {p.name[:2]: p for p in SRC.glob("[0-9][0-9]-*.md")}
    modules, cards = [], []
    for _, ids in GROUPS:
        for mid in ids:
            text = files[mid].read_text(encoding="utf-8")
            title, body = convert(mid, text)
            modules.append((mid, title, body))
            cards.extend(flashcards(mid, text))

    nav = []
    for g, ids in GROUPS:
        items = "".join(
            f'<li><a href="#m{mid}" data-mid="{mid}"><span class="num">{mid}</span>'
            f'<span class="lbl">{html.escape(LABELS[mid])}</span><span class="done" aria-hidden="true">✓</span></a></li>'
            for mid in ids)
        nav.append(f'<div class="navgroup"><p class="navhead">{html.escape(g)}</p><ul>{items}</ul></div>')

    sections = []
    for mid, title, body in modules:
        sections.append(
            f'<section class="module" id="m{mid}" data-mid="{mid}">'
            f'<header class="modhead"><span class="modnum">Module {mid}</span><h1>{html.escape(title)}</h1>'
            f'<label class="complete"><input type="checkbox" class="persist modcheck" id="done-{mid}" data-mid="{mid}"> Mark as complete</label></header>'
            f'<div class="prose">{body}</div>'
            f'<div class="notes"><label for="note-{mid}">My notes for module {mid}</label>'
            f'<textarea id="note-{mid}" class="persist" rows="4" placeholder="Key points, client questions, things to verify…"></textarea></div>'
            f'</section>')

    tpl = (ROOT / "tools" / "template.html").read_text(encoding="utf-8")
    page = (tpl.replace("{{NAV}}", "".join(nav))
               .replace("{{MODULES}}", "".join(sections))
               .replace("{{CARDS}}", json.dumps(cards, ensure_ascii=False).replace("</", "<\\/"))
               .replace("{{MINDMAP}}", json.dumps(MINDMAP, ensure_ascii=False))
               .replace("{{LABELS}}", json.dumps(LABELS, ensure_ascii=False))
               .replace("{{NMOD}}", str(len(modules)))
               .replace("{{NCARDS}}", str(len(cards))))
    OUT.mkdir(exist_ok=True)
    (OUT / "publish-body.html").write_text(page, encoding="utf-8")
    standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                  '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>\n'
                  '<script>document.addEventListener("DOMContentLoaded",function(){if(window.mermaid){mermaid.initialize({startOnLoad:false,theme:"neutral"});mermaid.run({querySelector:"pre.mermaid"});}});</script>\n'
                  '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
    (OUT / "London-Market-Field-Guide.html").write_text(standalone, encoding="utf-8")
    print(f"modules={len(modules)} cards={len(cards)} bytes={len(page)}")


if __name__ == "__main__":
    main()
