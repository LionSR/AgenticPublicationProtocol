# Phase 5 — Final Review and Staging Freeze

This phase is shared by real publication mode and developer-sandbox mode. It validates `publication-staging/`, tests a fresh paper-agent session from the staging root, walks the researcher through the final candidate, records approval, and freezes the validated tree. Phase 6 final outcomes live in [`release.md`](release.md).

## 5.1 Full validation from staging root

Invoke `/validate-publication --stage full` with `publication-staging/` as the effective repository root — APP structure, privacy, paths, clear factual consistency, README↔AGENTS.md cross-checks, validation status, and reader-agent usability. Fix any errors before showing the validation report to the researcher, except explicitly deferred developer-sandbox release blockers such as a missing `LICENSE`.

Save the final validation report as `publication-staging/supplementary/validation-report.md`. The real publication manifest will include the SHA-256 hash of this report. If validation fails, do not proceed to real publication. In developer-sandbox mode, a run with unresolved full-release blockers may still be recorded as a sandbox workflow result, but not as a clean full-validation pass.

Licensing is a required part of full APP compliance. Before treating validation as passed, verify that `publication-staging/LICENSE` exists and matches the author's phase-2 licensing decision. If it is missing:

- in real publication mode, stop and ask the researcher to choose or provide a license before continuing;
- in developer sandbox mode, continue only if the researcher explicitly deferred licensing for the sandbox test, and classify the outcome as "completed with public-release blocker: missing LICENSE" rather than a clean full-validation pass.

Track the final validation outcome with these categories:

- `release-ready`: full validation passed and no public-release blockers remain.
- `release-blocked`: validation found errors or release blockers; real publication cannot proceed.
- `sandbox-pass`: developer-sandbox workflow completed and the candidate would be release-ready except for the intentionally absent public repo/tag/manifest.
- `sandbox-pass-with-release-blockers`: developer-sandbox workflow completed, but one or more public-release blockers remain, such as missing `LICENSE`, unresolved temporary figure statuses, stale validation language, hidden/generated artifacts that must be cleaned, or validation errors intentionally preserved for protocol testing.
- `sandbox-fail`: developer-sandbox workflow did not complete or the candidate cannot be meaningfully evaluated.

Also check that `publication-staging/` has no dependency on the private parent repo:

- no commands that require files outside staging;
- no absolute private paths;
- no references to unpublished notes, drafts, or private remotes;
- no symlinks that escape staging;
- no generated artifacts that are required but ignored or missing.
- `code/figure-reproduction/README.md` exists for papers with generated figures/tables, lists every paper figure/table, and matches `AGENTS.md`/README figure-reproduction summaries.

## 5.2 Test the paper agent from staging root

Before public release, test the candidate as a reader agent would see it. Launch a **fresh agent session** with `publication-staging/` as its working directory:

```bash
cd publication-staging
```

The fresh session should load `AGENTS.md` naturally from the staging root. Do not rely on the publishing agent's existing memory of the private working repo or on a separate loader skill; the publish-paper workflow tests the staged tree directly.

Ask 3-5 smoke-test questions, adapted to the paper:

1. What is the ground-truth paper/source for this publication?
2. What is the main contribution?
3. How do I reproduce one representative figure/table?
4. Which figures/tables are blocked, manual-only, dependency-blocked, or otherwise not directly reproduced?
5. What should a reader avoid or ask before running because it is heavy, platform-specific, or requires unavailable data?

Save the transcript or concise Q&A summary as:

```text
publication-staging/supplementary/paper-agent-test.md
```

The test passes if the fresh agent answers only from staged files, identifies the ground truth, gives paths and commands that exist inside staging, and accurately reports reproduction limitations. If the environment cannot launch a fresh agent session, record `paper-agent-test: not performed` as a public-release blocker in the validation report and sandbox result rather than calling a documentation review a paper-agent test.

For real publication mode, this is the final check that the public repo will work. For dev-sandbox mode, this is the key implementation test of the protocol.

## 5.3 Walk the researcher through the final staged state

Present the final staged state **one piece at a time**, not as a single wall of information.

1. **File inventory.** Show what's included in `publication-staging/` and what stayed outside it. Ask: "Is this the right set of files? Anything missing or anything that shouldn't be here?"
2. **License.** Confirm `publication-staging/LICENSE` and summarize the reuse terms. Ask: "Is this the license/reuse language you want attached to the staged publication?" In dev-sandbox mode, if licensing was deferred, say explicitly that this is a public-release blocker.
3. **`AGENTS.md` and `README.md`.** Briefly confirm they still read correctly after all revisions — this is a staleness check, not a full re-review (that was phase 4).
4. **Supplementary materials.** List what's in `publication-staging/supplementary/`. Ask: "Are you comfortable with all of this being public?" In dev-sandbox mode, phrase this as "safe for this sandbox test" if the fixture is not intended for publication.
5. **Validation results.** Show passed checks, warnings, public-release blockers, sandbox-only deferrals, and manual verification items separately. Walk through each issue — don't just list them.
6. **Figure reproduction.** Summarise counts from `code/figure-reproduction/README.md`: total figures/tables, direct scripts, reproduced, runs-but-differs, blocked, and manual-only. Walk through any non-`reproduced` items.
7. **Paper-agent test.** Summarise what the local staging-root test showed.

Wait for the researcher to engage with each item. If they say "all good" without engaging, ask about one specific thing — e.g. "I want to double-check: the supplementary materials include [X]. Are you sure that should be in the staged release tree?"

## 5.4 Confirm process completion and author approval

Use your internal phase checklist to confirm phases 1-5 are complete:

- Phase 1 — Understand: canonical paper and prior-version state identified.
- Phase 2 — Discuss: key results, include/exclude decisions, supplementary materials, and repo name confirmed.
- Phase 2 licensing: license/reuse terms chosen, or explicitly deferred for dev-sandbox with public-release blocker recorded.
- Phase 3 — Build staging: approved files copied, paths updated, `LICENSE` created/copied unless explicitly deferred for dev-sandbox, structure validation run.
- Phase 3 figure reproduction: `code/figure-reproduction/README.md` created when applicable, direct scripts attempted for every figure/table, and statuses documented.
- Phase 4 — Paper-agent docs: `AGENTS.md`, `CLAUDE.md`, and `README.md` drafted and researcher-reviewed.
- Phase 5 — Final review: full validation report saved, fresh staging-root paper-agent smoke test performed and saved to `supplementary/paper-agent-test.md`, remaining warnings/manual limitations reviewed.

Do not write this process checklist into `publication-staging/`. It is an internal workflow control, not publication content.

Do not proceed until the researcher has explicitly confirmed they reviewed the staged files, `AGENTS.md`, supplementary materials, validation results, and paper-agent test summary.

For real publication mode, do not record author approval unless `publication-staging/LICENSE` exists and the researcher has confirmed it. For developer sandbox mode with a deferred license, record that author approval applies only to the sandbox test, not to public APP release.

Record the human approval statement for real publication mode. At minimum capture:

- approval date;
- approving author names;
- a plain statement that the listed authors approve this staged tree for public APP release.

## 5.5 Freeze the validated release tree

Once approved, freeze the staging tree. At minimum:

- record the validation date;
- record the validation report path and SHA-256 hash;
- record the human approval statement;
- record the exact `publication-staging/` tree hash or archive checksum if available;
- avoid further edits except controlled fixes that return to phase 5.1.

The final public release in real publication mode must equal this validated tree.
