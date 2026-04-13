---
name: publish-paper
description: Orchestrate the publication of an academic paper as an AI agent following the Agentic Publication Protocol. This is the main skill — it calls /extract-context and /validate-publication as sub-skills at the appropriate stages.
---

# Publish Paper as Agent

This is the **orchestrator skill**. It guides the full publication process and calls sub-skills:
- `/extract-context` — to extract research context from conversation history (phase 2)
- `/validate-publication` — to run automated quality checks (phases 3, 4, and 5)

## Roadmap

At the very start, show the researcher this roadmap so they know what's ahead:

```
PUBLICATION ROADMAP

  Phase 1 — Understand        [ ]  Read the repo, check for previous versions
  Phase 2 — Discuss           [ ]  Interview (5 short rounds), extract context
  Phase 3 — Build             [ ]  Create repo, organize files, verify code
  Phase 4 — Draft             [ ]  AGENTS.md, iterate with you, README
  Phase 5 — Final review      [ ]  Walk through everything, validation sweep
  Phase 6 — Release           [ ]  Publish (with your explicit confirmation)

  This is a deliberate process — it can span multiple sessions.
  I'll update this checklist as we go.
```

## Progress tracking

After completing each phase, **re-display the roadmap** with updated status so the researcher always knows where they are. Mark completed phases with `[x]` and show the current phase:

```
  Phase 1 — Understand        [x]  Done
  Phase 2 — Discuss           [x]  Done
  Phase 3 — Build             [>]  In progress — organizing files
  Phase 4 — Draft             [ ]  Next
  Phase 5 — Final review      [ ]  
  Phase 6 — Release           [ ]  
```

If resuming a previous session, reconstruct the progress state from what already exists (e.g., if AGENTS.md and README already exist, phases 1-4 are done).

## Guiding principles

Publishing a paper is a significant responsibility. This process should be deliberate, not rushed. It is fine — and expected — for this to span multiple sessions.

**Pace principle:** Never treat a partial answer as a complete one. If you asked three questions and the researcher answered one, follow up on the unanswered ones before moving on — they may have missed them, not declined them. When showing the researcher something for feedback (a draft, a file list, a checklist), wait for them to engage with it substantively. A one-word acknowledgement ("ok", "sure", "fine") after presenting five things to review is not confirmation — ask which specific items they've looked at. The researcher's attention is finite; work with that, not against it.

**Author's voice principle:** The supplementary materials (`authors-note.md`, `know-how.md`), the AGENTS.md paper summary, and any content that speaks for the researcher must reflect what *they* want to convey — not what the agent thinks is important. Before drafting any of these, ask the researcher what they want the document to say and who the intended audience is. Draft from their intent, then iterate. Never generate these documents first and ask for approval after — that inverts the authorship.

When asking the researcher to make choices, use structured question tools if the platform supports them (e.g. `AskUserQuestion` in Claude Code). Present clear options with descriptions rather than open-ended text questions. This makes the process faster and less ambiguous.

---

## Phase 1 — Understand

### 1.1 Check for previous versions

First, check the **working repo** for a `.publications.md` file — this is automatically created in phase 6 after each release and tracks all publication repos created from this working repo.

**If `.publications.md` exists:**
- Read it to find the previous publication repo URL, version, and date
- Clone or locate that publication repo
- Read its `AGENTS.md`, `README.md`, `supplementary/`, and `skills/` thoroughly
- Most content already exists and just needs updating
- The researcher's interview (phase 2) can focus on **what changed** — "What's new or different in this version?"
- Carry forward anything that hasn't changed rather than re-creating it
- In phase 4, start from the previous AGENTS.md and modify it, rather than drafting from scratch
- When creating the new version, update the `version` field in AGENTS.md frontmatter and tag a new release (e.g., v2.0.0)

**If `.publications.md` does not exist**, ask the researcher: "Is this the first version, or is there a previous publication repo?"

If a previous version exists, get the repo URL and follow the same process as above.

