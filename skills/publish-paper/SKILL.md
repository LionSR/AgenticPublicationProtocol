---
name: publish-paper
description: Orchestrate the publication of an academic paper as an AI agent following the Agentic Publication Protocol. This is the main skill — users invoke `/publish-paper` and this file dispatches to the detail files alongside it.
---

# Publish Paper as Agent

This skill produces an APP-compliant publication repo — the format defined in [PROTOCOL.md](../../PROTOCOL.md). This file is the **master**; the detail for each phase lives in sibling files that you read as you reach that phase.

**Scope.** APP publishes a paper that is already written. This skill does not help write the paper, run experiments, or produce results — those must already exist in the author's working repo.

## Sub-skills called

- `/extract-context` — pull research context from conversation history (optional, in phase 2).
- `/validate-publication` — automated quality checks (phases 3, 4, and 5).

## Files in this skill

| File | When to read it |
|------|-----------------|
| [`gather.md`](gather.md) | Phases 1–2: understand the repo, check for prior versions, interview the researcher, optionally extract context. |
| [`build.md`](build.md) | Phase 3: create the publication repo, copy and organize files, run structure validation, verify code. |
| [`draft.md`](draft.md) | Phase 4: draft `AGENTS.md` and `README.md`, iterate with the researcher, run agents-md validation. |
| [`release.md`](release.md) | Phases 5–6: final validation, walk the checklist, confirm, tag, push, record in `.publications.md`. |
| [`paper-types.md`](paper-types.md) | Format-specific guidance — theory-only, computational, experimental, notebook, video. Consult whenever you need to adapt to a non-default paper type. |

Read `SKILL.md` first. Open the phase file when you enter that phase — don't pre-load all of them.

## Roadmap

Show the researcher this roadmap at the start of the process:

```
PUBLICATION ROADMAP

  Phase 1 — Understand        [ ]  Read the repo, check for previous versions
  Phase 2 — Discuss           [ ]  Interview (up to 5 short rounds), extract context
  Phase 3 — Build             [ ]  Create repo, organize files, verify code
  Phase 4 — Draft             [ ]  AGENTS.md, iterate with you, README
  Phase 5 — Final review      [ ]  Walk through everything, validation sweep
  Phase 6 — Release           [ ]  Publish (with your explicit confirmation)

  This is a deliberate process — it can span multiple sessions.
  I'll update this checklist as we go.
```

For normal phase-to-phase transitions, a brief status line is enough: "Phase 3 complete. Moving to Phase 4 — Draft."

## Resuming a session

If the researcher has already begun, detect progress from the filesystem before continuing:

- No publication repo yet → start at Phase 1 (`gather.md`).
- Publication repo exists but has no `AGENTS.md` → resume in Phase 3 or its tail (`build.md`).
- `AGENTS.md` exists but no tagged release → resume in Phase 4 or 5 (`draft.md`/`release.md` depending on whether iteration with the researcher has happened).
- Tagged release exists → the publication is live; this run is a new version. `gather.md` picks it up from `.publications.md`.

## Cross-cutting principles

These apply across every phase. Keep them in mind while reading the phase files.

**Pace principle.** Never treat a partial answer as a complete one. If you asked three questions and the researcher answered one, follow up on the unanswered ones before moving on — they may have missed them, not declined them. When showing the researcher something for feedback (a draft, a file list, a checklist), wait for them to engage substantively. A one-word acknowledgement ("ok", "sure", "fine") after presenting five things to review is not confirmation — ask which specific items they've looked at. The researcher's attention is finite; work with that, not against it.

**Author's voice principle.** The supplementary materials (`authors-note.md`, `know-how.md`), the `AGENTS.md` paper summary, and any content that speaks for the researcher must reflect what *they* want to convey — not what the agent thinks is important. Before drafting, ask the researcher what they want the document to say and who the intended audience is. Draft from their intent, then iterate. Never generate these documents first and ask for approval after — that inverts the authorship.

**Structured questions.** When asking the researcher to make choices, use structured question tools if the platform supports them (e.g. `AskUserQuestion` in Claude Code). Present clear options rather than open-ended text prompts. This is faster and less ambiguous, and keeps the researcher's typing load low.

## Process

Work through the phases in order by reading the corresponding file when you reach that phase. Each phase file invokes `/validate-publication` at its own checkpoint. Do not duplicate phase content here — the phase files are the source of truth for their respective phases.

1. Read [`gather.md`](gather.md) → execute phases 1–2.
2. Read [`build.md`](build.md) → execute phase 3.
3. Read [`draft.md`](draft.md) → execute phase 4.
4. Read [`release.md`](release.md) → execute phases 5–6.

Consult [`paper-types.md`](paper-types.md) whenever the paper is not a standard LaTeX-plus-code computational paper.
