---
name: load-paper-agent
description: Use when you want to load a published paper agent as a sub-agent in your current project. Clones the paper repo and sets up the agent for consultation.
---

# Load Paper Agent

Load a PPP-published paper as a sub-agent in your current project.

## Usage

The user says something like:
- "Load paper agent from https://github.com/user/paper-repo"
- "Add this paper as a sub-agent: <url>"
- "I want to consult the paper at <url>"

## Steps

### 1. Clone the Paper

```bash
mkdir -p papers/
git clone <url> papers/<repo-name>
# Or for a specific version:
git clone --branch v1.0.0 <url> papers/<repo-name>
```

### 2. Verify PPP Compliance

Read `papers/<repo-name>/AGENTS.md` and check:
- Does it have YAML frontmatter with `protocol: paper-publication-protocol`?
- Does it have the required sections (Identity, Summary, Key Results)?

If not PPP-compliant, inform the user. The repo can still be used — read whatever AGENTS.md or README.md exists.

### 3. Report Capabilities

Tell the user:
- Paper title and authors (from frontmatter)
- Available skills (from Available Skills section)
- Computational requirements (from that section)

### 4. Use as Sub-Agent

The paper agent is now available. When the user asks questions about this paper:
1. Read the paper agent's AGENTS.md for context
2. Read relevant files from the paper's directory (paper/, code/, data/)
3. Follow the skills defined in the paper's skills/ directory
4. Attribute information to the paper (e.g., "According to [Paper Title]...")

### 5. Cross-Paper Interaction

If multiple paper agents are loaded in `papers/`:
- The user can ask to compare findings across papers
- Each paper agent's AGENTS.md defines its perspective
- Clearly attribute which claims come from which paper
