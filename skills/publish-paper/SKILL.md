---
name: publish-paper
description: Orchestrate preparation, validation, and release of an academic paper as an AI agent following the Agentic Publication Protocol. Users invoke /publish-paper; this file dispatches to the phase files and templates alongside it.
---

# Publish Paper as Agent — Orchestrator

This skill prepares an APP-structured candidate release tree in `publication-staging/`, validates it as if it were the root of the future public repository, and then either publishes that validated tree with a verifiable APP manifest or records a developer-sandbox outcome.

**Scope.** APP publishes a paper that is already written. This skill does not help write the paper, run experiments, or produce results — those must already exist in the author's working repo before the skill is useful.

**Core object.** `publication-staging/` is the clean candidate release tree inside the private working repo. The agent may use the full working repo as context while preparing it, but the candidate must be self-contained: an outside agent should be able to enter `publication-staging/` and interact with it as the root of the eventual APP publication.

**Modes.** Phases 1-5 are mode-neutral. The only workflow branch is the final outcome:

- **Real publication mode** (default): promote the validated `publication-staging/` tree to a public publication repo, tag/version it, create `APP_PUBLICATION.json`, and record the public URL, tag, commit/tree hash, and `app_publication_id`.
- **Developer sandbox mode** (`--mode dev-sandbox`): exercise the same prepare and validate standards against an explicit sandbox target, then record an implementation test result. Do not create a public repo and do not write APP compliance records.

## Roadmap to show the researcher

Show this at the very start of the process:

```
PUBLICATION ROADMAP

  Phase 1 — Understand        [ ]  Read the repo, check previous versions or staging
  Phase 2 — Discuss           [ ]  Interview (up to 5 short rounds), extract chat context
  Phase 3 — Build staging     [ ]  Create/revise publication-staging/, organize files, verify code
  Phase 4 — Paper-agent docs  [ ]  AGENTS.md, iterate with you, README
  Phase 5 — Final review      [ ]  Validate staging, test paper-agent, freeze tree
  Phase 6 — Final outcome     [ ]  Publish publicly, or record dev-sandbox result

  This is a deliberate process — it can span multiple sessions.
  I'll keep this phase checklist updated in chat as we go. It is an internal
  process tracker, not a file to include in the publication.
```

For phase-to-phase transitions after the start, a brief status line is enough: "Phase 3 complete. Moving to Phase 4 — Paper-agent docs."

## Cross-cutting principles

These apply across every phase. Keep them in mind as you read each phase file.

**Staging root discipline.** In phases 3-5, run validation, path checks, paper compilation, figure reproduction, and paper-agent smoke testing with `publication-staging/` as the effective repository root. Paths in `AGENTS.md`, `README.md`, skills, commands, and supplementary materials must be relative to that root, not to the private parent repo.

**Publication invariants.**

- `publication-staging/` is staging, not the public APP publication.
- The final public release must equal the validated `publication-staging/` tree.
- Full APP compliance requires a public tagged release plus a valid `APP_PUBLICATION.json` release manifest whose `app_publication_id` verifies against the repo URL, tag, commit, tree, validation report hash, and human approval record.
- APP compliance records attach only to public versions and their repo URL, tag, commit/tree hash, and `app_publication_id`.
- Dev-sandbox runs have no publication meaning and must not create APP compliance records.

**Pace.** Never treat a partial answer as a complete one. If you asked three questions and the researcher answered one, follow up on the unanswered ones before moving on — they may have missed them, not declined them. When showing the researcher something for feedback (a draft, file list, or multi-item status summary), wait for them to engage substantively. A one-word acknowledgement ("ok", "sure", "fine") after presenting five things to review is not confirmation — ask which specific items they've looked at. The researcher's attention is finite; work with that, not against it.

**Author's voice.** The supplementary materials (`authors-note.md`, `know-how.md`), the `AGENTS.md` paper summary, and any content that speaks for the researcher must reflect what *they* want to convey — not what the agent thinks is important. Before drafting, ask the researcher what they want the document to say and who the intended audience is. Draft from their intent, then iterate. Never generate these documents first and ask for approval after — that inverts the authorship.

**Structured questions.** When asking the researcher to make choices, use structured question tools if the platform supports them (e.g. `AskUserQuestion` in Claude Code). Present clear options rather than open-ended text prompts. This is faster and less ambiguous, and keeps the researcher's typing load low.

## Phase files (read in order)

### [`gather.md`](gather.md) — Phases 1-2

- **Purpose.** Understand the working repo. Interview the researcher. Optionally extract publication-safe research context from agent chat/session history.
- **Assumes.** Invoked in the researcher's private working repo, or an explicit developer sandbox target that stands in for one.
- **Produces.** A staging plan: the canonical paper document and format; previous public release or existing staging info; new-vs-revision decision; key results in the researcher's words; include / exclude / defer file list; intended publication/repo name; optional extracted chat context.
- **Sub-skills called.** `/extract-chat-context` (optional).
- **Interaction load.** Heavy — up to five short interview rounds with the researcher.

### [`build.md`](build.md) — Phase 3

