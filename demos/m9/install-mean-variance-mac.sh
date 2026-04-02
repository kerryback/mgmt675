#!/bin/bash
echo "Installing mean-variance skill for Claude Code..."
echo
python3 "$(dirname "$0")/install-mean-variance.py"
echo
echo "Press Enter to close..."
read
