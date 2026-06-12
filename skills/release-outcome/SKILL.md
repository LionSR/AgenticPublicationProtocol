---
name: release-outcome
description: Perform the lightweight final author review/freeze gate after full APP validation, then either publish a real tagged APP release with manifest or record a developer-sandbox outcome without public compliance records.
---

# Release Outcome

Use this after `/validate-publication --stage full`. This skill performs final author approval/freeze and then the final outcome.

It is not a second validator. If final review finds a substantive issue, stop and return to `prepare-staging`, `define-paper-agent`, or `validate-publication`.

## Publication Repo And Paper Link

For real publication mode, settle the public repo and any in-paper link before the release gate, because the paper cannot cite a repo that does not exist yet:

1. Ask the author which public repo will host the release: an existing repo, or a new one created now. The repo may start empty and private and become public at release time. There is no required naming convention; suggest candidates and let the author choose (for example `<papername>.app` — dots are valid in GitHub repo names).
2. Choose the intended release tag with the author now (see `release-real.md` step 1). The tag is predictable before release; the commit SHA is not.
3. Ask whether the paper should reference the publication. The stable link targets are the repo URL, or preferably the tag URL `https://github.com/<owner>/<repo>/releases/tag/<tag>`. Never promise a commit URL in the paper.
4. If the paper needs the link added or changed, update the paper sources and rebuild affected paper artifacts in `publication-staging/` now, then rerun `/validate-publication --stage full` before proceeding — the gate below requires no changes after full validation.

If the author declines an in-paper link, or the link is already correct, nothing changes and validation stands.

## Lightweight Release Gate

Before any release action:

1. Confirm full validation passed, or dev-sandbox blockers are explicitly classified.
2. Confirm required final artifacts exist:
   - `publication-staging/supplementary/validation-report.md`;
   - `publication-staging/supplementary/paper-agent-test.md` for real publication;
   - `publication-staging/LICENSE` for real publication.
3. Confirm no files changed since full validation before freezing; if they changed, rerun validation.
4. Walk the author through the final staged state in plain language:
   - included files/folders;
   - excluded files;
   - ground truth versus optional context;
   - warnings, manual checks, sandbox-only deferrals;
   - what becomes public in real mode.
5. Record approval:
   - approval date;
   - approving author names;
   - approval statement;
   - validation report SHA-256;
   - staging tree hash/checksum when available.
6. Freeze the tree. After freeze, do not edit without returning to validation.

## Final Outcome

Choose exactly one:

- real publication mode: follow `release-real.md`;
- developer sandbox mode: follow `release-sandbox.md`.

Do not mix modes. Dev-sandbox must not create a public repo, `APP_PUBLICATION.json`, or `.publications.md` compliance record.

