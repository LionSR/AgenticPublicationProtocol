# Validation Criteria

Detailed criteria for the APP compliance checks in validate-publication.

## APP factual consistency

The paper is the ground truth. Everything else is secondary.

**What to check:**
- Stated numbers, figure/table references, dataset names, and result summaries in AGENTS.md and README — verify they do not conflict with the paper
- Key results listed in AGENTS.md — verify the numbers, claims, and scope match the paper when the claim is concrete enough to check
- "What You Can Do" section — are the described capabilities actually supported by the code and files in the repo?
- `supplementary/know-how.md` — does it contradict anything in the paper?
- `supplementary/authors-note.md` — does it contain factual claims that contradict the paper or could mislead a reader agent?
- Skills — do any skill descriptions make claims about the paper's findings?

**What counts as an APP-relevant inconsistency:**
- A specific number (accuracy, speed, size) that doesn't match the paper
- A claim about what the method achieves that the paper doesn't make
- An implication about generality that the paper's experiments don't support
- Causal claims where the paper only shows correlation
- A figure/table reproduction claim that is not supported by runnable code or documented manual steps

**What's OK:**
- Paraphrasing the paper in simpler terms (as long as the meaning is preserved)
- Stating implications the paper explicitly discusses
- The know-how describing methodology choices not mentioned in the paper (that's its purpose)
- Generic or high-level author language, unless it creates a clear contradiction or blocks reader-agent use

## Path, structure & command validity

**Folder structure conformance:**

The authoritative layout is defined in [PROTOCOL.md § Repository layout](../../PROTOCOL.md#repository-layout). This file does not restate it — validators resolve "what is required" against PROTOCOL.md, and flag deviations as follows.

**What to flag (all stages):**
- Paper, code, data, or dependency files loose at root (e.g., `main.tex`, `*.py`, `requirements.txt`, `*.csv`) when a dedicated top-level directory exists.
- Paper source outside `paper/` (e.g., in `src/` or at root).
- Code files outside `code/` (e.g., scripts at root or in `paper/`).
- Dependency files outside `environment/` (`requirements.txt`, `environment.yml`, `pyproject.toml`).
- Supplementary materials outside `supplementary/` (e.g., `know-how.md` at root).
- Severity: `warning` for misplaced files (the repo works but the structure is inconsistent).

**Required files by stage.** The `/publish-paper` workflow creates required files progressively: `build.md` (phase 3) produces the layout and the checklist; `draft.md` (phase 4) produces `AGENTS.md`, `CLAUDE.md`, and `README.md`; the researcher adds `LICENSE` at some point before release. Validate accordingly so `--stage structure` does not block on files that phase 4 hasn't created yet.

| Required file | `structure` | `agents-md` | `full` |
|---------------|-------------|-------------|--------|
| `paper/` with at least one document | error if missing | error if missing | error if missing |
| `supplementary/checklist.md` | error if missing | error if missing | error if missing |
| `.gitignore` at root | warning if missing | warning if missing | warning if missing |
| `AGENTS.md` at root | — | error if missing | error if missing |
| `CLAUDE.md` at root (`@AGENTS.md`) | — | warning if missing | warning if missing |
| `README.md` at root | — | error if missing | error if missing |
| `LICENSE` at root | — | — | error if missing |

**File paths:**
- Every path in AGENTS.md Repository Structure must resolve to a real file or directory
- Every path in README must resolve
- Every path in `supplementary/` references must resolve
- Relative paths should be relative to the repo root, or to `publication-staging/` when validating a staged candidate release

**Commands:**
- Figure generation commands should be syntactically valid (parseable by the shell)
- Install commands should reference real package files (e.g., `environment/requirements.txt` exists)
- Don't run heavy commands — just check they parse and reference real files

**External links:**
- Test with `curl -sIL <url>` — flag non-2xx responses
- Note: some links may require authentication; flag as "needs manual verification" rather than "broken"
- Hugging Face, Zenodo, Figshare URLs should resolve

## Privacy & confidentiality

Extends `../extract-chat-context/confidentiality-checklist.md` to cover the entire repo, not just supplementary materials.

**Additional places to check (beyond supplementary/):**
- Paper source (LaTeX, Markdown, etc.) — check for hardcoded paths in `\input{}`, comments with TODOs mentioning names
- Code files — check comments, docstrings, print statements, logging, config defaults
- Notebook outputs — cell outputs may contain paths, usernames, API responses
- Config files — YAML/JSON/TOML may have default paths, URLs, keys
- `.gitignore` — check that it covers sensitive files; flag if `.env` or credentials files exist but aren't ignored
- README — check for internal URLs or private references

**Patterns (quick reference — see confidentiality-checklist.md for full list):**
- Credentials: `sk-`, `ghp_`, `Bearer`, `password=`, `token=`, connection strings
- Personal: email addresses, phone numbers, physical addresses, non-author names
- Infrastructure: `/Users/*/`, `C:\Users\*/`, `192.168.*`, `10.0.*`, internal hostnames
- Access-controlled: private repo URLs, internal tool references, unreleased work

## Consistency

**Cross-file checks:**

| Field | AGENTS.md | README | Should match? |
|-------|-----------|--------|---------------|
| Paper title | Frontmatter + identity | Heading | Exact |
| Authors | Frontmatter | Under heading | Exact |
| Paper summary | Paper Summary section | 1-2 sentence summary | Compatible (README is shorter) |
| Figure table | "Reproduce figures" | "Figures" section | Exact commands and paths |
| Citation | Citation section | Citation section | Identical BibTeX |
| Computational reqs | Computational Requirements | Setup section | Compatible |

**Internal consistency:**
- `paper_format` in frontmatter matches the actual paper file type
- Computational requirements match what the code actually needs (e.g., don't say "any laptop" if code imports CUDA)
- `version` in frontmatter matches the git tag per the normalization rule in [PROTOCOL.md § Versioning](../../PROTOCOL.md#versioning): for `vMAJOR.MINOR.PATCH` tags, `version` has no leading `v` (tag `v1.0.0` → `version: "1.0.0"`); for non-semver tags, `version` matches the tag exactly.

## Verified APP publication manifest

The manifest is required only for a public tagged release. It is not required during `publication-staging/` validation because the public commit and release do not exist yet.

**Manifest location:**
- Canonical: GitHub Release asset named `APP_PUBLICATION.json`.
- Optional mirrors: annotated tag message or public APP registry.
- Do not trust a committed `APP_PUBLICATION.json` alone as proof of verified APP publication.

**Manifest checks:**
- `protocol` is `agentic-publication-protocol`.
- `manifest_version` is present.
- `publication_type` is `app-publication`.
- `repo_url` identifies the same GitHub repository as the clone remote after normalizing SSH/HTTPS forms.
- `tag` equals the checked-out tag.
- `commit` equals `git rev-parse HEAD`.
- `tree` equals `git rev-parse HEAD^{tree}`.
- `validation.stage` is `full`.
- `validation.result` is `passed`.
- `validation.validation_report_sha256` matches the validation report distributed with the publication.
- `human_approval.approved` is `true`.
- `human_approval.approved_by` lists the approving authors.
- Recomputed `app_publication_id` equals the manifest value.

**ID recomputation:**
- Remove `app_publication_id` from the manifest.
- Canonicalize the remaining JSON with sorted keys and compact separators.
- SHA-256 hash the canonical JSON.
- Compare `app-v1:sha256:<digest>` to `app_publication_id`.

**Classification:**
- Valid manifest: verified APP publication.
- APP frontmatter but missing/invalid manifest: APP-structured candidate.
- Agent docs without APP frontmatter: agent-readable repo, not APP-compliant.

## APP completeness and usability

This is not a referee or prose-quality check. Do not flag wording simply because it sounds generic, promotional, or insufficiently polished. Flag only missing or inconsistent information that would prevent a reader agent from understanding the paper's ground truth, locating artifacts, setting up the environment, or reproducing documented results.

**Reader-agent usability checks:**
- The paper source designated as ground truth is easy to identify.
- AGENTS.md explains what the agent can do with concrete paths or commands where needed.
- README gives enough setup context for a reader to start using the paper agent.
- Figure/table reproduction instructions cover the figures/tables the publication claims are reproducible.
- Data requirements are clear: what is included, what must be downloaded, what is too large or access-controlled, and what is optional.
- Heavy commands are labeled with expected runtime/hardware or marked as manual/heavy.
- Skills, if present, have descriptions and steps sufficient for an agent to run them.

**Ground truth hierarchy check:**
- AGENTS.md identity section must explicitly state the paper is the ground truth
- Supplementary materials section must note they are secondary
- If skills are present, the Skills section should note they are tools, not claims
