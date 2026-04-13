---
name: publish-paper
description: Create an AI agent for an academic paper following the Agentic Publication Protocol. Use when a researcher wants to publish their paper repo with an AGENTS.md so any coding agent can represent the work — explain it, reproduce figures, run experiments, answer questions about the methodology.
---

# Publish Paper as Agent

Create a publication repo for a paper — a clean, public repo with an AGENTS.md that turns it into an AI agent. The researcher's working repo may be private and messy; the publication repo is a curated subset meant for public consumption.

Every step involves the researcher. This is a collaborative process — inform them what you're doing, show them what you find, and get their input before moving on.

When asking the researcher to make choices, use structured question tools if the platform supports them (e.g. `AskUserQuestion` in Claude Code). Present clear options with descriptions rather than open-ended text questions. This makes the process faster and less ambiguous.

## Process

### 0. Check for previous versions

First, check the **working repo** for a `.publications.md` file — this is automatically created in step 12 after each release and tracks all publication repos created from this working repo.

**If `.publications.md` exists:**
- Read it to find the previous publication repo URL, version, and date
- Clone or locate that publication repo
- Read its `AGENTS.md`, `README.md`, `supplementary/`, and `skills/` thoroughly
- Most content already exists and just needs updating
- The researcher's interview (step 2) can focus on **what changed** — "What's new or different in this version?"
- Carry forward anything that hasn't changed rather than re-creating it
- In step 7, start from the previous AGENTS.md and modify it, rather than drafting from scratch
- When creating the new version, update the `version` field in AGENTS.md frontmatter and tag a new release (e.g., v2.0.0)

**If `.publications.md` does not exist**, ask the researcher: "Is this the first version, or is there a previous publication repo?"

If a previous version exists, get the repo URL and follow the same process as above.

This saves significant time and avoids losing good content that was already reviewed and approved.

### 1. Understand the paper

Read the working repo thoroughly before asking the researcher anything. Build a mental model:

**Paper source:**
- Find the main document: look for `*.tex`, `*.md`, `*.docx`, `*.pdf`, `*.html`, `*.pptx`, video files
- The paper can be in any format — LaTeX, DOCX, Markdown, HTML, video, PPTX, PDF
- If multiple candidates exist, note them all — you'll ask the researcher which is canonical in step 2
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

**Supplementary materials:**
- Are there slides, talks, posters, or tutorials in the repo?
- Are there conversation logs or research notes?

**Build the script→figure mapping:**
For each figure in the paper:
1. Find the figure reference in the paper source (`\includegraphics`, figure filenames)
2. Find the script that generates it (look for `savefig`, `plt.save`, output paths)
3. Identify what data the script reads

**What's missing:**
- Is there anything you can't figure out from reading the repo? Note questions for step 2.

**Tell the researcher** what you found — present your understanding of the repo structure, the paper, and the code. Show them the script→figure mapping. This demonstrates you've done the homework and gives them a chance to correct misunderstandings early.

### 2. Discuss with the researcher

Ask about gaps and intent (one or two questions at a time, not all at once):

**About the paper:**
- If multiple paper-like documents exist, ask which is the canonical paper (the ground truth). The paper format is flexible — LaTeX, DOCX, Markdown, HTML, video, PPTX are all valid.
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
- Which files should go into the publication repo? Which should stay private? Present the file list with a structured choice for each: include / exclude / ask me later.
- What would a reader most likely want to do? Offer options: reproduce figures, extend the work, understand the math/theory, run with different inputs.
- What should the publication repo be called?

**About key information for readers** (2-3 questions max):
- "What do you wish someone had told you before reading this paper?"
- "What's not in the paper but matters for understanding or using the work?"
- The answers become `supplementary/authors-note.md`.

**About supplementary materials:**
- "Do you have slides, talks, posters, or tutorials for this work?"
- "Do you have the copyright/permission to share them publicly?"
- Clarify: these are secondary to the paper — useful context for readers, not ground truth. They'll go in `supplementary/materials/`.

**About skills:**
- "Are there specific workflows or analyses you'd like readers to be able to run through the agent? For example: a guided analysis pipeline, a visualization tool, a parameter sweep."
- If yes, help the author define each skill (name, description, step-by-step instructions). You'll create `skills/<name>/SKILL.md` files in step 5.
- If no, skip — skills are optional.

### 3. Extract research context (optional)

Ask the researcher if they want to include research context from their conversation history. Offer a structured choice:
- **Yes — extract from sessions** (recommended): captures reasoning, decisions, dead ends from Claude Code / Codex history. By default all project sessions are included and a thematic summary is produced. The researcher can optionally publish more detailed session transcripts too.
- **Yes — I'll write notes manually**: the researcher provides context themselves
- **No — skip this**: no research context in the publication

