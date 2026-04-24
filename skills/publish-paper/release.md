# Phases 5–6 — Final review and Release

Run the full validation sweep, walk the checklist, confirm, commit, tag, push, record in `.publications.md`. **This is the point of no return** — once pushed, the publication is public. Each remote action requires its own explicit confirmation.

Invoked from [`SKILL.md`](SKILL.md) after phase 4. Follow the cross-cutting principles declared there.

## Phase 5 — Final review

### 5.1 Full validation

Invoke `/validate-publication --stage full` — factuality, privacy, paths, consistency, substance, and README↔AGENTS.md cross-checks. Fix any errors before showing results to the researcher.

### 5.2 Walk the researcher through the final state

Present the final state **one piece at a time**, not as a single wall of information.

1. **File inventory.** Show what's included and what was excluded. Ask: "Is this the right set of files? Anything missing or anything that shouldn't be here?"
2. **`AGENTS.md` and `README.md`.** Briefly confirm they still read correctly after all revisions — this is a staleness check, not a full re-review (that was phase 4).
3. **Supplementary materials.** List what's in `supplementary/`. Ask: "Are you comfortable with all of this being public?"
4. **Validation results.** Show any remaining warnings from the validation sweep. Walk through each one — don't just list them.

Wait for the researcher to engage with each item. If they say "all good" without engaging, ask about one specific thing — e.g. "I want to double-check: the supplementary materials include [X]. Are you sure that should be public?"

### 5.3 Walk the checklist

Walk through `supplementary/checklist.md` with the researcher as the final quality gate. Go through each item and mark them off. Flag any unchecked items — the researcher decides whether to resolve or mark N/A before proceeding.

Do NOT proceed until the researcher has explicitly confirmed they reviewed the files, the `AGENTS.md`, and the supplementary materials.

## Phase 6 — Release

### 6.1 Confirm and publish

Before doing anything in this step, present a concrete summary. This is the point of no return; the confirmation must be specific, not a generic "should I proceed?"

Fill in the actual values and show:

```
PUBLICATION SUMMARY — please review before I publish:

  Repo name:    <repo-name>
  Visibility:   PUBLIC — anyone on the internet can see this
  Version:      v1.0.0
  Tag:          v1.0.0

  Files included (<N> files):
    paper/          — <paper source format>, figures, bibliography
    code/           — <brief description>
    data/           — <brief description>
    environment/    — <dependencies file>
    supplementary/  — <list which files: know-how, authors-note, sessions, checklist>
    skills/         — <list skill names, or "none">
    AGENTS.md       — paper agent instructions
    README.md       — public README

  Files NOT included (stayed in working repo):
    <list key excluded files/directories, or "nothing excluded">

  External data links:
    <list any URLs that will be referenced, or "none">

  Checklist status:
    <N>/<M> items checked — <list any unchecked items>

  What happens next:
    1. Commit all files to the publication repo
    2. Tag as v1.0.0
    3. Push to GitHub as a PUBLIC repository
    4. Create a GitHub release (v1.0.0)
    5. Record this release in the working repo (.publications.md)
```

**Wait for the researcher to explicitly confirm.** A clear "yes", "go ahead", "publish it", or equivalent. Do NOT proceed on ambiguous responses like "looks good" or "ok" — ask: "Just to be clear — shall I push this as a public repo now?"

Do NOT proceed without unambiguous confirmation.

After confirmation, commit and tag locally. This does not push anything yet:

```bash
cd <publication-repo>
git add -A
git commit -m "Initial publication"
git tag -a v1.0.0 -m "Paper agent v1.0.0"
```

Tell the researcher: "Everything is committed and tagged locally. Nothing has been pushed yet."

**Separate confirmation before each remote action.** Each push or remote operation requires its own confirmation — do not chain them.

**If `gh` is available and the repo isn't on GitHub yet:**

Ask: "Ready to create the public GitHub repo and push? This makes everything visible."
```bash
gh repo create <repo-name> --public --source . --push
```

Then ask: "Repo is live. Shall I also create a GitHub release tagged v1.0.0?"
```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If the repo is already on GitHub:**

Ask: "Ready to push to GitHub? This makes everything visible."
```bash
git push origin main --tags
```

Then ask: "Push complete. Shall I also create a GitHub release tagged v1.0.0?"
```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Paper agent publication"
```

**If `gh` is not available**, tell the researcher what to run manually:

- Push: `git remote add origin <url> && git push -u origin main --tags`
- Create the release on GitHub's web UI: Releases → Create a new release → tag `v1.0.0`.

Tell the researcher the publication is live and share the repo URL.

### 6.2 Record the release in the working repo

After the publication is live, switch back to the **working repo** and record the release in `.publications.md`. This ensures that future sessions know a publication repo exists — no need to ask the researcher or guess.

**If `.publications.md` doesn't exist**, create it (the template lives at [`template/publications.md`](../../template/publications.md)):

```markdown
# Publications

Repos created from this working repo via the Agentic Publication Protocol.

| Repo | Version | Date | Notes |
|------|---------|------|-------|
| [<repo-name>](<repo-url>) | v1.0.0 | YYYY-MM-DD | Initial publication |
```

**If `.publications.md` already exists**, append a new row:

```markdown
| [<repo-name>](<repo-url>) | v2.0.0 | YYYY-MM-DD | Updated results, new figures |
```

Commit in the working repo:

```bash
cd <working-repo>
git add .publications.md
git commit -m "Record publication: <repo-name> v1.0.0"
```

This file is the link between the working repo and its publication repos. [`gather.md`](gather.md) reads it to detect previous versions automatically on the next run.

## Handoff

Report to the researcher: the publication URL, the tag, and the release page. Done.
