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
   - publication GitHub `owner/repo` and intended release tag;
   - license/reuse terms or explicit dev-sandbox-only deferment;
   - reader perspective and desired supplementary materials.

   From the selected `owner/repo` and tag, derive the canonical release URL as
   `https://github.com/<owner>/<repo>/releases/tag/<tag>`. Record the normalized
   publication version using the APP tag rule: tag `v1.2.3` gives version
   `1.2.3`; non-semver tags use the tag exactly. Remind the author that if they
   want the published repo URL included in the paper, the paper URL should match
   this derived release URL. If the author asks you to add or update that URL in
   the paper, confirm the exact placement and text, make only that requested URL
   edit, and avoid unrelated paper changes.

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
   - when a full fresh rerun is blocked but saved outputs, notebooks, plotted-data files,
     logs, tables, cached benchmark text files, or generated summaries exist, perform the
     strongest read-only partial numeric audit available before assigning the final status.
     Extract observed values, ratios, threshold crossings, counts, orderings, or explicit
     ambiguities from those artifacts. Do not collapse this to "files exist" when the
     cached artifact contains the number a reader is likely to ask about;
   - for primary benchmark or headline claims that require combining cached artifacts,
     parsing notebooks, or computing a reported ratio/count, create a compact private
     checker or documented one-liner under `working/reproduction/scripts/` when feasible.
     The checker should report the observed signature from the original working layout so
     `prepare-staging` can migrate it into a reader-facing quick check;
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

Include canonical paper, prior state, author decisions, key results, figure/table map, derivation checks, data/environment findings, include/exclude/defer list, selected publication `owner/repo`, selected release tag, normalized version, derived release URL, whether the author wants that URL included in the paper, license decision, chat-context decision, commands attempted, outputs, blockers, and open questions.

For every primary numerical, benchmark, or headline qualitative claim, include one of:

- fresh reproduction evidence;
- a partial cached audit with observed values/ratios/counts/orderings and the exact
  source artifacts inspected;
- a concrete reason no partial audit is possible.

If full rerun is blocked but a partial cached audit was performed, say both things
explicitly. Example: `blocked-heavy-compute for fresh rerun; partial cached audit
observed A/B ratio 7.6x from notebook plotted points and benchmark text table`.
This distinction is important because later reader agents need numeric anchors, not
only workflow blockers.

This report is private workflow context by default. `prepare-staging` decides what becomes reader-facing material.

9. Present an author-facing reproduction gate before any next workflow step:
   - summarize what was reproduced successfully;
   - summarize what ran but differed from the paper or saved outputs;
   - summarize what could not be reproduced and name the blocker for each item;
   - distinguish minor/documentation blockers from significant blockers that affect central claims, required figures/tables, public data availability, or executable reproduction;
   - warn clearly when reproduction fails or significant blockers remain, and say this will likely cause problems during `validate-publication` unless resolved, explicitly deferred, or accepted as part of a dev-sandbox/partial outcome;
   - offer concrete options, such as supplying missing data, fixing dependencies, providing compute access or cached outputs, revising scripts, marking a result manual-only with evidence, excluding/deferring nonessential artifacts, switching to dev-sandbox mode, continuing with known validation risk, or stopping.

Do not move on to `prepare-staging` automatically when blockers, `runs-but-differs`, or `manual-only` statuses remain. Wait for explicit author instruction to resolve the blockers, defer/exclude specific items, accept the risk and continue, switch outcome mode, or stop. If there are no blockers and all required checks are `reproduced`, say so and continue according to the orchestrator.
