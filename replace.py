import os

files = [
    "0-intro",
    "1-simulation",
    "2-data",
    "3-alphas_betas",
    "4-visualization",
    "5-portfolios",
    "6-autoregression",
    "7-linear",
    "8-trees",
    "9-classification",
    "10-nets"
]
for file in files:
    with open(f"docs\{file}.qmd", 'r') as f:
        contents = f.read()
        updated = contents.replace("0.3", "0.4")
    with open(f"docs\{file}.qmd", 'w') as f:
        f.write(updated)

