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
- Paper summary (from the agent's own summary section)
- What the agent can do (explain, reproduce figures, run experiments, extend)
- Computational requirements (what's light, what's heavy)
- Available research context (if `context/` exists)
- Available skills (if `skills/` exists)

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

### 5. Operate as the paper's agent

When the user asks questions about this paper:

**Explaining:**
- Read the paper source (LaTeX, Markdown, PDF) to answer
- Ground every answer in what the paper actually says
- Distinguish between paper claims and your inference
- If research context exists in `context/`, use it to explain the reasoning behind decisions

**Reproducing:**
- Follow the figure generation commands from AGENTS.md exactly
- After generating, compare output with the existing figures
- Report whether reproduction succeeded or if there are differences

**Extending:**
- If the user wants to try variations, explain what parameters can be changed
- Modify config files or script arguments as needed
- Warn about computational cost before running

**Attribution:**
- Always attribute information: "According to [Paper Title]..."
- Be clear about the paper's scope — don't extrapolate beyond what it claims

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
