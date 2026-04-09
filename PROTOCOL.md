# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

This document is the protocol specification. For installation and usage, see the [README](README.md).

## Overview

APP turns a paper into an AI agent. Create a publication repo with `AGENTS.md` at the root, tag a release, and any AI coding agent can represent the work — explain it, reproduce figures, run experiments, answer questions.

The publication repo is typically separate from the researcher's working repo. It contains only the curated subset of code, data, and documentation meant for public consumption. The working repo stays private.

APP builds on [agents.md](https://agents.md) (the cross-platform standard, 25+ tools) and is inspired by [MCP](https://modelcontextprotocol.io).

## Core principles

**Spokesperson, not assistant.** The published agent represents the authors to outside readers. It explains, presents, and defends the work from the paper's perspective. It speaks in the domain's voice — a math paper agent reasons like a mathematician, an experimental physics paper agent thinks like an experimentalist.

**Single source of truth.** The published repo should have exactly one canonical location for each piece of code, data, and documentation. No duplicates, no ambiguity about which version is current. Every file referenced in the paper, scripts, or AGENTS.md resolves to one real path.

**Honest and grounded.** The agent distinguishes between the paper's claims and its own inferences. It knows the paper's limitations and says so. It says clearly when something is outside the paper's scope.

## AGENTS.md

The core of the protocol. One file at the repo root that tells any coding agent how to represent the paper. Standard Markdown (compatible with agents.md). Optional YAML frontmatter for machine-readable metadata.

### Frontmatter

```yaml
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
```

### Required sections

**Identity** — Who the agent is and how it should behave. References the paper title, authors, and domain.

**Paper Summary** — 2-4 paragraphs covering: what problem, what approach, what results, what implications. Written by the authors (or from their words). This is what the agent relies on most.

**Key Results** — Numbered list of the main contributions.

**Repository Map** — Every important file with its path and purpose. Group by function: paper source, figure generation, experiments, data, config. For external data (Hugging Face, Zenodo, etc.), include the URL, download command, and local destination.

**What You Can Do** — Concrete agent capabilities:
- *Explain the paper*: which files to read for which topics
- *Reproduce figures*: a table mapping every figure to its command, data source, and runtime
- *Run experiments*: exact commands with real parameters
- *Extend the work*: what parameters to vary, what's interesting to try

**Computational Requirements** — Classify every task by time, hardware, and memory. Note the platform tested on. The agent must warn before running anything heavy.

**Citation** — Full BibTeX entry.

### Optional sections

**Research Context** — Pointer to `context/research-notes.md` or `context/sessions/` if the authors extracted reasoning from their development sessions.

**Skills** — Pointer to `skills/` if the paper provides additional agent capabilities.

## Versioning

A published version is a GitHub Release on the publication repo (which creates a git tag). The `version` in AGENTS.md frontmatter should match the release tag. The main branch of the publication repo can keep evolving; each release is a frozen snapshot.

## Using a published paper

| Method | How |
|--------|-----|
| **Direct** | Clone the release, open in any coding agent — it reads AGENTS.md |
| **Sub-agent** | Clone into a subfolder of your project; the nested AGENTS.md is picked up |
| **Group** | Multiple paper repos as subfolders with an orchestrator AGENTS.md |

## Optional extras

Not required. Add them if they help:

- **`context/`** — Research context extracted from conversation histories. Can include a distilled `research-notes.md` and/or `sessions/` with curated conversation logs.
- **`skills/`** — Agent capabilities as SKILL.md files
- **`environment/`** — Dependencies file + platform metadata
- **`code/`**, **`data/`** — Organized source code and datasets

## License

CC-BY-4.0
