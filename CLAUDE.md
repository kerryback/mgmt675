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
  - m1-ai-financial-tool, m3-claude (Getting Started with Claude Code)
  - m3-portfolio-optimization, m3-dcf-analysis
  - m4-data-tools, m5-automating-workflows, m6-rag
  - m7-apps, m8-reliability, m9-trading-markets

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

## Modules (in order)
1. AI Fundamentals
2. Getting Started with Claude Code
3. Portfolio Optimization (3a) and Company Valuation (3b)
4. Connecting AI to Data and Tools
5. Automating Financial Workflows
6. Working with Financial Documents
7. Building Financial AI Applications
8. Verification and Governance
9. AI in Trading and Markets

## Session Schedule (12 sessions, 6 weeks)
| Session | Date | Module |
|---------|------|--------|
| 1 | Tue 3/17 | M1: AI Fundamentals |
| 2 | Thu 3/19 | M2: Getting Started with Claude Code |
| 3 | Tue 3/24 | M3a: Portfolio Optimization |
| 4 | Thu 3/26 | M3b: Company Valuation |
| 5 | Tue 3/31 | M4: Connecting to Data & Tools |
| 6 | Thu 4/2 | M5a: Automation: Skills & Database Agents |
| 7 | Tue 4/7 | M5b: Automation: Reporting Pipeline & PowerPoint |
| 8 | Thu 4/10 | M6: Financial Documents & RAG |
| 9 | Tue 4/15 | M7: Building AI Applications |
| 10 | Thu 4/17 | M8: Verification & Governance |
| 11 | Tue 4/22 | M9a: Trading: Sentiment Models & Research |
| 12 | Thu 4/24 | M9b: Trading: Implementation & Industry |

## Assignment Schedule (6 weeks)
| Week | Due | Modules | Exercises |
|------|-----|---------|-----------|
| 1 | 3/24 | M1 + M2 | 1A, 1B, 1C |
| 2 | 3/31 | M3 | 2A, 2B, 2C, 2D |
| 3 | 4/7 | M4 + M5a | 3A, 3B, 3C, 3D |
| 4 | 4/14 | M5b + M6 | 4A, 4B, 4C |
| 5 | 4/21 | M7 + M8 | 5A, 5B, 5C |
| 6 | 4/28 | M9 | 6A, 6B |

## Grading
Six group assignments (15% each) + peer assessments (10%). Due Tuesdays at 11:59pm, March 24 through April 28.
