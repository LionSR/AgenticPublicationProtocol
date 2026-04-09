---
name: prepublish-organize
description: Organize a messy research repo into a clean structure before publishing. Use when a researcher has a working repo with scattered files — notebooks, scripts, data, LaTeX — and wants to clean it up. Can be used standalone or as preparation for /publish-paper.
---

# Pre-Publish Organize

Help a researcher turn a messy working repo into a clean, navigable structure. This is the "clean your desk before guests arrive" step — the repo was organized for doing the work, now it needs to be organized for others to understand it.

## When to use

- Before `/publish-paper` when the repo is disorganized
- Standalone when a researcher wants to clean up for collaborators or archival
- When inheriting someone else's messy project

## Process

### 1. Survey the current state

Read the repo thoroughly. Build a complete picture:

**Find everything:**
- Paper source files (`.tex`, `.bib`, `.md`, `.docx`)
- Code files — what languages, what frameworks
- Notebooks (`.ipynb`, `.Rmd`) — these are often the messiest part
- Data files — CSVs, HDF5, JSON, images, simulation output
- Figures — generated images, plots, diagrams
- Config files — YAML, JSON, TOML configs for experiments
- Build artifacts — compiled PDFs, cached outputs, `__pycache__`, `.aux` files
- Environment files — `requirements.txt`, `environment.yml`, `Pipfile`, lock files
- Stale files — old versions, backup copies (`*_old`, `*_v2`, `Copy of *`)
- Hidden files — `.env`, credentials, API keys (flag these immediately)

**Understand the relationships:**
- Which scripts produce which figures?
- Which notebooks depend on which data files?
- What order do things need to run in?
- What's the entry point for reproducing the main results?
- Are there scripts that download or preprocess data?

**Estimate sizes:**
- Which files/directories are large? (`du -sh *`)
- Is anything too large for git? (>50MB → needs LFS or external hosting)
- Are there generated files that shouldn't be tracked?

### 2. Present findings and propose a plan

Show the researcher what you found:
- Total files and size
- What looks like it belongs together
- What looks stale or duplicated
- Any credentials or sensitive files found
- Large files that need special handling

Propose a target structure. Adapt to what's actually in the repo — don't force a structure that doesn't fit:

**For a typical computational paper:**
```
paper/
├── main.tex, *.bib
├── figures/          ← generated figures (final versions)
└── build/            ← compiled PDF

code/
├── src/              ← core implementation
├── scripts/          ← utility scripts, figure generation
├── configs/          ← experiment configurations
└── notebooks/        ← cleaned Jupyter notebooks (if any)

data/
├── raw/              ← original data (or download instructions)
├── processed/        ← intermediate results
└── README.md         ← what the data is, where it came from

environment/
├── requirements.txt  ← pinned dependencies
└── README.md         ← setup instructions
```

**For a theory paper with minimal code:**
```
paper/
├── main.tex, *.bib
├── figures/
└── build/

code/                 ← maybe just a few scripts or notebooks
└── ...
```

**For a notebook-heavy project:**
```
paper/
├── ...

notebooks/
├── 01_data_prep.ipynb
├── 02_analysis.ipynb
├── 03_figures.ipynb
└── README.md         ← run order, what each notebook does

data/
└── ...
```

Wait for the researcher to approve or modify the plan. They know which files matter and which don't.

### 3. Clean up

With researcher approval, execute the reorganization:

**Move files into the target structure:**
- Move, don't copy — avoid creating duplicates
- Preserve git history: use `git mv` when possible
- Update any internal references (imports, file paths in scripts, `\includegraphics` paths in LaTeX)

**Handle notebooks:**
- Notebooks are often the hardest part — they contain code, output, and narrative mixed together
- Ask the researcher: keep as notebooks, or extract key code into scripts?
- If keeping notebooks: clear output cells, add a run-order README
- If extracting: pull figure-generation and key analysis into standalone `.py` scripts

**Handle stale files:**
- Show the researcher a list of files that look stale or duplicated
- Let them decide: delete, archive (move to `_archive/`), or keep
- Don't delete anything without explicit approval

**Handle large files:**
- Files >50MB: suggest Git LFS or external hosting (Hugging Face, Zenodo)
- Generated files that can be reproduced: add to `.gitignore`, document the generation command
- Intermediate data: keep if needed for figures, remove if reproducible

**Handle sensitive files:**
- `.env`, API keys, credentials: add to `.gitignore` immediately
- If they're already in git history, warn the researcher (they may need to scrub history)
- Replace hardcoded paths with relative paths or config variables

**Create a .gitignore:**
```
# Build artifacts
__pycache__/
*.pyc
*.aux
*.log
*.out
*.synctex.gz

# Large generated files
*.h5
*.hdf5
*.checkpoint

# Sensitive
.env
*.key

# OS files
.DS_Store
Thumbs.db
```

Adapt to what's actually in the repo.

### 4. Verify nothing broke

After reorganizing:
- Can the paper still compile? (`pdflatex`, `typst`, etc.)
- Do the figure generation scripts still work with the new paths?
- Do notebooks run in the documented order?
- Are all imports/includes updated?

Fix anything that broke from the move.

### 5. Create a README

Write a README.md for the repo (if one doesn't exist) or update it:

```markdown
# [Paper Title]

## Structure
- `paper/` — LaTeX source and compiled PDF
- `code/` — [what the code does]
- `data/` — [what data is included]

## Reproducing results

### Setup
[how to install dependencies]

### Figures
[how to generate each figure]

### Full experiment
[how to run from scratch, if applicable]
```

### 6. Report to the researcher

Summarize what was done:
- Files moved (from → to)
- Files deleted or archived
- Files added to .gitignore
- References updated
- Anything that needs manual attention

If being used before `/publish-paper`, the repo is now ready — publish-paper can proceed with creating the AGENTS.md.
