---
name: publish-paper
description: Use when a researcher wants to publish their paper as an AI agent. Helps create AGENTS.md and organize the repo.
---

# Publish Paper as Agent

Help a researcher add an AI agent to their paper repo following the Agentic Publication Protocol.

## Steps

### 1. Understand the project
Read the repo. Find the paper source, code, data, figures.

### 2. Discuss with the researcher
Ask: What is this paper about? What are the key results? What code/data should be included? What computational resources are needed? What should NOT be published (private working artifacts, intermediate experiments, personal notes)?

### 3. Create AGENTS.md
Generate `AGENTS.md` at the repo root using the template from this protocol. Fill in the researcher's answers. The AGENTS.md is the agent — it defines the paper's spokesperson.

Also create `CLAUDE.md` containing `@AGENTS.md`.

### 4. Organize (if needed)
If the repo is messy, propose reorganizing into `paper/`, `code/`, `data/` directories. Only do this with researcher approval.

### 5. Create a GitHub Release
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
