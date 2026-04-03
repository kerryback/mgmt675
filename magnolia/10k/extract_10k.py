"""
Extract sections from Magnolia Oil & Gas 10-K HTML filings.
Produces clean markdown files for MD&A, Risk Factors, and Financial Statements.
"""

from bs4 import BeautifulSoup, NavigableString, Tag
import re
import os
import sys

OUTDIR = r"C:\Users\kerry\repos\mgmt675\magnolia\10k\extracted"
os.makedirs(OUTDIR, exist_ok=True)

YEARS = {
    "2021": r"C:\Users\kerry\repos\mgmt675\magnolia\10k\mgy-10k-2021.htm",
    "2020": r"C:\Users\kerry\repos\mgmt675\magnolia\10k\mgy-10k-2020.htm",
}


def load_and_prep(path):
    """Load HTML, strip style/script, unwrap XBRL tags."""
    print(f"Reading {path}...")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    print(f"  File size: {len(html):,} chars")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["style", "script", "link"]):
        tag.decompose()
    for tag in soup.find_all(re.compile(r"^ix:")):
        tag.unwrap()

    return soup


def table_to_markdown(table_tag):
    """Convert an HTML table to markdown format."""
    rows = []
    for tr in table_tag.find_all("tr"):
        cells = []
        for td in tr.find_all(["td", "th"]):
            text = td.get_text(separator=" ", strip=True)
            text = re.sub(r"\s+", " ", text).strip()
            text = text.replace("|", "/")
            cells.append(text)
        if any(c for c in cells):
            rows.append(cells)

    if not rows:
        return ""

    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    lines = []
    for i, row in enumerate(rows):
        line = "| " + " | ".join(row) + " |"
        lines.append(line)
        if i == 0:
            lines.append("| " + " | ".join(["---"] * max_cols) + " |")

    return "\n".join(lines)


def extract_section_clean(soup, start_pat, end_pat, start_occ=0, end_occ=0, include_start=True):
    """
    Find text nodes matching start/end patterns, collect everything between them.
    Tables are converted to markdown format. Bold text is marked with **.
    """
    all_text_nodes = list(soup.strings)

    # Find start
    start_idx = None
    occ = 0
    for i, s in enumerate(all_text_nodes):
        if re.search(start_pat, s.strip(), re.IGNORECASE):
            if occ == start_occ:
                start_idx = i
                break
            occ += 1

    if start_idx is None:
        print(f"  ERROR: start pattern not found: {start_pat}")
        return None

    # Find end
    end_idx = None
    occ = 0
    for i, s in enumerate(all_text_nodes):
        if i <= start_idx:
            continue
        if re.search(end_pat, s.strip(), re.IGNORECASE):
            if occ == end_occ:
                end_idx = i
                break
            occ += 1

    if end_idx is None:
        print(f"  ERROR: end pattern not found: {end_pat}")
        return None

    print(f"  Range: text nodes {start_idx} to {end_idx}")
    print(f"  Start: {all_text_nodes[start_idx].strip()[:80]!r}")
    print(f"  End:   {all_text_nodes[end_idx].strip()[:80]!r}")

    # Collect content
    output_parts = []
    processed_tables = set()

    begin = start_idx if include_start else start_idx + 1
    for i in range(begin, end_idx):
        node = all_text_nodes[i]
        text = node.strip()
        if not text:
            continue

        # Check if inside a table
        table_el = None
        p = node.parent
        while p:
            if isinstance(p, Tag) and p.name == "table":
                table_el = p
                break
            p = p.parent

        if table_el is not None:
            tid = id(table_el)
            if tid not in processed_tables:
                processed_tables.add(tid)
                md = table_to_markdown(table_el)
                if md:
                    output_parts.append("\n" + md + "\n")
        else:
            # Detect bold text for headers
            is_bold = False
            p = node.parent
            while p and isinstance(p, Tag):
                if p.name in ("b", "strong"):
                    is_bold = True
                    break
                style = p.get("style", "")
                if "font-weight" in style and ("bold" in style or "700" in style):
                    is_bold = True
                    break
                p = p.parent

            if is_bold and len(text) < 200 and not text.startswith("("):
                output_parts.append(f"\n**{text}**\n")
            else:
                output_parts.append(text)

    return "\n\n".join(output_parts) if output_parts else None


def clean_markdown(text):
    """Clean up the markdown output."""
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = text.replace("\ufffd", "'")
    # Clean up common unicode issues
    text = text.replace("\u00a0", " ")
    return text.strip()


def process_year(year, path):
    soup = load_and_prep(path)

    # === MD&A ===
    print(f"\n{'='*60}")
    print(f"[{year}] Extracting MD&A (Item 7)")
    print("=" * 60)

    mda = extract_section_clean(
        soup,
        r"^Item\s+7\.\s*Management",
        r"^Item\s+7A[\.\s]",
    )

    if mda:
        mda = clean_markdown(mda)
        outpath = os.path.join(OUTDIR, f"mgy-{year}-mda.md")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# Management's Discussion and Analysis of Financial Condition and Results of Operations\n\n")
            f.write(f"## Magnolia Oil & Gas Corporation -- FY{year}\n\n")
            f.write(mda)
        print(f"  Wrote {outpath} ({len(mda):,} chars)")
    else:
        print("  FAILED")

    # === Risk Factors ===
    print(f"\n{'='*60}")
    print(f"[{year}] Extracting Risk Factors (Item 1A)")
    print("=" * 60)

    risk = extract_section_clean(
        soup,
        r"^Item\s+1A[\.\s]+Risk\s+Factors",
        r"^Item\s+1B[\.\s]",
    )

    if risk:
        risk = clean_markdown(risk)
        outpath = os.path.join(OUTDIR, f"mgy-{year}-risk-factors.md")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# Risk Factors\n\n")
            f.write(f"## Magnolia Oil & Gas Corporation -- FY{year}\n\n")
            f.write(risk)
        print(f"  Wrote {outpath} ({len(risk):,} chars)")
    else:
        print("  FAILED")

    # === Financial Statements ===
    print(f"\n{'='*60}")
    print(f"[{year}] Extracting Financial Statements (Item 8)")
    print("=" * 60)

    fin = extract_section_clean(
        soup,
        r"^Item\s+8\.\s*Financial\s+Statements",
        r"^Item\s+9[\.\s]",
    )

    if fin:
        fin = clean_markdown(fin)
        outpath = os.path.join(OUTDIR, f"mgy-{year}-financial-statements.md")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# Financial Statements and Supplementary Data\n\n")
            f.write(f"## Magnolia Oil & Gas Corporation -- FY{year}\n\n")
            f.write(fin)
        print(f"  Wrote {outpath} ({len(fin):,} chars)")
    else:
        print("  FAILED")


if __name__ == "__main__":
    for year, path in YEARS.items():
        process_year(year, path)
    print("\nAll done!")
