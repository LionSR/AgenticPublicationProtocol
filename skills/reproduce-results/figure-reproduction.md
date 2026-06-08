# Figure and Table Reproduction

Make a serious attempt to reproduce every paper figure/table generated from data or computation before files are reorganized into APP staging.

For each artifact:

1. Find the paper reference and artifact path.
2. Inspect original scripts, notebooks, saved outputs, and data.
3. Identify the closest source path that produced the artifact.
4. If ambiguous, ask the author a concrete question with candidate scripts and your best hypothesis.
5. Write or adapt a direct wrapper against the original working repo layout. Prefer one wrapper per figure/table; grouped wrappers are allowed only when clearly natural.
6. Write outputs under `working/reproduction/generated/` or another clearly named non-public scratch location.
7. Record attempted commands, inputs, outputs, and status in `working/reproduction/reproduction-report.md`.

If a fresh rerun cannot be completed, inspect cached or saved evidence before deciding
what the report says. Notebooks, plotted-data arrays, CSV/JSON/HDF5/text result files,
logs, saved figures with adjacent source values, and generated summaries can often
support a partial audit even when the original computation is too heavy or a dependency
is unavailable. For each headline or primary benchmark figure, record the strongest
cheap observation available: actual plotted values, thresholds, ratios, row counts,
aggregate pass/fail counts, orderings, signs, min/max values, or explicit uncertainty.
Do not treat artifact existence alone as a sufficient check when the artifact can be
parsed for the claim-relevant number.

Prefer the closest figure-generating artifact for headline figure claims. If a notebook
hard-codes plotted points or uses constants that differ from adjacent cached tables,
record the plotted values, the table-derived values, and the ambiguity. Do not let an
easier adjacent table silently replace the exact plotted source for a figure-specific
question.

When the partial audit requires more than opening one file, prefer a small checker in
`working/reproduction/scripts/` that prints the observed signature from the original
working layout. Keep it read-only and avoid changing scientific content.

Allowed final statuses:

- `reproduced`
- `runs-but-differs`
- `blocked-missing-data`
- `blocked-heavy-compute`
- `blocked-broken-code`
- `blocked-dependency`
- `manual-only`

Do not use `todo`, `unknown`, `not-yet-run`, or blank statuses as final states.

Before marking `blocked-dependency`, make a safe project-scoped install/setup attempt when authorized, or record why no attempt was safe.

Do not silently create new scientific results. The wrapper should reproduce/check what the paper already reports.
