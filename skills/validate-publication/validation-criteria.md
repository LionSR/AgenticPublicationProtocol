# Validation Criteria

Detailed criteria for each validation agent in validate-publication.

**Severity convention.** By default, PROTOCOL.md `MUST` violations → `error`; `SHOULD` → `warning`; `MAY` → `note`. Map new checks accordingly unless this file explicitly defines a narrower exception for a non-blocking organizational issue; such exceptions must be stated where the check is defined.

## Factuality

Paper, code, and data are the ground truth. Supplementary materials and external knowledge are secondary.

**What to check:**
- Every factual claim in AGENTS.md paper summary — find it in the paper source
- Every key result — verify the numbers, claims, and scope match the paper
- "What You Can Do" section — are the described capabilities actually supported by the code?
- `supplementary/know-how.md` — does it contradict anything in the paper?
- `supplementary/authors-note.md` — does it make claims beyond what the paper supports?
- Skills — do any skill descriptions make claims about the paper's findings?

**What counts as ungrounded:**
- A specific number (accuracy, speed, size) that doesn't match the paper
- A claim about what the method achieves that the paper doesn't make
- An implication about generality that the paper's experiments don't support
- Causal claims where the paper only shows correlation

**What's OK:**
- Paraphrasing the paper in simpler terms (as long as the meaning is preserved)
- Stating implications the paper explicitly discusses
- The know-how describing methodology choices not mentioned in the paper (that's its purpose)

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

**Required files by stage.** The `/publish-paper` workflow creates required files progressively: `build.md` (phase 3) produces the layout, `data/README.md` when data ships, and `LICENSE`; `draft.md` (phase 4) produces `AGENTS.md`, `CLAUDE.md`, and `README.md`. Validate accordingly so `--stage structure` does not block on files that phase 4 hasn't created yet.

| Required file | `structure` | `agents-md` | `full` |
|---------------|-------------|-------------|--------|
| `paper/` with at least one document | error if missing | error if missing | error if missing |
| `data/README.md` (when the publication uses any dataset, local or external) | error if missing | error if missing | error if missing |
| `LICENSE` at root | error if missing | error if missing | error if missing |
| `.gitignore` at root | warning if missing | warning if missing | warning if missing |
| `AGENTS.md` at root | — | error if missing | error if missing |
| `CLAUDE.md` at root (`@AGENTS.md`) | — | warning if missing | warning if missing |
| `README.md` at root | — | error if missing | error if missing |

The publication checklist is a skill-internal artifact of `/publish-paper` and is **not** a publication file — do not flag its absence.

**File paths:**
- Every path in AGENTS.md Repository Structure must resolve to a real file or directory
- Every path in README must resolve
- Every path in `supplementary/` references must resolve
- Relative paths should be relative to the repo root

**Commands:**
- Figure generation commands should be syntactically valid (parseable by the shell)
- Install commands should reference real package files (e.g., `environment/requirements.txt` exists)
- Don't run heavy commands — just check they parse and reference real files

**Figure reproduction scripts (one per figure):**
- Each row in AGENTS.md "Reproduce figures" maps to a distinct script in `code/`
- Flag duplicates (two figures pointing at the same script) as `warning` — this is an explicit exception to the severity convention: the spec says MUST, but splitting may be non-trivial and the decision belongs to the researcher

**External links:**
- Test with `curl -sIL <url>` — flag non-2xx responses
- Note: some links may require authentication; flag as "needs manual verification" rather than "broken"
- Hugging Face, Zenodo, Figshare URLs should resolve

## Privacy & confidentiality

Extends `../extract-context/confidentiality-checklist.md` to cover the entire repo, not just supplementary materials.

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

## Substance

**Red flags for generic language:**
- "We propose a novel method" — what specifically is novel?
- "State-of-the-art results" — on what benchmark? by what margin?
- "Significant improvement" — how much? over what baseline?
- "Various experiments" — which experiments?
- "Extensive evaluation" — how extensive?

**What makes a summary substantive:**
- Names the specific problem (not just the field)
- Describes the specific approach (not just "a new method")
- States specific results with numbers
- Explains why this matters with concrete implications

**What makes key results specific:**
- Each result is a concrete claim (not a restatement of the approach)
- Numbers are included where the paper provides them
- The scope is clear (what dataset, what conditions)

**Ground truth hierarchy check:**
- AGENTS.md identity section must explicitly state that the paper, code, and data are the ground truth
- Supplementary materials section must note they are secondary
- If skills are present, the Skills section should note they are tools, not claims
