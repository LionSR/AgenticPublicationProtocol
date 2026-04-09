---
name: publish-paper
description: Use when a researcher wants to publish their paper as an AI agent following the Paper Publication Protocol. Guides through repo organization, AGENTS.md creation, environment documentation, and the publishing checklist.
---

# Publish Paper as Agent

Guide a researcher through publishing their paper as a PPP-compliant AI agent.

## Workflow

### Step 1: Understand the Project

Read the current repo structure. Identify:
- Where is the paper source? (LaTeX, Markdown, PDF)
- Where is the code? What language/framework?
- Is there data? How large?
- What figures exist? Can they be regenerated from code?
- What dependencies are needed?

### Step 2: Discuss with the Researcher

Ask the researcher:
- What is this paper about? (for the Paper Summary section)
- What are the key results? (numbered list)
- Which figures should be reproducible from code+data?
- What computational resources are needed? (laptop? GPU? cluster?)
- What domain-specific skills would be useful?
- Is there anything they do NOT want to include?

Do not proceed until the researcher has answered these questions.

### Step 3: Propose a Plan

Based on Step 1 and 2, propose:
- Directory reorganization (what goes into paper/, code/, data/)
- Draft AGENTS.md content
- Which skills to create
- What the environment/platform.json should contain

Present the plan and wait for approval. If the researcher modifies or rejects parts, revise accordingly.

### Step 4: Execute

Once approved:

1. **Create directory structure:**
   ```
   paper/          — move paper source here
   paper/figures/  — move/copy pre-built figures
   paper/build/    — compiled PDF
   code/           — move code here
   code/scripts/   — figure generation scripts
   data/           — move data here
   environment/    — create new
   skills/         — create new
   ```

2. **Generate AGENTS.md** at repo root with:
   - YAML frontmatter (protocol, title, authors, date, version, domain, tags)
   - Identity and Role section
   - Paper Summary (from researcher's input)
   - Key Results (from researcher's input)
   - Available Skills (list with paths)
   - Computational Requirements (from discussion)
   - Citation (BibTeX)

3. **Create CLAUDE.md** at repo root:
   ```markdown
   @AGENTS.md
   ```

4. **Generate environment/platform.json** by inspecting:
   - Current OS and architecture
   - Language version (python --version, etc.)
   - Package manager and dependency file
   - GPU requirements (from discussion)

5. **Generate environment/requirements.txt** (or equivalent) by analyzing imports.

6. **Create skill files** under skills/:
   - figure-generation/SKILL.md (if code generates figures)
   - presentation/SKILL.md (default)
   - Any domain-specific skills discussed

7. **Create README.md** with:
   - Paper title and authors
   - Links to paper PDF, arXiv, project page
   - Quick start for humans and agents
   - Repository structure table
   - Environment summary
   - Agent capabilities checklist

### Step 5: Run the Publishing Checklist

Verify each item. Report status (PASS/FAIL/N/A):

**Structure:**
- [ ] AGENTS.md exists at root with valid YAML frontmatter
- [ ] CLAUDE.md exists and contains `@AGENTS.md`
- [ ] README.md exists
- [ ] environment/ directory exists

**Paper:**
- [ ] Paper source in paper/
- [ ] Compiled PDF in paper/build/

**Environment:**
- [ ] Dependency file with pinned versions
- [ ] platform.json with OS/language/compute info

**Code (if code/ exists):**
- [ ] code/README.md with entry points
- [ ] No hardcoded absolute paths
- [ ] No credentials or secrets in tracked files
- [ ] Figure generation scripts exist
- [ ] Running figure scripts produces output without errors

**Data (if data/ exists):**
- [ ] data/README.md with provenance
- [ ] Large files (>50MB) use Git LFS or external links

If any items FAIL, help the researcher fix them before proceeding.

### Step 6: Release

Once checklist passes:

1. Stage and commit all changes
2. Tag the release: `git tag -a v1.0.0 -m "Paper agent v1.0.0"`
3. Push: `git push origin main --tags`
4. Create GitHub Release (if gh CLI available)
5. (Optional) Set up GitHub Pages for a landing page

Report the final status and the repository URL.
