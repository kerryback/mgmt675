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

## CSS Class Reference

### Layout Classes

| Class | Purpose | Usage |
|-------|---------|-------|
| `.two-cards` | Two-column card layout | Problem/solution, comparison pairs |
| `.three-cards` | Three-column card layout | Three options/categories |
| `.four-cards` | Four-column card layout | Summary grids |
| `.two-col` | Simple two-column text | Side-by-side lists without cards |
| `.stat-cards` | Grid of statistic cards | Survey data, metrics |
| `.step-flow` | Horizontal step sequence with arrows | Process flows (4 steps) |
| `.tool-grid` | Grid of icon cards | Tool/feature showcases |

### Card Classes

| Class | Purpose |
|-------|---------|
| `.card` | Base card styling |
| `.card-dark` | Dark navy background card |
| `.card-light` | Light blue background card |
| `.card-title` | Title span inside a card |
| `.info-box` | Shaded information box (replaces `\shadedbox`) |
| `.highlight-box` | Highlighted content box |

### Text Classes

| Class | Purpose |
|-------|---------|
| `.amber` | Amber/gold highlighted text (replaces `\alert{}`) |
| `.accent` | Blue accent text (replaces `\textcolor{accentblue}{}`) |
| `.metric` | Bold blue metric numbers |
| `.explainer` | Smaller explanatory text below main content |

### Slide Type Classes

| Class | Purpose |
|-------|---------|
| `.section-divider` | Dark full-slide section title |
| `.quote-slide` | Dark background quote slide |
| `.image-slide` | Centered image slide |

### Quote Components

| Class | Purpose |
|-------|---------|
| `.quote-text` | Italic serif quote body |
| `.quote-source` | Small attribution line |
| `.case-quote` | Centered case study quote |
| `.case-source` | Case study source citation |

### Special Components

| Class | Purpose |
|-------|---------|
| `.code-box` | Styled code/pseudocode block |
| `.comparison-table` | Side-by-side comparison table |
| `.timeline` | Timeline/roadmap visual |

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

For TikZ flowcharts, convert to Mermaid:

````markdown
```{mermaid}
%%| fig-width: 16
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '28px'}, 'flowchart': {'nodeSpacing': 100, 'rankSpacing': 140, 'padding': 28, 'useMaxWidth': true}}}%%
flowchart LR
  A["<b>Label A</b>"] -->|"edge label"| B["<b>Label B</b>"]

  style A fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#0f172a,font-size:28px,padding:24px
  style B fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#0f172a,font-size:28px,padding:24px
```
````

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

## Common Pitfalls

- **Content overflow**: Large slides may need `.shrink` or reduced content
- **Mermaid scaling**: The shared SCSS scales mermaid by 3.5x — design diagrams small
- **Nested divs**: Every `:::` must be matched; use consistent indentation
- **Empty lines**: Quarto requires empty lines before/after div fences (`:::`)
- **Math**: LaTeX math works directly in `.qmd` files
- **Code blocks**: Use fenced code blocks with language identifiers
- **Special characters**: `$` in dollar amounts needs care — use `\$` or wrap in code
- **Links**: External links should open in new window: `[text](url){target="_blank"}`
