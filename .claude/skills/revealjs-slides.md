# RevealJS Slide Conversion Skill

## Trigger
Use this skill when the user asks to create, convert, or edit RevealJS slide decks for the MGMT 675 course. This includes converting Beamer LaTeX slides to Quarto RevealJS format.

## YAML Header Template

Every `.qmd` slide deck begins with this header:

```yaml
---
title: "Module N: Title"
subtitle: "MGMT 675: Generative AI for Finance"
author: "Kerry Back"
format:
  revealjs:
    theme: [default, revealjs-style.scss]
    slide-number: c
    transition: fade
    navigation-mode: linear
    width: 1920
    height: 1080
    margin: 0.05
    center: true
---
```

## Slide Structure

- Each slide begins with `## Title`
- Section dividers use `## Title {.section-divider}`
- Quote slides use `## Title {.quote-slide}`
- Image slides use `## Title {.image-slide}`
- Slides with large content can use `{.shrink}` attribute (maps to Beamer's `[shrink]`)

## Full SCSS Stylesheet

The file `slides/revealjs-style.scss` defines all available classes. Here is the complete stylesheet — use these classes exactly as defined:

```scss
/*-- scss:defaults --*/

// Color palette
$dark-navy: #0f172a;
$slate: #334155;
$bright-blue: #3b82f6;
$amber: #f59e0b;
$off-white: #f8fafc;
$light-blue-tint: #eff6ff;

// Fonts
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

$font-family-sans-serif: 'Inter', system-ui, -apple-system, sans-serif;
$presentation-font-size-root: 44px;
$presentation-line-height: 1.5;
$presentation-h1-font-size: 1.8em;
$presentation-h2-font-size: 1.5em;

$body-color: $slate;
$presentation-heading-color: $dark-navy;
$link-color: $bright-blue;
$body-bg: $off-white;

/*-- scss:rules --*/

// ── Global slide styling ──
// Vertically center all slide content
.reveal .slides section {
  text-align: left;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  height: 100% !important;
  padding: 0.5em 0;
}

.reveal .slide-number {
  font-family: 'Inter', sans-serif;
  font-size: 0.5em;
  color: rgba($slate, 0.5);
}

.reveal h2 {
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-top: 0;
  margin-bottom: 0.4em;
  border-bottom: 3px solid $bright-blue;
  padding-bottom: 0.15em;
  display: inline-block;
}

// ── Title slide ──
#title-slide {
  background: $dark-navy !important;
  text-align: left !important;
  padding: 3em 2em !important;
  position: relative;
  overflow: hidden;

  &::before { display: none; }

  h1.title {
    color: #fff !important;
    font-size: 2.4em !important;
    font-weight: 900 !important;
    letter-spacing: -0.03em;
    border: none !important;
    margin-bottom: 0.2em;
  }

  .subtitle {
    color: $bright-blue !important;
    font-size: 1.1em !important;
    font-weight: 400;
  }

  .author, .quarto-title-authors {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 1.1em !important;
    font-weight: 400;
    margin-top: 1.5em;
    text-align: left !important;
  }

  .quarto-title-author-name {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 1em !important;
    font-weight: 400;
  }

  .date { display: none; }
}

// ── Quote slides ──
.quote-slide {
  h2 {
    color: rgba(255, 255, 255, 0.9) !important;
    border-bottom-color: $amber !important;
    font-size: 1.2em;
  }

  background: $dark-navy !important;
  color: rgba(255, 255, 255, 0.92) !important;

  .quote-text {
    font-family: Georgia, 'Times New Roman', serif;
    font-style: italic;
    font-size: 1.15em;
    line-height: 1.65;
    max-width: 88%;

    .amber { color: $amber; font-weight: 600; font-style: normal; }
  }

  .quote-source {
    margin-top: 1.5em;
    font-family: 'Inter', sans-serif;
    font-style: normal;
    font-size: 0.7em;
    color: rgba(255, 255, 255, 0.45);
  }
}

// ── Stat cards ──
.stat-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1em;
  margin-top: 0.5em;

  .stat-card {
    background: $light-blue-tint;
    border-radius: 12px;
    padding: 1em 1.2em;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    text-align: center;

    .stat-number { font-size: 2.4em; font-weight: 900; color: $bright-blue; line-height: 1.1; }
    .stat-label { font-size: 0.65em; color: $slate; margin-top: 0.3em; line-height: 1.3; }
  }
}

.stat-cards .bottom-row {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1em;
}

// ── Two cards (problem / solution) ──
.two-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5em;
  margin-top: 0.4em;

  .card {
    border-radius: 12px;
    padding: 1.2em 1.5em;
    .card-title { display: block; font-size: 0.9em; font-weight: 700; margin-bottom: 0.5em; }
    ul { font-size: 0.78em; line-height: 1.5; margin: 0; padding-left: 1.2em; }
  }

  .card-dark {
    background: $dark-navy; color: #fff;
    .card-title { color: $amber; }
  }

  .card-light {
    background: $light-blue-tint; color: $slate;
    .card-title { color: $bright-blue; }
    .metric { font-weight: 800; color: $bright-blue; }
  }
}

.case-quote {
  text-align: center; margin-top: 0.8em; font-size: 0.75em; font-style: italic; color: $slate;
  .amber { color: $amber; font-weight: 700; font-style: normal; }
}

.case-source { text-align: center; font-size: 0.6em; color: rgba($slate, 0.6); margin-top: 0.3em; }

// ── Section divider ──
.section-divider {
  background: $dark-navy !important;
  text-align: center !important;
  align-items: center !important;
  h2 { color: #fff !important; font-size: 2.2em !important; border-bottom-color: $amber !important; }
}

// ── Step flow ──
.step-flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.2em;
  margin-top: 0.8em;

  .step-card {
    background: $light-blue-tint; border-radius: 12px; padding: 1.2em 1em;
    text-align: center; position: relative;
    .step-icon { font-size: 2em; margin-bottom: 0.2em; }
    .step-title { font-size: 0.8em; font-weight: 800; color: $dark-navy; margin-bottom: 0.2em; }
    .step-desc { font-size: 0.6em; color: $slate; line-height: 1.4; }
    &::after { content: "\2192"; position: absolute; right: -0.8em; top: 50%; transform: translateY(-50%); font-size: 1.4em; color: $bright-blue; font-weight: 700; }
    &:last-child::after { display: none; }
  }
}

// ── Tool grid ──
.tool-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.2em;
  margin-top: 1em;

  .tool-card {
    background: $light-blue-tint; border-radius: 12px; padding: 1.5em 1em;
    text-align: center; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    .tool-icon { font-size: 2.5em; margin-bottom: 0.3em; }
    .tool-label { font-size: 0.75em; font-weight: 600; color: $dark-navy; }
  }
}

// ── Mermaid diagrams ──
.reveal .mermaid svg { max-width: 100%; margin: 0 auto; }

.reveal .mermaid {
  margin-top: 0.5em; margin-bottom: 0.5em;
  transform: scale(3.5); transform-origin: top left; margin-bottom: 14em;
}

.mermaid-small .mermaid { transform: scale(2) !important; margin-bottom: 6em !important; }
.mermaid-compact .mermaid { transform: scale(1.5) !important; margin-bottom: 3em !important; }

.reveal .mermaid .nodeLabel { font-weight: 700 !important; font-size: 1.1em !important; }
.reveal .mermaid .edgeLabel { font-weight: 600 !important; }

// ── Inline code ──
.reveal code { color: #e74c3c; background: rgba(0, 0, 0, 0.06); padding: 0.1em 0.3em; border-radius: 4px; font-size: 0.9em; }

// ── Code blocks ──
.reveal pre { background: #272822; border-radius: 10px; padding: 1.2em 1.5em; font-size: 0.75em; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
.reveal pre code { color: #f8f8f2; background: transparent; }

// ── Explainer text ──
.explainer { font-size: 0.82em; line-height: 1.55; color: $slate; margin-top: 0.8em; }

// ── Agent components list ──
.agent-components { font-size: 0.82em; li { margin-bottom: 0.6em; } }

// ── Image slide ──
.image-slide {
  text-align: center !important; align-items: center !important;
  h2 { display: inline-block; margin-bottom: 0.2em; }
  h3 { font-size: 1em; margin-top: 0; margin-bottom: 0.2em; }
  img { border-radius: 8px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); }
}

// ── Fix images in flex-column slide layout ──
.reveal .slides section img { flex-shrink: 0; max-height: 75vh; width: auto; max-width: 90%; display: block; margin: auto; }
.reveal .slides section img.r-stretch { max-height: 75vh !important; width: auto !important; max-width: 90% !important; }

// ── Inline text classes ──
.amber { color: $amber; font-weight: 600; }
.accent { color: $bright-blue; font-weight: 600; }

// ── Info box (replaces \shadedbox) ──
.info-box {
  background: $light-blue-tint; border-radius: 12px; padding: 1em 1.3em;
  margin-top: 0.4em; margin-bottom: 0.4em; font-size: 0.82em;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  .box-title { display: block; font-size: 1.05em; font-weight: 700; color: $bright-blue; margin-bottom: 0.4em; }
  ul, ol { margin: 0; padding-left: 1.2em; line-height: 1.5; }
}

// ── Highlight box ──
.highlight-box {
  background: rgba($bright-blue, 0.06); border-left: 4px solid $bright-blue;
  border-radius: 0 12px 12px 0; padding: 0.8em 1.2em;
  margin-top: 0.4em; margin-bottom: 0.4em; font-size: 0.82em;
}

// ── Two-column text layout ──
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em; margin-top: 0.4em; font-size: 0.82em; }

// ── Three-column text layout ──
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5em; margin-top: 0.4em; font-size: 0.82em; }

// ── Three cards ──
.three-cards {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2em; margin-top: 0.4em;
  .card {
    border-radius: 12px; padding: 1em 1.2em;
    .card-title { display: block; font-size: 0.9em; font-weight: 700; margin-bottom: 0.4em; }
    ul, ol { font-size: 0.78em; line-height: 1.5; margin: 0; padding-left: 1.2em; }
  }
  .card-dark { background: $dark-navy; color: #fff; .card-title { color: $amber; } }
  .card-light { background: $light-blue-tint; color: $slate; .card-title { color: $bright-blue; } }
}

// ── Four cards ──
.four-cards {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 1em; margin-top: 0.4em;
  .card {
    border-radius: 12px; padding: 0.8em 1em;
    .card-title { display: block; font-size: 0.85em; font-weight: 700; margin-bottom: 0.3em; }
    ul, ol { font-size: 0.72em; line-height: 1.4; margin: 0; padding-left: 1.1em; }
  }
  .card-dark { background: $dark-navy; color: #fff; .card-title { color: $amber; } }
  .card-light { background: $light-blue-tint; color: $slate; .card-title { color: $bright-blue; } }
}

// ── Code box (styled pseudocode) ──
.code-box {
  background: #272822; color: #f8f8f2; border-radius: 10px; padding: 1.2em 1.5em;
  font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
  font-size: 0.72em; line-height: 1.6; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); margin-top: 0.5em;
  .box-title { display: block; color: $bright-blue; font-weight: 700; margin-bottom: 0.5em; font-family: 'Inter', sans-serif; font-size: 1.1em; }
}

// ── Comparison table ──
.comparison-table {
  margin-top: 0.5em; font-size: 0.78em;
  table { width: 100%; border-collapse: collapse;
    th { background: $dark-navy; color: #fff; padding: 0.6em 1em; text-align: left; font-weight: 700; }
    td { padding: 0.5em 1em; border-bottom: 1px solid rgba($slate, 0.15); }
    tr:nth-child(even) td { background: $light-blue-tint; }
  }
}

// ── Timeline ──
.timeline {
  display: flex; gap: 1em; margin-top: 0.6em; position: relative;
  &::before { content: ''; position: absolute; top: 1.5em; left: 0; right: 0; height: 3px; background: $bright-blue; z-index: 0; }
  .timeline-item {
    flex: 1; text-align: center; position: relative; z-index: 1;
    .timeline-dot { width: 16px; height: 16px; background: $bright-blue; border-radius: 50%; margin: 0.8em auto 0.5em; border: 3px solid $off-white; box-shadow: 0 0 0 2px $bright-blue; }
    .timeline-label { font-size: 0.7em; font-weight: 700; color: $dark-navy; }
    .timeline-desc { font-size: 0.6em; color: $slate; margin-top: 0.2em; line-height: 1.3; }
  }
}

// ── Centered statement slide ──
.centered-statement { text-align: center !important; align-items: center !important; h2 { border: none !important; } }

// ── Shrink class for dense slides ──
.shrink { font-size: 0.9em; h2 { font-size: 1.3em; } ul, ol { font-size: 0.92em; } }

// ── Styled tables ──
.reveal table {
  font-size: 0.78em; border-collapse: collapse; margin-top: 0.3em;
  th { background: $dark-navy; color: #fff; padding: 0.5em 0.8em; font-weight: 700; text-align: left; }
  td { padding: 0.4em 0.8em; border-bottom: 1px solid rgba($slate, 0.15); }
  tr:nth-child(even) td { background: $light-blue-tint; }
}

// ── Step flow variants ──
.step-flow-5 {
  @extend .step-flow;
  grid-template-columns: repeat(5, 1fr);
  .step-card { padding: 1em 0.8em; .step-icon { font-size: 1.6em; } .step-title { font-size: 0.72em; } .step-desc { font-size: 0.55em; } }
}

.step-flow-6 {
  @extend .step-flow;
  grid-template-columns: repeat(6, 1fr);
  .step-card { padding: 0.8em 0.6em; .step-icon { font-size: 1.4em; } .step-title { font-size: 0.68em; } .step-desc { font-size: 0.5em; } }
}

// ── Top-aligned slide (image fills below title) ──
.top-aligned {
  display: flex !important; flex-direction: column !important;
  align-items: center !important; justify-content: flex-start !important;
  padding-top: 0.5em !important;
  h2 { margin-bottom: 0.3em; font-size: 1.4em; }
  .quarto-figure { flex: 1; display: flex; align-items: flex-start; justify-content: center;
    img { max-height: 78vh; width: auto; object-fit: contain; }
  }
}
```

## Beamer → RevealJS Mapping

| Beamer | RevealJS |
|--------|----------|
| `\begin{frame}{Title}` | `## Title` |
| `\begin{frame}[shrink=N]{Title}` | `## Title {.shrink}` |
| `\shadedbox[title=\textbf{X}]{...}` | `:::{.info-box}\n[X]{.box-title}\n...\n:::` |
| `\begin{baritemize}` | Bullet list in `:::{.highlight-box}` |
| `\begin{barenumerate}` | Numbered list in `:::{.highlight-box}` |
| `\begin{columns}[T]\begin{column}{0.5\textwidth}` | `:::{.two-col}` or `:::{.two-cards}` |
| Three columns | `:::{.three-cards}` |
| Four columns | `:::{.four-cards}` |
| `\alert{text}` | `[text]{.amber}` |
| `\textcolor{accentblue}{text}` | `[text]{.accent}` |
| `\textbf{text}` | `**text**` |
| `\textit{text}` | `*text*` |
| `\texttt{text}` | `` `text` `` |
| `\href{url}{text}` | `[text](url)` |
| `\url{url}` | `[url](url)` |
| `\begin{itemize}` | `- item` |
| `\begin{enumerate}` | `1. item` |
| `\begin{verbatim}...\end{verbatim}` | ````language\n...\n```` |
| `\begin{tabular}` | Markdown table or styled div |
| TikZ flowcharts | Mermaid diagrams |
| `\section{Title}` | `## Title {.section-divider}` |
| `\vspace{0.3cm}` | (omit — spacing handled by CSS) |
| `$formula$` | `$formula$` (same) |
| `\$` | `$` |
| `\%` | `%` |
| `\&` | `&` |
| `\textbackslash` | `\` |
| `\textasciitilde` | `~` |
| `\ldots` | `...` |
| `\rightarrow` | `→` |

## Mermaid Diagram Template

For TikZ flowcharts, convert to Mermaid. The SCSS scales mermaid diagrams by 3.5x (or 2x/1.5x with `.mermaid-small`/`.mermaid-compact`), so design diagrams at small base sizes — the scaling handles the rest.

**Important sizing rules:**
- **Font size**: Use `fontSize: '56px'` in themeVariables and `font-size:56px` in node styles (the SCSS scaling makes these render at the right size on 1920×1080 slides)
- **Arrow/stroke width**: Use `stroke-width:6px` on node styles (3x the default) for visible arrows at scale
- **Link thickness**: Use `linkStyle default stroke-width:6px` to thicken connecting arrows

````markdown
```{mermaid}
%%| fig-width: 16
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '56px'}, 'flowchart': {'nodeSpacing': 100, 'rankSpacing': 140, 'padding': 28, 'useMaxWidth': true}}}%%
flowchart LR
  A["<b>Label A</b>"] -->|"edge label"| B["<b>Label B</b>"]

  style A fill:#eff6ff,stroke:#3b82f6,stroke-width:6px,color:#0f172a,font-size:56px,padding:24px
  style B fill:#dbeafe,stroke:#3b82f6,stroke-width:6px,color:#0f172a,font-size:56px,padding:24px
  linkStyle default stroke-width:6px
