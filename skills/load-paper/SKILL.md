---
name: load-paper
description: Load a published paper repository, local publication-staging tree, non-APP paper repository, or arXiv paper into your current project. Use when a user wants to consult, build on, test, import, or discuss a paper. For arXiv IDs or URLs, fetch metadata/source, search for associated public code, and create a protocol-shaped local import before continuing with paper classification.
---

# Load Paper

Load a published paper into your project so you can consult it, reproduce results, and build on the work. This is a reader/import utility, not a required part of publishing or validating an APP publication.

For debugging or exploratory review, this skill can also inspect a local APP candidate such as `publication-staging/`. In that case, do not clone anything; treat the supplied local staging directory as the paper repo root. The `/publish-paper` workflow performs its required final paper-agent smoke test directly from the staging root rather than depending on this loader.

## Triggering

User says something like:
- "Load paper from https://github.com/user/paper-repo"
- "I want to consult the paper at <url>"
- "Add this paper as a sub-agent: <url>"
- "Load arXiv paper 2301.07041"
- "Load this paper from arXiv: https://arxiv.org/abs/2301.07041"
- "Load <arxiv-id> as a paper"
- "Test/load the paper from publication-staging"

## Steps

### 1. Locate or import the paper

If the user supplies a local staging path such as `publication-staging/`, skip cloning:

```bash
cd publication-staging
```

Then continue with the APP compliance and exploration checks below, treating this directory as the repo root. This is a pre-publication test; it does not imply the staged tree is publicly released.

For remote public repos:

```bash
mkdir -p papers/
git clone <url> papers/<repo-name>
```

If the user specifies a version:
```bash
git clone --branch v1.0.0 <url> papers/<repo-name>
```

If the user does not specify a version and the default branch is not exactly at a release tag, the repo can still be explored, but it cannot be verified as an APP publication from that checkout. For APP verification, prefer checking out an explicit release tag. If GitHub release metadata is available, identify the latest release tag and offer to check it out before verification.

If the user gives an arXiv ID or URL instead of a GitHub URL, use the arXiv input mode in [`arxiv.md`](arxiv.md). That mode creates a local import under `papers/arxiv-ARXIV_ID/`, then returns here for APP compliance and exploration checks using that import root.

If the clone fails (private repo, wrong URL), inform the user and ask for the correct URL or access.

### 2. Classify APP status

Do not treat `AGENTS.md` or `CLAUDE.md` alone as proof of APP compliance. Classify the repo into one of three levels:

1. **Agent-readable repo** — has `AGENTS.md`, `CLAUDE.md`, README, or other useful docs, but no verified APP release manifest.
2. **APP-structured candidate** — has `AGENTS.md` with YAML frontmatter containing `protocol: agentic-publication-protocol`, but no verified release manifest.
3. **Verified APP publication** — the current checkout corresponds to a public tagged release with a valid `APP_PUBLICATION.json` release manifest. The manifest must match the repo URL, tag, commit, tree, validation report hash, and human approval record, and its `app_publication_id` must recompute correctly.

Look for agent and human documentation:

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- docs directories or paper-specific instructions if present

If `AGENTS.md` exists, read it and check:

- Does it have YAML frontmatter with `protocol: agentic-publication-protocol`?
- Does the checkout correspond to a tag?
- Is there a release asset named `APP_PUBLICATION.json` for that tag?

If `AGENTS.md` does not exist, still continue. Read `CLAUDE.md`, README, docs, paper files, and code entry points directly. The repo is not APP-structured, but it may still be useful.

For local `publication-staging/`, stop at **APP-structured candidate** at most. Staging can be tested for reader-agent usability, but it is not a verified APP publication because it has no public release manifest.

### 2.1 Verify APP publication manifest

For remote public repos, verify the manifest before calling the repo fully APP-compliant.

Identify the checkout and tag:

```bash
cd <repo-root>
COMMIT_SHA=$(git rev-parse HEAD)
TREE_SHA=$(git rev-parse HEAD^{tree})
TAG=$(git describe --tags --exact-match 2>/dev/null || true)
```

If `TAG` is empty, the checkout is not a verified APP publication. Report it as an APP-structured candidate if `AGENTS.md` has APP frontmatter.

Download the release manifest:

```bash
gh release download "$TAG" --pattern APP_PUBLICATION.json --dir /tmp/app-manifest
```

If `gh` is unavailable, use the GitHub releases API or ask the user to provide the `APP_PUBLICATION.json` release asset. Do not trust a committed `APP_PUBLICATION.json` file as the canonical manifest unless it exactly matches the release asset.

Verify manifest fields:

```bash
jq -e '.protocol == "agentic-publication-protocol"' /tmp/app-manifest/APP_PUBLICATION.json
jq -e '.publication_type == "app-publication"' /tmp/app-manifest/APP_PUBLICATION.json
jq -e --arg tag "$TAG" '.tag == $tag' /tmp/app-manifest/APP_PUBLICATION.json
jq -e --arg commit "$COMMIT_SHA" '.commit == $commit' /tmp/app-manifest/APP_PUBLICATION.json
jq -e --arg tree "$TREE_SHA" '.tree == $tree' /tmp/app-manifest/APP_PUBLICATION.json
jq -e '.validation.stage == "full" and .validation.result == "passed"' /tmp/app-manifest/APP_PUBLICATION.json
jq -e '.human_approval.approved == true' /tmp/app-manifest/APP_PUBLICATION.json
```