- **Purpose.** Create or revise `publication-staging/`. Copy and organize approved files. Run structure validation. Verify the code runs with staging-root paths.
- **Assumes.** Staging plan from `gather.md`.
- **Produces.** A self-contained `publication-staging/` tree with files in the layout defined by [`PROTOCOL.md` § Repository layout](../../PROTOCOL.md#repository-layout); `.gitignore` in place; `LICENSE` written; `data/README.md` populated whenever the publication uses any dataset, local or external; `environment/README.md` and dependency manifests populated whenever executable code/tooling exists; approved supplementary materials copied; `code/figure-reproduction/` created for generated figures/tables when applicable; environment setup and code verified from staging root when safe. Keep the phase checklist in chat/internal notes, not inside `publication-staging/`.
- **Sub-skills called.** `/validate-publication --stage structure`.
- **Interaction load.** Light — confirmation on the file list before copying, then mostly automated.

### [`draft.md`](draft.md) — Phase 4: Paper-agent docs

- **Purpose.** Create the paper-agent documentation (`AGENTS.md`, `CLAUDE.md`, and `README.md`) inside `publication-staging/`. Iterate with the researcher until they agree the agent represents their intent, not just their words.
- **Assumes.** `publication-staging/` with organized files and verified code from `build.md`.
- **Produces.** `publication-staging/AGENTS.md` (per the schema in [`PROTOCOL.md` § AGENTS.md](../../PROTOCOL.md#agentsmd)), `publication-staging/CLAUDE.md` (`@AGENTS.md`), and `publication-staging/README.md` — all approved by the researcher.
- **Sub-skills called.** `/validate-publication --stage agents-md`.
- **Templates used.** [`template/AGENTS.md`](../../template/AGENTS.md), [`template/CLAUDE.md`](../../template/CLAUDE.md), [`template/README.md`](../../template/README.md).
- **Interaction load.** Heavy — walk the researcher through `AGENTS.md` one section at a time and revise until intent matches.

### [`release.md`](release.md) — Phases 5-6

- **Purpose.** Run a full validation sweep from staging root, test the paper agent through a fresh agent session rooted at `publication-staging/`, freeze the validated tree, then execute the final outcome.
- **Assumes.** Paper-agent docs approved from `draft.md`.
- **Produces in real publication mode.** A tagged public release whose tree equals the validated staging tree; `APP_PUBLICATION.json` release manifest; working repo publication record updated with public URL, tag, commit/tree hash, and `app_publication_id`.
- **Produces in dev-sandbox mode.** An implementation test result; optional logs or preserved failing state; no public repo and no APP compliance record.
- **Sub-skills called.** `/validate-publication --stage full`.
- **Templates used.** [`template/publications.md`](../../template/publications.md).
- **Interaction load.** Heavy — final approval before freezing; per-action confirmation required for every remote operation in real publication mode.

### [`paper-types.md`](paper-types.md) — appendix

Not a workflow step. Format-specific guidance for theory-only, computational, experimental, notebook, and video/slideware papers. Phase files link to it when they need to adapt; consult it whenever the paper is not a default LaTeX-plus-code computational paper.

## Templates

Four files ship in `template/` at the repo root. Phase files copy or adapt them at the right moment — do not re-author these artifacts; start from the template.

| Template | Adapted by | Lands as |
|----------|------------|----------|
| [`template/AGENTS.md`](../../template/AGENTS.md) | `draft.md` (phase 4 paper-agent docs) | `publication-staging/AGENTS.md`, populated and researcher-approved. |
| [`template/CLAUDE.md`](../../template/CLAUDE.md) | `draft.md` (phase 4 paper-agent docs) | `publication-staging/CLAUDE.md` — one line: `@AGENTS.md`. |
| [`template/README.md`](../../template/README.md) | `draft.md` (phase 4 paper-agent docs) | `publication-staging/README.md`, populated from phases 1-2 and the finalized `AGENTS.md`. |
| [`template/publications.md`](../../template/publications.md) | `release.md` (phase 6, real mode only) | `<working-repo>/.publications.md` — a table of this working repo's public APP releases. |

## Sub-skills

Separate skills that phase files invoke. Read the linked SKILL.md if the phase-file summary is not enough.

- [`/extract-chat-context`](../extract-chat-context/SKILL.md) — pull publication-safe research context from local Claude Code / Codex chat/session history for supplementary materials (called in phase 2).
- [`/validate-publication`](../validate-publication/SKILL.md) — automated quality checks at each phase's checkpoint (`--stage structure`, `--stage agents-md`, `--stage full`) with `publication-staging/` as root during `/publish-paper`.

## Optional companion skills

These skills are useful alongside `/publish-paper`, but they are not required for APP compliance and should not be treated as core publication phases.

- [`/create-paper-page`](../create-paper-page/SKILL.md) — after a real public release succeeds, optionally offer to create a GitHub Pages project page for the published paper.
- [`/load-paper`](../load-paper/SKILL.md) — reader/import utility for loading an existing paper repo, local candidate, or arXiv paper; `/publish-paper` tests `publication-staging/` directly instead of depending on this loader.

## Resuming a session

If the researcher has already begun, detect filesystem state and jump to the matching phase file:

| State | Resume at |
|-------|-----------|
| No `publication-staging/` yet | `gather.md` |
| `publication-staging/` exists, no `AGENTS.md` | `build.md` |
| `publication-staging/AGENTS.md` exists, paper-agent docs not yet reviewed with researcher | `draft.md` |
| Paper-agent docs reviewed, staging not yet fully validated/tested | `release.md` phase 5 |
| Validated staging tree already frozen, no final outcome yet | `release.md` phase 6 |
| Public tagged release exists | `gather.md` (new version; `.publications.md` provides prior-version context in real mode) |
