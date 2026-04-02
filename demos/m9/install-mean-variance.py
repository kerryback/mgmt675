"""
Installer for the mean-variance skill for Claude Code.
Creates ~/.claude/skills/mean-variance/ with SKILL.md and scripts/mean_variance.py
"""

import os
import shutil
from pathlib import Path

SKILL_MD = r"""---
description: Run mean-variance portfolio optimization. Prompts for asset parameters, computes the tangency portfolio (no short sales), and generates efficient frontier plots (HTML and PNG).
user_invocable: true
---

Run the mean-variance optimization script:

```bash
python ~/.claude/skills/mean-variance/scripts/mean_variance.py
```

The script will interactively prompt for:
- Number of risky assets
- Expected returns (%) for each asset
- Standard deviations (%) for each asset
- Correlations (upper triangle)
- Risk-free rate (%)

It then computes the tangency portfolio (long-only) and plots the efficient frontier, capital allocation line, tangency portfolio, and individual assets. Two files are saved in the current directory:
- `efficient_frontier.html` (interactive Plotly chart)
- `efficient_frontier.png` (static Matplotlib chart)
""".lstrip()

# mean_variance.py is next to this installer
SCRIPT_SOURCE = Path(__file__).parent / "mean_variance.py"

def main():
    home = Path.home()
    skill_dir = home / ".claude" / "skills" / "mean-variance"
    scripts_dir = skill_dir / "scripts"

    scripts_dir.mkdir(parents=True, exist_ok=True)

    (skill_dir / "SKILL.md").write_text(SKILL_MD, encoding="utf-8")
    print(f"  Created {skill_dir / 'SKILL.md'}")

    if SCRIPT_SOURCE.exists():
        shutil.copy2(SCRIPT_SOURCE, scripts_dir / "mean_variance.py")
        print(f"  Copied  {scripts_dir / 'mean_variance.py'}")
    else:
        print(f"  ERROR: Could not find {SCRIPT_SOURCE}")
        print("  Make sure mean_variance.py is in the same folder as this installer.")
        return

    print()
    print("Done! The /mean-variance skill is now available in Claude Code.")
    print("Restart Claude Code if it is currently running.")

if __name__ == "__main__":
    main()
