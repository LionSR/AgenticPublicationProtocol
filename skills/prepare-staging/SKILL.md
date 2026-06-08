---
name: prepare-staging
description: Build or revise an APP publication-staging tree from a pre-staging reproduction report, organizing paper, code, data, environment, supplementary materials, licenses, and figure/table reproduction scripts under the protocol layout.
---

# Prepare Staging

Use this after `reproduce-results`. The input is the working repo plus `working/reproduction/reproduction-report.md`. The output is a self-contained APP candidate tree at `publication-staging/`.

Explain to the author that `publication-staging/` is a draft public repository inside the private repo; it is not public yet.

## Process

1. Read `working/reproduction/reproduction-report.md`.
2. Create or revise `publication-staging/`:
   - first release: create from scratch;
   - revision: start from previous public release or coherent existing staging, whichever is cleaner;
   - preserve/summarize any old staging before replacing generated files.
3. Show the author the copy plan and get confirmation before copying.
4. Organize approved files under APP layout:
   - `paper/`, `code/`, `data/`, `environment/`, `supplementary/`, `skills/`;
   - exactly one canonical public location per file;
   - no private parent-repo dependencies or absolute private paths.
5. Create `data/README.md` whenever any dataset is used, local or external.
6. Prepare the environment following `environment.md`.
7. Create/copy `LICENSE` following `licensing.md`.
8. Copy only approved supplementary materials:
   - extracted chat context;
   - `authors-note.md` drafted from author intent;
   - `know-how.md` or materials the author wants public/sandbox-visible;
   - concise experiment notes, lab reports, design notes, or follow-up notes when they are
     publication-safe and directly help readers interpret figures, reproduce checks, understand
     parameter choices, or design next sanity checks;
   - slides, posters, tutorials, or paper-specific skills.
   Select notes rather than copying whole scratch trees. Exclude virtual environments, caches,
   build products, private paths, credentials, abandoned drafts, and notes whose status or authorship
   is unclear. If a note is useful but too broad or private, create a short reader-facing summary in
   `supplementary/` and cite the exact staged code/data/paper anchors it explains.
9. Migrate reproduction wrappers:
   - follow `figure-wrapper-migration.md`;
   - create `publication-staging/code/figure-reproduction/README.md`;
   - rerun scripts from staging root when safe.
10. Run `/validate-publication --stage structure` with `publication-staging/` as effective root.
11. Verify from staging root when safe:
   - environment setup;
   - paper compilation;
   - figure/table scripts marked `reproduced`;
   - tests, notebooks, imports;
   - parent/private path checks.
12. Give the author a plain-language staging summary:
   - what is in each top-level folder;
   - what stayed outside staging;
   - what is ground truth (`paper/`, staged code/data) versus optional context (`supplementary/`);
   - remaining blockers or decisions before paper-agent drafting.

Do not write process checklists into `publication-staging/`; keep workflow status in chat/internal notes.
