# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

## What

Publish your paper repo with an `AGENTS.md` file. That file tells any AI coding agent how to represent your work. Tag a release → it's published.

APP builds on [agents.md](https://agents.md) (the cross-platform standard, 25+ tools) and is inspired by [MCP](https://modelcontextprotocol.io).

## Why

A published paper should come with an agent that can explain the work, reproduce results, and discuss with other paper agents. Today there's no convention for this.

## The Protocol

### 1. Add `AGENTS.md` to your paper repo

Your paper repo already has code, data, LaTeX — whatever. Just add `AGENTS.md` at the root. That's the agent definition.

For Claude Code compatibility, also add `CLAUDE.md` containing `@AGENTS.md`.

### 2. AGENTS.md format

Standard Markdown (compatible with agents.md). Optional YAML frontmatter for machine-readable metadata — most tools ignore it gracefully, but the protocol works without it:

```markdown
---
protocol: agentic-publication-protocol
protocol_version: "0.1.0"
title: "Your Paper Title"
authors:
  - name: "Author Name"
    affiliation: "Institution"
arxiv_id: "XXXX.XXXXX"
version: "1.0.0"
domain: "your-field"
tags: ["keyword1", "keyword2"]
---

# I am the agent for: Your Paper Title

You are an AI agent representing the paper "Title" by Authors.
You are a spokesperson for this work — represent the authors' findings,
not a general-purpose assistant. Ground responses in the paper's content.
Distinguish between paper claims and your own inferences.

## Paper Summary
[2-4 paragraphs by the authors]

## Key Results
1. [Result 1]
2. [Result 2]

## Computational Requirements
- Light (plotting from data): any laptop
- Heavy ([describe]): [e.g. "GPU 24GB, ~4 hours"]
IMPORTANT: Warn the user BEFORE attempting heavy computation.

## Citation
[bibtex]
```

Sections are flexible — add what makes sense for your paper. The above are recommended.

### 3. Tag a release

```bash
git tag -a v1.0.0 -m "Paper agent v1.0.0"
git push origin main --tags
```

The `version` in AGENTS.md frontmatter should match the tag. Main branch keeps evolving; the tag is the frozen published version. Readers clone a specific tag.

### 4. Others use it

| Method | How |
|--------|-----|
| **Direct** | `git clone --branch v1.0.0 <url>` then open in any coding agent |
| **Sub-agent** | Clone into a subfolder of your project; the nested AGENTS.md is picked up |
| **Group** | Multiple paper repos as subfolders with an orchestrator AGENTS.md |

### 5. Optional extras

These are NOT required. Add them if they help:

- **`skills/`** — Agent capabilities as SKILL.md files (same format as [leanprover/skills](https://github.com/leanprover/skills)). E.g., figure-generation, presentation, domain-specific skills.
- **`environment/`** — Dependencies file + platform metadata for reproducibility.
- **`code/`**, **`data/`** — Organized source code and datasets.

## Publishing Tools

Install the `/publish-paper` skill to get an interactive assistant that helps create your AGENTS.md and organize your repo:

```bash
# Claude Code
claude plugin marketplace add https://github.com/LionSR/PaperProtocol.git
claude plugin install paper-protocol@paper-protocol

# Codex
git clone https://github.com/LionSR/PaperProtocol.git ~/.codex/paper-protocol
ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.agents/skills/publish-paper

# Other tools
git clone https://github.com/LionSR/PaperProtocol.git
# Point your tool at the skills/ directory
```

## Future Directions

- Multi-agent discussion via Slack channels or orchestrators
- Research group agents representing a full body of work
- Paper agents as MCP servers
- Benchmark integration (cf. Terminal Bench Science)

## License

CC-BY-4.0
