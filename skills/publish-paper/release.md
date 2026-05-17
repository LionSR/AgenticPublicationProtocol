# Phases 5-6 — Final Review and Final Outcome

Phase 5 is shared by real publication mode and developer-sandbox mode. Phase 6 is the only branch:

- **Real publication mode:** promote the validated `publication-staging/` tree to a public repo, tag/version it, create the verifiable APP publication manifest, and record the public release.
- **Developer sandbox mode:** record an implementation test result, optionally preserve logs or failure state, and reset/preserve the sandbox according to the test plan. Do not create public repos or APP compliance records.

## Phase 5 — Final review and staging freeze

### 5.1 Full validation from staging root

Invoke `/validate-publication --stage full` with `publication-staging/` as the effective repository root — APP structure, privacy, paths, clear factual consistency, README↔AGENTS.md cross-checks, validation status, and reader-agent usability. Fix any errors before showing the validation report to the researcher.

Save the final validation report as `publication-staging/supplementary/validation-report.md`. The real publication manifest will include the SHA-256 hash of this report. If validation fails, do not proceed to release.

Also check that `publication-staging/` has no dependency on the private parent repo:

- no commands that require files outside staging;
- no absolute private paths;
- no references to unpublished notes, drafts, or private remotes;
- no symlinks that escape staging;
- no generated artifacts that are required but ignored or missing.
- `code/figure-reproduction/README.md` exists for papers with generated figures/tables, lists every paper figure/table, and matches `AGENTS.md`/README figure-reproduction summaries.

### 5.2 Test/load the paper agent from staging root

Before public release, test the candidate as a reader agent would see it. Use `/load-paper-agent` in local staging mode, or manually perform the equivalent:

```bash
cd publication-staging
```

Then read `AGENTS.md`, `README.md`, the ground-truth paper file, `supplementary/`, and any `skills/`. Confirm that a fresh agent can answer basic questions, identify the ground truth, understand what it can run, and follow any reproduction commands without needing the parent repo.

For real publication mode, this is the final check that the public repo will work. For dev-sandbox mode, this is the key implementation test of the protocol.

### 5.3 Walk the researcher through the final staged state

Present the final staged state **one piece at a time**, not as a single wall of information.

1. **File inventory.** Show what's included in `publication-staging/` and what stayed outside it. Ask: "Is this the right set of files? Anything missing or anything that shouldn't be here?"
2. **`AGENTS.md` and `README.md`.** Briefly confirm they still read correctly after all revisions — this is a staleness check, not a full re-review (that was phase 4).
3. **Supplementary materials.** List what's in `publication-staging/supplementary/`. Ask: "Are you comfortable with all of this being public?" In dev-sandbox mode, phrase this as "safe for this sandbox test" if the fixture is not intended for publication.
4. **Validation results.** Show any remaining warnings from the validation sweep. Walk through each one — don't just list them.
5. **Figure reproduction.** Summarise counts from `code/figure-reproduction/README.md`: total figures/tables, direct scripts, reproduced, runs-but-differs, blocked, and manual-only. Walk through any non-`reproduced` items.
6. **Paper-agent test.** Summarise what the local staging-root test showed.

Wait for the researcher to engage with each item. If they say "all good" without engaging, ask about one specific thing — e.g. "I want to double-check: the supplementary materials include [X]. Are you sure that should be in the staged release tree?"

### 5.4 Confirm process completion and author approval

Use your internal phase checklist to confirm phases 1-5 are complete:

- Phase 1 — Understand: canonical paper and prior-version state identified.
- Phase 2 — Discuss: key results, include/exclude decisions, supplementary materials, and repo name confirmed.
- Phase 3 — Build staging: approved files copied, paths updated, structure validation run.
- Phase 3 figure reproduction: `code/figure-reproduction/README.md` created when applicable, direct scripts attempted for every figure/table, and statuses documented.
- Phase 4 — Paper-agent docs: `AGENTS.md`, `CLAUDE.md`, and `README.md` drafted and researcher-reviewed.
- Phase 5 — Final review: full validation report saved, local paper-agent test performed, remaining warnings/manual limitations reviewed.

Do not write this process checklist into `publication-staging/`. It is an internal workflow control, not publication content.

Do not proceed until the researcher has explicitly confirmed they reviewed the staged files, `AGENTS.md`, supplementary materials, validation results, and paper-agent test summary.

Record the human approval statement for real publication mode. At minimum capture:

- approval date;
- approving author names;
- a plain statement that the listed authors approve this staged tree for public APP release.

### 5.5 Freeze the validated release tree

Once approved, freeze the staging tree. At minimum:

- record the validation date;
- record the validation report path and SHA-256 hash;
- record the human approval statement;
- record the exact `publication-staging/` tree hash or archive checksum if available;
- avoid further edits except controlled fixes that return to phase 5.1.

The final public release in real publication mode must equal this validated tree.

