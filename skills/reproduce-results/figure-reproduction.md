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

