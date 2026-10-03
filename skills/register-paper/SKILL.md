---
name: register-paper
description: Submit a released APP paper to the registry at agenticpapers.app on behalf of the author. Use after creating a verified GitHub release (public repository, tag, and APP_PUBLICATION.json asset), or when an author requests registration of an existing release.
---

# Register Paper

Submit a released APP paper to the [APP registry](https://agenticpapers.app/). The registry catalogs APP publications and verifies releases during submission. Listing is optional and distinct from protocol compliance.

## When to use

- Offered by `release-outcome` after a public release succeeds and its release asset is verified.
- Standalone execution when an author requests registration of an existing release.

Do not use this skill in developer sandbox mode. Do not submit a release before publishing it. The registry requires:

- A public GitHub repository;
- A published release at a specific tag (for example, `https://github.com/OWNER/REPO/releases/tag/v1.0.0`);
- An `APP_PUBLICATION.json` asset attached to the release.

If any prerequisite is missing, stop and report the missing item. Do not create or modify releases in this skill; use `release-outcome`.

## Request author approval

Submission creates a public issue in [LionSR/app-registry](https://github.com/LionSR/app-registry) under the account of the submitting user. Complete these steps before submission:

1. Confirm the release URL with the author.
2. Ask the author to read and accept the [terms of use](https://agenticpapers.app/terms/).
3. If the authenticated user cannot push to the repository, confirm that the user has permission from the authors to submit.

If the author declines, abort the procedure. The author can submit later through the [submission portal](https://agenticpapers.app/submit/).

## Submit

Follow the instructions on [Register a paper with an agent](https://agenticpapers.app/agents/):

1. Request an OAuth device code from GitHub for the registry client.
2. Direct the author to open `https://github.com/login/device` and enter the user code.
3. Poll the token endpoint until GitHub returns an access token.
4. Send the release URL to the registry endpoint `/submit` with `"accept_terms": true`. Set `"authors_permission": true` when third-party submission applies.

The registry accepts only tokens issued through this device flow. Do not store or persist the access token in any file.

## After submission

The response returns the issue number of the submission. The registry repository is public, so read the result without authentication:

```bash
curl -s https://api.github.com/repos/LionSR/app-registry/issues/<number>/comments
```

Read the last comment from the registry. If the GitHub CLI is authenticated, `gh issue view <number> --repo LionSR/app-registry --comments` shows the same comments.

Each registry response comment concludes with an `app-registry-status` JSON block. The `state` field contains one of:
- `accepted`: The paper is indexed. The block provides the assigned registry ID.
- `awaiting-editor`: The submission requires manual review by an editor.
- `checks-failed`: Automated verification checks failed. The `checks` array describes each failure.
- `already-listed`: The release is already registered.
- `declined`: The registry rejected the submission.

Inform the author of the status and issue URL.

If verification checks fail:
- For transient infrastructure failures (such as temporary rate limits or network errors), the author can post `/recheck` as a comment on the submission issue.
- For publication errors (such as missing files, invalid manifests, or metadata discrepancies), resolve the issues and create a new tagged release via `release-outcome`. Submit the new release URL as a separate submission. Do not use `/recheck` to evaluate a different tag.

When `.publications.md` exists in the local repository, record the submission issue URL and assigned registry ID in the `Notes` column of the release entry.
