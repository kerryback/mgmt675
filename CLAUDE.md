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
- Module decks: `m1` through `m13`:
  - m1-ai-in-finance, m2-intro-claude, m3-mean-variance, m4-claude
  - m5-skills, m6-makers-checkers, m7-tips, m8-scraping
  - m9-agents, m10-corporate, m11-rag, m12-sentiment, m13-extras

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
2. Exploring Claude (m2)
3. Portfolio Optimization (m3)
4. Getting Started with Claude Code (m4)
5. Company Valuation (m5)
6. Makers and Checkers (m6)
7. More Tips (m7)
8. Building a RAG Corpus (m8)
9. Build and Deploy Agents (m9)
10. Corporate Agent Deployment (m10)
11. Magnolia (m11)
12. Retrieval Augmented Generation (m12)
13. Predictive Modeling (m13)
14. Sentiment Analysis (m14)
15. Extra Topics (m15)

## Session Schedule (12 sessions, 6 weeks)
| Session | Date | Module |
|---------|------|--------|
| 1 | Tue 3/17 | M1: AI Fundamentals + M2: Exploring Claude |
| 2 | Thu 3/19 | M4: Getting Started with Claude Code |
| 3 | Tue 3/24 | M3: Portfolio Optimization |
| 4 | Thu 3/26 | M5: Company Valuation |
| 5 | Tue 3/31 | M6: Makers and Checkers + M7: More Tips |
| 6 | Thu 4/2 | M8: Building a RAG Corpus + M9: Build and Deploy Agents |
| 7 | Tue 4/7 | M9: Build and Deploy Agents (cont.) |
| 8 | Thu 4/10 | M10: Corporate Agent Deployment |
| 9 | Tue 4/15 | M11: Retrieval Augmented Generation |
| 10 | Thu 4/17 | M11: RAG (cont.) |
| 11 | Tue 4/22 | M12: Sentiment Analysis |
| 12 | Thu 4/24 | M12: Sentiment Analysis (cont.) |

## Assignment Schedule (6 weeks)
| Week | Due | Modules | Exercises |
|------|-----|---------|-----------|
| 1 | 3/24 | M1 + M2 | 1A, 1B, 1C |
| 2 | 3/31 | M3 + M4 | 2A, 2B, 2C, 2D |
| 3 | 4/7 | M5 + M6 | 3A, 3B, 3C, 3D |
| 4 | 4/14 | M9 + M10 | 4A, 4B, 4C |
| 5 | 4/21 | M11 | 5A, 5B, 5C |
| 6 | 4/28 | M12 | 6A, 6B, 6C |

## Grading
Six group assignments (15% each) + peer assessments (10%). Due Tuesdays at 11:59pm, March 24 through April 28.
