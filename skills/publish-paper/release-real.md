# Phase 6A — Real Publication Mode

**Point of no return** — once pushed, the publication is public. Each remote action requires its own explicit confirmation.

Before doing anything in this step, present a concrete summary. The confirmation must be specific, not a generic "should I proceed?"

Before showing the summary, choose the intended `<tag>` with the researcher (e.g. `v1.0.0` for a first release, `v2.0.0` for a subsequent one). Reuse that exact tag throughout phase 6.

Fill in the actual values, including `<tag>` and the matching AGENTS.md `version`, and show:

```text
PUBLICATION SUMMARY — please review before I publish:

  Source tree:   publication-staging/
  Repo name:     <repo-name>
  Visibility:    PUBLIC — anyone on the internet can see this
  Version:       <version>  (e.g. 1.0.0 for a first release)
  Tag:           <tag>      (e.g. v1.0.0; reused throughout phase 6)

  Files included (<N> files):
    paper/          — <paper source format>, figures, bibliography
    code/           — <brief description>
    data/           — <brief description>
    environment/    — README.md plus dependency manifests/lockfiles/setup scripts when executable code or build tooling exists
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
    5. Tag as <tag>
    6. Push to GitHub as a PUBLIC repository
    7. Create a GitHub release (<tag>) with release notes and APP_PUBLICATION.json attached
    8. Record this release in the working repo (.publications.md) with URL, tag, commit/tree hash, and app_publication_id
```

**Wait for the researcher to explicitly confirm.** A clear "yes", "go ahead", "publish it", or equivalent. Do not proceed on ambiguous responses like "looks good" or "ok" — ask: "Just to be clear — shall I publish this validated staging tree as a public repo now?"

Do not proceed without unambiguous confirmation.

## 6A.1 Create or update the public repo from staging

Create a separate public publication repo or working directory whose contents equal the validated `publication-staging/` tree. Use a structured copy tool that preserves file contents and excludes parent-repo-only metadata. For example:

```bash
rsync -a --delete publication-staging/ ../<repo-name>/
cd ../<repo-name>
git init
git add -A
git commit -m "Initial APP publication"
```

For a revision, update the existing public repo working copy from `publication-staging/`, commit, and tag the new version after APP_PUBLICATION.json is generated.

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
  "tag": "<tag>",
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
git tag -a <tag> -m "APP publication <tag>

app_publication_id: ${APP_ID}
commit: ${COMMIT_SHA}
tree: ${TREE_SHA}"
```

Tell the researcher: "Everything is committed and tagged as `<tag>` locally in the public publication repo, and APP_PUBLICATION.json has been generated. Nothing has been pushed yet."

Draft GitHub release notes before creating the release. Release notes are where edit/version history lives, and the only place readers see what changed between versions.

For a **first release** (`<tag>`, typically `v1.0.0`), summarize the publication itself: paper title, authors, a one-line statement of what the agent can do, and links (arXiv/DOI/PDF) if available.

For a **subsequent release**, base the notes on what actually changed:

- Read `.publications.md` in the working repo to find the previous publication's repo URL and tag.
- If this is an update to the same public publication repo, compare the previous tag to the new committed tree from inside that public repo working copy: `git log <prev-tag>..HEAD --oneline`, then inspect the changed files.
- If this release is being made in a new public repo while `.publications.md` points to an older publication repo, shallow-clone the old repo for historical context (`git clone --depth=50 <prev-repo-url> /tmp/prev-pub`) and inspect its previous tag. Do not run `git log <prev-tag>..HEAD` in a repo that does not contain `<prev-tag>`.
- Ask the researcher, in their own words: "What changed in this version that a reader should know about?" Cover: results that were added/revised, figures that were redrawn, code that was refactored in ways readers will notice, data updates.

Draft the notes and show them to the researcher for revision. Do not auto-generate boilerplate like "Bug fixes and improvements." After approval, write them to a file path that includes the actual tag so the later `gh release create` command can read them:

```bash
cat > /tmp/release-notes-<tag>.md <<'NOTES'
<the drafted notes>
NOTES
```

## 6A.2 Remote publication

Separate confirmation before each remote action. Do not chain remote operations.

If `gh` is available and the repo is not on GitHub yet, ask: "Ready to create the public GitHub repo and push? This makes everything visible."

```bash
gh repo create <repo-name> --public --source . --remote origin --push
git push origin --tags
```

Then ask: "Repo is live. Shall I also create a GitHub release tagged <tag> and attach APP_PUBLICATION.json?" (where `<tag>` is the tag applied above, e.g. `v1.0.0` for the first release or `v2.0.0` for a subsequent one).

```bash
gh release create <tag> \
  --title "<tag>" \
  --notes-file /tmp/release-notes-<tag>.md \
  APP_PUBLICATION.json
```

If the repo is already on GitHub, ask: "Ready to push to GitHub? This makes everything visible."

```bash
git push origin main --tags
```

Then ask: "Push complete. Shall I also create a GitHub release tagged <tag> and attach APP_PUBLICATION.json?"

```bash
gh release create <tag> \
  --title "<tag>" \
  --notes-file /tmp/release-notes-<tag>.md \
  APP_PUBLICATION.json
```

If `gh` is not available, tell the researcher what to run manually:

- Push: `git remote add origin <url> && git push -u origin main --tags`
- Create the release on GitHub's web UI: Releases → Create a new release → tag `<tag>` (the value chosen above; e.g. `v1.0.0`).
- Paste the release notes from `/tmp/release-notes-<tag>.md` into the release description field so the drafted notes aren't lost.
- Attach `APP_PUBLICATION.json` as a release asset.

After the release exists, verify the release asset is downloadable and matches the local manifest:

```bash
gh release download <tag> --pattern APP_PUBLICATION.json --dir /tmp/app-verify
diff APP_PUBLICATION.json /tmp/app-verify/APP_PUBLICATION.json
```

Tell the researcher the publication is live and share the repo URL, release URL, and `app_publication_id`.

## 6A.3 Record the public release in the working repo

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
| [<repo-name>](<repo-url>) | <tag> | YYYY-MM-DD | `<commit>` / `<tree>` | `app-v1:sha256:<hash>` | Initial publication |
```

If `.publications.md` already exists, append a new row:

```markdown
| [<repo-name>](<repo-url>) | <tag> | YYYY-MM-DD | `<commit>` / `<tree>` | `app-v1:sha256:<hash>` | Updated results, new figures |
```

Commit in the working repo:

```bash
cd <working-repo>
git add .publications.md
git commit -m "Record APP publication: <repo-name> <tag>"
```

Report to the researcher: the publication URL, the tag, the release page, the commit/tree hash, and the `app_publication_id`.

Optionally offer to run [`/create-paper-page`](../create-paper-page/SKILL.md) to add a GitHub Pages project page for the published paper. This is a convenience add-on, not an APP compliance requirement. Do not block the publication record or manifest on whether a project page exists.
