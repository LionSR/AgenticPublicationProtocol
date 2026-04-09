# Agentic Publication Protocol (APP)

**Publish papers as AI agents.**

Add `AGENTS.md` to your paper repo. Create a GitHub Release. Now any AI coding agent can represent your work.

## Publish your paper

Install the `/publish-paper` skill — it walks you through everything interactively:

```bash
# Claude Code
claude plugin marketplace add https://github.com/LionSR/PaperProtocol.git
claude plugin install paper-protocol@paper-protocol

# Codex
git clone https://github.com/LionSR/PaperProtocol.git ~/.codex/paper-protocol
ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.agents/skills/publish-paper

# Other tools — clone and point at skills/
```

Then run `/publish-paper` in your coding agent.

## Use a published paper

```bash
git clone https://github.com/author/their-paper.git
# Open in Claude Code, Codex, Cursor, etc. — agent reads AGENTS.md
```

## What's in this repo

- [PROTOCOL.md](PROTOCOL.md) — the spec
- [skills/](skills/) — `/publish-paper` and `/load-paper-agent`
- [template/](template/) — starter `AGENTS.md` and `CLAUDE.md`

## License

Protocol: CC-BY-4.0 | Skills & templates: MIT
