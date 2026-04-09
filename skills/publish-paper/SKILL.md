---
name: publish-paper
description: Create an AI agent for an academic paper following the Agentic Publication Protocol. Use when a researcher wants to publish their paper repo with an AGENTS.md so any coding agent can represent the work — explain it, reproduce figures, run experiments.
---

# Publish Paper as Agent

This skill creates an AGENTS.md file that turns a paper repo into an AI agent. Think of it as onboarding a coding agent to represent a specific paper.

## Process

### 1. Understand the paper

Read the repo. Identify:
- Paper source (LaTeX, Markdown, PDF)
- Code — what language, what it does, how to run it
- Data — what's included, how large
- Figures — which can be regenerated from code
- Dependencies — what's needed to run things
- Compute — what's light (any laptop) vs heavy (GPU/cluster)

### 2. Discuss with the researcher

Ask (one or two questions at a time, not all at once):
- What is this paper about? What are the key results?
- Which code/data should be public vs private?
- What computational resources are needed?
- What would a reader most likely want to do with this? (reproduce figures? extend the work? understand the method?)

### 3. Create AGENTS.md

Generate `AGENTS.md` at repo root. Use the template at `template/AGENTS.md` as a starting point. The AGENTS.md must give the agent everything it needs to operate:

**Required sections:**
- Identity — spokesperson for this work, not a generic assistant
- Paper Summary — 2-4 paragraphs
- Key Results — numbered list
- Repository Map — where files are and what they do
- What You Can Do — explain, reproduce figures (with commands), run experiments, extend
- Computational Requirements — what's light, what's heavy, platform tested
- Citation — BibTeX

**Key principle:** The AGENTS.md is an onboarding guide for an AI agent. Include specific commands, file paths, and parameter descriptions. The agent reading this has never seen the repo before.

Also create `CLAUDE.md` containing `@AGENTS.md` (Claude Code import syntax).

### 4. Extract research context (optional)

Ask the researcher if they want to include research context from their conversation history. This captures the reasoning behind the work — key decisions, methodology choices, debugging insights — so the published agent can answer "why did you do X?" from real reasoning.

Offer three levels:

- **Gist** — Extract and distill a short `context/research-notes.md` summarizing key decisions, what was tried, what worked, what didn't. The researcher reviews and edits before publishing.
- **Cleaned history** — Export relevant conversation sessions, remove private/irrelevant parts, save to `context/sessions/`. The researcher curates which sessions to include.
- **Full history** — Raw conversation dumps in `context/sessions/`. Maximum transparency.

The researcher can also decline entirely — context is optional.

If the researcher chooses to include context:
1. Use the conversation history extraction approach (similar to sci-brain's conversation-dump) to find sessions related to this paper
2. For **gist**: read the sessions, extract key decisions and reasoning into a concise markdown summary
3. For **cleaned/full history**: export the sessions, let the researcher review and remove anything private
4. Add a line to AGENTS.md: `For deeper context on the research process, read the files in context/`

### 5. Organize (if needed)

If the repo is messy, propose reorganizing. Only with researcher approval. Common structure:
- `paper/` — source + compiled PDF + figures
- `code/` — scripts, src
- `data/` — datasets

### 6. Create a GitHub Release

Once the researcher approves:
```bash
git add AGENTS.md CLAUDE.md
git commit -m "Add paper agent"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```
**Ask for confirmation** before pushing and creating the release:
```bash
git push origin main --tags
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```
