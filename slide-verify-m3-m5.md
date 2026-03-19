# Slide Verification Report: M3, M4, M5

**Date:** 2026-03-17
**Method:** Playwright screenshots at 1920x1080, all slides navigated programmatically
**Screenshots saved to:** `.claude/screenshots/`

---

## M3: Mean-Variance Analysis (16 slides)

### Issues Found

**Slide 8 (In-Class Exercise: Data)** -- Minor
- The Font Awesome CSV icon (`fa-solid fa-file-csv`) next to the "returns.csv" download link is not rendering. Only the link text appears. This is likely because Font Awesome is not loaded in the Reveal.js deck (no FA stylesheet included in the YAML header or SCSS).

### No Issues
- All other slides render correctly
- Math (MathJax) renders perfectly on slides 6, 9, 11, 12, 13 -- equations, matrices, Greek letters all display correctly
- Two-column layout (slide 6), two-card layout (slide 5) all render cleanly
- No overflow or cut-off text on any slide

---

## M4: Claude Desktop & Code (19 slides)

### Issues Found

**Slide 15 (Merging Data from Different Sources)** -- Moderate
- Mermaid diagram renders but node fill colors are not applied. The boxes for CSV, Excel, PDF, Claude Code, and Unified Table show as nearly transparent/white with faint blue or orange outlines instead of the solid fills specified in the mermaid style directives (`fill:#eff6ff`, `fill:#dbeafe`, `fill:#fff7ed`).
- The diagram uses `transform: scale(3.5)` from the SCSS, which makes it quite large. The "PDF" node extends close to the bottom edge of the slide. The diagram is functional but visually underwhelming compared to the intended design.
- The node text is left-aligned instead of centered within the boxes.

### No Issues
- Three-card layout (slide 3) renders well
- Two-card layouts (slides 6, 11, 12, 13) all render cleanly
- Explainer text below cards (slides 3, 11, 13) displays correctly
- Section dividers (slides 2, 10, 14) render correctly
- All text-only slides are clean and well-spaced

---

## M5: Discounted Cash Flow Analysis (24 slides)

### Issues Found

**Slide 5 (The Assumption Set)** -- MAJOR
- Content overflows the bottom of the slide. The closing paragraph "Capital expenditures are not assumed directly -- they are computed from PP&E and depreciation." is cut off at the bottom. The word "depreciation" is barely visible, clipped by the slide boundary. The title is also pushed to the very top edge.
- Root cause: the 8-row table plus the intro paragraph and closing paragraph exceed the available vertical space at the default 44px font size.
- Fix: Add `.shrink` class to this slide, or reduce the table font size, or move the closing paragraph to the next slide.

**Slide 6 (Pro Forma Income Statement)** -- Minor
- The table fills the slide well but the title "Pro Forma Income Statement" is pushed to the very top edge with no top padding. Not clipped, but tight.

**Slide 9 (Two-Stage DCF: Overview)** -- MAJOR
- The title "Two-Stage DCF: Overview" is cut off at the top -- only the bottom portion of the letters is visible.
- The mermaid flowchart (top-down, 3 nodes) takes significant vertical space. Combined with the bullet points and paragraph below, the slide overflows both top and bottom.
- The paragraph "Equity value = Enterprise value - net debt. Discount at the WACC." appears to be cut off or missing at the bottom.
- The mermaid node fill colors are not applied (same issue as M4 slide 15) -- boxes are nearly transparent instead of solid blue/orange fills.
- Fix: Either reduce the mermaid `transform: scale()` for this slide, split content across two slides, or use a smaller diagram.

**Slide 15 (Simulation Setup)** -- Minor
- This slide has BOTH a mermaid diagram AND a 4-row table, but it actually renders better than slide 9. The horizontal flowchart (LR direction) takes less vertical space. However, the mermaid node fill colors are again not applied (transparent boxes instead of solid fills).

---

## Cross-Deck Issues

### Mermaid Diagram Fill Colors Not Rendering (all decks)
- **Affected slides:** M4 slide 15, M5 slides 9 and 15
- The inline `style` directives in mermaid code (e.g., `style S1 fill:#eff6ff,stroke:#3b82f6`) are not producing visible background fills. Nodes appear as nearly transparent boxes with faint outlines.
- This may be caused by the mermaid theme or CSS specificity conflicts. The SCSS applies `transform: scale(3.5)` and `transform-origin: top left` to `.reveal .mermaid`, which affects sizing but not colors.
- Possible cause: Quarto's mermaid initialization may override the `base` theme settings, or the SVG rendering pipeline may strip inline styles.

### Font Awesome Icons Not Loading
- **Affected:** M3 slide 8 (CSV icon)
- The `<i class="fa-solid fa-file-csv">` element doesn't render because Font Awesome CSS is not included in the Reveal.js slides. The main Quarto site likely loads FA, but the standalone slide decks do not.

---

## Summary

| Deck | Slides | Major Issues | Minor Issues |
|------|--------|-------------|-------------|
| M3   | 16     | 0           | 1 (FA icon) |
| M4   | 19     | 0           | 1 (mermaid colors) |
| M5   | 24     | 2 (overflow on slides 5, 9) | 2 (tight titles, mermaid colors) |

### Priority Fixes
1. **M5 slide 5 ("The Assumption Set")** -- text cut off at bottom, needs `.shrink` or content reduction
2. **M5 slide 9 ("Two-Stage DCF: Overview")** -- title clipped at top, content overflows bottom, needs restructuring
3. **All mermaid diagrams** -- node fill colors not rendering (cosmetic but makes diagrams look unfinished)
4. **M3 slide 8** -- Font Awesome icon missing (minor, link text works fine)
