# Real Publication Mode

Public release is irreversible. Ask for explicit confirmation before every remote action.

1. Confirm the recorded publication `owner/repo` and release tag with the author. Use the repo, tag, and normalized version recorded during `reproduce-results` unless the author explicitly changes them. If the author changes the repo or tag at this step, rerun validation before release because paper URL consistency may have changed. Ensure `AGENTS.md` `version` matches the tag normalization rule.
2. Show a concrete publication summary:
   - source `publication-staging/`;
   - repo `owner/repo`, derived release URL, and public visibility;
   - version/tag;
   - included/excluded files;
   - validation status and report hash;
   - author approval;
   - what remote actions will happen.
3. Export the validated staging tree to the public repo/worktree, preserving contents and excluding private parent metadata.
4. Commit locally and compute:
   - commit SHA;
   - tree SHA;
   - validation report SHA-256.
5. Create `APP_PUBLICATION.json` as a GitHub Release asset payload following `PROTOCOL.md` verified manifest schema. Compute `app_publication_id` from the canonical payload excluding the ID.
6. Create an annotated tag containing the APP ID, commit, and tree.
7. Draft release notes and get author approval.
8. Confirm before pushing. Push repo and tags.
9. Confirm before creating GitHub Release. Attach `APP_PUBLICATION.json`.
10. Verify the release asset downloads and matches the local manifest.
11. Record the release in the working repo `.publications.md` using `template/publications.md`.
12. Optionally offer `/create-paper-page`.

Do not change the frozen staging tree during this step.