This context is valuable for writing the AGENTS.md later (steps 7-8), because the agent can answer "why did you do X?" from real reasoning rather than guessing.

If extracting from sessions, follow the `/extract-context` skill. Run it in the **working repo** (that's where the sessions are). The output will be copied into the publication repo later. The extract-context process includes a mandatory confidentiality screening step — but you should also check for sensitive content during steps 7-8 when incorporating context into the AGENTS.md.

### 4. Create the publication repo

Ask the researcher how they want to create the publication repo. Offer a structured choice:
- **Create on GitHub now** (requires `gh` CLI)
- **Create locally first** (push to GitHub later)

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

The researcher can push to GitHub later in step 11.

### 5. Copy and organize selected files

Show the researcher the list of files you're about to copy and the target structure. Confirm before copying.

Create the target directories first, then copy:

```bash
# Example — adapt to what's actually being published
mkdir -p paper/figures paper/build code/src code/scripts data environment supplementary
cp ../working-repo/paper/main.tex paper/
cp ../working-repo/paper/*.bib paper/
cp ../working-repo/figures/*.pdf paper/figures/
cp -r ../working-repo/src/ code/src/
cp ../working-repo/scripts/generate_*.py code/scripts/
cp ../working-repo/data/results.csv data/
cp ../working-repo/requirements.txt environment/
```

Use the file list from step 2 — copy only what the researcher approved. Organize into a clean structure:

```
paper/
├── main.tex (or .docx, .md, .html, .pptx)  ← paper source (GROUND TRUTH)
├── *.bib
├── figures/          ← generated figures (final versions)
└── build/            ← compiled PDF (if applicable)

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

supplementary/
├── know-how.md       ← tacit knowledge, methodology decisions (from extract-context or manual)
├── authors-note.md   ← what the authors want readers to know beyond the paper
├── checklist.md      ← publication checklist (from template)
├── sessions/         ← (optional) conversation history from the research process
└── materials/        ← (optional) slides, talks, posters, tutorials

skills/               ← (optional) author-published agent capabilities
└── skill-name/
    └── SKILL.md
```

Adapt the structure to what's actually being published — don't force directories that have nothing in them. A theory paper might just have `paper/` and a few scripts.

**Single source of truth:** Each file lives in exactly one place. No duplicates, no ambiguity about which version is current.

**Update all internal references** — imports, file paths in scripts, `\includegraphics` paths in LaTeX, data paths in notebooks. These will differ from the working repo's paths.

**Handle large files:**
- Files >50MB: suggest Git LFS or external hosting (Hugging Face, Zenodo)
- Generated files that can be reproduced: add to `.gitignore`, document the generation command

**Verify external data links:**
For every external data URL identified in step 1 (Hugging Face, Zenodo, Figshare, etc.):
- Test accessibility: `curl -sIL <url>` (follow redirects) or platform-specific commands (`huggingface-cli download --dry-run`, etc.)
- Show results to the researcher: "Link X returned 200 OK" or "Link Y returned 404 — is this still the right URL?"
- Ask the researcher to confirm each link works (some may require authentication the agent doesn't have)
- Record verified/flagged status in `supplementary/checklist.md`

**Create a .gitignore** tailored to what's in the repo — cover build artifacts, generated files, sensitive files, and OS files.

**Copy supplementary materials:**
- If research context was extracted in step 3, copy it into `supplementary/` now
- Generate `supplementary/authors-note.md` from the step 2 interview answers
- Copy any supplementary materials (slides, talks, posters) the researcher approved into `supplementary/materials/`
- Copy `template/publication-checklist.md` to `supplementary/checklist.md` and adapt it by removing sections that don't apply to this publication

**Create skills:**
- If the researcher defined skills in step 2, create `skills/<name>/SKILL.md` for each one with name and description in frontmatter and step-by-step instructions in the body

Tell the researcher what was copied and how it's organized. Flag anything that needed special handling (large files, updated paths, broken data links).

**Validation checkpoint:** Launch a validation agent following `/validate-publication --stage structure` to check file paths, sensitive files, and data links. Fix any errors (search for `REVIEW: error` in files — markers may be `<!-- REVIEW:` in Markdown or `# REVIEW:` in code). Show warnings to the researcher.

### 6. Verify the code works

Tell the researcher you're testing that everything works in the publication repo.

Actually run things to confirm they work with the new paths:

- **Paper compilation**: Run the build command and check it succeeds (if applicable — not all paper formats compile)
- **Figure generation**: Run each figure script and verify it produces output
- **Tests**: If the repo has tests, run them
- **Notebooks**: Execute in order and check for errors
- **Imports**: Verify import paths resolve with the new structure

Fix anything that broke from the copy/reorganization. Report results to the researcher — what passed, what needed fixing, what you changed.

### 7. Create AGENTS.md

Tell the researcher you're drafting the AGENTS.md now, drawing on everything from steps 1-3.

Generate `AGENTS.md` at the publication repo root. This is the most important file — it must give an agent everything it needs to operate in this repo.

**Writing the identity section:**
- The agent is a spokesperson for THIS work, not a generic assistant
- It should adopt the domain's reasoning style (mathematician for math, experimentalist for physics, etc.)
- It must distinguish between the paper's claims and its own inferences
- It should know the paper's limitations and say so honestly
- **The paper is the ground truth** — state this explicitly. Supplementary materials provide context but are secondary. If anything conflicts with the paper, the paper takes precedence.

**Writing the frontmatter:**
- Include all standard fields (protocol, title, authors, arxiv_id, version, domain, tags)
- Set `paper_format` to the correct format (latex, docx, markdown, html, video, pptx, pdf)

**Writing the Paper Summary:**
- Use the researcher's own words from step 2
- If research context was extracted in step 3, draw on it — the reasoning and motivation behind decisions
- 2-4 paragraphs covering: what problem, what approach, what results, what implications
- This is what the agent will rely on most — make it substantive

**Writing the Repository Map:**
- Don't just list files — explain what each one does and how they connect
- Mark the paper source as `(GROUND TRUTH)`
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

**Writing the Supplementary Materials section:**
- Point to `supplementary/know-how.md` for methodology insights and tacit knowledge
- Point to `supplementary/authors-note.md` for the authors' message to readers
- If sessions were published, point to `supplementary/sessions/`
- If materials (slides, talks, etc.) were included, point to `supplementary/materials/` and note these are secondary to the paper
- Keep this section brief — it's pointers, not content

**Writing the Skills section:**
- If the author published skills, list each one with its name, location, and a one-line description
- If no skills, omit this section

**Writing Computational Requirements:**
- Classify every task: figure generation, individual experiments, full reproduction
- For each: estimated time, required hardware, required memory
- Note the platform the code was tested on (OS, language version)
- The agent MUST warn before running anything heavy

**Writing the Citation:**
- Full BibTeX entry

Also create `CLAUDE.md` containing `@AGENTS.md` (Claude Code import syntax).

**Self-check before showing to the researcher:**
- Verify every file path in the Repository Map exists in the publication repo
- Run every command in the figure generation table
- Confirm computational requirements are accurate

Fix any mechanical issues found.

**Validation checkpoint:** Launch a validation agent following `/validate-publication --stage agents-md` to check factuality against the paper, path validity, privacy, and substance. Fix any errors. Show warnings to the researcher before the iteration step — they can address both the validation findings and their own feedback together.

### 8. Iterate on the AGENTS.md with the researcher

Show the researcher the draft AGENTS.md and discuss it with them. This is not a rubber-stamp review — it's a conversation about what the agent should convey.

**Focus on substance, not formatting:**
- **Paper Summary**: Does it capture what makes this work distinctive? Push back on generic language — "we propose a novel method" says nothing. What specifically is the insight? What would the authors say at a whiteboard that they wouldn't write in the abstract?
- **Key Results**: Are these the results the authors are most proud of, or just the ones that are easiest to describe? Ask: "If someone remembers one thing from this paper, what should it be?"
- **What You Can Do / Extend the work**: What questions do the authors wish people would ask? What variations would be interesting? This is where the agent becomes more than a paper reader — it becomes a collaborator.

**Ask directly:**
- "What do you want people to take away from this work?"
- "What's the thing that's hard to get from just reading the paper?"
- "Is there anything the agent should say that isn't in the paper itself — context, motivation, what you tried that didn't work?"

Revise the AGENTS.md based on their feedback. Go back and forth until the researcher is satisfied that the agent represents their intent, not just their words.

### 9. Create README

Show the researcher the README draft. The publication README is for readers who want to use the paper agent — not a copy of the working repo's README.

```markdown
# [Paper Title]

[Authors, affiliations]

[1-2 sentence summary of the paper]

[Link to arXiv / DOI / PDF if available]

## Talk to this paper

This paper is published with an AI agent ([Agentic Publication Protocol](https://github.com/LionSR/AgenticPublicationProtocol)). Clone this repo and open it in an AI coding agent to ask questions, reproduce figures, and explore the work.

**Claude Code:**
Clone and open in Claude Code — it reads AGENTS.md automatically. Or use the load skill:
> /load-paper-agent https://github.com/<owner>/<repo>

**Codex / other agents:**
Clone and open — any agent that reads AGENTS.md or README will pick up the paper context.

## Figures

| Figure in paper | Script | Data | Output |
|-----------------|--------|------|--------|
| Fig 1 (description) | `code/scripts/fig1.py` | `data/results.csv` | `paper/figures/fig1.pdf` |
| Fig 2 (description) | `code/scripts/fig2.py` | `data/sim_output.h5` | `paper/figures/fig2.pdf` |

## Reproducing results

### Setup
[how to install dependencies — platform-agnostic]

### Run figures
[commands]

### Full experiment
[how to run from scratch, if applicable]

## Citation

\`\`\`bibtex
[bibtex entry]
\`\`\`
```

Get the researcher's feedback on the README before finalizing.

**Validation checkpoint:** Launch a validation agent following `/validate-publication --stage readme` to check consistency between README and AGENTS.md, links, and privacy. Fix any errors. Show warnings to the researcher.

### 10. Final review

Show the researcher the complete publication repo — all files, the AGENTS.md, the README, the supplementary materials (if any), the skills (if any). Summarize:

- What's included and what was left out
- What the agent will be able to do
- What goes public when they release

**Validation checkpoint:** Launch a validation agent following `/validate-publication --stage full` for a comprehensive sweep — factuality, privacy, paths, consistency, and substance across all files. Fix any errors. Show warnings and notes to the researcher.

**Walk through the checklist** (`supplementary/checklist.md`) as a quality gate. Go through each item with the researcher and mark them off. Flag any unchecked items that need attention before release.

Ask: "Does this accurately represent your paper? Is there anything to change, add, or remove?"

Do NOT proceed until the researcher explicitly confirms.

### 11. Release

**Before doing anything in this step**, present the researcher with a concrete summary of exactly what is about to happen. This is the point of no return — once pushed, the repo is public. The confirmation must be specific, not a generic "should I proceed?"

Present this to the researcher (fill in the actual values):

```
PUBLICATION SUMMARY — please review before I publish:

  Repo name:    <repo-name>
  Visibility:   PUBLIC — anyone on the internet can see this
  Version:      v1.0.0
  Tag:          v1.0.0

  Files included (<N> files):
    paper/          — <paper source format>, figures, bibliography
    code/           — <brief description>
    data/           — <brief description>
    environment/    — <dependencies file>
    supplementary/  — <list which files: know-how, authors-note, sessions, etc.>
    skills/         — <list skill names, or "none">
    AGENTS.md       — paper agent instructions
    README.md       — public README

  Files NOT included (stayed in working repo):
    <list key excluded files/directories, or "nothing excluded">

  External data links:
    <list any URLs that will be referenced, or "none">

  Checklist status:
    <N>/<M> items checked — <list any unchecked items>

  What happens next:
    1. Commit all files to the publication repo
    2. Tag as v1.0.0
    3. Push to GitHub as a PUBLIC repository
    4. Create a GitHub release (v1.0.0)
    5. Record this release in your working repo (.publications.md)
```

**Wait for the researcher to explicitly confirm.** A clear "yes", "go ahead", "publish it", or equivalent. Do NOT proceed on ambiguous responses like "looks good" or "ok" — ask: "Just to be clear — shall I push this as a public repo now?"

Do NOT proceed until you have unambiguous confirmation.

After confirmation:

```bash
cd <publication-repo>
git add -A
git commit -m "Initial publication"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```

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

Tell the researcher the publication is live and share the repo URL.

### 12. Record the release in the working repo

After the publication is live, switch back to the **working repo** and record the release in `.publications.md`. This ensures that future sessions know a publication repo exists — no need to ask the researcher or guess.

**If `.publications.md` doesn't exist yet**, create it:
```markdown
# Publications

Repos created from this working repo via the Agentic Publication Protocol.

| Repo | Version | Date | Notes |
|------|---------|------|-------|
| [<repo-name>](<repo-url>) | v1.0.0 | YYYY-MM-DD | Initial publication |
```

**If `.publications.md` already exists**, append a new row to the table:
```markdown
| [<repo-name>](<repo-url>) | v2.0.0 | YYYY-MM-DD | Updated results, new figures |
```

Commit `.publications.md` in the working repo:
```bash
cd <working-repo>
git add .publications.md
git commit -m "Record publication: <repo-name> v1.0.0"
```

This file is the link between the working repo and its publication repos. Step 0 reads it to detect previous versions automatically.

### Handling different paper types

The paper can be in any format — LaTeX, DOCX, Markdown, HTML, video, PPTX, PDF. Adapt the process accordingly.

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

**Video / slideware paper:**
- The video or PPTX is the ground truth document
- The agent should be able to discuss its contents and reference specific sections/timestamps
- Supplementary materials may include a text summary or transcript
