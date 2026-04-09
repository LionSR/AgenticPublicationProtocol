---
name: publish-paper
description: Create an AI agent for an academic paper following the Agentic Publication Protocol. Use when a researcher wants to publish their paper repo with an AGENTS.md so any coding agent can represent the work — explain it, reproduce figures, run experiments, answer questions about the methodology.
---

# Publish Paper as Agent

This skill creates an AGENTS.md file that turns a paper repo into an AI agent. Think of it as onboarding a coding agent to represent a specific paper — the agent reading that AGENTS.md has never seen the repo before and needs everything spelled out.

## Process

### 1. Understand the paper

Read the repo thoroughly before asking the researcher anything. Build a mental model of what's here:

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

**What's missing:**
- Is there anything you can't figure out from reading the repo? Note questions for step 2.

### 2. Discuss with the researcher

Present your understanding of the repo first — show them you've done the homework. Then ask about gaps (one or two questions at a time, not all at once):

**About the paper:**
- What are the key results? (Ask them to state it in their own words — this becomes the Paper Summary)
- What's the main contribution vs. existing work?
- What domain should the agent reason in? (math? physics? ML? biology?)

**About the code:**
- Which scripts generate which figures? (Map every figure to a command)
- What's the main experiment and how do you run it?
- What parameters can a reader change to explore variations?
- What parts of the code are fragile / require specific setup?
- Are there any scripts that take a long time? How long, on what hardware?

**About publishing:**
- Which code/data should be public vs private?
- Is there anything in the conversation history they want to include as research context?
- What would a reader most likely want to do? (reproduce figures? extend? understand the math? run with different inputs?)

### 3. Create AGENTS.md

Generate `AGENTS.md` at repo root. Use the template at `template/AGENTS.md` as a starting point. This is the most important file — it must give the agent everything it needs to operate.

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
- Include file paths relative to repo root
- Note which files are entry points vs. supporting
- For external data (Hugging Face, Zenodo, Figshare, etc.), document:
  - What the dataset is and its size
  - The URL
  - The exact download command (e.g. `huggingface-cli download ...`, `wget ...`, `zenodo_get ...`)
  - Where to put it locally (e.g. `data/`)
  - Whether it's required for basic usage (figures) or only for full reproduction

**Writing "What You Can Do":**
- **Explain the paper**: which files to read for which sections, how the paper is structured
- **Reproduce figures**: a table mapping EVERY figure to its command, data source, and runtime. Include the exact install command for dependencies.
- **Run experiments**: exact commands with real parameters, not placeholders. What config files exist and what do the key parameters mean?
- **Extend the work**: what can a reader change? Which parameters are interesting to vary? What would the agent suggest trying?
- For each capability, include the actual commands, not just descriptions

**Writing Computational Requirements:**
- Classify every task: figure generation, individual experiments, full reproduction
- For each: estimated time, required hardware, required memory
- Note the platform the code was tested on (OS, language version)
- The agent MUST warn before running anything heavy

**Writing the Citation:**
- Full BibTeX entry

Also create `CLAUDE.md` containing `@AGENTS.md` (Claude Code import syntax).

### 4. Extract research context (optional)

Ask the researcher if they want to include research context from their conversation history. This captures the reasoning behind the work — key decisions, methodology choices, debugging insights — so the published agent can answer "why did you do X?" from real reasoning.

Offer three levels:

- **Gist** — Distill a `context/research-notes.md` summarizing key decisions, what was tried, what worked, what didn't.
- **Cleaned history** — Export conversation sessions into structured markdown, cleaned up for readability.
- **Full history** — Raw conversation dumps, minimally processed.

The researcher can also decline entirely — context is optional.

**How to extract and clean up:**

1. Find relevant sessions using the extraction script:

```bash
# List all Claude Code sessions for this project
python skills/publish-paper/scripts/extract_sessions.py list --source claude

# List all Codex sessions
python skills/publish-paper/scripts/extract_sessions.py list --source codex

# Extract a specific session to JSON
python skills/publish-paper/scripts/extract_sessions.py extract --source claude --session <id>
```

Show the session list to the researcher. Let them pick which sessions are related to the paper. Extract each selected session to JSON, then convert to structured markdown:
2. For each session, produce a structured markdown file in `context/sessions/`:

```markdown
# Session: [descriptive title]

Date: YYYY-MM-DD
Topic: [what this session was about]

## Key decisions
- [Decision 1 — what was decided and why]
- [Decision 2]

## Conversation

**Researcher:** [cleaned-up message — fix typos, remove tangents, keep substance]

**Agent:** [summarized response — keep the key information, trim verbose output]

**Researcher:** [next message]

...
```

3. Guide the researcher through each session:
   - Show them the raw conversation
   - Help them decide: keep, summarize, or skip
   - Remove private content (API keys, personal info, unrelated tangents)
   - Clean up messages for readability while preserving the reasoning
   - Add a "Key decisions" header at the top of each session summarizing what came out of it

4. For **gist** level: after cleaning sessions, further distill everything into a single `context/research-notes.md`:

```markdown
# Research Notes

## Methodology decisions
- [Why we chose approach X over Y]
- [What didn't work and why]

## Key insights during development
- [Insight 1 — from session Z]
- [Insight 2]

## Known limitations and future ideas
- [Limitation the researcher is aware of]
- [Idea that didn't make it into the paper]
```

5. Add to AGENTS.md: `For deeper context on the research process, see context/`

### 5. Organize (if needed)

If the repo is messy, propose reorganizing. Only with researcher approval. Common structure:
- `paper/` — source + compiled PDF + figures
- `code/` — scripts, src, configs
- `data/` — datasets
- `environment/` — requirements.txt, platform info
- `context/` — research notes and session logs

### 6. Verify the agent works

Before releasing, test the AGENTS.md by role-playing as a reader:
- Read the AGENTS.md as if you've never seen this repo
- Can you find every file mentioned in the Repository Map?
- Can you run every command in the figure generation table?
- Are the computational requirements accurate?
- Does the Paper Summary actually convey the key contribution?
- Would a reader know what to do first?

Fix any issues found.

### 7. Create a GitHub Release

Once the researcher approves everything:
```bash
git add AGENTS.md CLAUDE.md context/
git commit -m "Add paper agent"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```
**Ask for confirmation** before pushing and creating the release:
```bash
git push origin main --tags
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

### Handling different paper types

**Theory-only paper (no code):**
- Skip Repository Map code entries, figure generation, experiments
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
