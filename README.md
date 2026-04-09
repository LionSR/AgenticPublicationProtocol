# Agentic Publication Protocol (APP)

**Publish papers as AI agents.**

Add `AGENTS.md` to your paper repo. Create a GitHub Release. Now any AI coding agent can represent your work.

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

## Installation (Other Platforms)

### Codex

Tell Codex:

```
Fetch and follow instructions from https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/refs/heads/main/.codex/INSTALL.md
```

### Other tools

Clone and point your tool at the `skills/` directory.

## Use a published paper

```bash
git clone https://github.com/author/their-paper.git
# Open in Claude Code, Codex, Cursor, etc. — agent reads AGENTS.md
```

## What's in this repo

- [PROTOCOL.md](PROTOCOL.md) — the spec
- [VISION.md](VISION.md) — ideas and future directions
- [skills/](skills/) — `/publish-paper` and `/load-paper-agent`
- [template/](template/) — starter `AGENTS.md` and `CLAUDE.md`

## License

Protocol: CC-BY-4.0 | Skills & templates: MIT
