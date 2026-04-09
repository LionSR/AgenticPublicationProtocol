# YOUR PAPER TITLE

**Paper Publication Protocol v0.1**

> One-sentence summary of the paper.

## Authors

- Author One (Institution)
- Author Two (Institution)

## Links

- [Paper PDF](paper/build/paper.pdf)
- [arXiv](https://arxiv.org/abs/XXXX.XXXXX)

## Quick Start

### As a Human Reader

1. Read the paper: `paper/build/paper.pdf`
2. Explore the code: `code/README.md`
3. Browse the data: `data/README.md`

### As an AI Agent

1. Clone this repository
2. The `AGENTS.md` file defines the paper agent — any compatible coding agent will read it automatically
3. Install dependencies: see `environment/`

### Load as Sub-Agent in Your Project

```bash
# Clone into your project
git clone https://github.com/YOUR/REPO.git papers/paper-name

# In Claude Code, add to your CLAUDE.md:
# @papers/paper-name/AGENTS.md
```

## Repository Structure

| Path | Description |
|------|-------------|
| `AGENTS.md` | Agent instructions — the "brain" of this publication |
| `paper/` | LaTeX source and compiled PDF |
| `code/` | Implementation code |
| `data/` | Datasets |
| `environment/` | Dependencies and platform requirements |
| `skills/` | Agent capabilities |

## Environment

- **Platform**: <!-- macOS / Linux / Windows -->
- **Language**: <!-- Python 3.11+ / etc. -->
- **Key dependencies**: <!-- list 3-5 -->
- **Compute**: <!-- "Laptop sufficient for figures; GPU needed for full experiments" -->

## Agent Capabilities

This publication includes an AI agent that can:

- [ ] Explain the paper's content and methodology
- [ ] Reproduce figures from code + data
- [ ] Generate presentation slides
- [ ] <!-- domain-specific capability -->

## Versioning

- `v1.0.0` — Initial publication (YYYY-MM-DD)

## License

<!-- Your license -->
