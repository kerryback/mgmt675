# MGMT 675: Generative AI for Finance

## Project Overview

Course materials for MGMT 675 at Rice Business, including slides, exercises, and documentation.

## Skills

### gamma-presentations

Create professional slide decks using gamma.app with AI-generated images. Use this skill when:

- Creating presentation slides with AI-generated imagery
- Processing gamma.app PPTX exports
- Creating cover slides for course topics
- Generating custom images via the Gamma API

**Key capabilities:**
- Generate presentations with AI images via Gamma API
- Post-process PPTX files (ensure 16:9, adjust fonts, replace colors)
- Create cover slides with course branding

**Example commands:**
- "Create a gamma image for [topic]"
- "Process gamma export [filename]"
- "Create cover slide for [topic]"

See `.claude/skills/gamma-presentations.md` for full documentation.

## File Structure

- `slides/` - Beamer LaTeX slide decks
- `slides/images/` - Images for presentations
- `docs/` - Course documentation and exercises
- `gamma_pptx_utils.py` - Python utilities for PPTX processing
- `test_gamma_api.py` - Gamma API test script

## Conventions

- Slides use 16:9 aspect ratio
- Section title slides: large title on left, image on right
- Images stored in `slides/images/`
