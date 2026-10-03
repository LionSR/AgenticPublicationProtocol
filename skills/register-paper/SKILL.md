---
name: register-paper
description: List a released APP paper in the APP registry at agenticpapers.app, on the author's behalf. Use after a real APP release exists on GitHub (public repo, tag, and APP_PUBLICATION.json release asset), when the author wants the paper listed, or when they ask to register or submit an existing APP release.
---

# Register Paper

Submit a released APP paper to the [APP registry](https://agenticpapers.app/), which lists APP papers and checks each release before listing it. Listing is optional and not part of APP compliance.

## When to use

- Offered by `release-outcome` after a real release succeeds and its release asset is verified.
- Standalone, when an author asks to list an existing APP release.

Do not use in developer sandbox mode, and do not submit a release that does not exist yet. The registry needs all of:

- a public GitHub repository;
- a published release at a tag, for example `https://github.com/OWNER/REPO/releases/tag/v1.0.0`;
- the `APP_PUBLICATION.json` asset attached to that release.

If any is missing, stop and say which. Do not create or change the release here; that is `release-outcome`.

## Ask the author first

Submitting opens a public issue on [LionSR/app-registry](https://github.com/LionSR/app-registry) in the author's name. Before submitting:

1. Confirm the release URL with the author.
2. Ask them to read the [terms of use](https://agenticpapers.app/terms/) and confirm they agree.
3. If the person signing in cannot push to the paper repository, ask whether they have the authors' permission to submit. Submit only if they confirm.

If the author declines, stop. They can submit later on the [Submit page](https://agenticpapers.app/submit/).

## Submit

Follow the steps on [Register a paper with an agent](https://agenticpapers.app/agents/). That page has the current commands, with the registry's endpoint and sign-in client filled in. In short:

1. Ask GitHub for a sign-in code for the registry (device flow).
2. Ask the author to open `https://github.com/login/device`, sign in, and enter the code.
3. Exchange the device code for a token, polling at the given interval.
4. Send the release URL to the registry's `/submit` endpoint with `"accept_terms": true`, and `"authors_permission": true` only if step 3 above applies.

The registry accepts only tokens from this sign-in; other GitHub tokens, including `gh auth token`, are rejected. Do not store the token or write it to any file.

## After submitting

The reply names the submission issue. Read the outcome with:

```bash
gh issue view <number> --repo LionSR/app-registry --comments
```

Each registry comment ends with a JSON block marked `app-registry-status`. Its `state` is one of `accepted` (listed; the block gives the registry ID), `awaiting-editor`, `checks-failed` (the `checks` list says which failed and why), `already-listed`, or `declined`. Tell the author the result and the issue link. If checks failed, explain what to fix; fixing means a new release, which goes back through `release-outcome`. The author can comment `/recheck` on the issue after fixing.

If the working repo has `.publications.md`, add the issue link, and the registry ID once listed, to the Notes column of that release's row.
