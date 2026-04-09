# Paper Publication Protocol (PPP)

**Publish papers as AI agents.**

When you publish a paper, also publish an agent that can explain it, reproduce its results, and discuss with other paper agents.

## What is PPP?

PPP is a **repo convention** — a standard way to structure a paper repository so that any AI coding agent (Claude Code, Codex, Cursor, Copilot, Gemini, Devin, etc.) can read it and act as a representative of the paper.

It builds on:
- [**agents.md**](https://agents.md) — the cross-platform agent instruction standard (25+ tools)
- [**MCP**](https://modelcontextprotocol.io) — inspiration for structuring agent capabilities

## How It Works

### For Authors: Publish

Install the publishing skill, then run `/publish-paper` in your coding agent:

```bash
# Claude Code
claude plugin marketplace add https://github.com/paper-protocol/skills.git
claude plugin install paper-protocol@paper-protocol

# Codex
git clone https://github.com/paper-protocol/skills.git ~/.codex/paper-protocol
ln -s ~/.codex/paper-protocol/skills/* ~/.agents/skills/

# Gemini CLI
gemini skills install https://github.com/paper-protocol/skills --path skills
```

The skill guides you through:
1. Organizing your repo (paper/, code/, data/, environment/)
2. Creating `AGENTS.md` — the agent definition
3. Running the publishing checklist
4. Tagging a release

### For Readers: Use

Clone any PPP paper and open it in your coding agent:

```bash
git clone https://github.com/author/their-paper.git
cd their-paper
# Open in Claude Code, Codex, Cursor, etc.
# The agent reads AGENTS.md and represents the paper
```

Or load it as a sub-agent in your own project:

```bash
git clone https://github.com/author/their-paper.git papers/their-paper
# The paper agent is now available as a sub-agent
```

## Repository Structure (Published Paper)

```
my-paper/
├── AGENTS.md              # Agent definition (source of truth)
├── CLAUDE.md              # @AGENTS.md import for Claude Code
├── README.md              # Human-readable overview
├── paper/                 # Paper source + PDF
├── code/                  # Implementation
├── data/                  # Datasets
├── environment/           # Dependencies + platform.json
└── skills/                # Agent capabilities
    ├── figure-generation/
    └── presentation/
```

## This Repository

```
PaperProtocol/
├── PROTOCOL.md            # The formal protocol specification
├── README.md              # This file
├── skills/                # Cross-platform skills for publishing
│   ├── publish-paper/     # /publish-paper skill
│   └── load-paper-agent/  # /load-paper-agent skill
├── template/              # Starter template for a new publication
├── .claude-plugin/        # Claude Code marketplace metadata
└── .codex/                # Codex installation instructions
```

## Protocol Specification

See [PROTOCOL.md](PROTOCOL.md) for the full specification.

## License

Protocol specification: CC-BY-4.0
Skills and templates: MIT
