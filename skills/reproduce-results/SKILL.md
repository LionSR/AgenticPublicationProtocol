---
name: reproduce-results
description: Deliberately reproduce and check the existing results of an academic paper before APP staging, including figures, tables, key experiments, and analytic derivations, while asking the author targeted questions and producing a pre-staging reproduction report.
---

# Reproduce Results

Use this skill before `prepare-staging` when preparing an Agentic Publication Protocol (APP) paper. The goal is to understand and check the results the author already provided, before moving files into `publication-staging/`.

## Scope

Reproduce or check existing paper results only. Do not propose scientific improvements, add new experiments, optimize the method, or create new claims/results as part of the publication workflow. If a possible extension appears, record it only as an optional author question outside the reproduction status.

Assume the author may not know APP. Explain that this step checks the existing paper, and that later `publication-staging/` will become a draft public repository.

## Process

1. Inspect prior state:
   - `.publications.md`, if present;
   - any existing `publication-staging/`;
   - prior public release/staging content that should be carried forward.
2. Read the source repo before asking broad questions:
   - canonical paper candidates, title, abstract, claims, figures, tables, appendices;
   - code, scripts, notebooks, tests, dependencies, data, saved outputs;
   - supplementary notes, slides, tutorials, prior chat/session artifacts.
   - For nonstandard paper types, consult `paper-types.md`.
3. Interview the author in short rounds:
   - canonical paper if ambiguous;
   - key results and contribution in the author's words;
   - figure/table mapping confirmation;
   - include/exclude/defer file decisions;
   - publication repo name;
   - license/reuse terms or explicit dev-sandbox-only deferment;
   - reader perspective and desired supplementary materials.
4. Ask explicitly about chat context:
   - tell the author publication-safe chat/session context can capture reasoning, design decisions, failed attempts, debugging notes, or methodology choices;
   - ask whether they want to include any;
   - if they have prepared context, review it for relevance/confidentiality;
   - if they want context but do not have it ready, give extraction instructions and use `/extract-chat-context` from the working repo when available;
   - stage only author-approved output later.
5. Build a result inventory:
   - empirical results, figures, tables, experiments;
   - analytic/theoretical results;
   - datasets and external links;
   - environment/toolchain requirements;
   - heavy, proprietary, credentialed, platform-specific, or manual steps.
6. Reproduce figures/tables and key computational results:
   - follow `figure-reproduction.md`;
   - write wrappers against the original working layout first;
   - record commands, generated outputs, and blockers;
   - use final APP statuses: `reproduced`, `runs-but-differs`, `blocked-missing-data`, `blocked-heavy-compute`, `blocked-broken-code`, `blocked-dependency`, `manual-only`.
7. Check analytic derivations:
   - follow `derivation-checks.md`;
   - verify included derivation steps when feasible;
   - distinguish derivations in the paper, derivations quoted from literature, and missing nontrivial derivations;
   - if a more detailed derivation of certain key steps would help readers or future agents, write a detailed note in Markdown or LaTeX and inform the author. Add detailed derivation notes to `supplementary/` by default, since `paper/` is ground truth and `supplementary/` is optional context. Tell the author that if they want a derivation note to become part of the paper itself, they should move or adapt it into `paper/`.
8. Write the handoff report:

```text
working/reproduction/reproduction-report.md
```

Include canonical paper, prior state, author decisions, key results, figure/table map, derivation checks, data/environment findings, include/exclude/defer list, repo name, license decision, chat-context decision, commands attempted, outputs, blockers, and open questions.

This report is private workflow context by default. `prepare-staging` decides what becomes reader-facing material.

9. Present an author-facing reproduction gate before any next workflow step:
   - summarize what was reproduced successfully;
   - summarize what ran but differed from the paper or saved outputs;
   - summarize what could not be reproduced and name the blocker for each item;
   - distinguish minor/documentation blockers from significant blockers that affect central claims, required figures/tables, public data availability, or executable reproduction;
   - warn clearly when reproduction fails or significant blockers remain, and say this will likely cause problems during `validate-publication` unless resolved, explicitly deferred, or accepted as part of a dev-sandbox/partial outcome;
   - offer concrete options, such as supplying missing data, fixing dependencies, providing compute access or cached outputs, revising scripts, marking a result manual-only with evidence, excluding/deferring nonessential artifacts, switching to dev-sandbox mode, continuing with known validation risk, or stopping.

Do not move on to `prepare-staging` automatically when blockers, `runs-but-differs`, or `manual-only` statuses remain. Wait for explicit author instruction to resolve the blockers, defer/exclude specific items, accept the risk and continue, switch outcome mode, or stop. If there are no blockers and all required checks are `reproduced`, say so and continue according to the orchestrator.
