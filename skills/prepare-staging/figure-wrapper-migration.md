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

