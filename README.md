# Agentic Publication Protocol (APP)

**Publish papers as AI agents.**

Create a publication repo with `AGENTS.md`. Tag a release. Now any AI coding agent can represent your work.

Works with [Claude Code](https://claude.ai/claude-code), [Codex](https://github.com/openai/codex), and [OpenCode](https://github.com/opencode-ai/opencode).

## Quick Start

**Claude Code:**

```
/plugin marketplace add LionSR/AgenticPublicationProtocol
```
```
/plugin install paper-protocol@paper-protocol
```

Then type `/publish-paper` and follow the interactive workflow.

**Updating:**
```
/plugin update paper-protocol
```

## Installation (Other Platforms)

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/refs/heads/main/.codex/INSTALL.md
```

Updating: `cd ~/.codex/paper-protocol && git pull`

### Other tools

Clone and point your tool at the `skills/` directory. To update, `git pull` in the cloned directory.

## Use a published paper

**Claude Code** (with plugin installed):
```
/load-paper-agent https://github.com/author/their-paper
```

**Load directly from arXiv:**
```
/load-paper-agent 2301.07041
```

**Any agent:**
```bash
git clone https://github.com/author/their-paper.git
# Open in Claude Code, Codex, Cursor, etc. — agent reads AGENTS.md
```

## Skills

| Skill | Description |
|-------|-------------|
| `/publish-paper` | Create a publication repo with AGENTS.md from your working repo |
| `/load-paper-agent` | Load a paper into your project — from GitHub URL or arXiv ID |
| `/find-paper-resources` | Find code repos, author blog posts, and OpenReview reviews for a paper |
| `/extract-context` | Extract research context (decisions, reasoning) from conversation history |
| `/create-paper-page` | Generate a GitHub Pages landing page for your paper |

## What's in this repo

- [PROTOCOL.md](PROTOCOL.md) — the AGENTS.md format spec (for tool builders and curious readers)
- [VISION.md](VISION.md) — ideas and future directions
- [skills/](skills/) — all five skills above
- [template/](template/) — starter `AGENTS.md` and `CLAUDE.md`

## License

Protocol: CC-BY-4.0 | Skills & templates: MIT
