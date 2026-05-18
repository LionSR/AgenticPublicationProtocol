# Agentic Publication Protocol (APP)

[![Protocol version](https://img.shields.io/badge/protocol-0.1.0--draft-orange)](PROTOCOL.md)
[![Latest release](https://img.shields.io/github/v/release/LionSR/AgenticPublicationProtocol?include_prereleases&sort=semver)](https://github.com/LionSR/AgenticPublicationProtocol/releases)
[![License: CC-BY-4.0 / MIT](https://img.shields.io/badge/license-CC--BY--4.0%20%2F%20MIT-blue)](#license)

APP is a format for authors to publish a finished paper as a GitHub repository any AI coding agent can represent. The repo carries the paper alongside the code, data, and context needed for the agent to explain the work, reproduce figures, run experiments, and answer questions — more of what the research actually contains than a static PDF can convey. A verified APP publication is a tagged public release with `AGENTS.md` plus an `APP_PUBLICATION.json` release manifest tying the release to validation and author approval. Readers clone the repo, open it in [Claude Code](https://claude.ai/claude-code), [Codex](https://github.com/openai/codex), or any other agent that reads [`AGENTS.md`](https://agents.md), and the agent speaks for the paper.

APP packages results authors have already produced; it does not help write or produce the research. Bring a finished paper, and APP defines how to publish it.

This repository contains:

- [`PROTOCOL.md`](PROTOCOL.md) — the specification of what an APP publication looks like.
- [`skills/`](skills/) — tools that walk authors through producing one.
- [`template/`](template/) — starter files the skills adapt:
  - [`template/AGENTS.md`](template/AGENTS.md) — starter for the publication's `AGENTS.md`.
  - [`template/README.md`](template/README.md) — starter for the publication's human-facing `README.md`.
  - [`template/CLAUDE.md`](template/CLAUDE.md) — one-line Claude Code import (`@AGENTS.md`).
  - [`template/publications.md`](template/publications.md) — template for the working repo's `.publications.md` release log.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to propose changes to the protocol, templates, and official skills.

## Install

### Claude Code

```
/plugin marketplace add LionSR/AgenticPublicationProtocol
/plugin install paper-protocol@paper-protocol
```

### Codex

```
codex plugin marketplace add LionSR/AgenticPublicationProtocol
```

Then open Codex, find `Agentic Publication Protocol` in the plugin browser, and enable it.

### Other tools

Clone this repo and point your agent at the `skills/` directory.

## Update

| Platform | Command |
|----------|---------|
| Claude Code | `/plugin update paper-protocol` |
| Codex | `codex plugin marketplace upgrade paper-protocol` |
| Other tools | `git pull` in the cloned directory |

New skills, reference files, and templates appear automatically after update — no re-install needed.

## Publish a paper

Open your working repo in an AI coding agent with this plugin installed, then invoke:

```
/publish-paper
```

The skill interviews you about the paper, copies the approved files into `publication-staging/`, creates the paper-agent docs with you, runs validation, and walks you through publishing a tagged release with a verifiable APP manifest. The process can span multiple sessions.

## Use a published paper

Clone the repo and open it in an AI coding agent:

```bash
git clone https://github.com/author/their-paper.git
cd their-paper
# open in Claude Code, Codex, Cursor, or any agent that reads AGENTS.md
```

The agent reads `AGENTS.md` on startup and now speaks for the paper.

Claude Code users can also run `/load-paper <repo-url>` to clone or import a paper into the current project without leaving the working session.

## Skills

The skills in this repository are grouped by how essential they are to the APP workflow.

**Core publication workflow**

| Skill | What it does |
|-------|--------------|
| `/publish-paper` | Package a working repo into an APP publication. |
| `/validate-publication` | Check APP structure, paths, privacy, clear factual consistency, reader-agent usability, and release manifest verification when applicable. Called by `/publish-paper` and also useful on its own. |
| `/extract-chat-context` | Pull publication-safe research context from local Claude Code / Codex chat/session history for supplementary materials. Optional helper called by `/publish-paper`. |

**Optional publication add-ons**

| Skill | What it does |
|-------|--------------|
| `/create-paper-page` | Generate a GitHub Pages landing page for a published paper. Not required for APP compliance; may be offered after `/publish-paper` succeeds. |

**Reader and import utility**

This is a useful companion skill, but it is not required to create or validate an APP publication.

| Skill | What it does |
|-------|--------------|
| `/load-paper` | Load a published paper, local APP candidate, non-APP paper repo, or arXiv paper into the current project. Classifies APP status when possible; for arXiv inputs, fetches metadata/source, searches for associated public code, and creates a protocol-shaped local import. |

## External skills and extensions

APP publications may point to reusable skills or extensions hosted outside the publication repo, including community-maintained skill collections or individual researchers' repositories. Use `recommended_external_skills`, `app_extensions`, or the **External Skills and Extensions** section of `AGENTS.md` to record the source URL, version or tag, and purpose. Skill sources should point directly to a directory containing `SKILL.md`, preferably at a stable tag or commit.

External skills are recommendations only. They are not part of an author-approved APP publication unless they are bundled into the tagged release and covered by the publication manifest.

## Contributing

Contributions to the protocol, templates, documentation, validation behavior, and official APP workflow skills are welcome. Reusable field-specific or authoring skills can also live in independent repositories and be referenced from APP publications. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the boundary between official APP repo changes and external skill contributions.

## License

`PROTOCOL.md`: CC-BY-4.0. Skills and templates: MIT.
