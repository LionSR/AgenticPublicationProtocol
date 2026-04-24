# Phase 3 — Build

## 3.1 Create the publication repo

Offer the researcher a structured choice:

- **Create on GitHub now** (requires `gh` CLI).
- **Create locally first** (push to GitHub later).

First check if `gh` is available and authenticated:

```bash
gh auth status
```

If `gh` is not installed or not authenticated, tell the researcher and offer alternatives:

- Install: https://cli.github.com
- Authenticate: `gh auth login`
- Or skip `gh` and create the repo manually on GitHub later.

**If `gh` is available and the researcher wants GitHub immediately:**

```bash
gh repo create <repo-name> --public --clone
cd <repo-name>
```

**Otherwise**, create locally first:

```bash
mkdir <repo-name> && cd <repo-name> && git init
```

The researcher can push to GitHub later in phase 6.

## 3.2 Copy and organize selected files

Show the researcher the list of files you're about to copy and the target structure. Confirm before copying.

Create the target directories first, then copy. Example — adapt to what's actually being published:

```bash
mkdir -p paper/figures paper/build code/src code/scripts data environment supplementary
cp ../working-repo/paper/main.tex paper/
cp ../working-repo/paper/*.bib paper/
cp ../working-repo/figures/*.pdf paper/figures/
cp -r ../working-repo/src/ code/src/
cp ../working-repo/scripts/generate_*.py code/scripts/
cp ../working-repo/data/results.csv data/
cp ../working-repo/requirements.txt environment/
```

Use the file list from phase 2 — copy only what the researcher approved. Organize into the directory layout defined in [PROTOCOL.md § Repository layout](../../PROTOCOL.md#repository-layout). Not every directory is required — adapt to what is actually being published. See [`paper-types.md`](paper-types.md) for format-specific minimums.

**Single source of truth.** Each file lives in exactly one place. No duplicates, no ambiguity about which version is current.

**Update all internal references** — imports, file paths in scripts, `\includegraphics` paths in LaTeX, data paths in notebooks. These will differ from the working repo's paths.

**Handle large files:**

- Files over 50 MB: suggest Git LFS or external hosting (Hugging Face, Zenodo).
- Generated files that can be reproduced: add to `.gitignore` and document the generation command.

**Verify external data links.** For every external data URL identified in phase 1 (Hugging Face, Zenodo, Figshare, etc.):

- Test accessibility: `curl -sIL <url>` (follow redirects), or platform commands (`huggingface-cli download --dry-run`, etc.).
- Report results to the researcher: "Link X returned 200 OK" or "Link Y returned 404 — is this still the right URL?"
- Ask the researcher to confirm each link works (some require authentication the agent doesn't have).
- Record verified/flagged status in `supplementary/checklist.md`.

**Create a `.gitignore`** tailored to the repo — build artifacts, generated files, sensitive files, OS files.

**Copy supplementary materials:**

- If research context was extracted in phase 2, copy it into `supplementary/` now.
- For `supplementary/authors-note.md`: ask the researcher what message they want to leave for readers — what should someone know that isn't in the paper? Draft from their answer and the phase 2 interview, then show them for revision. This is their voice, not the agent's.
- Copy any approved slides, talks, posters into `supplementary/materials/`.
- Copy [`template/publication-checklist.md`](../../template/publication-checklist.md) to `supplementary/checklist.md` and adapt it by removing sections that do not apply.

**Create skills.** If the researcher defined skills in phase 2, create `skills/<name>/SKILL.md` for each, with `name` and `description` in frontmatter and step-by-step instructions in the body.

Tell the researcher what was copied and how it is organized. Flag anything that needed special handling (large files, updated paths, broken data links).

### Structure validation

Invoke `/validate-publication --stage structure` — checks file paths, folder structure, sensitive files, data links. Fix any errors (search for `REVIEW: error` markers — `<!-- REVIEW:` in Markdown, `# REVIEW:` in code). Show warnings to the researcher.

## 3.3 Verify the code works

Tell the researcher you're testing that everything runs with the new paths.

- **Paper compilation.** Run the build command and check it succeeds (if the format compiles).
- **Figure generation.** Run each figure script and verify it produces output.
- **Tests.** If the repo has tests, run them.
- **Notebooks.** Execute in order and check for errors.
- **Imports.** Verify import paths resolve with the new structure.

Fix anything that broke from the copy/reorganization. Report to the researcher: what passed, what needed fixing, what you changed.

## Handoff

Summarise what the publication repo now contains. Next: [`draft.md`](draft.md).
