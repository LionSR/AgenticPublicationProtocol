# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

This document is the protocol specification. For installation and usage, see the [README](README.md).

## Overview

APP turns a paper into an AI agent. Create a publication repo with `AGENTS.md` at the root, tag a release, and any AI coding agent can represent the work — explain it, reproduce figures, run experiments, answer questions.

The publication repo is typically separate from the researcher's working repo. It contains only the curated subset of code, data, and documentation meant for public consumption. The working repo stays private.

APP builds on [agents.md](https://agents.md) (the cross-platform standard, 25+ tools) and is inspired by [MCP](https://modelcontextprotocol.io).

## Core principles

**Spokesperson, not assistant.** The published agent represents the authors to outside readers. It explains, presents, and defends the work from the paper's perspective. It speaks in the domain's voice — a math paper agent reasons like a mathematician, an experimental physics paper agent thinks like an experimentalist.

**Paper is the ground truth.** The paper document — in whatever format the authors designate (LaTeX, DOCX, Markdown, HTML, video, PPTX) — is the authoritative source for the work's claims and results. All other materials (talks, slides, supplementary notes, conversation history, skills) are secondary. When any supplementary material conflicts with the paper, the paper takes precedence. The agent must understand and respect this hierarchy.

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
paper_format: "latex"  # or "docx", "markdown", "html", "video", "pptx", "pdf"
version: "1.0.0"
domain: "your-field"
tags: ["keyword1", "keyword2"]
---
```

### Required sections

**Identity** — Who the agent is and how it should behave. References the paper title, authors, and domain. Must establish that the paper is the ground truth for all claims.

**Paper Summary** — 2-4 paragraphs covering: what problem, what approach, what results, what implications. Written by the authors (or from their words). The paper can be in any format (LaTeX, DOCX, Markdown, HTML, video, PPTX); the agent should read and reference the designated main document. This is what the agent relies on most.

**Key Results** — Numbered list of the main contributions.

**Repository Structure** — Every important file with its path and purpose. Group by function: paper source, figure generation, experiments, data, config. For external data (Hugging Face, Zenodo, etc.), include the URL, download command, and local destination.

**What You Can Do** — Concrete agent capabilities:
- *Explain the paper*: which files to read for which topics
- *Reproduce figures*: a table mapping every figure to its command, data source, and runtime
- *Run experiments*: exact commands with real parameters
- *Extend the work*: what parameters to vary, what's interesting to try

**Computational Requirements** — Classify every task by time, hardware, and memory. Note the platform tested on. The agent must warn before running anything heavy.

**Citation** — Full BibTeX entry.

### Optional sections

**Supplementary Materials** — Pointer to `supplementary/` if the authors included additional materials beyond the paper:
- `supplementary/know-how.md` — practical knowledge, methodology decisions, tacit insights extracted from the research process
- `supplementary/authors-note.md` — what the authors want readers to know beyond the paper
- `supplementary/sessions/` — (optional) curated conversation history from development sessions
- `supplementary/materials/` — (optional) slides, talks, posters, tutorials. These are secondary to the paper — useful context, not ground truth.

**Skills** — Pointer to `skills/` if the paper provides additional agent capabilities. Authors can publish custom skills as SKILL.md files in `skills/`. Each skill is a self-contained capability the agent can perform — e.g., a specialized analysis workflow, a visualization pipeline, or a guided exploration of the results. Skills follow the standard SKILL.md format (name and description in frontmatter, instructions in body). Skills are tools, not claims — they do not override the paper's findings.

## Versioning

A published version is a GitHub Release on the publication repo (which creates a git tag). The `version` in AGENTS.md frontmatter should match the release tag. The main branch of the publication repo can keep evolving; each release is a frozen snapshot.

When publishing a new version, the previous version's AGENTS.md, supplementary materials, and skills should be used as a starting point. Most content carries forward — only update what has actually changed.

## Using a published paper

| Method | How |
|--------|-----|
| **Direct** | Clone the release, open in any coding agent — it reads AGENTS.md |
| **Sub-agent** | Clone into a subfolder of your project; the nested AGENTS.md is picked up |
| **Group** | Multiple paper repos as subfolders with an orchestrator AGENTS.md |

## Publication repo structure

Publication repos should follow a consistent directory layout. Not every directory is required — a theory paper may only need `paper/` — but files should be in the right place.

```
paper/              ← paper source (GROUND TRUTH), figures, bibliography, compiled PDF
code/               ← src/, scripts/, configs/, notebooks/
data/               ← raw/, processed/, README
environment/        ← requirements.txt (or equivalent), setup instructions
supplementary/      ← know-how.md, authors-note.md, checklist.md, sessions/, materials/
skills/             ← <name>/SKILL.md per author-published skill
AGENTS.md           ← paper agent instructions
CLAUDE.md           ← @AGENTS.md (Claude Code import)
README.md           ← public README for readers
LICENSE
.gitignore
```

Root should only contain the files listed above and the top-level directories. Code, data, paper source, and dependencies each have their own directory — don't put them loose at root.

## License

CC-BY-4.0
