---
name: extract-chat-context
description: Extract publication-safe research context from Claude Code or Codex chat/session history and prepare it as supplementary material. Use when a researcher wants to capture the reasoning behind their work — key decisions, methodology choices, debugging insights — from their actual sessions. Can be used standalone or as part of /publish-paper.
---

# Extract Chat Context

Extract and curate conversation history from Claude Code or Codex sessions into structured research context that can be published as supplementary material alongside a paper.

## When to use

- During `/publish-paper` when the researcher wants to include research context — run this in the **working repo** (where the sessions are), then copy approved output to `publication-staging/`
- Standalone when a researcher wants to document their reasoning process
- When preparing supplementary material for a paper

## Parallelism

When there are many sessions, parallelize the work. Launch subagents to extract and summarize batches of sessions concurrently rather than processing them one by one. For example, with 12 sessions, launch 3-4 subagents each handling a batch, then merge their summaries into the final `know-how.md`. This applies to both extraction (step 2) and summarization (step 3).

## Process

### 1. Gather all sessions

**Pick the platform.** This skill reads history from both Claude Code and Codex. Ask the researcher which they used. If they are unsure, check which store exists and is non-empty — and note the research may have happened in a different tool than the one now running this skill, so check both:

```bash
ls ~/.claude/projects   # Claude Code — one directory per project
ls ~/.codex/sessions    # Codex — dated subfolders (presence means history exists)
```

> **Version caveat.** These store locations and their JSONL layouts are
> internal to Claude Code and the Codex CLI, not stable APIs; this skill and
> `extract_sessions.py` track the formats current as of mid-2026. If a newer
> tool version has moved or reshaped its session store (empty listings,
> parse errors on files that clearly exist), inspect the store layout
> directly and adapt — and update this skill and the script.

This is just a quick existence check; the `list` command below is what actually shows the sessions. Use the chosen platform as `<source>` (`claude` or `codex`) in every command below, and keep the same source for listing and extracting.

**Find the extraction script.** It ships with the plugin, so search wherever the host installed it — under Claude Code or Codex:
```bash
EXTRACT_SCRIPT=$(find ~/.claude/plugins ~/.codex/plugins -name extract_sessions.py 2>/dev/null | head -1)
```

If it is not in either root (e.g. a manual or dev checkout), download it:
```bash
curl -sO https://raw.githubusercontent.com/LionSR/AgenticPublicationProtocol/main/skills/extract-chat-context/scripts/extract_sessions.py
EXTRACT_SCRIPT=./extract_sessions.py
```

**List the sessions.** By default the list is scoped to the **current working directory**, so run this skill from the working repo where the research happened:
```bash
python "$EXTRACT_SCRIPT" list --source <source>                # this repo's sessions
python "$EXTRACT_SCRIPT" list --source <source> --project all  # every session on the machine
python "$EXTRACT_SCRIPT" list --source <source> --project <id> # a specific repo (Codex: a path; Claude: a dash-key)
```

Each row is `timestamp | session_id | preview`; Codex adds the directory **name** (basename) the session ran in after the timestamp. Use the timestamp, the directory name, and the first-message preview to confirm each session belongs to this paper — and when two repos share a basename, lean on the timestamp and preview to tell them apart.

**Finding the right history** when scoping is unclear or you are not in the original repo (a fresh clone, `publication-staging/`, or a moved directory):
- **Claude Code** keys each project by its working-directory path with `/` replaced by `-`. The default list shows only the current repo; use `--project all`, or `--project <key>` (the dash-encoded path, e.g. `-Users-me-old-repo`) for the original path.
- **Codex** keeps all sessions in one store, tagged with the directory each ran in. The default filters to the current directory; if that comes back empty the script says to retry with `--project all` (then pick by directory + timestamp + preview) or `--project <path>` (a real filesystem path). Archived sessions are not listed by default — add `--sessions-root ~/.codex/archived_sessions` to reach them.

Show the session list to the researcher. **By default, include every session the list shows for this repo.** Narrow only if the researcher asks to exclude specific ones or some are clearly unrelated. On Codex, where sessions from all repos share one store, first confirm the listed directory names match this research before including them.

### 2. Extract sessions

Extract all included sessions to JSON (use the same `<source>` you listed with; parallelize across batches if many):

```bash
python "$EXTRACT_SCRIPT" extract --source <source> --session <id>
```

Outputs structured JSON with normalized user/assistant turns, system tags stripped.

### 3. Produce the summary (default output)

Before drafting, ask the researcher: "What kind of behind-the-scenes knowledge do you want readers to have? What decisions, dead ends, or insights matter most?" Their answer guides what to emphasize — the know-how should reflect what the author considers important, not just everything the agent can find in the sessions.

Then distill all sessions into a single `supplementary/know-how.md` — a thematic summary of the reasoning behind the work. Read through every extracted session, pull out key decisions, methodology choices, dead ends, and insights that align with the researcher's stated intent. Organize by theme, not by session. See `session-formats.md` for the know-how template.

Show the draft to the researcher before finalizing — this document speaks for them.

### 4. Consider extractable skills

While reading the sessions, watch for recurring procedures a reader or agent
might want to rerun — a parameter-sweep recipe, a data-preparation pipeline,
a diagnostic check, a figure-regeneration workflow. These can become Agent
Skills ([agentskills.io](https://agentskills.io)) instead of, or in addition
to, prose in `know-how.md`:

- **Paper-specific** procedures (running the paper's method, regenerating a
  class of results) → propose bundling as `skills/<name>/SKILL.md` in the
  publication repo, per the `skills/` section of PROTOCOL.md.
- **Reusable across papers** (a general workflow or tool recipe) → propose
  publishing it externally and referencing it from the
  `recommended_external_skills` frontmatter field.

Suggest candidates to the researcher with a one-line purpose each, and draft
a `SKILL.md` (frontmatter `name` and `description`, step-by-step body) only
for the ones they approve. A skill must encode a procedure the sessions
actually validated — do not invent capabilities the research never
exercised.

### 5. Ask about publishing more detail

After showing the summary, ask the researcher if they also want to publish more detailed session records:

- **Summary only** (default) — publish just `supplementary/know-how.md`. Fastest option; captures the key reasoning. Best for most papers.
- **Summary + cleaned sessions** — also publish curated session transcripts in `supplementary/sessions/`. Choose this when the research process itself is part of the contribution (e.g., novel methodology development).
- **Summary + full history** — also publish lightly processed transcripts. Choose this when full transparency is the goal (e.g., reproducibility-focused publications).

For cleaned and full session formatting, see `session-formats.md`.

### 6. Confidentiality and privacy screening

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

### 7. Researcher review

Show the final output to the researcher before it's committed. They may want to remove content, rephrase for clarity, add context that wasn't in the conversation, or delete entire sessions. Nothing goes into `supplementary/` without researcher approval.

### 8. Wire into AGENTS.md and supplementary doc

The research context appears in two places:

**In AGENTS.md** — a brief pointer:

```markdown
## Supplementary Materials
Practical knowledge and methodology insights are documented in [`supplementary/know-how.md`](supplementary/know-how.md).
```

If session transcripts were also published, add a link to `supplementary/sessions/`.
If skills were bundled (step 4), list each under the optional Skills section
of AGENTS.md with a one-line description.

**In `supplementary/know-how.md`** — the full thematic summary from step 3. This is what the agent reads when asked "why did you do X?"

The separation is intentional: AGENTS.md stays concise and navigable; the detailed reasoning lives in its own document.

If used standalone (not as part of `/publish-paper`), tell the researcher where the files were saved and suggest they add the AGENTS.md reference themselves.
