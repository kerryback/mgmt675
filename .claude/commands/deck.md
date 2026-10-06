---
description: Export a rendered deck to PDF with the global deck skill
argument-hint: <week number or filename>
allowed-tools: Bash(bash ~/.claude/skills/deck/assets/deck-to-pdf.sh:*)
---

Export the deck `$1` by running, from the project root:

```
bash ~/.claude/skills/deck/assets/deck-to-pdf.sh $1 --root docs --out pdfs --size 1920x1080
```

Those three flags are all this repo contributes. Everything else — loose name
matching, re-rendering a stale deck, serving the site over HTTP, mirroring the
result — lives in the global `deck` skill at `~/.claude/skills/deck/`, so it
stays the same across every repo. Do not reimplement any of it here, and if the
export itself needs fixing, fix it there.

`--out pdfs` is the override specific to this repo. Every other course repo of
mine writes to `pdf/`; this one is `pdfs/`, so the flag is not optional and the
script's own `pdf` default is wrong here.

`--root docs` is the rendered site and `--out pdfs` is the tracked copy; the
script mirrors each PDF into `docs/pdfs/` so it is live on the served site
without a full re-render. `pdfs/*.pdf` is in the `resources:` list in
`_quarto.yml`, so a later `quarto render` keeps that copy rather than dropping
it. Commit both.

The `--size 1920x1080` override is the other reason this file exists. The
skill's 1920x1200 default is 16:10 — deliberately taller than a 1920x1080 deck,
to give back the margin decktape drops. Every deck here is shoji, which is a
1280x720 (16:9) canvas with `margin: 0`, so there is no margin to give back and
a 16:10 viewport would just letterbox the slides with bands of page either side.
1920x1080 is 1.5x the canvas, exactly 16:9, and lands a 1440x810pt page.

| Deck | Theme | Canvas | `--size` | Page |
|---|---|---|---|---|
| `week1`–`week6` | `shoji.scss` | 1280x720, 16:9 | 1920x1080 | 1440x810pt |

A deck built here on another canvas gets a second row, and matches its own
aspect ratio rather than keeping this number.

Name the deck in full: `/deck week3`. The skill's loose matching splits a stem
on `_` (it is built for names like `3_teaching`), and `weekN` has no underscore,
so `/deck 3` matches nothing here. Omit `$1` to export every deck currently
rendered under `docs/slides/`. If the name matches nothing the script lists what
it found; relay that list. Report where the PDF landed and its page count.

Only decks listed in the `render:` block of `_quarto.yml` reach `docs/slides/`
in the first place, so an unfinished deck cannot be exported or published by
accident.
