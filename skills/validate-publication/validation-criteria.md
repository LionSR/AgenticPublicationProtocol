# Validation Criteria

Detailed criteria for the APP compliance checks in validate-publication.

**Severity convention.** By default, PROTOCOL.md `MUST` violations -> `error`; `SHOULD` -> `warning`; `MAY` -> `note`. Map new checks accordingly unless this file explicitly defines a narrower exception for a non-blocking organizational issue; such exceptions must be stated where the check is defined.

## APP factual consistency

The manuscript, primary code, and data are the ground truth. Supplementary materials and external knowledge are secondary.

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
- A figure/table marked `reproduced` in `code/figure-reproduction/README.md` when its script is absent, fails, or has no generated output/evidence

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

**Required files by stage.** The modular `/publish-paper` workflow creates required files progressively: `prepare-staging` produces the layout, `data/README.md` whenever the publication uses any dataset, local or external, and creates or copies `LICENSE` after asking the researcher for licensing/reuse terms; `define-paper-agent` produces `AGENTS.md`, `CLAUDE.md`, and `README.md`; full validation produces/checks `supplementary/validation-report.md` and the staging-root paper-agent smoke test. Validate accordingly so `--stage structure` does not block on files that later steps have not created yet.

| Required file | `structure` | `agents-md` | `full` |
|---------------|-------------|-------------|--------|
| `paper/` with at least one document | error if missing | error if missing | error if missing |
| `data/README.md` (when the publication uses any dataset, local or external) | error if missing | error if missing | error if missing |
| `LICENSE` at root | error if missing | error if missing | error if missing |
| `.gitignore` at root | warning if missing | warning if missing | warning if missing |
| `environment/README.md` (when executable code, figure/table scripts, notebooks, or nontrivial build tools exist) | error if missing | error if missing | error if missing |
| `AGENTS.md` at root | — | error if missing | error if missing |
| `CLAUDE.md` at root (`@AGENTS.md`) | — | warning if missing | warning if missing |
| `README.md` at root | — | error if missing | error if missing |
| `code/figure-reproduction/README.md` for papers with generated figures/tables | warning if missing | error if missing | error if missing |
| `supplementary/validation-report.md` | — | — | warning if missing during full validation of an APP candidate/release; not required for explicitly scoped pre-report audits |
| `supplementary/paper-agent-test.md` | — | — | error if missing during full validation of an APP candidate/release unless `supplementary/validation-report.md` records author manual paper-agent testing and approval; not required for explicitly scoped pre-test audits |

The publication checklist is a skill-internal artifact of `/publish-paper` and is **not** a publication file — do not flag its absence.

For developer-sandbox publish-paper runs, a missing `LICENSE` may be recorded as a release-outcome blocker only if the researcher explicitly deferred licensing for the sandbox test. It is still an error for real publication mode and still means the staged tree is not release-ready.

**File paths:**
- Every path in AGENTS.md Repository Structure must resolve to a real file or directory
- Every path in README must resolve
- Every path in `supplementary/` references must resolve
- Every script and output path in `code/figure-reproduction/README.md` must resolve, except outputs for blocked/manual items
- Relative paths should be relative to the repo root, or to `publication-staging/` when validating a staged candidate release

**Paper-agent smoke test:**
- During full validation of an APP candidate or release, including standalone `--stage full`, the validating agent should explicitly ask the author which route they want for the fresh paper-agent smoke test:
  - authorize the publishing agent to launch a fresh subagent/fresh agent session rooted at `publication-staging/`, when the platform supports that and the author explicitly asks for it; or
  - run the smoke test manually by opening a new agent session themselves, setting the working directory to `publication-staging/`, asking the smoke-test questions, and confirming whether the paper-agent behaved correctly.
- If the publishing/validating agent runs the test, `supplementary/paper-agent-test.md` should exist and document the resulting fresh agent session transcript or concise Q&A summary.
- If the author runs the test manually, a transcript is optional; `supplementary/validation-report.md` should record that the author manually tested and approved the paper-agent.
- The smoke-test questions should cover ground-truth identification, main contribution, at least one representative reproduction command, blocked/manual/dependency-limited figures or tables, and heavy/platform-specific warnings when relevant.
- An agent-run test passes only if the fresh agent answers from staged files, uses paths and commands that resolve inside staging, and accurately reports reproduction limitations. An author-run manual test passes when the author confirms the paper-agent behaved correctly.
- If the author declines both routes, the environment could not launch a fresh agent session, or the author does not confirm manual approval, the report should say `paper-agent-test: not performed` and classify this as a release-outcome blocker. A documentation-only review may be useful, but it is not a paper-agent smoke test.

**Commands:**
- Figure reproduction commands in `code/figure-reproduction/README.md` should be syntactically valid (parseable by the shell)
- Install commands should reference real package files (e.g., `environment/requirements.txt` exists)
- If `environment/README.md` exists, setup commands in AGENTS.md, README, and figure-reproduction commands should use the documented environment or runner prefix (`.venv/bin/python`, `uv run`, project-local Julia depot, conda env, `Rscript`, `octave`, `matlab -batch`, `wolframscript`, etc.) unless the environment README says no activation/prefix is required.
- Installed environment directories such as `.venv/`, `.julia_depot/`, `node_modules/`, conda env folders, and package caches should be gitignored rather than committed. Dependency manifests, lockfiles, setup scripts, and `environment/README.md` should be committed.
- If reproduction requires external licensed or manually installed software such as VASP, MATLAB, Mathematica, COMSOL, Gaussian, or commercial solvers, `environment/README.md` should document the software name, version if known, required components, access/license requirement, expected executable/command, and whether validation could run it. Absence of the software in the validation environment is a blocker to record, not a reason to omit the requirement.
- Don't run heavy commands unless explicitly approved — check they parse and reference real files, and require heavy commands to be marked as such

