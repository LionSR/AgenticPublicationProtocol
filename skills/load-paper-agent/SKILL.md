---
name: load-paper-agent
description: Load a published paper agent into your current project as a sub-agent. Use when a user wants to consult, build on, or discuss a paper that follows the Agentic Publication Protocol. Also works with non-APP repos that have code and a README.
---

# Load Paper Agent

Load a published paper into your project so you can consult it, reproduce results, and build on the work.

## Triggering

User says something like:
- "Load paper agent from https://github.com/user/paper-repo"
- "I want to consult the paper at <url>"
- "Add this paper as a sub-agent: <url>"
- "Load <arxiv-id> as a paper agent"

## Steps

### 1. Clone the paper

```bash
mkdir -p papers/
git clone <url> papers/<repo-name>
```

If the user specifies a version:
```bash
git clone --branch v1.0.0 <url> papers/<repo-name>
```

If the user gives an arXiv ID instead of a GitHub URL, search for the corresponding repo (check the paper's PDF for a GitHub link, or search GitHub for the arXiv ID).

If the clone fails (private repo, wrong URL), inform the user and ask for the correct URL or access.

### 2. Check for APP compliance

Read `papers/<repo-name>/AGENTS.md`. Check:
- Does it exist? If yes, this is an APP-compliant paper.
- Does it have YAML frontmatter with `protocol: agentic-publication-protocol`? If yes, it's a fully structured APP paper.
- If AGENTS.md doesn't exist, check for `README.md`, `CLAUDE.md`, or any documentation. The repo can still be useful — you'll just need to explore it manually.

### 3. Explore and report

**For APP-compliant papers**, read the AGENTS.md and report to the user:
- Paper title and authors
- Paper format (from `paper_format` in frontmatter)
- Paper summary (from the agent's own summary section)
- What the agent can do (explain, reproduce figures, run experiments, extend)
- Computational requirements (what's light, what's heavy)
- Available supplementary materials (if `supplementary/` exists) — know-how, author notes, sessions, additional materials
- Available skills (if `skills/` exists) — list each skill with its name and description from the SKILL.md frontmatter

**For non-APP repos**, explore the repo and report:
- What the repo contains (paper, code, data, notebooks)
- What language/framework the code uses
- Whether there are obvious entry points (README, scripts, notebooks)
- What you'd need to figure out to use this

### 4. Set up the environment (if the user wants to run code)

Before running anything from the paper:
1. Check `environment/requirements.txt` or equivalent
2. Check the computational requirements section of AGENTS.md
3. If anything is heavy or requires special hardware, warn the user
4. If the platform differs from what was tested, warn about potential compatibility issues
5. Only install dependencies with user approval:
   ```bash
   cd papers/<repo-name>
   pip install -r environment/requirements.txt  # or equivalent
   ```
6. Check if the paper references external datasets (Hugging Face, Zenodo, Figshare, etc.). The Repository Map in AGENTS.md should list these with download commands. If the user needs data that isn't in the repo:
   - Tell them what's needed, how large it is, and where to get it
   - Offer to run the download command (with approval)
   - Don't attempt to run code that depends on missing data — explain what's needed first

### 5. Operate as the paper's agent

**The paper is the ground truth.** The paper document (in whatever format — LaTeX, DOCX, Markdown, HTML, video, PPTX) is the authoritative source for all claims and results. Supplementary materials provide additional context but are secondary. If anything in the supplementary materials conflicts with the paper, defer to the paper.

When the user asks questions about this paper, route to the right source:

**Routing guide — which file for which question:**

| User asks about... | Primary source | Also check |
|---------------------|---------------|------------|
| What the paper claims, methods, results | Paper source (ground truth) | AGENTS.md Paper Summary |
| Why a specific choice was made | `supplementary/know-how.md` | Paper source for what the choice was |
| What to know before reading | `supplementary/authors-note.md` | AGENTS.md Paper Summary |
| How to reproduce a figure | AGENTS.md figure table | Run the command |
| How to run an analysis or workflow | `skills/` (check for matching skill) | AGENTS.md "What You Can Do" |
| What parameters to change | AGENTS.md "Extend the work" | Code configs |
| Computational requirements | AGENTS.md Computational Requirements | |

**Explaining:**
- Read the paper source to answer — it is the ground truth
- Ground every answer in what the paper actually says
- Distinguish between paper claims and your inference
- If supplementary materials exist in `supplementary/`, use them to explain the reasoning behind decisions — but note that these provide context, not authoritative claims
- If `supplementary/know-how.md` exists, use it to answer "why did you do X?" questions — this is where tacit knowledge lives
- If `supplementary/authors-note.md` exists, use it for the authors' perspective on what matters beyond the paper

**Reproducing:**
- Follow the figure generation commands from AGENTS.md exactly
- After generating, compare output with the existing figures
- Report whether reproduction succeeded or if there are differences
- **If a command fails:** read the error, check the environment setup (step 4), and report what went wrong. Common issues: missing dependencies, wrong Python version, missing data files. Don't silently retry — explain the failure and suggest fixes.
- **If external data is needed:** check AGENTS.md Repository Map for download commands. Tell the user what's needed, how large it is, and offer to download it (with approval) before retrying.

**Extending:**
- If the user wants to try variations, explain what parameters can be changed
- Modify config files or script arguments as needed
- Warn about computational cost before running
- After running a variation, compare results with the paper's reported results and note differences

**Using skills:**
- If the paper includes skills in `skills/`, read the SKILL.md files to discover what capabilities the authors provided
- **Proactively suggest skills** when the user's request matches a skill name or description — e.g., "This paper includes a guided analysis skill that can walk you through this. Would you like to use it?"
- When using a skill, read the SKILL.md and follow its instructions step by step
- Report what the skill produced and whether it succeeded
- If a skill's output appears to contradict the paper, flag the discrepancy to the user
- If a skill fails partway through, report where it failed and what the expected behavior was

**Attribution:**
- Always attribute information: "According to [Paper Title]..."
- Be clear about the paper's scope — don't extrapolate beyond what it claims

**Feedback loop:**
- After answering a substantive question, ask: "Did that answer your question, or should I look deeper into the paper or code?"
- If the user's question can't be fully answered from the available materials, say so explicitly and suggest what might help (e.g., "The paper doesn't discuss this; you might want to contact the authors")

### 6. Multiple papers

If the user loads multiple papers into `papers/`:

- Keep each paper's context separate — don't mix up claims from different papers
- When the user asks to compare, read both AGENTS.md files and compare specific aspects
- Attribute every claim to its source paper
- Identify connections: shared methods, contradictory results, complementary approaches
- When asked to synthesize, be explicit about what comes from where

### 7. Integrating with the user's project

If the user wants to reference the paper from their own AGENTS.md or CLAUDE.md:

**For Claude Code:**
```markdown
# In the user's CLAUDE.md:
@papers/paper-name/AGENTS.md
```

**For any platform:**
Add to the user's AGENTS.md:
```markdown
## Referenced Papers
- [Paper Title](papers/paper-name/AGENTS.md) — [one-line description of how it relates to this project]
```

This makes the paper agent's context available whenever the user works on their project.
