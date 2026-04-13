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

## Parallelism

When there are many sessions, parallelize the work. Launch subagents to extract and summarize batches of sessions concurrently rather than processing them one by one. For example, with 12 sessions, launch 3-4 subagents each handling a batch, then merge their summaries into the final `know-how.md`. This applies to both extraction (step 2) and summarization (step 3).

## Process

### 1. Gather all sessions

Ask the researcher which platform they used: Claude Code or Codex.

Find the extraction script (bundled with the plugin):
```bash
EXTRACT_SCRIPT=$(find ~/.claude/plugins -name extract_sessions.py 2>/dev/null | head -1)
```

If not found (e.g. running outside Claude Code):
```bash
curl -sO https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/main/skills/extract-context/scripts/extract_sessions.py
EXTRACT_SCRIPT=./extract_sessions.py
```

List all sessions for the project:
```bash
python "$EXTRACT_SCRIPT" list --source claude        # current project
python "$EXTRACT_SCRIPT" list --source claude --project all  # all projects (if needed)
python "$EXTRACT_SCRIPT" list --source codex          # Codex
```

Show the session list to the researcher. **By default, include all sessions for the project.** Only narrow the selection if the researcher asks to exclude specific ones or there are clearly unrelated sessions.

### 2. Extract sessions

Extract all included sessions to JSON (parallelize across batches if many):

```bash
python "$EXTRACT_SCRIPT" extract --source claude --session <id>
```

Outputs structured JSON with normalized user/assistant turns, system tags stripped.

### 3. Produce the summary (default output)

Before drafting, ask the researcher: "What kind of behind-the-scenes knowledge do you want readers to have? What decisions, dead ends, or insights matter most?" Their answer guides what to emphasize — the know-how should reflect what the author considers important, not just everything the agent can find in the sessions.

Then distill all sessions into a single `supplementary/know-how.md` — a thematic summary of the reasoning behind the work. Read through every extracted session, pull out key decisions, methodology choices, dead ends, and insights that align with the researcher's stated intent. Organize by theme, not by session. See `session-formats.md` for the know-how template.

Show the draft to the researcher before finalizing — this document speaks for them.

### 4. Ask about publishing more detail

After showing the summary, ask the researcher if they also want to publish more detailed session records:

- **Summary only** (default) — publish just `supplementary/know-how.md`. Fastest option; captures the key reasoning. Best for most papers.
- **Summary + cleaned sessions** — also publish curated session transcripts in `supplementary/sessions/`. Choose this when the research process itself is part of the contribution (e.g., novel methodology development).
- **Summary + full history** — also publish lightly processed transcripts. Choose this when full transparency is the goal (e.g., reproducibility-focused publications).

For cleaned and full session formatting, see `session-formats.md`.

### 5. Confidentiality and privacy screening

**Mandatory before anything is published.** Scan all output files for content that should not be made public.

**Quick checklist — flag these patterns:**
- Credentials: API keys (`sk-...`, `ghp_...`), tokens, passwords, connection strings
- Personal info: email addresses, phone numbers, names of non-authors
- Private infrastructure: internal URLs, file paths like `/Users/name/...`, private repo references
- Access-controlled data: dataset identifiers, license keys
- Tone: profanity, negative comments about people/institutions, off-topic tangents

For each flagged item, present the researcher with the exact text and suggest: **redact**, **keep**, or **rephrase**.

See `confidentiality-checklist.md` for the extended reference with full pattern details and procedure.

Report every flagged item to the researcher. Do not silently remove content. Err on the side of over-flagging. After the researcher resolves all flags, do a final pass to confirm nothing was missed.

### 6. Researcher review

Show the final output to the researcher before it's committed. They may want to remove content, rephrase for clarity, add context that wasn't in the conversation, or delete entire sessions. Nothing goes into `supplementary/` without researcher approval.

### 7. Wire into AGENTS.md and supplementary doc

The research context appears in two places:

**In AGENTS.md** — a brief pointer:

```markdown
## Supplementary Materials
Practical knowledge and methodology insights are documented in [`supplementary/know-how.md`](supplementary/know-how.md).
```

If session transcripts were also published, add a link to `supplementary/sessions/`.

**In `supplementary/know-how.md`** — the full thematic summary from step 3. This is what the agent reads when asked "why did you do X?"

The separation is intentional: AGENTS.md stays concise and navigable; the detailed reasoning lives in its own document.

If used standalone (not as part of `/publish-paper`), tell the researcher where the files were saved and suggest they add the AGENTS.md reference themselves.
