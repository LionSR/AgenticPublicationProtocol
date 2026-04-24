---
name: publish-paper
description: Orchestrate the publication of an academic paper as an AI agent following the Agentic Publication Protocol. This is the main skill — users invoke /publish-paper and this file dispatches to the phase files and templates alongside it.
---

# Publish Paper as Agent — Orchestrator

This skill produces an APP-compliant publication repo — the format defined in [`PROTOCOL.md`](../../PROTOCOL.md). It is a **four-phase orchestrator**: the agent reads this file first to understand the flow, the cross-cutting principles, and the available templates and sub-skills; then it opens each phase file in turn to execute.

**Scope.** APP publishes a paper that is already written. This skill does not help write the paper, run experiments, or produce results — those must already exist in the author's working repo before the skill is useful.

## Orchestration model

The work happens in the **phase files** — `gather.md`, `build.md`, `draft.md`, `release.md`. This `SKILL.md` does **not** duplicate their content. What lives here instead:

- The roadmap the researcher sees at the start.
- The cross-cutting principles (pace, author's voice, structured questions) that apply to every phase.
- The input/output contract for each phase — enough to know which phase you're in, whether you can skip ahead on resume, and what state each phase leaves behind.
- The list of templates and sub-skills the phase files draw on.

Read this file in full at the start. Open each phase file only when you reach that phase — they are intentionally scoped to one step at a time.

## Phase files (read in order)

### [`gather.md`](gather.md) — Phases 1–2

- **Purpose.** Understand the working repo. Interview the researcher. Optionally extract research context from conversation history.
- **Assumes.** Invoked in the researcher's working repo. The publication repo does not exist yet.
- **Produces.** A publication plan: the canonical paper document and its format; the key results in the researcher's words; the include / exclude / defer file list; the publication repo name; optional extracted research context; previous-version info if any.
- **Sub-skills called.** `/extract-context` (optional).
- **Interaction load.** Heavy — up to five short interview rounds with the researcher.

### [`build.md`](build.md) — Phase 3

- **Purpose.** Create the publication repo. Copy and organize the approved files. Run structure validation. Verify the code runs with the new paths.
- **Assumes.** Publication plan from `gather.md`.
- **Produces.** A working publication repo with files in the layout defined by [`PROTOCOL.md` § Repository layout](../../PROTOCOL.md#repository-layout); `.gitignore` in place; supplementary materials copied including `supplementary/checklist.md`; code verified to run.
- **Sub-skills called.** `/validate-publication --stage structure`.
- **Templates used.** [`template/publication-checklist.md`](../../template/publication-checklist.md).
- **Interaction load.** Light — confirmation on the file list before copying, then mostly automated.

### [`draft.md`](draft.md) — Phase 4

- **Purpose.** Draft `AGENTS.md` and `README.md`. Iterate with the researcher until they agree the agent represents their intent, not just their words.
- **Assumes.** Publication repo with organized files and verified code from `build.md`.
- **Produces.** `AGENTS.md` (per the schema in [`PROTOCOL.md` § AGENTS.md](../../PROTOCOL.md#agentsmd)), `CLAUDE.md` (`@AGENTS.md`), and `README.md` — all approved by the researcher.
- **Sub-skills called.** `/validate-publication --stage agents-md`.
- **Templates used.** [`template/AGENTS.md`](../../template/AGENTS.md), [`template/CLAUDE.md`](../../template/CLAUDE.md).
- **Interaction load.** Heavy — walk the researcher through `AGENTS.md` one section at a time and revise until intent matches.

### [`release.md`](release.md) — Phases 5–6

- **Purpose.** Full validation sweep, checklist walk-through, commit, tag, push, GitHub release, record in `.publications.md`. **Point of no return** — once pushed, the publication is public.
- **Assumes.** Drafts approved from `draft.md`.
- **Produces.** A tagged public release on GitHub. Working repo's `.publications.md` updated with the new release.
- **Sub-skills called.** `/validate-publication --stage full`.
- **Templates used.** [`template/publications.md`](../../template/publications.md).
- **Interaction load.** Heavy — per-action confirmation required for every remote operation (create repo, push, create release).

### [`paper-types.md`](paper-types.md) — appendix

Not a workflow step. Format-specific guidance for theory-only, computational, experimental, notebook, and video/slideware papers. Phase files link to it when they need to adapt; consult it yourself whenever the paper is not a default LaTeX-plus-code computational paper.

## Templates

Four files ship in `template/` at the repo root. Phase files copy or adapt them at the right moment — do not re-author these artifacts; start from the template.

| Template | Adapted by | Lands as |
|----------|------------|----------|
| [`template/AGENTS.md`](../../template/AGENTS.md) | `draft.md` (phase 4) | `<publication-repo>/AGENTS.md`, populated and researcher-approved. |
| [`template/CLAUDE.md`](../../template/CLAUDE.md) | `draft.md` (phase 4) | `<publication-repo>/CLAUDE.md` — one line: `@AGENTS.md`. |
| [`template/publication-checklist.md`](../../template/publication-checklist.md) | `build.md` (phase 3) | `<publication-repo>/supplementary/checklist.md`, adapted (irrelevant sections removed). |
| [`template/publications.md`](../../template/publications.md) | `release.md` (phase 6) | `<working-repo>/.publications.md` — a table of this working repo's publications. |

## Sub-skills

Separate skills that phase files invoke. Read the linked SKILL.md if the phase-file summary is not enough.

- [`/extract-context`](../extract-context/SKILL.md) — pull research context from local Claude Code / Codex session history (called in phase 2).
- [`/validate-publication`](../validate-publication/SKILL.md) — automated quality checks at each phase's checkpoint (`--stage structure`, `--stage agents-md`, `--stage full`).

## Roadmap to show the researcher

Show this at the very start of the process:

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

For phase-to-phase transitions after the start, a brief status line is enough: "Phase 3 complete. Moving to Phase 4 — Draft."

## Resuming a session

If the researcher has already begun, detect progress from the filesystem before dispatching. Use the phase-file "Assumes/Produces" contracts above to decide where to resume:

- No publication repo yet → start at `gather.md`.
- Publication repo exists but no `AGENTS.md` → resume in `build.md` (or its tail if the structure is already valid).
- `AGENTS.md` exists but no tagged release → resume in `draft.md` or `release.md`, depending on whether iteration with the researcher has happened.
- Tagged release exists → the publication is live. This run is a new version; `gather.md` picks it up from `.publications.md`.

## Cross-cutting principles

These apply across every phase. Keep them in mind as you read each phase file.

**Pace.** Never treat a partial answer as a complete one. If you asked three questions and the researcher answered one, follow up on the unanswered ones before moving on — they may have missed them, not declined them. When showing the researcher something for feedback (a draft, a file list, a checklist), wait for them to engage substantively. A one-word acknowledgement ("ok", "sure", "fine") after presenting five things to review is not confirmation — ask which specific items they've looked at. The researcher's attention is finite; work with that, not against it.

**Author's voice.** The supplementary materials (`authors-note.md`, `know-how.md`), the `AGENTS.md` paper summary, and any content that speaks for the researcher must reflect what *they* want to convey — not what the agent thinks is important. Before drafting, ask the researcher what they want the document to say and who the intended audience is. Draft from their intent, then iterate. Never generate these documents first and ask for approval after — that inverts the authorship.

**Structured questions.** When asking the researcher to make choices, use structured question tools if the platform supports them (e.g. `AskUserQuestion` in Claude Code). Present clear options rather than open-ended text prompts. This is faster and less ambiguous, and keeps the researcher's typing load low.