## Phase 6 — Final outcome

Determine the mode before doing anything irreversible.

### 6A. Real publication mode

**Point of no return** — once pushed, the publication is public. Each remote action requires its own explicit confirmation.

Before doing anything in this step, present a concrete summary. The confirmation must be specific, not a generic "should I proceed?"

Fill in the actual values and show:

```text
PUBLICATION SUMMARY — please review before I publish:

  Source tree:   publication-staging/
  Repo name:     <repo-name>
  Visibility:    PUBLIC — anyone on the internet can see this
  Version:       v1.0.0
  Tag:           v1.0.0

  Files included (<N> files):
    paper/          — <paper source format>, figures, bibliography
    code/           — <brief description>
    data/           — <brief description>
    environment/    — <dependencies file>
    supplementary/  — <list which files: know-how, authors-note, sessions, validation-report, materials>
    skills/         — <list skill names, or "none">
    AGENTS.md       — paper agent instructions
    README.md       — public README

  Files NOT included (stayed outside publication-staging/):
    <list key excluded files/directories, or "nothing excluded">

  External data links:
    <list any URLs that will be referenced, or "none">

  Process status:
    Phases 1-5 complete — <list any warnings or manual limitations>

  Staging validation:
    <validation status, local paper-agent test status, tree hash/checksum if available>

  APP verification:
    Manifest:      APP_PUBLICATION.json will be attached to the GitHub Release
    Identifier:    app_publication_id will be computed after the public commit exists
    Evidence:      full validation report + human author approval

  What happens next:
    1. Export the validated publication-staging/ tree to the public repo
    2. Commit all files to the public publication repo
    3. Compute commit/tree/report hashes
    4. Create APP_PUBLICATION.json with app_publication_id
    5. Tag as v1.0.0
    6. Push to GitHub as a PUBLIC repository
    7. Create a GitHub release (v1.0.0) with APP_PUBLICATION.json attached
    8. Record this release in the working repo (.publications.md) with URL, tag, commit/tree hash, and app_publication_id
```

**Wait for the researcher to explicitly confirm.** A clear "yes", "go ahead", "publish it", or equivalent. Do not proceed on ambiguous responses like "looks good" or "ok" — ask: "Just to be clear — shall I publish this validated staging tree as a public repo now?"

Do not proceed without unambiguous confirmation.

#### 6A.1 Create or update the public repo from staging

Create a separate public publication repo or working directory whose contents equal the validated `publication-staging/` tree. Use a structured copy tool that preserves file contents and excludes parent-repo-only metadata. For example:

```bash
rsync -a --delete publication-staging/ ../<repo-name>/
cd ../<repo-name>
git init
git add -A
git commit -m "Initial APP publication"
```

For a revision, update the existing public repo working copy from `publication-staging/`, commit, and tag the new version.

After committing locally, compute the immutable release facts:

```bash
COMMIT_SHA=$(git rev-parse HEAD)
TREE_SHA=$(git rev-parse HEAD^{tree})
REPORT_SHA=$(shasum -a 256 supplementary/validation-report.md | awk '{print $1}')
```

Create a release manifest payload that excludes `app_publication_id`, using the exact public repo URL, tag, commit SHA, tree SHA, validation report hash, and recorded human approval. Example shape:

```json
{
  "protocol": "agentic-publication-protocol",
  "protocol_version": "0.1.0",
  "manifest_version": "1",
  "publication_type": "app-publication",
  "repo_url": "https://github.com/owner/repo",
  "tag": "v1.0.0",
  "commit": "<COMMIT_SHA>",
  "tree": "<TREE_SHA>",
  "validation": {
    "validated_by": "validate-publication",
    "validator_protocol_version": "0.1.0",
    "stage": "full",
    "result": "passed",
    "validated_at": "YYYY-MM-DD",
    "validation_report_sha256": "<REPORT_SHA>"
  },
  "human_approval": {
    "approved": true,
    "approved_at": "YYYY-MM-DD",
    "approved_by": ["Author Name"],
    "approval_statement": "The listed authors approved this release as an APP publication."
  }
}
```

Canonicalize the payload with sorted keys and compact JSON, then hash it:

```bash
jq -S -c . APP_PUBLICATION.payload.json > APP_PUBLICATION.payload.canonical.json
APP_ID="app-v1:sha256:$(shasum -a 256 APP_PUBLICATION.payload.canonical.json | awk '{print $1}')"
jq --arg app_id "$APP_ID" '. + {app_publication_id: $app_id}' \
  APP_PUBLICATION.payload.json > APP_PUBLICATION.json
```

