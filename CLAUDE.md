# MGMT 675: Generative AI for Finance

## Overview
Course materials for MGMT 675 at Rice Business, Spring 2026. Instructor: Kerry Back. Meets TTh 12:30-2:00, McNair 212, 3/17/2026-4/23/2026. Deployed at mgmt675.kerryback.com via GitHub Pages.

## Build
- `quarto render` renders the site to `docs/`
- `quarto preview` for local development
- Slides are compiled separately with LaTeX (not Quarto)

## Structure

### Website (Quarto)
- `_quarto.yml` — site config (renders index, slides, assignments pages)
- `index.qmd` — syllabus and course description
- `slides.qmd` — slide deck index (links to PDFs)
- `assignments.qmd` — assignment overview
- `1A.qmd` through `6B.qmd` — individual exercise sheets (rendered to PDF)
- `index-pdf.qmd` — PDF version of syllabus
- `docs/` — rendered site (committed for GitHub Pages)
- `files/` — data files for exercises (.xlsx, .zip)

### Slides (Beamer LaTeX)
- `slides/` — all slide decks as `.tex` + `.pdf` pairs
- `slides/mgmt675-style.tex` — shared style (metropolis theme, custom colors, tcolorbox environments)
- `slides/images/` — images used in slides
- `00-intro` — course introduction
- Module decks: `m1` through `m9`:
  - m1-ai-in-finance, m3-claude (Getting Started with Claude Code)
  - m2-mean-variance, m4-dcf
  - m6-agents, m7-mcp, m5-reliability
  - m8-rag, m9-sentiment

### Other
- `gamma_pptx_utils.py` — Python utilities for PPTX processing
- `test_gamma_api.py` — Gamma API test script
- `.claude/skills/gamma-presentations.md` — skill for creating slides with Gamma API

## Slide Conventions
- **Aspect ratio:** 16:9 (`\documentclass[aspectratio=169]{beamer}`)
- **Theme:** metropolis with custom style via `\input{mgmt675-style}`
- **Colors:** accentblue (RGB 37,99,235), titlegray (RGB 19,60,71), alertorange (RGB 230,90,50)
- **Custom environments:** `shadedbox`, `baritemize` (bulleted list in shaded box), `barenumerate` (numbered list in shaded box)
- **Title slides:** radial gradient background, title graphic on right
- **Compile:** `pdflatex slides/XX-name.tex` (from repo root, or `cd slides && pdflatex XX-name.tex`)

## Quarto Conventions
- Themes: flatly (light) / superhero (dark)
- External links open in new window
- Hypothesis comments enabled
- Font Awesome icons for PDF download links

## Modules (in order, numbers match slide filenames)
1. AI Fundamentals (m1)
2. Portfolio Optimization (m2)
3. Getting Started with Claude Code (m3)
4. Company Valuation (m4)
5. Verification and Governance (m5)
6. AI Agents (m6)
7. Connecting AI to Data and Tools (m7)
8. Working with Financial Documents (m8)
9. AI in Trading and Markets (m9)

## Session Schedule (12 sessions, 6 weeks)
| Session | Date | Module |
|---------|------|--------|
| 1 | Tue 3/17 | M1: AI Fundamentals |
| 2 | Thu 3/19 | M3: Getting Started with Claude Code |
| 3 | Tue 3/24 | M2: Portfolio Optimization |
| 4 | Thu 3/26 | M4: Company Valuation |
| 5 | Tue 3/31 | M6: AI Agents |
| 6 | Thu 4/2 | M6: AI Agents (cont.) |
| 7 | Tue 4/7 | M7: Connecting AI to Data & Tools |
| 8 | Thu 4/10 | M5: Verification & Governance |
| 9 | Tue 4/15 | M8: Working with Financial Documents |
| 10 | Thu 4/17 | M8: Financial Documents (cont.) |
| 11 | Tue 4/22 | M9: Trading: Sentiment Models & Research |
| 12 | Thu 4/24 | M9: Trading: Implementation & Industry |

## Assignment Schedule (6 weeks)
| Week | Due | Modules | Exercises |
|------|-----|---------|-----------|
| 1 | 3/24 | M1 + M3 | 1A, 1B, 1C |
| 2 | 3/31 | M2 + M4 | 2A, 2B, 2C, 2D |
| 3 | 4/7 | M6 | 3A, 3B, 3C |
| 4 | 4/14 | M7 + M5 | 4A, 4B, 4C |
| 5 | 4/21 | M8 | 5A, 5B, 5C |
| 6 | 4/28 | M9 | 6A, 6B, 6C |

## Grading
Six group assignments (15% each) + peer assessments (10%). Due Tuesdays at 11:59pm, March 24 through April 28.
