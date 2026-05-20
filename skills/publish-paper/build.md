# Phase 3 — Build Staging

## 3.1 Create or revise `publication-staging/`

Use the staging plan from [`gather.md`](gather.md). The output of this phase is not a public repo; it is a clean candidate release tree at:

```bash
publication-staging/
```

For a new publication, create `publication-staging/` from scratch. For a revision, start from the previous public release or the existing `publication-staging/`, whichever is cleaner, then revise it. If replacing an existing staging tree, preserve or summarize anything the researcher may need before removing generated staging files.

Do not create a GitHub repository in this phase. Public repo creation happens only in [`release.md`](release.md) after the staging tree has passed validation, paper-agent testing, and Phase 5 review/freeze in [`review.md`](review.md).

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

Do not create an empty `LICENSE` placeholder at this point — wait until step 3.3 writes the real text.
If the publication uses any dataset, local or external, `publication-staging/data/README.md` must also exist — authored below with the researcher.
If the publication has executable code, figure/table reproduction scripts, notebooks, or a compilable manuscript with nontrivial tooling, `publication-staging/environment/README.md` must exist — authored below with the researcher and verified during validation.

Use the file list from phase 2 — copy only what the researcher approved. Organize into the directory layout defined in [PROTOCOL.md § Repository layout](../../PROTOCOL.md#repository-layout). Not every directory is required — adapt to what is actually being published. See [`paper-types.md`](paper-types.md) for format-specific minimums.

**Single source of truth.** Each public file lives in exactly one place inside `publication-staging/`. No duplicates, no ambiguity about which version is current.

**Self-contained staging.** A reader agent must be able to enter `publication-staging/` and use it without relying on the private parent repo. Update all internal references — imports, file paths in scripts, `\includegraphics` paths in LaTeX, notebook paths, data paths, and skill instructions — so they are relative to the staging root.

**Handle large files:**

- Files over 50 MB: suggest Git LFS or external hosting (Hugging Face, Zenodo).
- Generated files that can be reproduced: add to `.gitignore` and document the generation command.

**Author `data/README.md`.** The spec requires a `data/README.md` whenever the publication uses any dataset — local files in `data/` or external references from AGENTS.md / code. A theory-only publication with no dataset skips this step. For each dataset — local or external — record:

- what the dataset is and how it was produced;
- which figures, tables, or scripts use it;
- for external datasets: URL, exact download command, local destination under `data/`, and whether it is required for the default workflow;
- file size for anything the reader will download.

Detail lives here; `AGENTS.md` carries only a concise pointer to `data/README.md`.

**Verify external data links.** For every external data URL identified in phase 1 (Hugging Face, Zenodo, Figshare, etc.):

- Test accessibility: `curl -sIL <url>` (follow redirects), or platform commands (`huggingface-cli download --dry-run`, etc.).
- Report results to the researcher: "Link X returned 200 OK" or "Link Y returned 404 — is this still the right URL?"
- Ask the researcher to confirm each link works (some require authentication the agent doesn't have).
- Record verified/flagged status in your internal phase notes and later in `publication-staging/supplementary/validation-report.md` during final validation.

**Create a staging `.gitignore`** tailored to the candidate release tree — build artifacts, generated files, sensitive files, OS files.

**Prepare the execution environment.** Follow [`environment.md`](environment.md) to detect toolchains, create `publication-staging/environment/README.md`, copy dependency manifests, gitignore local installed environments, and attempt safe project-scoped setup when authorized.

**Create or copy `LICENSE`.** Use the licensing decision recorded in phase 2.

- If the working repo already has the approved `LICENSE`, copy it to `publication-staging/LICENSE`.
- If the researcher chose a standard license, create `publication-staging/LICENSE` from the standard text and add any component-specific terms the researcher approved.
- If different components have different licenses, make the root `LICENSE` explain the terms for manuscript, code, data, and supplementary materials, and point to any component-level license files.
- Do not invent or guess licensing terms. If the researcher has not chosen a license, ask before creating the file.
- In real publication mode, do not proceed beyond phase 3 without `publication-staging/LICENSE`.
- In developer sandbox mode, if the researcher explicitly defers licensing, leave `publication-staging/LICENSE` absent and record "license deferred — public-release blocker" in the internal phase notes for phase 5. Do not let this become a silent omission.

**Copy supplementary materials:**

- If research context was extracted in phase 2, copy the approved output into `publication-staging/supplementary/` now.
- For `publication-staging/supplementary/authors-note.md`: ask the researcher what message they want to leave for readers — what should someone know that isn't in the paper? Draft from their answer and the phase 2 interview, then show them for revision. This is their voice, not the agent's.
- Copy any approved slides, talks, posters into `publication-staging/supplementary/materials/`.

Do not create a procedural checklist inside `publication-staging/`. Track phase status internally and in chat; the publication tree should contain only reader-facing paper materials and validation artifacts.

**Create skills.** If the researcher defined skills in phase 2, create `publication-staging/skills/<name>/SKILL.md` for each, with `name` and `description` in frontmatter and step-by-step instructions in the body.

Tell the researcher what was copied and how it is organized. Flag anything that needed special handling (large files, updated paths, broken data links).

## 3.3 Write `LICENSE`

The spec requires a `LICENSE` file at the repo root with no extension. Ask the researcher which license they want using a structured choice: `MIT`, `Apache-2.0`, `CC-BY-4.0`, `BSD-3-Clause`, or `Other`.

Fetch the canonical text rather than paraphrasing. Fetch into a temporary file first, show it to the researcher, and only move it into place as `LICENSE` after explicit confirmation. Try GitHub's licenses API first; fall back to choosealicense.com raw for licenses the API does not carry, notably CC licenses:

```bash
rm -f LICENSE.tmp LICENSE.api.json

# Primary: GitHub licenses API
if curl -fsSL https://api.github.com/licenses/<spdx> -o LICENSE.api.json; then
  jq -r '.body // empty' LICENSE.api.json > LICENSE.tmp
fi

# Fallback (CC-BY-4.0, CC-BY-SA-4.0, etc.): strip the YAML frontmatter after the second "---"
if [ ! -s LICENSE.tmp ]; then
  curl -fsSL https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/<spdx>.txt \
    | awk 'f;/^---$/{c++;if(c==2)f=1}' > LICENSE.tmp
fi

# Sanity-check the fetch succeeded before showing the researcher
[ -s LICENSE.tmp ] || { echo "LICENSE fetch failed"; rm -f LICENSE.api.json; exit 1; }
```

SPDX identifiers for the menu: `mit`, `apache-2.0`, `cc-by-4.0`, `bsd-3-clause`.

Fill placeholders: MIT and BSD-3-Clause have `[year]` and `[fullname]` — substitute the current year and the authors' names from phase 2. Apache-2.0's canonical text has no placeholders; mention that the researcher may add a `NOTICE` file separately if they want attribution callouts. For `Other`, ask the researcher to paste the full license text; write it to `LICENSE.tmp` verbatim.

Show the populated `LICENSE.tmp` to the researcher. Only after explicit confirmation:

```bash
mv LICENSE.tmp publication-staging/LICENSE
rm -f LICENSE.api.json
```

**Multi-component licensing.** Ask whether paper, code, and data are all under the same license. If not, for example paper under CC-BY-4.0 and code under MIT, the single `LICENSE` file must explicitly call this out per the spec. The skill does not auto-assemble multi-section LICENSE files — prompt the researcher to author the full text themselves and write it verbatim.

## 3.4 Create direct figure/table reproduction scripts

For any paper with generated figures or tables, follow [`figure-reproduction.md`](figure-reproduction.md). Make a serious attempt to directly reproduce every paper figure/table from code, document every artifact in `publication-staging/code/figure-reproduction/README.md`, and use only final statuses with concrete evidence or blockers before Phase 5.

## 3.5 Run structure validation

Invoke `/validate-publication --stage structure` with `publication-staging/` as the effective repository root. Review the validation report, fix any errors, and summarize warnings or manual verification items for the researcher.

## 3.6 Verify the code works from staging root

Tell the researcher you're testing that everything runs with the new staging-root paths.

Run commands from inside `publication-staging/` unless a tool truly requires a parent-repo command.

- **Environment setup.** Follow [`environment.md`](environment.md): run documented setup or verification commands when safe, verify tool versions and command prefixes, and record blockers in `environment/README.md` and the validation report.
- **Paper compilation.** Run the build command and check it succeeds (if the format compiles).
- **Figure generation.** Run each script in `code/figure-reproduction/` whose status is intended to be `reproduced`; verify it produces the documented output and update the README status. Confirm the script-to-figure mapping still holds after the copy and reorganization — no new duplicates, no missing scripts.
- **Tests.** If the staging tree has tests, run them.
- **Notebooks.** Execute in order and check for errors.
- **Imports.** Verify import paths resolve with the staged structure.
- **Parent dependency check.** Search for references to parent-repo paths such as `../`, absolute private paths, or unpublished directories. Fix or document any legitimate exception.

Fix anything that broke from the copy/reorganization. Report to the researcher: what passed, what needed fixing, what you changed.

## Handoff

Summarise what `publication-staging/` now contains. Next: [`draft.md`](draft.md).
