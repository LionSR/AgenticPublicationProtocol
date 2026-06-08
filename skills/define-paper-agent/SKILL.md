---
name: define-paper-agent
description: Draft and iterate the APP paper-agent documentation in publication-staging, including AGENTS.md, CLAUDE.md, and README.md, using the author-approved staging tree and reproduction report.
---

# Define Paper Agent

Use this after `prepare-staging`. The output is author-reviewed paper-agent documentation inside `publication-staging/`.

Assume the author may not know APP. Explain that `AGENTS.md` tells future reader agents how to represent the paper, where to find authoritative information, and how to behave as a helpful paper assistant.

## Process

1. Read:
   - `publication-staging/`;
   - `working/reproduction/reproduction-report.md`;
   - `PROTOCOL.md` `AGENTS.md` schema;
   - templates under `template/`.
2. Ask the author for the core message they want readers to take away before drafting summary/key-results text.
3. Ensure the canonical reproduction/data docs support concrete reader checks:
   - add or verify a compact "Quick claim checks" subsection in `code/figure-reproduction/README.md`, `data/README.md`, or the most relevant canonical doc;
   - cover 2-5 headline or likely-reader claims, especially claims tied to figures, tables, reported ratios, thresholds, hierarchy gaps, or qualitative conclusions;
   - include the paper's primary benchmark or headline numerical result when one exists. Do not
     substitute easier adjacent checks, such as secondary cached figures or shape checks, for the
     main reported ratio, threshold crossing, ordering, or table value unless the exact check is
     unavailable in the staged material;
   - format each quick check so a future reader agent can answer without hunting:
     claim or reader question; exact paper figure/table/equation/section; direct staged anchors
     such as script, notebook, data, cached output, or generated figure paths; a lightweight command
     or read-only inspection path when feasible; expected numeric value, ratio, shape, count, threshold,
     ordering, or qualitative signature; evidence level; and blocker if a full rerun is not cheap;
   - prefer concrete expected signatures over prose. For example, include values like ratios,
     array shapes, row counts, min/max/gap signs, figure filenames, or "all N cached files satisfy
     condition X" when the staged material supports it;
   - when a paper claim is broad, such as "always", "consistently", "outperforms", "beats",
     "lower than", "in most cases", or "across the sweep", include a whole-staged-corpus aggregate
     when feasible, not only a representative slice. Report counts such as `91/91`, `57/91`,
     min/max gaps, number of violations, or the precise subset where the claim holds;
   - if the source repo contains a stronger cheap check than the staged docs currently expose,
     copy the relevant script/data or summarize the exact staged-accessible path in the canonical docs
     during staging-doc drafting, rather than expecting the paper agent to rediscover it later;
   - when the exact headline check is unavailable or ambiguous, say so in the quick check and give
     the strongest partial check plus the missing file, dependency, or provenance ambiguity. Do not
     let the absence of the exact check disappear behind a different successful check;
   - if a full rerun is blocked but cached plotted data, notebooks, logs, or generated-result files
     exist, include a partial numeric audit of those artifacts when feasible. For example, inspect
     hard-coded plotted points, cached benchmark text files, saved tables, generated JSON summaries,
     or notebook constants and report the observed ratio, threshold, count, ordering, or ambiguity;
   - keep this out of `AGENTS.md` except for a pointer; the detailed commands and values belong in the canonical docs.
4. Draft `publication-staging/AGENTS.md` from `template/AGENTS.md`:
   - required frontmatter;
   - identity and ground-truth hierarchy;
   - 1-2 concise paper-summary paragraphs and key results in author intent;
   - brief canonical pointers with staging-root paths, including 2-5 high-value direct entry points for checks when they exist, such as the main paper file, main analysis module, cached result file, or figure wrapper;
   - reader-help operating mode: answer science first, inspect exact paper equations/figures/tables for technical questions, inspect direct code/data evidence when useful, cite concrete files/sections/commands, and label evidence level when useful;
   - claim-check guidance: for "how would I check this?" questions, name the relevant script/data files and perform the strongest cheap check available, such as reading cached data, computing a small aggregate, comparing reported values, or locating the exact implementation path;
   - concrete-answer guidance: for result-check questions, do not stop at a reproduction plan when a
     cheap staged check is available. Inspect the referenced artifact and report the observed value,
     count, shape, ordering, or caveat in the answer;
   - blocker guidance: "full rerun blocked" is not enough when staged cached plotted data exists.
     In that case, inspect the cached or plotted artifact and report the strongest partial numeric
     audit before explaining the blocker;
   - precision guidance: separate formal/mathematical claims from numerical or solver-based evidence, and state tolerances, approximations, cached-data status, or dependency blockers when relevant;
   - pointer to `environment/README.md` for setup commands, runner prefixes, tested platform, computational requirements, and external software;
   - pointer to `code/figure-reproduction/README.md` for figure/table commands, inputs, outputs, statuses, runtimes, and blockers;
   - pointer to `data/README.md` for dataset provenance, download/access instructions, local destinations, and dataset-to-result mapping;
   - heavy-command, network, licensed-software, and destructive-action warnings in concise policy form only;
   - citation;
   - supplementary materials and skills when present.
   Keep `AGENTS.md` brief: target under 100 lines and exceed 120 lines only for a concrete reason. Do not duplicate figure tables, dataset catalogs, setup commands, validation summaries, or computational requirement tables when the information belongs in a canonical README. Concision should not remove the most useful direct entry points for reader checks.
5. Create `publication-staging/CLAUDE.md` as `@AGENTS.md`.
6. Self-check:
   - every path exists from staging root;
   - AGENTS.md points to the canonical docs that contain detailed setup, data, reproduction, validation, and license information;
   - `environment/README.md` contains setup commands, runner prefixes, tested platform, computational requirements, and external software requirements when executable code exists;
   - `code/figure-reproduction/README.md` contains figure/table statuses, commands, inputs, outputs, runtimes, and blockers when generated figures/tables exist;
   - `data/README.md` contains dataset details when the publication uses any dataset, local or external;
   - canonical docs contain quick claim checks for the most important checkable results, with exact script/data paths and expected values or signatures where feasible;
   - AGENTS.md gives future reader agents enough direct pointers to inspect exact equations, scripts, and cached data without hunting through the whole tree;
   - for each quick claim check, a reader agent should be able to produce at least one concrete
     paper anchor and one concrete staged artifact anchor, and should be able to say whether it
     observed the expected signature, only saw cached/provenance evidence, or is blocked;
   - compare the quick checks against the `Key Results` and figure/table map. Every primary
     numerical claim should either have an exact staged quick check, a clearly labeled partial
     staged check, or an explicit blocker/ambiguity entry;
   - any entry marked full-rerun blocked but backed by cached plotted data should still include
     the best partial observed number, ratio, count, ordering, or a precise explanation of why
     even a partial numeric audit is impossible;
   - no duplicated details in AGENTS.md that could become stale relative to the canonical docs;
   - no stale "not validated" or overbroad "fully validated" claims in AGENTS.md or README;
   - licensing language matches `LICENSE` or sandbox deferral.
7. Invoke `/validate-publication --stage agents-md`.
8. Walk the author through `AGENTS.md` section by section. Revise until the author agrees it reflects their intent.
9. Draft `publication-staging/README.md` from `template/README.md`. Keep it human-facing and compatible with AGENTS.md, but use canonical README pointers instead of duplicating detailed setup, data, reproduction, and validation content.
10. Show README to the author and revise.

Do not invent author voice. Do not imply that optional supplementary material is ground truth.
