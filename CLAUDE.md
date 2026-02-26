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
- `assignment1.qmd` through `assignment6.qmd` — individual assignments
- `index-pdf.qmd` — PDF version of syllabus
- `docs/` — rendered site (committed for GitHub Pages)
- `files/` — data files for exercises (.xlsx, .zip)

### Slides (Beamer LaTeX)
- `slides/` — all slide decks as `.tex` + `.pdf` pairs
- `slides/mgmt675-style.tex` — shared style (metropolis theme, custom colors, tcolorbox environments)
- `slides/images/` — images used in slides
- Numbered `00` through `15` (plus `18-obsidian`):
  - 00-intro, 01-claude, 02-meanvariance, 03-colab, 04-mcp, 05-cowork
  - 06-claude-code, 07-excel, 08-dashboards, 09-skills, 10-vscode
  - 11-dcf, 12-rag, 13-slms, 14-agents, 15-trading, 18-obsidian

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

## Course Topics (in order)
1. AI with code execution (Claude)
2. Mean-variance analysis with AI
3. AI-written code in Jupyter notebooks
4. Connecting tools to AI (MCP)
5. Connecting a virtual machine to AI (Cowork)
6. Connecting your computer to AI (Claude Code)
7. Using AI in Excel
8. Replacing dashboards with natural language
9. Automating specialized prompts (skills)
10. Using AI inside an IDE (VS Code)
11. Valuing companies with AI (DCF)
12. Retrieval augmented generation
13. Fine-tuning and small language models
14. Building AI agents
15. Trading on news with AI

## Grading
Six group assignments (15% each) + peer assessments (10%). Due Tuesdays at 11:59pm, March 24 through April 28.
