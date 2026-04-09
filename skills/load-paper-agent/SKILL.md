---
name: load-paper-agent
description: Use when you want to load a published paper agent into your current project as a sub-agent.
---

# Load Paper Agent

## Usage
User says: "Load paper agent from <github-url>"

## Steps

1. `git clone <url> papers/<repo-name>` (use `--branch <tag>` for a specific version)
2. Read `papers/<repo-name>/AGENTS.md` — report title, authors, and what the agent can do
3. When the user asks about the paper, read its AGENTS.md and work within its directory
4. Attribute information to the paper: "According to [Paper Title]..."