The final `APP_PUBLICATION.json` should follow the manifest schema in [`PROTOCOL.md` § Verified APP publication manifest](../../PROTOCOL.md#verified-app-publication-manifest). Keep `APP_PUBLICATION.payload.json` and `APP_PUBLICATION.payload.canonical.json` out of the public repo unless the researcher explicitly wants to include them; `APP_PUBLICATION.json` is a release asset, not part of the committed tree.

Now create the annotated tag. Include the APP publication ID in the tag message:

```bash
git tag -a v1.0.0 -m "APP publication v1.0.0

app_publication_id: ${APP_ID}
commit: ${COMMIT_SHA}
tree: ${TREE_SHA}"
```

Tell the researcher: "Everything is committed and tagged locally in the public publication repo, and APP_PUBLICATION.json has been generated. Nothing has been pushed yet."

#### 6A.2 Remote publication

Separate confirmation before each remote action. Do not chain remote operations.

If `gh` is available and the repo is not on GitHub yet, ask: "Ready to create the public GitHub repo and push? This makes everything visible."

```bash
gh repo create <repo-name> --public --source . --remote origin --push
git push origin --tags
```

Then ask: "Repo is live. Shall I also create a GitHub release tagged v1.0.0 and attach APP_PUBLICATION.json?"

```bash
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "APP paper-agent publication

app_publication_id: ${APP_ID}" \
  APP_PUBLICATION.json
```

If the repo is already on GitHub, ask: "Ready to push to GitHub? This makes everything visible."

```bash
git push origin main --tags
```

Then ask: "Push complete. Shall I also create a GitHub release tagged v1.0.0 and attach APP_PUBLICATION.json?"

```bash
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "APP paper-agent publication

app_publication_id: ${APP_ID}" \
  APP_PUBLICATION.json
```

If `gh` is not available, tell the researcher what to run manually:

- Push: `git remote add origin <url> && git push -u origin main --tags`
- Create the release on GitHub's web UI: Releases -> Create a new release -> tag `v1.0.0`; attach `APP_PUBLICATION.json` as a release asset.

After the release exists, verify the release asset is downloadable and matches the local manifest:

```bash
gh release download v1.0.0 --pattern APP_PUBLICATION.json --dir /tmp/app-verify
diff APP_PUBLICATION.json /tmp/app-verify/APP_PUBLICATION.json
```

Tell the researcher the publication is live and share the repo URL, release URL, and `app_publication_id`.

#### 6A.3 Record the public release in the working repo

After the publication is live, switch back to the **working repo** and record the release in `.publications.md`. This ensures that future sessions know a publication repo exists — no need to ask the researcher or guess.

Record enough information to attach APP compliance to a concrete public version:

- public repo URL;
- version/tag;
- date;
- commit hash and/or tree hash;
- `app_publication_id`;
- brief notes.

If `.publications.md` doesn't exist, create it (the template lives at [`template/publications.md`](../../template/publications.md)):

```markdown
# Publications

Repos created from this working repo via the Agentic Publication Protocol.

| Repo | Version | Date | Commit/Tree | APP ID | Notes |
|------|---------|------|-------------|--------|-------|
| [<repo-name>](<repo-url>) | v1.0.0 | YYYY-MM-DD | `<commit>` / `<tree>` | `app-v1:sha256:<hash>` | Initial publication |
```

If `.publications.md` already exists, append a new row:

```markdown
| [<repo-name>](<repo-url>) | v2.0.0 | YYYY-MM-DD | `<commit>` / `<tree>` | `app-v1:sha256:<hash>` | Updated results, new figures |
```

Commit in the working repo:

```bash
cd <working-repo>
git add .publications.md
git commit -m "Record APP publication: <repo-name> v1.0.0"
```

Report to the researcher: the publication URL, the tag, the release page, the commit/tree hash, and the `app_publication_id`.

### 6B. Developer sandbox mode

Dev-sandbox mode is an implementation-testing workflow, not a publication workflow. It uses the same prepare and validate standards up through phase 5, then substitutes a sandbox outcome for public release.

Before finalizing the sandbox run, show:

```text
DEV-SANDBOX RESULT SUMMARY:

  Sandbox target:          <path>
  Candidate tree:          publication-staging/
  Test case:               <new publication example | revision example | fixture name>
  Validation status:       <passed | failed>
  Paper-agent test status: <passed | failed>
  Tree hash/checksum:      <hash if available>

  Outcome:
    <record success | preserve failing state for debugging | reset sandbox>

  Important:
    No public repo will be created.
    No APP_PUBLICATION.json manifest will be created.
    No APP compliance record will be written.
```

Record the implementation test result in the agreed sandbox log or test notes for the protocol implementation. Include:

- date;
- protocol/skill version or commit;
- sandbox target;
- source fixture/example;
- validation result;
- paper-agent test result;
- failures and fixes needed, if any.

If the run passed and the sandbox policy says to reset, reset the reusable sandbox to baseline. If the run failed or the researcher wants to inspect it, preserve `publication-staging/` and relevant logs temporarily.

Never write `.publications.md` as a compliance record in dev-sandbox mode. If a sandbox log is needed, use an implementation-test location whose name makes clear it is not an APP publication record.
