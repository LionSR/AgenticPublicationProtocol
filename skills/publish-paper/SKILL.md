---
name: publish-paper
description: Create an AI agent for an academic paper following the Agentic Publication Protocol. Use when a researcher wants to publish their paper repo with an AGENTS.md so any coding agent can represent the work — explain it, reproduce figures, run experiments, answer questions about the methodology.
---

# Publish Paper as Agent

Create a publication repo for a paper — a clean, public repo with an AGENTS.md that turns it into an AI agent. The researcher's working repo may be private and messy; the publication repo is a curated subset meant for public consumption.

## Process

### 1. Understand the paper

Read the working repo thoroughly before asking the researcher anything. Build a mental model:

**Paper source:**
- Find the main document: look for `*.tex`, `*.md`, `*.pdf` files
- Read it — understand the title, abstract, key claims, structure
- Find figures: where are they stored? Are there source files (`.py`, `.ipynb`) that generate them?

**Code:**
- What language? What framework? Is there a clear entry point?
- Look for `setup.py`, `pyproject.toml`, `requirements.txt`, `environment.yml`, `package.json`, `Cargo.toml`, etc.
- Try to understand what the code does: is it a simulation? data analysis? a model? a proof assistant script?
- Look for scripts that generate figures, run experiments, or produce tables
- Check if there are config files that control parameters

**Data:**
- Is there data in the repo? How large?
- Is it raw data, processed data, or both?
- Are there external data sources referenced?
- Is large data hosted externally? Check for references to:
  - Hugging Face (`huggingface.co/datasets/...`)
  - Zenodo (`zenodo.org/record/...`)
  - Figshare, Dryad, Materials Project, or other domain repositories
  - Google Drive, Dropbox, or cloud storage links
- For any external data, note the URL and how to download it

**Environment:**
- What platform was this developed on? Check for OS-specific code
- Are there GPU requirements? Cluster job scripts?
- Are there Docker files or containerization?

**Build the script→figure mapping:**
For each figure in the paper:
1. Find the figure reference in the paper source (`\includegraphics`, figure filenames)
2. Find the script that generates it (look for `savefig`, `plt.save`, output paths)
3. Identify what data the script reads

**What's missing:**
- Is there anything you can't figure out from reading the repo? Note questions for step 2.

### 2. Discuss with the researcher

Present your understanding of the repo first — show them you've done the homework. Then ask about gaps (one or two questions at a time, not all at once):

**About the paper:**
- What are the key results? (Ask them to state it in their own words — this becomes the Paper Summary)
- What's the main contribution vs. existing work?
- What domain should the agent reason in? (math? physics? ML? biology?)

**About the code:**
- Confirm the script→figure mapping. Fill gaps — which scripts generate which figures?
- What's the main experiment and how do you run it?
- What parameters can a reader change to explore variations?
- What parts of the code are fragile / require specific setup?
- Are there any scripts that take a long time? How long, on what hardware?

**About what to publish:**
- Which files should go into the publication repo? Which should stay private?
- Is there anything in the conversation history they want to include as research context?
- What would a reader most likely want to do? (reproduce figures? extend? understand the math? run with different inputs?)
- What should the publication repo be called?

### 3. Create the publication repo

Create a new repo for the publication. This is separate from the working repo — it contains only what the researcher chose to share.

First check if `gh` CLI is available and authenticated:
```bash
gh auth status
```

If `gh` is not installed or not authenticated, tell the researcher and offer alternatives:
- Install: see https://cli.github.com for all platforms
- Authenticate: `gh auth login`
- Or skip `gh` and create the repo manually on GitHub later

**If `gh` is available** and the researcher wants it on GitHub immediately:
```bash
gh repo create <repo-name> --public --clone
cd <repo-name>
```

**Otherwise**, create locally first:
```bash
mkdir <repo-name> && cd <repo-name> && git init
```

The researcher can push to GitHub later in step 10.

### 4. Copy and organize selected files

Copy the selected files from the working repo into the publication repo. Create the target directories first, then copy:

```bash
# Example — adapt to what's actually being published
mkdir -p paper/figures paper/build code/src code/scripts data environment
cp ../working-repo/paper/main.tex paper/
cp ../working-repo/paper/*.bib paper/
cp ../working-repo/figures/*.pdf paper/figures/
cp -r ../working-repo/src/ code/src/
cp ../working-repo/scripts/generate_*.py code/scripts/
cp ../working-repo/data/results.csv data/
cp ../working-repo/requirements.txt environment/
```

Use the file list from step 2 — copy only what the researcher approved. Then organize into a clean structure:

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

Adapt the structure to what's actually being published — don't force directories that have nothing in them. A theory paper might just have `paper/` and a few scripts.

**Single source of truth:** Each file lives in exactly one place. No duplicates, no ambiguity about which version is current.

**Update all internal references** — imports, file paths in scripts, `\includegraphics` paths in LaTeX, data paths in notebooks. These will differ from the working repo's paths.