```
````

### Mermaid Size Classes

| Slide class | Mermaid scale | Use when |
|-------------|--------------|----------|
| (none) | 3.5x | Default — diagram is the main content |
| `.mermaid-small` | 2x | Diagram with text below |
| `.mermaid-compact` | 1.5x | Diagram with substantial text |

### Mermaid Style Colors
- Blue tint nodes: `fill:#eff6ff,stroke:#3b82f6`
- Darker blue nodes: `fill:#dbeafe,stroke:#3b82f6`
- Amber/warning nodes: `fill:#fef3c7,stroke:#f59e0b`
- Green nodes: `fill:#f0fdf4,stroke:#22c55e`
- Orange/alert nodes: `fill:#fff7ed,stroke:#ea580c` or `fill:rgba(230,90,50,0.12)`

## Content Patterns

### Info Box with Title (replaces shadedbox)
```markdown
:::{.info-box}
[**Title**]{.box-title}

- Item 1
- Item 2
:::
```

### Two-Column Cards
```markdown
:::{.two-cards}
:::{.card .card-dark}
[Title]{.card-title}

- Content
:::

:::{.card .card-light}
[Title]{.card-title}

- Content
:::
:::
```

### Stat Cards
```markdown
:::{.stat-cards}
:::{.stat-card}
:::{.stat-number}
87%
:::
:::{.stat-label}
description text
:::
:::
:::
```

