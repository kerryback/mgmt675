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
- Module decks: `m1` through `m8`:
  - m1-ai-financial-tool, m2-portfolio-valuation, m3-data-tools
  - m4-automating-workflows, m5-verification, m6-financial-documents
  - m7-financial-applications, m8-trading-markets

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
1. AI as a Financial Tool
2. Portfolio Optimization and Company Valuation
3. Connecting AI to Data and Tools
4. Automating Financial Workflows
5. Verifying AI-Generated Analysis
6. Working with Financial Documents
7. Building Financial AI Applications
8. AI in Trading and Markets

## Assignment Schedule (6 weeks)
| Week | Due | Modules | Exercises |
|------|-----|---------|-----------|
| 1 | 3/24 | M1 | 1A, 1B, 1C |
| 2 | 3/31 | M2 | 2A, 2B, 2C |
| 3 | 4/7 | M3 | 3A, 3B, 3C, 3D |
| 4 | 4/14 | M4 + M5 | 4A, 4B, 4C |
| 5 | 4/21 | M6 + M7 | 5A, 5B, 5C |
| 6 | 4/28 | M8 | 6A, 6B |

## Grading
Six group assignments (15% each) + peer assessments (10%). Due Tuesdays at 11:59pm, March 24 through April 28.
