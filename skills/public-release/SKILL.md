---
name: public-release
description: Perform the lightweight final author review/freeze gate after full APP validation, then either publish a real tagged APP release with manifest or record a developer-sandbox outcome without public compliance records.
---

# Public Release

Use this after `/validate-publication --stage full`. This skill performs final author approval/freeze and then the final outcome.

It is not a second validator. If final review finds a substantive issue, stop and return to `prepare-staging`, `define-paper-agent`, or `validate-publication`.

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