### Centered Statement Slide
```markdown
## {.centered-statement}

:::{style="text-align:center;"}
**Bold statement here.**

Supporting text below.
:::
```

### Tables
Use standard markdown tables:
```markdown
| Column 1 | Column 2 |
|----------|----------|
| data | data |
```

For styled tables, add a wrapping div if needed.

## Conversion Workflow

1. **Read** the source `.tex` file
2. **Read** `revealjs-style.scss` and `m1-ai-in-finance.qmd` as reference
3. **Write** the `.qmd` file following all conventions above
4. **Render** with `quarto render slides/mN-name.qmd`
5. **Screenshot** each slide: `npx playwright screenshot --viewport-size=1920,1080 http://localhost:... slides/mN-name-slideK.png`
6. **Review** screenshots visually for:
   - No content overflow or clipping
   - Centered content filling the slide
   - Readable font sizes
   - Proper styling of all components
7. **Fix** any issues found
8. **Re-render and re-screenshot** until satisfied

## Images

### Critical: Always use `.nostretch` on images

RevealJS automatically adds an `r-stretch` class to standalone images, which interacts badly with the flex layout in `revealjs-style.scss` — the stretch height calculation breaks under flexbox and the CSS `width: auto !important` rule overrides any inline width. **The result is images that silently collapse to 0 height and don't display.**

