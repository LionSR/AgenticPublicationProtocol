# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

## What

Publish your paper repo with an `AGENTS.md` file. Create a GitHub Release. Now any AI coding agent can represent your work.

APP builds on [agents.md](https://agents.md) (the cross-platform standard, 25+ tools) and is inspired by [MCP](https://modelcontextprotocol.io).

## Why

A published paper should come with an agent that can explain the work, reproduce results, and discuss with other paper agents. Today there's no convention for this.

## Get Started

Install the `/publish-paper` plugin — it walks you through everything interactively:

```
/plugin marketplace add LionSR/AgenticPublicationProtocol
/plugin install paper-protocol@paper-protocol
```

Then run `/publish-paper`. See [README](README.md) for Codex and OpenCode installation.

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

## Repository Map
- `paper/main.tex` — paper source (LaTeX)
- `paper/build/paper.pdf` — compiled PDF
- `code/src/` — core implementation in Python
- `code/scripts/generate_figures.py` — generates all figures
- `data/results.csv` — pre-computed results for plotting
- `environment/requirements.txt` — Python dependencies

## What You Can Do

### Explain the paper
Read `paper/main.tex` to answer questions about methods, results,
and implications. Always ground answers in what the paper actually says.

### Reproduce figures
Each figure can be regenerated:
| Figure | Command | Data | Time |
|--------|---------|------|------|
| Fig 1 | `python code/scripts/generate_figures.py --fig 1` | `data/results.csv` | ~5s |
| Fig 2 | `python code/scripts/generate_figures.py --fig 2` | `data/results.csv` | ~10s |
Before running, install deps: `pip install -r environment/requirements.txt`
After generating, compare output with `paper/figures/` to verify correctness.

### Run experiments
The main experiment can be run with:
`python code/src/main.py --config code/configs/default.yaml`
This requires [describe resources]. Warn the user before starting.

### Extend the work
Users may ask "what if we change X?" You can modify parameters in
the config files and re-run. Explain what each parameter controls.

## Computational Requirements
- **Figure generation** (from pre-computed data): any laptop, <1 min
- **Full experiment** (re-running from scratch): [e.g. "GPU 24GB, ~4 hours"]
- **Platform tested**: macOS 14.2 / Python 3.11
IMPORTANT: Always warn the user BEFORE attempting heavy computation.
If running on a different platform than tested, warn about potential issues.

## Skills
Additional capabilities in `skills/`:
- `skills/figure-generation/SKILL.md` — detailed figure reproduction
- `skills/presentation/SKILL.md` — generate slides from this paper

## Citation
[bibtex]
```

Sections are flexible — add what makes sense for your paper. The key principle: **tell the agent everything it needs to know to operate in your repo**. Map the files, explain the commands, describe the data, specify what's light and what's heavy.

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

- **`context/`** — Research context extracted from conversation histories. Can include a distilled `research-notes.md` (key decisions and reasoning) and/or `sessions/` with curated or raw conversation logs. Gives the agent access to the *why* behind the work, not just the *what*.
- **`skills/`** — Agent capabilities as SKILL.md files (same format as [leanprover/skills](https://github.com/leanprover/skills))
- **`environment/`** — Dependencies file + platform metadata
- **`code/`**, **`data/`** — Organized source code and datasets

## Design Principle

The published agent is a **spokesperson**, not a general-purpose assistant. It represents the authors to outside readers — it explains, presents, and defends the work. It speaks from the perspective of the paper. If it's a math paper, the agent reasons like a mathematician. If it's an experimental physics paper, it thinks like an experimentalist.

## License

CC-BY-4.0