This saves significant time and avoids losing good content that was already reviewed and approved.

### 1.2 Understand the paper

Read the working repo thoroughly before asking the researcher anything. Build a mental model:

**Paper source:**
- Find the main document: look for `*.tex`, `*.md`, `*.docx`, `*.pdf`, `*.html`, `*.pptx`, video files
- The paper can be in any format — LaTeX, DOCX, Markdown, HTML, video, PPTX, PDF
- If multiple candidates exist, note them all — you'll ask the researcher which is canonical in phase 2
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
- Is there anything you can't figure out from reading the repo? Note questions for phase 2.

**Tell the researcher** what you found — present your understanding of the repo structure, the paper, and the code. Show them the script→figure mapping. This demonstrates you've done the homework and gives them a chance to correct misunderstandings early.

## Phase 2 — Discuss

### 2.1 Interview the researcher

Ask **1-3 questions per round**, wait for answers, then move to the next round. Do not dump all questions at once — researchers have limited attention and will miss things in a wall of text. Lead with what you can't figure out from reading the repo yourself; skip questions you already know the answer to.

**Within each round:** If the researcher answers some questions but not others, follow up on the unanswered ones specifically. Do not move to the next round until the current one is resolved — either answered or explicitly deferred by the researcher.

**Round 1 — The paper** (start here, it's the foundation):
- If multiple paper-like documents exist: "Which of these is the canonical paper?" (show the candidates you found)
- "In your own words, what are the key results and the main contribution?"

**Round 2 — The code** (only what you couldn't determine from phase 1):
- Show the script→figure mapping you built and ask the researcher to confirm or correct it
- "What's the main experiment and how do you run it?"
- If anything looked fragile or slow, ask about that specifically

**Round 3 — What to publish:**
- Present the file list with a structured choice for each: include / exclude / ask me later
- "What should the publication repo be called?"

**Round 4 — The reader's perspective:**
- "What do you wish someone had told you before reading this paper?"
- "What would a reader most likely want to do?" Offer options: reproduce figures, extend the work, understand the math/theory, run with different inputs

**Round 5 — Supplementary materials and skills** (optional — skip if researcher is low on time):
- "Do you have slides, talks, posters, or tutorials? Do you have permission to share them?"
- "Are there specific workflows you'd like readers to be able to run through the agent?"

**After all rounds — check for gaps.** Review what was answered. If any of these crucial items are still missing, ask again explicitly:
- Which document is the ground truth paper
- What the key results are
- Which files to include / exclude
- The repo name

These four are required to proceed. Everything else can be filled in later or inferred.

### 2.2 Extract research context (optional) — `/extract-context`

Ask the researcher if they want to include research context from their conversation history. Offer a structured choice:
- **Yes — extract from sessions** (recommended): captures reasoning, decisions, dead ends from Claude Code / Codex history. By default all project sessions are included and a thematic summary is produced. The researcher can optionally publish more detailed session transcripts too.
- **Yes — I'll write notes manually**: the researcher provides context themselves
- **No — skip this**: no research context in the publication

This context is valuable for writing the AGENTS.md in phase 4, because the agent can answer "why did you do X?" from real reasoning rather than guessing.

If extracting from sessions, run the `/extract-context` sub-skill in the **working repo** (that's where the sessions are). The output will be copied into the publication repo later. The extract-context process includes a mandatory confidentiality screening step — but you should also check for sensitive content in phase 4 when incorporating context into the AGENTS.md.

## Phase 3 — Build

### 3.1 Create the publication repo

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

The researcher can push to GitHub later in phase 6.

### 3.2 Copy and organize selected files

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

Use the file list from phase 2 — copy only what the researcher approved. Organize into the directory structure defined in [PROTOCOL.md](../../PROTOCOL.md#publication-repo-structure). Not every directory is required — adapt to what's actually being published. A theory paper might just have `paper/` and a few scripts.

**Single source of truth:** Each file lives in exactly one place. No duplicates, no ambiguity about which version is current.

**Update all internal references** — imports, file paths in scripts, `\includegraphics` paths in LaTeX, data paths in notebooks. These will differ from the working repo's paths.

**Handle large files:**
- Files >50MB: suggest Git LFS or external hosting (Hugging Face, Zenodo)
- Generated files that can be reproduced: add to `.gitignore`, document the generation command

**Verify external data links:**
For every external data URL identified in phase 1 (Hugging Face, Zenodo, Figshare, etc.):
- Test accessibility: `curl -sIL <url>` (follow redirects) or platform-specific commands (`huggingface-cli download --dry-run`, etc.)
- Show results to the researcher: "Link X returned 200 OK" or "Link Y returned 404 — is this still the right URL?"
- Ask the researcher to confirm each link works (some may require authentication the agent doesn't have)
- Record verified/flagged status in `supplementary/checklist.md`

**Create a .gitignore** tailored to what's in the repo — cover build artifacts, generated files, sensitive files, and OS files.

**Copy supplementary materials:**
- If research context was extracted in phase 2, copy it into `supplementary/` now
- For `supplementary/authors-note.md`: ask the researcher what message they want to leave for readers — what should someone know that isn't in the paper? Draft from their answer and the phase 2 interview, then show them the draft for revision. This is their voice, not the agent's.
- Copy any supplementary materials (slides, talks, posters) the researcher approved into `supplementary/materials/`
- Copy `template/publication-checklist.md` to `supplementary/checklist.md` and adapt it by removing sections that don't apply to this publication

**Create skills:**
- If the researcher defined skills in phase 2, create `skills/<name>/SKILL.md` for each one with name and description in frontmatter and step-by-step instructions in the body

Tell the researcher what was copied and how it's organized. Flag anything that needed special handling (large files, updated paths, broken data links).

**Sub-skill: `/validate-publication --stage structure`** — checks file paths, folder structure, sensitive files, and data links. Fix any errors (search for `REVIEW: error` in files — markers may be `<!-- REVIEW:` in Markdown or `# REVIEW:` in code). Show warnings to the researcher.

### 3.3 Verify the code works

Tell the researcher you're testing that everything works in the publication repo.

Actually run things to confirm they work with the new paths:

- **Paper compilation**: Run the build command and check it succeeds (if applicable — not all paper formats compile)
- **Figure generation**: Run each figure script and verify it produces output
- **Tests**: If the repo has tests, run them
- **Notebooks**: Execute in order and check for errors
- **Imports**: Verify import paths resolve with the new structure

Fix anything that broke from the copy/reorganization. Report results to the researcher — what passed, what needed fixing, what you changed.

## Phase 4 — Draft

### 4.1 Create AGENTS.md

Tell the researcher you're drafting the AGENTS.md now, drawing on everything from phases 1-2.

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
- Before drafting, ask the researcher: "What's the core message you want someone to take away from this paper?" Their answer sets the direction — don't draft from your own reading first.
- Use the researcher's own words from phase 2 and this answer as the foundation
- If research context was extracted in phase 2, draw on it — the reasoning and motivation behind decisions
- 2-4 paragraphs covering: what problem, what approach, what results, what implications
- This is what the agent will rely on most — make it substantive

**Writing the Repository Structure:**
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
- Verify every file path in the Repository Structure exists in the publication repo
- Run every command in the figure generation table
- Confirm computational requirements are accurate

Fix any mechanical issues found.

**Sub-skill: `/validate-publication --stage agents-md`** — checks factuality against the paper, path validity, privacy, and substance. Fix any errors. Show warnings to the researcher before the iteration step — they can address both the validation findings and their own feedback together.

### 4.2 Iterate on the AGENTS.md with the researcher

Show the researcher the draft AGENTS.md and discuss it with them. This is not a rubber-stamp review — it's a conversation about what the agent should convey.

Walk through the AGENTS.md **one section at a time** rather than asking the researcher to review the entire document at once. For each section, ask a focused question:

- **Paper Summary**: "Does this capture what makes your work distinctive? What would you change?"
- **Key Results**: "Are these the results you're most proud of, or just the easiest to describe? If someone remembers one thing from this paper, what should it be?"
- **What You Can Do / Extend the work**: "What questions do you wish people would ask about this work? What variations would be interesting?"

If the researcher says "looks good" without engaging with specifics, gently probe one concrete aspect — e.g., "I want to make sure the summary captures your intent. The first paragraph says [X] — does that match how you'd describe it?"

After walking through sections, ask:
- "Is there anything the agent should say that isn't in the paper itself — context, motivation, what you tried that didn't work?"

Revise the AGENTS.md based on their feedback. Go back and forth until the researcher is satisfied that the agent represents their intent, not just their words.

### 4.3 Create README

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

**Sub-skill: `/validate-publication --stage readme`** — checks consistency between README and AGENTS.md, links, and privacy. Fix any errors. Show warnings to the researcher.

## Phase 5 — Final review

**Sub-skill: `/validate-publication --stage full`** — comprehensive sweep: factuality, privacy, paths, consistency, and substance across all files. Fix any errors before showing results to the researcher.

Present the final state to the researcher **one piece at a time**, not as a single wall of information:

1. **File inventory**: Show what's included and what was excluded. Ask: "Is this the right set of files? Anything missing or anything that shouldn't be here?"
2. **AGENTS.md**: Show the final version. Ask: "Does this still accurately represent your paper after all the changes we made?"
3. **README**: Show the final version. Ask: "Is this what you want readers to see first?"
4. **Supplementary materials**: List what's in `supplementary/`. Ask: "Are you comfortable with all of this being public?"
5. **Validation results**: Show any remaining warnings or notes from the validation sweep. Walk through each one — don't just list them.

Wait for the researcher to engage with each item. If they say "all good" without engaging, ask about one specific thing — e.g., "I want to double-check: the supplementary materials include [X]. Are you sure that should be public?"

**Walk through the checklist** (`supplementary/checklist.md`) as a final quality gate. Go through each item with the researcher and mark them off. Flag any unchecked items.

Do NOT proceed until the researcher has explicitly confirmed they've reviewed the files, the AGENTS.md, and the supplementary materials.

## Phase 6 — Release

### 6.1 Confirm and publish

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

After confirmation, commit and tag locally — this does not push anything yet:

```bash
cd <publication-repo>
git add -A
git commit -m "Initial publication"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```

Tell the researcher: "Everything is committed and tagged locally. Nothing has been pushed yet."

**Separate confirmation before each remote action.** Each push or remote operation requires its own explicit confirmation — do not chain them.

**If `gh` is available and the repo isn't on GitHub yet:**

Ask: "Ready to create the public GitHub repo and push? This makes everything visible."
```bash
gh repo create <repo-name> --public --source . --push
```

Then ask: "Repo is live. Shall I also create a GitHub release tagged v1.0.0?"
```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If the repo is already on GitHub:**

Ask: "Ready to push to GitHub? This makes everything visible."
```bash
git push origin main --tags
```

Then ask: "Push complete. Shall I also create a GitHub release tagged v1.0.0?"
```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If `gh` is not available**, tell the researcher what to run manually:
- Push: `git remote add origin <url> && git push -u origin main --tags`
- Create the release on GitHub's web UI: Releases → Create a new release → tag `v1.0.0`

Tell the researcher the publication is live and share the repo URL.

### 6.2 Record the release in the working repo

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

---

## Handling different paper types

The paper can be in any format — LaTeX, DOCX, Markdown, HTML, video, PPTX, PDF. Adapt the process accordingly.

**Theory-only paper (no code):**
- The publication repo may just be `paper/` and AGENTS.md
- Focus on: explaining the theorems, the proof strategy, the assumptions
- The agent's value is being able to discuss the ideas and connect them to related work

**Computational paper:**
- Full Repository Structure, figure table, experiment commands
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
