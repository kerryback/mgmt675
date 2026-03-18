# Slide Formatting Review: M2–M11

Reviewed 2026-03-17 via Playwright screenshots of deployed RevealJS decks.

## No Issues Found
- **M2: Intro to Claude** — all slides clean
- **M6: Skills** — all slides clean

## Content Overflow (text/content cut off at bottom or top)

| Module | Slide | Issue |
|--------|-------|-------|
| M3 | Example of Linear Equations | Final equation cut off at bottom (too much math for one slide) |
| M4 | Title slide | Title "Module 4: Claude Desktop and Claude Code" wraps; "Claude" cut off at right edge |
| M4 | CLAUDE.md | Last line pressed against bottom edge |
| M4 | Installing the Terminal and VS Code | No top margin on title; bottom text partially cut off |
| M4 | Merging Data from Different Sources | Title not visible; "Common scenarios" bullets cut off at bottom |
| M5 | The Assumption Set | Last line ("...+ depreciation") cut off behind nav bar |
| M5 | Pro Forma Income Statement | Footnote about NOPAT pressed against bottom, no margin |
| M5 | Two-Stage DCF: Overview | Third bullet cut off mid-sentence |
| M5 | Simulation Setup | Third bullet partially cut off by nav bar |
| M7 | Defense in Depth | Closing sentence cut off at bottom |
| M7 | Improving SQL Quality | Closing sentence about Databricks finding cut off |
| M7 | Data Sovereignty | Left column last bullet cut off; title "D" clipped at top |
| M7 | Fine-Tuning and SLMs | Closing sentence pressed against bottom nav bar |
| M11 | Evolution of Text-Based Trading | Footnote text barely fits at bottom |

## Mermaid Diagram Overflow

| Module | Slide | Issue |
|--------|-------|-------|
| M8 | Sandboxed Execution | "Web UI" box cut off at top; "Database"/"Report" boxes below visible area |
| M9 | How MCP Works (architecture) | Title missing; "Browser Server" cut off at top; bottom text clipped |
| M9 | Multi-Server MCP Configurations | JSON code block truncated after ~line 11 |
| M10 | Three Approaches | Title partially cut off; third bullet cut off at bottom |
| M10 | RAG Pipeline | Title completely missing; only middle of pipeline visible (worst overflow) |
| M11 | Model Selection: Speed vs. Depth | Title missing; numbered list cut off at bottom |

## Other

| Module | Slide | Issue |
|--------|-------|-------|
| M5 | In-Class Exercise: Pro Forma Skill | `PP\&E` renders with literal backslash instead of `PP&E` in LaTeX |

## Suggested Fixes

1. **Content overflow**: Split dense slides into two, reduce content, or add `.shrink` class
2. **Mermaid overflow**: Reduce fontSize in mermaid init, use `%%| fig-width` / `fig-height`, or split diagrams across slides
3. **M9 JSON block**: Use smaller font class (`.shrink`) or trim the example
4. **M5 LaTeX bug**: Change `PP\&E` to `PP&E` inside `\text{}` or escape differently
