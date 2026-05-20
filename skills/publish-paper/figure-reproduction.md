# Phase 3 Support — Figure/Table Reproduction

For any paper with generated figures or tables, make a serious attempt to directly reproduce every paper figure/table from code. Do not downgrade to "selected reproduction" merely because the source repo is messy.

Create:

```text
publication-staging/code/figure-reproduction/
  README.md
  fig01_<short-name>.py
  fig02_<short-name>.py
  ...
```

`code/figure-reproduction/README.md` is source-of-truth computational documentation, not supplementary commentary. It must contain a table:

```text
Figure/Table | Paper artifact | Script | Inputs | Generated output | Status | Notes
```

Use these statuses:

- `reproduced` — script ran from staging root and generated the expected output.
- `runs-but-differs` — script ran, but generated output differs materially from the paper artifact; explain how.
- `blocked-missing-data` — required input data or external artifact is unavailable; name it.
- `blocked-heavy-compute` — reproduction requires compute the agent/researcher did not approve for this run; state requirements.
- `blocked-broken-code` — source code fails; include command/error summary.
- `blocked-dependency` — an external dependency, package resolver, network access, license restriction, or platform requirement prevents running the script; name the dependency and the attempted command.
- `manual-only` — figure requires manual post-processing; document the manual step and source artifacts.

Do not use temporary final statuses such as `not-yet-run`, `todo`, or `unknown`. Before phase 5 every figure/table must have one of the statuses above, with evidence or a concrete blocker.

Use the dependency installation policy in [`environment.md`](environment.md) before marking any figure/table or validation command `blocked-dependency`.

For each paper figure/table:

1. Inspect the paper source, existing scripts, notebooks, saved outputs, and paper figure files.
2. Identify the closest source path from which the final artifact was produced.
3. If the source path is ambiguous after inspection, ask the researcher a concrete question before guessing. Include the figure/table, candidate scripts/notebooks, observed inputs/outputs, and your best hypothesis.
4. Write or adapt a direct script under `code/figure-reproduction/` that can be run from the staging root.
5. Prefer making the code executable and direct, even if the original repo used notebooks or multi-step exploratory scripts. The goal is one clear script per figure/table whenever feasible. Grouped wrappers are acceptable only when a single command naturally produces several paper artifacts; in that case, mark the script as a grouped wrapper in `code/figure-reproduction/README.md` and list every generated output it covers.
6. Make each script write generated output under `code/figure-reproduction/generated/` unless there is a stronger local convention documented in `code/figure-reproduction/README.md`.
7. Document inputs and outputs in `code/figure-reproduction/README.md`.

Generated reproduced figures are local run artifacts by default. Add `code/figure-reproduction/generated/` to `publication-staging/.gitignore` unless the researcher explicitly wants to commit generated outputs as intentional publication artifacts, validation evidence, or outputs that are not cheaply reproducible. If generated outputs are committed, explain in `code/figure-reproduction/README.md` why they are included, how they were generated, and whether they match the paper artifact.

When the runtime supports parallel subagents, use two specialized agents:

- **Figure-script agent:** owns `publication-staging/code/figure-reproduction/`; reads paper, notebooks, scripts, data, and paper figures; writes the direct scripts and README map.
- **Figure-validation agent:** independently runs the figure scripts from `publication-staging/`, checks that outputs are created, compares dimensions/format and, when reasonable, image similarity to `paper/figures/`, then reports concrete failures.

If subagents are unavailable, do the same work sequentially. The publishing agent remains responsible for integrating fixes.

Only mark a figure/table as not directly reproduced after documenting in `code/figure-reproduction/README.md`:

- source scripts/notebooks inspected;
- any ambiguity question asked to the researcher and the answer received, or why the researcher could not answer;
- command attempted;
- exact missing input, failure, or manual/heavy step;
- what a future reader or author would need to do to make it `reproduced`.
