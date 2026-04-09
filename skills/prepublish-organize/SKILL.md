---
name: prepublish-organize
description: Organize a messy research repo into a clean structure before publishing. Use when a researcher has a working repo with scattered files — notebooks, scripts, data, LaTeX — and wants to clean it up. Can be used standalone or as preparation for /publish-paper.
---

# Pre-Publish Organize

Help a researcher turn a messy working repo into a clean, navigable structure. This is the "clean your desk before guests arrive" step — the repo was organized for doing the work, now it needs to be organized for others to understand it.

## Guiding principle: single source of truth

The published repo should have exactly one canonical location for each piece of code, data, and documentation. No duplicates, no ambiguity about which version is current. Every file referenced in the paper, scripts, or README should resolve to one real path. This principle drives every decision below — when in doubt, consolidate.

## When to use

- Standalone when a researcher wants to clean up a repo for collaborators or archival
- When inheriting someone else's messy project
- When organizing a repo in place (as opposed to `/publish-paper`, which creates a separate publication repo)

## Process

### 0. Create a branch

Before making any changes, create a new branch:

```bash
git checkout -b prepublish-organize
```

All moves, renames, and deletions stay on this branch. The researcher reviews, tests, and merges when ready.

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

**Build the script→figure mapping:**
This is essential for the README and for anyone reproducing results. For each figure in the paper:
1. Find the figure reference in the paper source (`\includegraphics`, figure filenames)
2. Find the script that generates it (look for `savefig`, `plt.save`, output paths)
3. Identify what data the script reads

Record this as a table — it goes into the README later (step 5).

**Understand other relationships:**
- Which notebooks depend on which data files?
- What order do things need to run in?
- What's the entry point for reproducing the main results?
- Are there scripts that download or preprocess data?

**Estimate sizes:**
- Which files/directories are large? (`du -sh *`)
- Is anything too large for git? (>50MB → needs LFS or external hosting)
- Are there generated files that shouldn't be tracked?

**Flag duplicates:**
Look for multiple versions of the same file, copies in different directories, or data that exists in both raw and processed form without clear separation. These violate single source of truth and need resolution in step 2.

### 2. Present findings and propose a plan

Show the researcher everything in one proposal for a single round of feedback:

- Total files and size
- What looks like it belongs together
- What looks stale or duplicated — and which version to keep as canonical
- Any credentials or sensitive files found
- Large files that need special handling
- The script→figure mapping (ask them to confirm or correct it)
- For notebooks: recommend keeping as notebooks or extracting to scripts, with reasoning

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

Wait for the researcher to approve or modify the plan before proceeding.

### 3. Clean up

With researcher approval, execute the reorganization:

**Move files into the target structure:**
- Move, don't copy — no duplicates. Use `git mv` to preserve history.
- Update all internal references (imports, file paths in scripts, `\includegraphics` paths in LaTeX)
- If the same data or code exists in multiple places, keep only the canonical version and delete the rest

**Handle stale files:**
- Show the researcher the list from step 2
- For each stale file (or group), offer a structured choice: delete / archive (move to `_archive/`) / keep
- Don't delete anything without explicit approval

**Handle large files:**
- Files >50MB: suggest Git LFS or external hosting (Hugging Face, Zenodo)
- Generated files that can be reproduced: add to `.gitignore`, document the generation command
- Intermediate data: keep if needed for figures, remove if reproducible

**Handle sensitive files:**
- `.env`, API keys, credentials: add to `.gitignore` immediately
- If they're already in git history, warn the researcher (they may need to scrub history)
- Replace hardcoded paths with relative paths or config variables

**Create a .gitignore** tailored to what's in the repo — cover build artifacts, generated files, sensitive files, and OS files.

### 4. Verify nothing broke

Actually run things to confirm they still work:

- **Paper compilation**: Run the build command and check it succeeds
- **Figure generation**: Run each figure script and verify it produces output
- **Tests**: If the repo has tests (`pytest`, `unittest`, `make test`, etc.), run them
- **Notebooks**: Execute in order and check for errors
- **Imports**: Verify import paths resolve with the new structure

Fix anything that broke. Common issues after reorganization:
- Relative imports that assumed the old directory structure
- Hardcoded paths in scripts or configs
- LaTeX `\includegraphics` or `\input` paths
- Data file paths in notebooks

### 5. Create a README

Write a README.md for the repo (if one doesn't exist) or update it. Include the script→figure mapping from step 1:

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

| Figure in paper | Script | Data | Output |
|-----------------|--------|------|--------|
| Fig 1 (description) | `code/scripts/fig1.py` | `data/results.csv` | `paper/figures/fig1.pdf` |
| Fig 2 (description) | `code/scripts/fig2.py` | `data/sim_output.h5` | `paper/figures/fig2.pdf` |

### Tests
[how to run the test suite, if one exists]

### Full experiment
[how to run from scratch, if applicable]
```

### 6. Report and hand off to the researcher

Summarize what was done:
- Files moved (from → to)
- Files deleted or archived
- Files added to .gitignore
- References updated
- Anything that needs manual attention

Then ask the researcher to verify on the branch before merging. Provide a tailored checklist focusing on things the agent cannot fully judge — visual correctness of figures, semantic correctness of results, domain-specific checks:

- [ ] Figures look correct (not just error-free — visually match expectations)
- [ ] Results/numbers in generated output match the paper
- [ ] Tests pass (if the repo has a test suite)
- [ ] Any domain-specific pipeline works end-to-end
- [ ] Nothing important was accidentally deleted or archived

Tell them: "Please check these on the `prepublish-organize` branch. Once you're satisfied, merge into your main branch. If anything is broken, let me know and I'll fix it."

Do NOT merge the branch yourself. The researcher merges after they've verified.

If being used before `/publish-paper`, the repo is ready once the researcher merges — publish-paper can then proceed with creating the AGENTS.md.