**Handle large files:**
- Files >50MB: suggest Git LFS or external hosting (Hugging Face, Zenodo)
- Generated files that can be reproduced: add to `.gitignore`, document the generation command

**Create a .gitignore** tailored to what's in the repo — cover build artifacts, generated files, sensitive files, and OS files.

### 5. Verify the code works

Actually run things in the publication repo to confirm they work with the new paths:

- **Paper compilation**: Run the build command and check it succeeds
- **Figure generation**: Run each figure script and verify it produces output
- **Tests**: If the repo has tests, run them
- **Notebooks**: Execute in order and check for errors
- **Imports**: Verify import paths resolve with the new structure

Fix anything that broke from the copy/reorganization.

### 6. Create AGENTS.md

Generate `AGENTS.md` at the publication repo root. This is the most important file — it must give an agent everything it needs to operate in this repo.

**Writing the identity section:**
- The agent is a spokesperson for THIS work, not a generic assistant
- It should adopt the domain's reasoning style (mathematician for math, experimentalist for physics, etc.)
- It must distinguish between the paper's claims and its own inferences
- It should know the paper's limitations and say so honestly

**Writing the Paper Summary:**
- Use the researcher's own words from step 2
- 2-4 paragraphs covering: what problem, what approach, what results, what implications
- This is what the agent will rely on most — make it substantive

**Writing the Repository Map:**
- Don't just list files — explain what each one does and how they connect
- Group by function: paper source, figure generation, experiments, data, config
- Include file paths relative to the publication repo root
- Note which files are entry points vs. supporting
- For external data (Hugging Face, Zenodo, Figshare, etc.), document:
  - What the dataset is and its size
  - The URL
  - The exact download command (e.g. `huggingface-cli download ...`, `wget ...`, `zenodo_get ...`)
  - Where to put it locally (e.g. `data/`)
  - Whether it's required for basic usage (figures) or only for full reproduction

**Writing "What You Can Do":**
- **Explain the paper**: which files to read for which sections
- **Reproduce figures**: a table mapping EVERY figure to its command, data source, and runtime. Include the exact install command for dependencies.
- **Run experiments**: exact commands with real parameters, not placeholders
- **Extend the work**: what can a reader change? Which parameters are interesting to vary?
- For each capability, include the actual commands, not just descriptions

**Writing Computational Requirements:**
- Classify every task: figure generation, individual experiments, full reproduction
- For each: estimated time, required hardware, required memory
- Note the platform the code was tested on (OS, language version)
- The agent MUST warn before running anything heavy

**Writing the Citation:**
- Full BibTeX entry

Also create `CLAUDE.md` containing `@AGENTS.md` (Claude Code import syntax).

**Self-check the AGENTS.md before moving on:**
- Verify every file path in the Repository Map exists in the publication repo
- Run every command in the figure generation table
- Confirm computational requirements are accurate
- Read the Paper Summary as if you've never seen this paper — does it convey the key contribution?

Fix any issues found.

### 7. Create README

Write a README.md for the publication repo:

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

### 8. Extract research context (optional)

Ask the researcher if they want to include research context from their Claude Code / Codex conversation history. This captures the reasoning behind the work so the published agent can answer "why did you do X?" from real reasoning.

If yes, follow the `/extract-context` skill. Run it in the **working repo** (that's where the sessions are), then copy the output into the publication repo's `context/` directory.

### 9. Final review with the researcher

Before releasing, the researcher must review and approve:

- Show them the complete publication repo contents
- Show them the AGENTS.md
- Summarize what will be published and what the agent will be able to do
- Ask: "Does this accurately represent your paper? Is there anything to change, add, or remove?"

Do NOT proceed until the researcher explicitly confirms.

### 10. Release

After the researcher approves:
```bash
cd <publication-repo>
git add -A
git commit -m "Initial publication"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```

Ask for confirmation before pushing — this makes it public.

**If `gh` is available and the repo isn't on GitHub yet:**
```bash
gh repo create <repo-name> --public --source . --push
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If the repo is already on GitHub:**
```bash
git push origin main --tags
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If `gh` is not available**, tell the researcher:
- Push manually: `git remote add origin <url> && git push -u origin main --tags`
- Create the release on GitHub's web UI: Releases → Create a new release → tag `v1.0.0`

### Handling different paper types

**Theory-only paper (no code):**
- The publication repo may just be `paper/` and AGENTS.md
- Focus on: explaining the theorems, the proof strategy, the assumptions
- The agent's value is being able to discuss the ideas and connect them to related work

**Computational paper:**
- Full Repository Map, figure table, experiment commands
- Extra care on environment specification — computational papers are the hardest to reproduce
- Document cluster/GPU requirements clearly

**Experimental paper (wet lab, etc.):**
- Code may be analysis scripts, not the experiment itself
- Focus on data analysis reproduction, figure generation
- The agent explains the experimental setup but can't re-run it

**Paper with notebooks:**
- Map notebooks to figures/results: "notebook X produces figure Y"
- Note that notebooks may need to be run in order
- Consider extracting key cells into standalone scripts for easier reproduction
