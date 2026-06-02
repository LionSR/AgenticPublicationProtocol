---
name: publish-paper
description: "Orchestrate the full Agentic Publication Protocol workflow by calling modular step skills: reproduce-results, prepare-staging, define-paper-agent, validate-publication, and release-outcome."
---

# Publish Paper — Orchestrator

Use this when an author wants help preparing a paper as an Agentic Publication Protocol (APP) release or dev-sandbox candidate.

This skill is intentionally thin. It coordinates step skills rather than containing all phase details.

## Core Ideas To Explain To The Author

Assume the author has not read `PROTOCOL.md`.

- `publication-staging/` is a draft public repository inside the private working repo. It is not public yet.
- `paper/` is ground truth: claims there are treated as part of the paper.
- `supplementary/` is optional context: useful for readers/agents, but secondary to the paper.
- `code/figure-reproduction/README.md` is the public map from figures/tables to scripts, statuses, and blockers.
- `AGENTS.md` tells a future reader's agent how to explain and work with the paper.
- A real APP publication exists only after a validated staging tree is released publicly with a tag and manifest.

## Modes

The workflow is mode-neutral until the final outcome:

- **Real publication mode**: publish the validated staging tree as a public tagged release with `APP_PUBLICATION.json`, then record `.publications.md`.
- **Developer sandbox mode** (`--mode dev-sandbox`): exercise the same prepare/validate standards, then record an implementation-test result. Do not create a public repo, `APP_PUBLICATION.json`, or `.publications.md`.

## Roadmap To Show

```text
PUBLICATION ROADMAP

  Step 1 — Reproduce results      [ ]  Understand paper, reproduce/check existing results, figures, tables, derivations
  Step 2 — Prepare staging        [ ]  Create/revise publication-staging/, organize files, migrate scripts
  Step 3 — Define paper agent     [ ]  Draft AGENTS.md, CLAUDE.md, README.md with author review
  Step 4 — Validate publication   [ ]  Full APP validation and staging-root paper-agent test
  Step 5 — Release outcome        [ ]  Final author review/freeze, then publish publicly or record dev-sandbox result

  You can run these steps one by one, or let /publish-paper orchestrate them.
```

Keep this roadmap in chat/internal notes, not in `publication-staging/`.

## Step Order

1. `/reproduce-results`
   - Checks existing results only.
   - Does not improve the science, add experiments, or create new claims.
   - Produces `working/reproduction/reproduction-report.md`.
2. `/prepare-staging`
   - Builds `publication-staging/` from the reproduction report and author decisions.
   - Runs `/validate-publication --stage structure`.
3. `/define-paper-agent`
   - Creates and iterates `AGENTS.md`, `CLAUDE.md`, and README.
   - Runs `/validate-publication --stage agents-md`.
4. `/validate-publication --stage full`
   - Finds substantive APP issues before release.
   - Requires the final validation report and staging-root paper-agent test.
5. `/release-outcome`
   - Performs only lightweight final release guards, author approval, freeze, and final outcome.
   - If a substantive issue appears, route back to the owning step.

## Resume State

Detect filesystem state and continue at the matching step:

| State | Resume at |
|---|---|
| No `working/reproduction/reproduction-report.md` and no reliable staging | `/reproduce-results` |
| Reproduction report exists, no coherent `publication-staging/` | `/prepare-staging` |
| `publication-staging/` exists, no approved `AGENTS.md`/README | `/define-paper-agent` |
| Paper-agent docs approved, no full validation report or paper-agent test | `/validate-publication --stage full` |
| Full validation passed, no final outcome | `/release-outcome` |
| Public tagged release exists | `/reproduce-results` for a new version/revision |

Existing `.publications.md` means a previous real release exists. Read it during `reproduce-results` and focus author questions on what changed.

## Cross-Cutting Rules

- Ask author questions in small rounds. If they answer only part of a round, follow up before moving on.
- Never treat "ok" after a multi-item review as full approval. Ask what they reviewed.
- Draft author-facing material from author intent, not from agent guesses.
- Explain each step at a high level before doing it.
- Keep paths in staged docs relative to `publication-staging/`, not the private parent repo.
- Do not write workflow checklists into `publication-staging/`.
- In dev-sandbox mode, record blockers honestly and never create real publication artifacts.

## Companion Skills

- `/extract-chat-context` may be called by `/reproduce-results` after asking the author whether they want chat/session context.
- `/validate-publication` is called at structure, agents-md, and full checkpoints.
- `/create-paper-page` may be offered only after a real public release succeeds.
