# Slide Formatting Verification: m10-rag and m11-sentiment

**Date:** 2026-03-17
**URLs tested:**
- https://mgmt675.kerryback.com/slides/m10-rag.html (22 slides)
- https://mgmt675.kerryback.com/slides/m11-sentiment.html (35 slides)

**Method:** Playwright headless browser at 1920x1080, navigated through every slide via arrow keys, captured and inspected each screenshot.

---

## m10-rag.html (22 slides)

**No issues found.** All 22 slides render cleanly with no overflow, cut-off text, missing titles, or formatting problems.

---

## m11-sentiment.html (35 slides)

### Slide 11 -- "LLMs vs. Traditional Sentiment Analysis"
- **Issue:** Bottom text ("Traditional bag-of-words methods are now **effectively obsolete** for this task.") sits very close to the bottom edge, partially overlapping the progress bar / hamburger menu area. The text baseline is nearly flush with the slide boundary.
- **Severity:** Minor. Text is still readable but tight.

### Slide 16 -- "What the LLM Extracts"
- **Issue:** Bottom callout text ("LLMs handle all dimensions in a single prompt; traditional methods handle only polarity.") is at the very bottom of the slide frame, partially overlapping the hamburger menu icon and progress bar.
- **Severity:** Minor. The orange text is still legible but the descenders are close to the edge.

### Slide 18 -- "Latency and Alpha Decay"
- **Issue:** Bottom callout text ("You don't need to be the fastest -- you need to be **fast enough for the alpha you're targeting**.") extends to the very bottom edge, with the second line ("targeting.") nearly touching the progress bar.
- **Severity:** Minor. Similar to slide 16.

### Slide 23 -- "The Propagation Problem"
- **Issue:** Content overflows the bottom of the slide. The last bullet sub-item ("3rd order: Food prices rise -> consumer staples margins squeezed") is cut off by the progress bar and hamburger menu. The title area is also pushed to the very top with no breathing room.
- **Severity:** Moderate. This slide has the most content and the bottom line is partially obscured.

### Slide 28 -- "Cautionary Tales"
- **Issue:** Bottom callout text ("The competitive edge is real, but so are the risks.") is at the very bottom, partially behind the progress bar area.
- **Severity:** Minor.

---

## Summary

| Deck | Total Slides | Issues | Severity |
|------|-------------|--------|----------|
| m10-rag | 22 | 0 | -- |
| m11-sentiment | 35 | 5 | 1 moderate, 4 minor |

**Common pattern in m11:** Several slides have a bottom callout/summary line (usually orange-colored text) that sits too close to the slide bottom edge, where it competes with RevealJS's progress bar and hamburger menu. The worst case is slide 23, where actual bullet content is cut off.

**Suggested fix:** For slides 11, 16, 18, 23, and 28, either reduce content slightly, decrease font size on those slides, or add `{.smaller}` class / adjust vertical spacing so the bottom text has more clearance from the slide edge.