Always include `.nostretch` and `fig-align` when inserting images:

```markdown
![](images/my-image.png){fig-align="center" width="85%" .nostretch}
```

**Why each attribute matters:**

| Attribute | Purpose |
|-----------|---------|
| `.nostretch` | Prevents RevealJS from adding `r-stretch` class, avoiding the broken height calculation |
| `fig-align="center"` | Wraps the image in a `<div class="quarto-figure">` container that integrates properly with the flex layout |
| `width="85%"` | Sets the desired width via inline style (not overridden when `r-stretch` is absent) |

### Image slide type

For slides that are primarily an image with a title, use the `.image-slide` class:

```markdown
## Title {.image-slide}

![](images/my-image.png){fig-align="center" width="100%" .nostretch}
```

### Top-aligned image slides

For slides where the image should fill below the title (no vertical centering):

```markdown
## Title {.top-aligned}

![](images/my-image.png){fig-align="center" width="100%" .nostretch}
```

### Never do this

```markdown
![](images/my-image.png){width=85%}
```

This produces a bare `<img>` with `r-stretch` that will be invisible in the browser.

## Common Pitfalls

- **Content overflow**: Large slides may need `.shrink` or reduced content
- **Mermaid scaling**: The shared SCSS scales mermaid by 3.5x — design diagrams small
- **Nested divs**: Every `:::` must be matched; use consistent indentation
- **Empty lines**: Quarto requires empty lines before/after div fences (`:::`)
- **Math**: LaTeX math works directly in `.qmd` files
- **Code blocks**: Use fenced code blocks with language identifiers
- **Special characters**: `$` in dollar amounts needs care — use `\$` or wrap in code
- **Links**: External links should open in new window: `[text](url){target="_blank"}`
