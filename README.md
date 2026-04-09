# Agentic Publication Protocol (APP)

**Publish papers as AI agents.**

Add `AGENTS.md` to your paper repo. Tag a release. Now any AI coding agent can represent your work.

## Quick Start

### Publish your paper

1. Add `AGENTS.md` to your paper repo (see [template](template/AGENTS.md))
2. Add `CLAUDE.md` containing `@AGENTS.md`
3. `git tag -a v1.0.0 -m "Paper agent v1.0.0" && git push --tags`

Or install the `/publish-paper` skill for an interactive assistant:

```bash
# Claude Code
claude plugin marketplace add https://github.com/LionSR/PaperProtocol.git
claude plugin install paper-protocol@paper-protocol

# Codex
git clone https://github.com/LionSR/PaperProtocol.git ~/.codex/paper-protocol
ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.agents/skills/publish-paper

# Other tools — clone and point at skills/
```

### Use a published paper

```bash
git clone --branch v1.0.0 https://github.com/author/their-paper.git
# Open in Claude Code, Codex, Cursor, etc. — agent reads AGENTS.md
```

## What's in this repo

- [PROTOCOL.md](PROTOCOL.md) — the spec
- [skills/](skills/) — publishing skills (`/publish-paper`, `/load-paper-agent`)
- [template/](template/) — starter files for a new publication
- [.claude-plugin/](.claude-plugin/) + [.codex/](.codex/) — cross-platform install metadata

## License

Protocol: CC-BY-4.0 | Skills & templates: MIT
