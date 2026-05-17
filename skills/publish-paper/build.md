# Phase 3 — Build Staging

## 3.1 Create or revise `publication-staging/`

Use the staging plan from [`gather.md`](gather.md). The output of this phase is not a public repo; it is a clean candidate release tree at:

```bash
publication-staging/
```

For a new publication, create `publication-staging/` from scratch. For a revision, start from the previous public release or the existing `publication-staging/`, whichever is cleaner, then revise it. If replacing an existing staging tree, preserve or summarize anything the researcher may need before removing generated staging files.

Do not create a GitHub repository in this phase. Public repo creation happens only in [`release.md`](release.md) after the staging tree has passed validation and paper-agent testing.

## 3.2 Copy and organize selected files

Show the researcher the list of files you're about to copy and the target structure under `publication-staging/`. Confirm before copying.

Create target directories first, then copy. Example — adapt to what's actually being published:

```bash
mkdir -p publication-staging/paper/figures \
         publication-staging/paper/build \
        publication-staging/code/src \
        publication-staging/code/scripts \
         publication-staging/code/figure-reproduction \
         publication-staging/data \
         publication-staging/reproduction/figures \
         publication-staging/environment \
         publication-staging/supplementary
cp paper/main.tex publication-staging/paper/
cp paper/*.bib publication-staging/paper/
cp figures/*.pdf publication-staging/paper/figures/
cp -r src/ publication-staging/code/src/
cp scripts/generate_*.py publication-staging/code/scripts/
cp data/results.csv publication-staging/data/
cp requirements.txt publication-staging/environment/
```

Use the file list from phase 2 — copy only what the researcher approved. Organize into the directory layout defined in [PROTOCOL.md § Repository layout](../../PROTOCOL.md#repository-layout). Not every directory is required — adapt to what is actually being published. See [`paper-types.md`](paper-types.md) for format-specific minimums.

**Single source of truth.** Each public file lives in exactly one place inside `publication-staging/`. No duplicates, no ambiguity about which version is current.

**Self-contained staging.** A reader agent must be able to enter `publication-staging/` and use it without relying on the private parent repo. Update all internal references — imports, file paths in scripts, `\includegraphics` paths in LaTeX, notebook paths, data paths, and skill instructions — so they are relative to the staging root.

**Handle large files:**

- Files over 50 MB: suggest Git LFS or external hosting (Hugging Face, Zenodo).
- Generated files that can be reproduced: add to `.gitignore` and document the generation command.

**Verify external data links.** For every external data URL identified in phase 1 (Hugging Face, Zenodo, Figshare, etc.):

- Test accessibility: `curl -sIL <url>` (follow redirects), or platform commands (`huggingface-cli download --dry-run`, etc.).
- Report results to the researcher: "Link X returned 200 OK" or "Link Y returned 404 — is this still the right URL?"
- Ask the researcher to confirm each link works (some require authentication the agent doesn't have).
- Record verified/flagged status in your internal phase notes and later in `publication-staging/supplementary/validation-report.md` during final validation.

**Create a staging `.gitignore`** tailored to the candidate release tree — build artifacts, generated files, sensitive files, OS files.

**Copy supplementary materials:**

- If research context was extracted in phase 2, copy the approved output into `publication-staging/supplementary/` now.
- For `publication-staging/supplementary/authors-note.md`: ask the researcher what message they want to leave for readers — what should someone know that isn't in the paper? Draft from their answer and the phase 2 interview, then show them for revision. This is their voice, not the agent's.
- Copy any approved slides, talks, posters into `publication-staging/supplementary/materials/`.

Do not create a procedural checklist inside `publication-staging/`. Track phase status internally and in chat; the publication tree should contain only reader-facing paper materials and validation artifacts.

**Create skills.** If the researcher defined skills in phase 2, create `publication-staging/skills/<name>/SKILL.md` for each, with `name` and `description` in frontmatter and step-by-step instructions in the body.

Tell the researcher what was copied and how it is organized. Flag anything that needed special handling (large files, updated paths, broken data links).

## 3.3 Create direct figure/table reproduction scripts

For any paper with generated figures or tables, make a serious attempt to directly reproduce every paper figure/table from code. Do not downgrade to "selected reproduction" merely because the source repo is messy.

Create:

```text
publication-staging/code/figure-reproduction/
  README.md
  fig01_<short-name>.py
  fig02_<short-name>.py
  ...
publication-staging/reproduction/figures/
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
- `manual-only` — figure requires manual post-processing; document the manual step and source artifacts.

For each paper figure/table:

1. Inspect the paper source, existing scripts, notebooks, saved outputs, and paper figure files.
2. Identify the closest source path from which the final artifact was produced.
3. If the source path is ambiguous after inspection, ask the researcher a concrete question before guessing. Include the figure/table, candidate scripts/notebooks, observed inputs/outputs, and your best hypothesis.
4. Write or adapt a direct script under `code/figure-reproduction/` that can be run from the staging root.
5. Prefer making the code executable and direct, even if the original repo used notebooks or multi-step exploratory scripts. The goal is one clear script per figure/table whenever feasible.
6. Make each script write generated output to `reproduction/figures/` unless there is a stronger local convention.
7. Document inputs and outputs in `code/figure-reproduction/README.md`.

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

### Structure validation

Invoke `/validate-publication --stage structure` with `publication-staging/` as the effective repository root. Review the validation report, fix any errors, and summarize warnings or manual verification items for the researcher.

## 3.4 Verify the code works from staging root

Tell the researcher you're testing that everything runs with the new staging-root paths.

Run commands from inside `publication-staging/` unless a tool truly requires a parent-repo command.

- **Paper compilation.** Run the build command and check it succeeds (if the format compiles).
- **Figure generation.** Run each script in `code/figure-reproduction/` whose status is intended to be `reproduced`; verify it produces the documented output and update the README status.
- **Tests.** If the staging tree has tests, run them.
- **Notebooks.** Execute in order and check for errors.
- **Imports.** Verify import paths resolve with the staged structure.
- **Parent dependency check.** Search for references to parent-repo paths such as `../`, absolute private paths, or unpublished directories. Fix or document any legitimate exception.

Fix anything that broke from the copy/reorganization. Report to the researcher: what passed, what needed fixing, what you changed.

## Handoff

Summarise what `publication-staging/` now contains. Next: [`draft.md`](draft.md).