Verify the validation report hash if the report is present in the repo:

```bash
REPORT_SHA=$(shasum -a 256 supplementary/validation-report.md | awk '{print $1}')
jq -e --arg report "$REPORT_SHA" '.validation.validation_report_sha256 == $report' \
  /tmp/app-manifest/APP_PUBLICATION.json
```

If the validation report is a release asset rather than committed in the repo, download that asset and hash it instead.

Recompute the APP publication ID per [`PROTOCOL.md` § Canonicalization rules for `app-v1`](../../PROTOCOL.md#canonicalization-rules-for-app-v1). Remove `app_publication_id`, canonicalize with sorted keys, compact output, and non-ASCII characters escaped to `\uXXXX`, then hash and compare:

```bash
jq -S -c -a 'del(.app_publication_id)' /tmp/app-manifest/APP_PUBLICATION.json \
  > /tmp/app-manifest/APP_PUBLICATION.payload.canonical.json
COMPUTED_ID="app-v1:sha256:$(shasum -a 256 /tmp/app-manifest/APP_PUBLICATION.payload.canonical.json | awk '{print $1}')"
MANIFEST_ID=$(jq -r '.app_publication_id' /tmp/app-manifest/APP_PUBLICATION.json)
test "$COMPUTED_ID" = "$MANIFEST_ID"
```

The `-a` flag is required for cross-platform reproducibility; without it, manifests containing non-ASCII characters (e.g. accented author names) can hash differently on different systems.

Also compare the manifest `repo_url` to the clone URL after normalizing common GitHub forms (`git@github.com:user/repo.git`, `https://github.com/user/repo`, `https://github.com/user/repo.git`). If they do not identify the same GitHub repo, do not mark the publication as verified.

If all checks pass, report the repo as a **verified APP publication** and include the `app_publication_id`.

If any check fails, report the highest level that is still supported:

- APP frontmatter but invalid/missing manifest: **APP-structured candidate, not verified**.
- No APP frontmatter but usable docs: **agent-readable repo, not APP-compliant**.
- No useful docs: **non-APP repo; direct content exploration required**.

### 3. Explore and report

**For verified APP publications or APP-structured candidates**, read the AGENTS.md and report to the user:
- Paper title and authors
- Paper format (from `paper_format` in frontmatter)
- APP status: verified APP publication, APP-structured candidate, or agent-readable repo
- `app_publication_id` if verified
- Paper summary (from the agent's own summary section)
- What the agent can do (explain, reproduce figures, run experiments, extend)
- Computational requirements (what's light, what's heavy)
- Available supplementary materials (if `supplementary/` exists) — know-how, author notes, sessions, additional materials
- Available skills (if `skills/` exists) — list each skill with its name and description from the SKILL.md frontmatter

**For agent-readable non-APP repos**, read the available docs in this order:

1. `AGENTS.md`, if present, even without APP frontmatter.
2. `CLAUDE.md`, especially for imports or pointers to other docs.
3. `README.md`.
4. docs directories, examples, notebooks, scripts, or paper-specific instructions.

Report:

- APP status: agent-readable repo, not verified APP.
- What the repo docs say the paper/project is.
- Any paper title, authors, abstract, or citation you can identify.
- Obvious entry points for reading, setup, reproduction, or experiments.
- Any warnings about missing APP metadata or unclear ground truth.

**For non-APP repos with no agent-readable docs**, proceed by inspecting the content directly. Do not stop just because `AGENTS.md`, `CLAUDE.md`, or README is missing. Report:

- What the repo contains (paper, code, data, notebooks)
- What language/framework the code uses
- Whether there are obvious entry points (paper files, scripts, notebooks, tests, examples)
- Which file appears to be the canonical paper or main result
- What you'd need to figure out to use this

### 4. Set up the environment (if the user wants to run code)

Before running anything from the paper:
1. Check `environment/requirements.txt` or equivalent
2. Check computational requirements in AGENTS.md if present; otherwise check README, docs, environment files, scripts, notebooks, and obvious hardware-specific imports
3. If anything is heavy or requires special hardware, warn the user
4. If the platform differs from what was tested, warn about potential compatibility issues
5. Only install dependencies with user approval:
   ```bash
   cd <repo-root>
   pip install -r environment/requirements.txt  # or equivalent
   ```
6. Check if the paper references external datasets (Hugging Face, Zenodo, Figshare, etc.). For APP repos, read `data/README.md` first for URLs, download commands, local destinations, and required-for-default-workflow flags; AGENTS.md Repository Structure may carry a high-level pointer. For non-APP repos, search README, docs, scripts, notebooks, configs, and paper source. If the user needs data that isn't in the repo:
   - Tell them what's needed, how large it is, and where to get it
   - Offer to run the download command (with approval)
   - Don't attempt to run code that depends on missing data — explain what's needed first

### 5. Operate as the paper's agent

**The paper, code, and data are the ground truth.** For APP repos, the paper document, accompanying code in `code/`, and data documented in `data/README.md` are authoritative for claims, results, and reproduction details. Supplementary materials provide additional context but are secondary. If anything in the supplementary materials conflicts with the ground truth, defer to the paper, code, and data. For non-APP repos, first identify the most likely canonical paper file by inspecting filenames, README/docs, build files, and paper directories.

When the user asks questions about this paper, route to the right source:

**Routing guide — which file for which question:**

| User asks about... | Primary source | Also check |
|---------------------|---------------|------------|
| What the paper claims, methods, results | Paper, code, data (ground truth) | AGENTS.md Paper Summary |
| Why a specific choice was made | `supplementary/know-how.md` | Paper source for what the choice was |
| What to know before reading | `supplementary/authors-note.md` | AGENTS.md Paper Summary |
| How to reproduce a figure | `code/figure-reproduction/README.md` if present | AGENTS.md figure summary, README/docs, scripts, notebooks, paper source, run the command |
| How to run an analysis or workflow | `skills/` if present | AGENTS.md "What You Can Do", README/docs, scripts |
| What parameters to change | AGENTS.md "Extend the work" if present | Code configs, scripts, notebooks |
| Computational requirements | AGENTS.md Computational Requirements if present | README/docs, environment files, imports, scripts |

**Explaining:**
- Read the paper source to answer claims; check code and data when the question concerns implementation, reproduction, or provenance
- Ground every answer in what the paper actually says
- Distinguish between paper claims and your inference
- If supplementary materials exist in `supplementary/`, use them to explain the reasoning behind decisions — but note that these provide context, not authoritative claims
- If `supplementary/know-how.md` exists, use it to answer "why did you do X?" questions — this is where tacit knowledge lives
- If `supplementary/authors-note.md` exists, use it for the authors' perspective on what matters beyond the paper

**Reproducing:**
- For APP repos, first check `code/figure-reproduction/README.md`. It is the authoritative map from paper figures/tables to reproduction scripts when present.
- Use AGENTS.md and README as summaries of the figure reproduction map; if they differ from `code/figure-reproduction/README.md`, trust the code README and report the inconsistency.
- For non-APP repos, infer reproduction commands from README/docs, scripts, notebooks, Makefiles, paper source figure references, and test/example files; explain uncertainty before running.
- After generating, compare output with the existing figures
- Report whether reproduction succeeded or if there are differences
- **If a command fails:** read the error, check the environment setup (step 4), and report what went wrong. Common issues: missing dependencies, wrong Python version, missing data files. Don't silently retry — explain the failure and suggest fixes.
- **If external data is needed:** check `data/README.md` first for APP repos; otherwise search README/docs, scripts, notebooks, configs, and paper source for download instructions. Tell the user what's needed, how large it is, and offer to download it (with approval) before retrying.

**Extending:**
- If the user wants to try variations, explain what parameters can be changed
- Modify config files or script arguments as needed
- Warn about computational cost before running
- After running a variation, compare results with the paper's reported results and note differences

**Using skills:**
- If the paper includes skills in `skills/`, read the SKILL.md files to discover what capabilities the authors provided
- **Proactively suggest skills** when the user's request matches a skill name or description — e.g., "This paper includes a guided analysis skill that can walk you through this. Would you like to use it?"
- When using a skill, read the SKILL.md and follow its instructions step by step
- Report what the skill produced and whether it succeeded
- If a skill's output appears to contradict the paper, flag the discrepancy to the user
- If a skill fails partway through, report where it failed and what the expected behavior was

**Attribution:**
- Always attribute information: "According to [Paper Title]..."
- Be clear about the paper's scope — don't extrapolate beyond what it claims

**Feedback loop:**
- After answering a substantive question, ask: "Did that answer your question, or should I look deeper into the paper or code?"
- If the user's question can't be fully answered from the available materials, say so explicitly and suggest what might help (e.g., "The paper doesn't discuss this; you might want to contact the authors")

### 6. Multiple papers

If the user loads multiple papers into `papers/`:

- Keep each paper's context separate — don't mix up claims from different papers
- When the user asks to compare, read both AGENTS.md files and compare specific aspects
- Attribute every claim to its source paper
- Identify connections: shared methods, contradictory results, complementary approaches
- When asked to synthesize, be explicit about what comes from where

### 7. Integrating with the user's project

If the user wants to reference the paper from their own AGENTS.md or CLAUDE.md:

**For Claude Code:**
```markdown
# In the user's CLAUDE.md:
@papers/paper-name/AGENTS.md
```

**For any platform:**
Add to the user's AGENTS.md:
```markdown
## Referenced Papers
- [Paper Title](papers/paper-name/AGENTS.md) — [one-line description of how it relates to this project]
```

This makes the paper context available whenever the user works on their project.
