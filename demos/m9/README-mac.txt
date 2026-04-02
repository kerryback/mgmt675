Mean-Variance Portfolio Optimization Skill for Claude Code
==========================================================

WHAT IT DOES
------------
Installs a /mean-variance skill in Claude Code that runs an interactive
portfolio optimization. It prompts for asset parameters (expected returns,
standard deviations, correlations, and the risk-free rate), computes the
tangency portfolio (no short sales), and generates two plots:

  - efficient_frontier.html  (interactive Plotly chart)
  - efficient_frontier.png   (static Matplotlib chart)

HOW TO INSTALL
--------------
1. Extract all files from this zip into a folder.
2. Open Terminal, cd to that folder, and run:
       bash install-mean-variance-mac.sh
3. Restart Claude Code if it is currently running.

HOW TO USE
----------
Type /mean-variance in Claude Code.
