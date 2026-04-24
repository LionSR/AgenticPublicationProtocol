# Agentic Publication Protocol (APP)

[![Protocol version](https://img.shields.io/badge/protocol-0.1.0--draft-orange)](PROTOCOL.md)
[![Latest release](https://img.shields.io/github/v/release/LionSR/AgenticPublicationProtocol?include_prereleases&sort=semver)](https://github.com/LionSR/AgenticPublicationProtocol/releases)
[![License: CC-BY-4.0 / MIT](https://img.shields.io/badge/license-CC--BY--4.0%20%2F%20MIT-blue)](#license)

APP is a format for authors to publish a finished paper as a GitHub repository any AI coding agent can represent. The repo carries the paper alongside the code, data, and context needed for the agent to explain the work, reproduce figures, run experiments, and answer questions — more of what the research actually contains than a static PDF can convey. Readers clone the repo, open it in [Claude Code](https://claude.ai/claude-code), [Codex](https://github.com/openai/codex), or any other agent that reads [`AGENTS.md`](https://agents.md), and the agent speaks for the paper.

APP packages results authors have already produced; it does not help write or produce the research. Bring a finished paper, and APP defines how to publish it.

This repository contains:

- [`PROTOCOL.md`](PROTOCOL.md) — the specification of what an APP publication looks like.
- [`skills/`](skills/) — tools that walk authors through producing one.
- [`template/`](template/) — starter files the skills adapt:
  - [`template/AGENTS.md`](template/AGENTS.md) — starter for the publication's `AGENTS.md`.
  - [`template/README.md`](template/README.md) — starter for the publication's human-facing `README.md`.
  - [`template/CLAUDE.md`](template/CLAUDE.md) — one-line Claude Code import (`@AGENTS.md`).
  - [`template/publication-checklist.md`](template/publication-checklist.md) — the publication checklist expanded into per-topic subchecks.
  - [`template/publications.md`](template/publications.md) — template for the working repo's `.publications.md` release log.

## Install

### Claude Code

```
/plugin marketplace add LionSR/AgenticPublicationProtocol
/plugin install paper-protocol@paper-protocol
```

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/refs/heads/main/.codex/INSTALL.md
```

### Other tools

Clone this repo and point your agent at the `skills/` directory.

## Update

| Platform | Command |
|----------|---------|
| Claude Code | `/plugin update paper-protocol` |
| Codex | `cd ~/.codex/paper-protocol && git pull` |
| Other tools | `git pull` in the cloned directory |

New skills, reference files, and templates appear automatically after update — no re-install needed.

## Publish a paper

Open your working repo in an AI coding agent with this plugin installed, then invoke:

```
/publish-paper
```

The skill interviews you about the paper, copies the approved files into a new publication repo, drafts `AGENTS.md` with you, runs validation, and walks you through tagging a release. The process can span multiple sessions.

## Use a published paper

Clone the repo and open it in an AI coding agent:

```bash
git clone https://github.com/author/their-paper.git
cd their-paper
# open in Claude Code, Codex, Cursor, or any agent that reads AGENTS.md
```

The agent reads `AGENTS.md` on startup and now speaks for the paper.

Claude Code users can also run `/load-paper-agent <repo-url>` to clone a published paper into the current project as a sub-agent without leaving the working session.

## Skills

**Main entry point**

| Skill | What it does |
|-------|--------------|
| `/publish-paper` | Package a working repo into an APP publication. |

**Called by `/publish-paper`**

| Skill | What it does |
|-------|--------------|
| `/validate-publication` | Check a publication against `PROTOCOL.md` — paths, privacy, factuality, consistency. |
| `/extract-context` | Pull research context (decisions, reasoning, dead ends) from local Claude Code / Codex conversation history. |

**Standalone**

| Skill | What it does |
|-------|--------------|
| `/create-paper-page` | Generate a GitHub Pages landing page for a published paper. |
| `/load-paper-agent` | Load a published paper into the current project as a sub-agent. |
| `/load-arxiv-paper` | Load a paper directly from arXiv — fetch PDF, metadata, and optionally code and reviews. Works on any paper, not only APP-compliant ones. |

## License

`PROTOCOL.md`: CC-BY-4.0. Skills and templates: MIT.
