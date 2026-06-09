# Figure Wrapper Migration

Convert pre-staging reproduction wrappers into staging-root APP scripts.

Create:

```text
publication-staging/code/figure-reproduction/
  README.md
  fig01_<short-name>.py
  ...
```

`code/figure-reproduction/README.md` is the public source of truth. It must list every paper figure/table with:

```text
Figure/Table | Paper artifact | Script | Inputs | Generated output | Status | Notes
```

Use only final statuses:

- `reproduced`
- `runs-but-differs`
- `blocked-missing-data`
- `blocked-heavy-compute`
- `blocked-broken-code`
- `blocked-dependency`
- `manual-only`

Make scripts runnable from `publication-staging/`. Write generated outputs under `code/figure-reproduction/generated/` unless the README documents a stronger convention. Add generated output directories to `.gitignore` unless the author intentionally commits them as publication artifacts or validation evidence.

For blocked/manual items, document source scripts inspected, attempted command, exact missing input/failure/manual step, and what a future reader needs.

For primary numerical or benchmark claims with cached evidence, preserve the strongest
partial audit from `working/reproduction/reproduction-report.md` even when the full
rerun status remains blocked. If the reproduction step created a read-only checker or
one-liner under `working/reproduction/scripts/`, migrate or adapt it into
`publication-staging/code/figure-reproduction/` and document the staging-root command,
inputs, and expected observed signature. A blocked full rerun should still leave a
reader-facing way to inspect cached plotted values, benchmark tables, row counts,
ratios, threshold crossings, or orderings when those artifacts are staged.

When the exact figure-generating notebook or script contains plotted constants, fitted
values, or figure-specific arrays, make that the primary quick-check anchor for the
figure. If nearby cached tables expose related but different columns, document both the
figure-plotted values and the table-derived values rather than hiding the ambiguity.

Do not use a mere "file exists" check as the only quick check for a primary benchmark
when the staged artifact contains claim-relevant numeric data. In that case, the README
should name the observed value/ratio/count or point to the command that prints it.
