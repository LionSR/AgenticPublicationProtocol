# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

## What

Publish your paper repo with an `AGENTS.md` file. Create a GitHub Release. Now any AI coding agent can represent your work.

APP builds on [agents.md](https://agents.md) (the cross-platform standard, 25+ tools) and is inspired by [MCP](https://modelcontextprotocol.io).

## Why

A published paper should come with an agent that can explain the work, reproduce results, and discuss with other paper agents. Today there's no convention for this.

## Get Started

Install the `/publish-paper` plugin — it walks you through everything interactively:

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

Then run `/publish-paper` in your coding agent. It will:
1. Read your repo and discuss what to include
2. Create `AGENTS.md` — the agent definition
3. Create `CLAUDE.md` containing `@AGENTS.md` (for Claude Code compatibility)
4. Create a GitHub Release

## The Protocol

What `/publish-paper` does under the hood:

### AGENTS.md

The core of the protocol. One file at the repo root that tells any coding agent how to represent your paper. Standard Markdown (compatible with agents.md). Optional YAML frontmatter for machine-readable metadata:

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

Sections are flexible — add what makes sense for your paper.

### GitHub Release

A published version is a GitHub Release (which creates a git tag). The `version` in AGENTS.md frontmatter should match the release tag. Main branch keeps evolving; the release is the frozen published version.

### Using a published paper

| Method | How |
|--------|-----|
| **Direct** | Clone the release, open in any coding agent — it reads AGENTS.md |
| **Sub-agent** | Clone into a subfolder of your project; the nested AGENTS.md is picked up |
| **Group** | Multiple paper repos as subfolders with an orchestrator AGENTS.md |

### Optional extras

Not required. Add them if they help:

- **`skills/`** — Agent capabilities as SKILL.md files (same format as [leanprover/skills](https://github.com/leanprover/skills))
- **`environment/`** — Dependencies file + platform metadata
- **`code/`**, **`data/`** — Organized source code and datasets

## Future Directions

- Multi-agent discussion via Slack channels or orchestrators
- Research group agents representing a full body of work
- Paper agents as MCP servers
- Benchmark integration (cf. Terminal Bench Science)

## License

CC-BY-4.0
