---
name: figure-generation
description: Reproduce figures from the paper using code and data. Use when asked to regenerate, re-plot, or verify any figure.
---

# Figure Generation

Reproduce any figure from the paper.

## Figure Mapping

<!-- Fill in one row per figure -->

| Figure | Script | Data | Estimated Runtime |
|--------|--------|------|-------------------|
| Fig. 1 | `code/scripts/plot_fig1.py` | `data/fig1_data.csv` | ~5 seconds |
| Fig. 2 | `code/scripts/plot_fig2.py` | `data/fig2_data.csv` | ~10 seconds |

## Instructions

1. Install dependencies:
   ```bash
   pip install -r environment/requirements.txt
   ```

2. Generate a specific figure:
   ```bash
   python code/scripts/generate_figures.py --fig 1
   ```

3. Generate all figures:
   ```bash
   python code/scripts/generate_figures.py --all
   ```

4. Output goes to `paper/figures/`

## Verification

After generating a figure, compare it with the pre-built version in `paper/figures/`. The figures should match visually.
