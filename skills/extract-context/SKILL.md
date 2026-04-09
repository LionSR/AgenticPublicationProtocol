---
name: extract-context
description: Extract research context from Claude Code or Codex conversation history. Use when a researcher wants to capture the reasoning behind their work — key decisions, methodology choices, debugging insights — from their actual sessions. Can be used standalone or as part of /publish-paper.
---

# Extract Research Context

Extract and curate conversation history from Claude Code or Codex sessions into structured research context that can be published alongside a paper.

## When to use

- During `/publish-paper` when the researcher wants to include research context — run this in the **working repo** (where the sessions are), then copy output to the publication repo
- Standalone when a researcher wants to document their reasoning process
- When preparing supplementary material for a paper

## Process

### 1. List available sessions

Ask the researcher which platform they used: Claude Code or Codex.

First, find the extraction script (it's bundled with the plugin):
```bash
EXTRACT_SCRIPT=$(find ~/.claude/plugins -name extract_sessions.py 2>/dev/null | head -1)
```

If not found (e.g. running outside Claude Code), the script can be fetched:
```bash
curl -sO https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/main/skills/extract-context/scripts/extract_sessions.py
EXTRACT_SCRIPT=./extract_sessions.py
```

Then list sessions:
```bash
# Claude Code — sessions for the current project
python "$EXTRACT_SCRIPT" list --source claude

# Claude Code — all projects
python "$EXTRACT_SCRIPT" list --source claude --project all

# Codex
python "$EXTRACT_SCRIPT" list --source codex
```

Show the session list to the researcher. Each entry shows a timestamp, session ID, and a preview of the first user message.

### 2. Select relevant sessions

Ask the researcher which sessions relate to this paper/project. They may:
- Pick specific sessions by number
- Select all sessions from a time range
- Select sessions matching a keyword (you can grep session previews)

### 3. Extract selected sessions

For each selected session, extract it to JSON:

```bash
python "$EXTRACT_SCRIPT" extract --source claude --session <id>
```

This outputs structured JSON with normalized user/assistant turns, system tags stripped.

### 4. Choose the output level

Offer three levels:

**Gist** — Distill all selected sessions into a single `context/research-notes.md`:

```markdown
# Research Notes

## Methodology decisions
- [Why we chose approach X over Y — from session Z]
- [What didn't work and why]

## Key insights during development
- [Insight 1]
- [Insight 2]

## Known limitations and future ideas
- [Limitation the researcher is aware of]
- [Idea that didn't make it into the paper]
```

Read through each extracted session. Pull out key decisions, methodology choices, dead ends, and insights. Organize by theme, not by session. The researcher reviews and edits before publishing.

**Cleaned history** — Convert each session into structured markdown in `context/sessions/`:

```markdown
# Session: [descriptive title]

Date: YYYY-MM-DD
Topic: [what this session was about]

## Key decisions
- [Decision 1 — what was decided and why]
- [Decision 2]

## Conversation

**Researcher:** [cleaned-up message — fix typos, remove tangents, keep substance]

**Agent:** [summarized response — keep the key information, trim verbose output]

**Researcher:** [next message]

...
```

Guide the researcher through each session:
- Show them the raw conversation
- Help them decide: keep, summarize, or skip each exchange
- Remove private content (API keys, personal info, unrelated tangents)
- Clean up messages for readability while preserving the reasoning
- Summarize long agent responses to their key points
- Add a "Key decisions" header at the top summarizing what came out of it

**Full history** — Export sessions with minimal processing. Still convert from JSON to readable markdown, but don't heavily edit. Just strip system tags and format readably.

### 5. Researcher review

Always show the final output to the researcher before it's committed. They may want to:
- Remove additional private content
- Rephrase things for clarity
- Add context that wasn't in the conversation
- Delete entire sessions they changed their mind about

Nothing goes into `context/` without researcher approval.

### 6. Wire into AGENTS.md

If being used as part of `/publish-paper`, add to the paper's AGENTS.md:

```markdown
## Research Context
For the reasoning behind key decisions, see `context/research-notes.md`
For conversation sessions from the research process, see `context/sessions/`
```

If used standalone, tell the researcher where the files were saved and suggest they reference them from their AGENTS.md or README.
