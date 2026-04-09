# Paper Publication Protocol (PPP)

**Version 0.1 — Draft**

## Abstract

The Paper Publication Protocol (PPP) defines a convention for publishing academic papers alongside AI agents that represent the work. A PPP-compliant repository contains the paper source, code, data, environment specification, and an `AGENTS.md` file that instructs any AI coding agent to act as a representative of the paper — explaining its content, reproducing its results, and interacting with other paper agents.

PPP is a **repo convention**, not a runtime protocol. It builds on two existing standards:
- **agents.md** (https://agents.md) — the cross-platform agent instruction format supported by 25+ tools
- **MCP** (https://modelcontextprotocol.io) — inspiration for structuring agent capabilities as tools/resources/prompts

## Motivation

Today, publishing a paper means uploading a PDF. Code and data, if shared at all, are often poorly documented and hard to reproduce. Readers spend hours understanding a paper's methods before they can build on it.

With AI coding agents becoming the primary interface for software development and research, we can do better. A published paper should come with an agent that:

1. **Explains** the paper's methods, results, and implications
2. **Reproduces** figures and experiments from the included code and data
3. **Interacts** with the reader's own agent, acting as a knowledgeable sub-agent
4. **Discusses** with other paper agents, enabling multi-agent research collaboration

PPP defines the minimal structure needed to make this work across any AI coding agent platform.

## Specification

### 1. Directory Structure

A PPP-compliant repository MUST contain the following structure. Items marked REQUIRED must exist; items marked OPTIONAL are encouraged.

```
my-paper/
│
├── AGENTS.md                     # REQUIRED — canonical agent definition
├── CLAUDE.md                     # REQUIRED — imports AGENTS.md for Claude Code
├── README.md                     # REQUIRED — human-readable overview
│
├── paper/                        # REQUIRED — paper source
│   ├── main.tex (or main.md)    #   primary source file
│   ├── figures/                  #   pre-built figure images
│   └── build/                   #   compiled output (paper.pdf)
│
├── code/                         # OPTIONAL — codebase
│   ├── README.md                #   entry points and usage
│   ├── src/                     #   source code
│   └── scripts/                 #   utility scripts
│       └── generate_figures.py  #   REQUIRED if code/ exists
│
├── data/                         # OPTIONAL — datasets
│   ├── README.md                #   provenance, format, size
│   └── ...                      #   small inline; large via LFS or links
│
├── environment/                  # REQUIRED — reproducibility
│   ├── requirements.txt         #   or environment.yml, package.json, etc.
│   └── platform.json            #   platform and compute metadata
│
└── skills/                       # OPTIONAL — agent capabilities
    └── [skill-name]/
        └── SKILL.md             #   skill definition
```

### 2. AGENTS.md

The `AGENTS.md` file is the **canonical source of truth** for the paper agent's instructions. It is the file that all agent platforms read.

Platform-specific files reference it:
- `CLAUDE.md` contains `@AGENTS.md` (Claude Code import syntax)
- Codex, Cursor, Copilot, Gemini, Devin, and 20+ other tools read `AGENTS.md` natively

#### Format

AGENTS.md uses standard Markdown with an optional YAML frontmatter block for machine-readable metadata:

```markdown
---
protocol: paper-publication-protocol
protocol_version: "0.1"
title: "Full Paper Title"
authors:
  - name: "Author Name"
    affiliation: "Institution"
arxiv_id: "XXXX.XXXXX"          # optional
doi: "10.XXXX/XXXXX"            # optional
published_date: "YYYY-MM-DD"
version: "1.0.0"                 # matches git tag
domain: "field-name"             # free-form
tags: ["keyword1", "keyword2"]   # free-form
---
```

The Markdown body MUST include these sections:

#### Identity and Role
Instructs the agent on what it represents and how to behave. The agent should:
- Ground responses in the paper's content, code, and data
- Distinguish between claims made in the paper and its own inferences
- Be honest about limitations and open questions
- Say clearly when a question is outside the paper's scope

#### Paper Summary
A 2-4 paragraph summary written by the authors. This is the agent's core knowledge.

#### Key Results
A numbered list of the paper's main findings, one sentence each.

#### Available Skills
Lists the skills the agent can perform, with paths to their SKILL.md files.

#### Computational Requirements
Documents what resources are needed for different tasks:
- **Light** tasks (plotting, simple analysis): any laptop
- **Medium** tasks: specify requirements
- **Heavy** tasks: specify requirements (GPU, cluster, estimated time)

**Critical rule**: The agent MUST inform the user before attempting any heavy computation. It must never silently hang on a long-running task.

#### Citation
BibTeX entry for citing the paper.

### 3. environment/platform.json

Machine-readable specification of the computational environment:

```json
{
  "os_tested": "macOS 14.2",
  "os_compatibility": ["macOS", "Linux"],
  "language": "python",
  "language_version": "3.11",
  "package_manager": "pip",
  "gpu_required": false,
  "heavy_computation": {
    "task_name": {
      "time": "estimated duration",
      "requires": "resource description"
    }
  }
}
```

### 4. Skills

Skills extend the agent's capabilities. Each skill is a folder under `skills/` containing a `SKILL.md` file.

#### SKILL.md Format

```markdown
---
name: skill-name
description: When and how to use this skill.
---

# Skill Title

[Instructions for the agent to follow when this skill is invoked.]
```

This follows the same format used by leanprover/skills and QuantumBFS/sci-brain — YAML frontmatter with `name` and `description`, followed by Markdown instructions.

#### Default Skills

PPP recommends these skills for most papers:

- **figure-generation**: Reproduce any figure from the paper using code + data
- **presentation**: Generate a slide deck summarizing the paper
- **explain**: Structured explanation of paper sections for interactive Q&A

Domain-specific skills can be added as needed (e.g., "run DFT calculation", "prove theorem", "train model").

### 5. Versioning

PPP uses git tags for versioning, following Semantic Versioning adapted for papers:

```
MAJOR.MINOR.PATCH

MAJOR: Paper revision (new results, changed conclusions)
MINOR: Improved agent, new skills, better documentation
PATCH: Bug fixes, dependency updates, typos
```

- The `version` field in AGENTS.md frontmatter MUST match the git tag
- GitHub Releases SHOULD be created for each version
- Readers clone a specific version: `git clone --branch v1.0.0 ...`

### 6. Loading a Paper Agent

A published paper agent can be used in several ways:

| Method | Description |
|--------|-------------|
| **Direct** | Clone the repo, open it in any coding agent. The agent reads AGENTS.md and represents the paper. |
| **Sub-agent** | Clone into a subfolder of your project. The agent platform detects the nested AGENTS.md. |
| **Import** | Add `@papers/their-paper/AGENTS.md` in your CLAUDE.md to inject the paper's context. |
| **Add directory** | `claude --add-dir ~/papers/their-paper` for Claude Code. |
| **Group** | Multiple paper repos as subfolders, with an orchestrator AGENTS.md. |

### 7. Publishing Checklist

Before releasing, verify:

**Structure:**
- [ ] AGENTS.md exists at root with valid YAML frontmatter
- [ ] CLAUDE.md exists and imports AGENTS.md
- [ ] README.md exists
- [ ] environment/ directory exists

**Paper:**
- [ ] Paper source in paper/
- [ ] Compiled PDF in paper/build/

**Environment:**
- [ ] Dependency file with pinned versions
- [ ] platform.json with OS/language/compute info

**Code (if code/ exists):**
- [ ] code/README.md with entry points
- [ ] No hardcoded absolute paths or secrets
- [ ] Figure generation scripts exist
- [ ] Figures reproducible from code + data

**Data (if data/ exists):**
- [ ] data/README.md with provenance
- [ ] Large files (>50MB) use Git LFS or external links

## Publishing Tools

The Paper Publication Protocol provides cross-platform skills to help researchers publish:

**Installation:**
```bash
# Claude Code
claude plugin marketplace add https://github.com/paper-protocol/skills.git
claude plugin install paper-protocol@paper-protocol

# Codex
git clone https://github.com/paper-protocol/skills.git ~/.codex/paper-protocol
ln -s ~/.codex/paper-protocol/skills/* ~/.agents/skills/

# Gemini CLI
gemini skills install https://github.com/paper-protocol/skills --path skills

# Any other tool
git clone https://github.com/paper-protocol/skills.git
# Point your tool at the skills/ directory
```

**Available skills:**
- `/publish-paper` — Interactive workflow to prepare and publish a paper agent
- `/load-paper-agent` — Load a published paper as a sub-agent in your project

## Future Directions

- **Multi-agent discussion**: Paper agents communicating via Slack channels or orchestrators
- **Research group agents**: A meta-agent representing a group's full body of work
- **MCP integration**: Paper agents exposable as MCP servers for runtime tool access
- **Benchmark integration**: Published agents usable as benchmarks (cf. Terminal Bench Science)
- **Automated review**: Agents that validate each other's claims

## License

This protocol specification is released under CC-BY-4.0.