**Figure/table reproduction:**
- `code/figure-reproduction/README.md` is authoritative when present.
- Every paper figure/table should appear in that README.
- Each item should include: paper artifact, script, inputs, generated output, status, and notes.
- Status should be one of: `reproduced`, `runs-but-differs`, `blocked-missing-data`, `blocked-heavy-compute`, `blocked-broken-code`, `blocked-dependency`, `manual-only`.
- Unknown or temporary statuses such as `not-yet-run`, `todo`, `unknown`, or blank statuses are `error` at `full`; at earlier stages, flag them as items that must be resolved before final validation.
- A `reproduced` item must have an existing script and either a generated output path or recorded run evidence.
- A blocked/manual item must document the attempted source scripts/notebooks, attempted command if any, and concrete blocker.
- A `blocked-dependency` item must name the dependency, resolver/network/platform/licensing blocker, and the command attempted or the reason no command could be attempted.
- If the figure-to-code mapping was ambiguous, the figure map should record the researcher clarification or state that clarification is still needed.
- `AGENTS.md` must reference `code/figure-reproduction/README.md` and summarize the figure/table statuses.
- README should either link to the same map or duplicate a compatible summary.
- Each paper figure/table should map to a distinct direct script when feasible. Grouped wrappers are allowed when explicitly documented: the map must say the script is a grouped wrapper and list every paper artifact and generated output covered by the command. Flag duplicate scripts as `warning` unless this grouped-wrapper documentation is present. This is an explicit exception to the severity convention: splitting may be non-trivial and the decision belongs to the researcher.

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

## Generated and hidden artifacts

Generated artifacts are allowed only when they are intentional publication artifacts, such as compiled paper PDFs, paper figures, shipped small datasets, or explicitly documented reproduction evidence. Generated reproduced figures are local run artifacts by default and should usually be gitignored under `code/figure-reproduction/generated/`. If generated reproduction outputs are committed, they should have a canonical location and be described by `AGENTS.md`, README, `data/README.md`, or `code/figure-reproduction/README.md`.

**Flag as errors when present and not explicitly justified:**
- `.ipynb_checkpoints/` directories or files.
- Notebook execution caches that expose local paths, outputs, credentials, private URLs, or unpublished data.
- Hidden generated directories that are not standard metadata, such as `.cache/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.ipynb_checkpoints/`, or tool-specific temporary output.

**Flag as warnings unless documented as intentional source artifacts:**
- Copied stale `results/`, `outputs/`, `figures/`, `plots/`, or build directories inside `code/`.
- Generated reproduction outputs committed without documentation that explains why they are intentional publication artifacts or validation evidence.
- Generated reproduction outputs stored outside `code/figure-reproduction/generated/` or another location explicitly documented in `code/figure-reproduction/README.md`.
- Notebook outputs that are large, stale, or not needed for reader-agent use.

When a generated artifact is intentionally included, the publication should explain why it is source-of-truth, validation evidence, or needed for reproducibility, and `.gitignore` should prevent accidental future generated files from being added.

## Consistency

**Cross-file checks:**

| Field | AGENTS.md | README | Should match? |
|-------|-----------|--------|---------------|
| Paper title | Frontmatter + identity | Heading | Exact |
| Authors | Frontmatter | Under heading | Exact |
| Paper summary | Paper Summary section | 1-2 sentence summary | Compatible (README is shorter) |
| Environment setup | Environment Setup section | Setup section | Compatible; same setup commands and runner prefixes |
| Figure reproduction | "Reproduce figures" section | "Figures" section | Compatible summary; both point to `code/figure-reproduction/README.md` when present |
| Citation | Citation section | Citation section | Identical BibTeX |
| Computational reqs | Computational Requirements | Setup section | Compatible |

**Internal consistency:**
- `paper_format` in frontmatter matches the actual paper file type
- Computational requirements match what the code actually needs (e.g., don't say "any laptop" if code imports CUDA)
- Environment setup instructions match actual dependency files and command evidence. Flag stale or impossible setup commands, missing `environment/README.md`, or figure commands that bypass the documented environment.
- `version` in frontmatter matches the git tag per the normalization rule in [PROTOCOL.md § Versioning](../../PROTOCOL.md#versioning): for `vMAJOR.MINOR.PATCH` tags, `version` has no leading `v` (tag `v1.0.0` → `version: "1.0.0"`); for non-semver tags, `version` matches the tag exactly.
- Validation status language in AGENTS.md, README, `code/figure-reproduction/README.md`, and `supplementary/validation-report.md` should agree. Flag stale statements such as "commands have not yet been validated" when the validation report records successful runs. Also flag overly broad statements such as "fully validated" when release blockers, blocked figures, or manual-only items remain.

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
- Environment setup is reproducible: installed env directories are not required to be committed, but manifests/lockfiles/setup commands are present and documented.
- Figure/table reproduction instructions cover the figures/tables the publication claims are reproducible.
- Data requirements are clear: what is included, what must be downloaded, what is too large or access-controlled, and what is optional.
- Heavy commands are labeled with expected runtime/hardware or marked as manual/heavy.
- Skills, if present, have descriptions and steps sufficient for an agent to run them.

**Ground truth hierarchy check:**
- AGENTS.md identity section must explicitly state the paper is the ground truth
- Supplementary materials section must note they are secondary
- If skills are present, the Skills section should note they are tools, not claims
