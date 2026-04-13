# Validation Criteria

Detailed criteria for each validation agent in validate-publication.

## Factuality

The paper is the ground truth. Everything else is secondary.

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

The publication repo should follow the convention from `/publish-paper` step 5. Not every directory is required (a theory paper may only have `paper/`), but files should be in the right place.

| Directory | Contains | Required? |
|-----------|----------|-----------|
| `paper/` | Paper source (ground truth), `.bib`, `figures/`, `build/` | Yes |
| `code/` | `src/`, `scripts/`, `configs/`, `notebooks/` | If the paper has code |
| `data/` | `raw/`, `processed/`, `README.md` | If the paper has data |
| `environment/` | `requirements.txt` (or equivalent), setup `README.md` | If the paper has code |
| `supplementary/` | `know-how.md`, `authors-note.md`, `checklist.md`, `sessions/`, `materials/` | Recommended |
| `skills/` | `<name>/SKILL.md` per skill | If author defined skills |

**What to flag:**
- Files at root that belong in a subdirectory (e.g., `main.tex`, `*.py`, `requirements.txt`, `*.csv` at root)
- Root should only contain: `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`
- Paper source outside `paper/` (e.g., in `src/` or root)
- Code files outside `code/` (e.g., scripts loose at root or in `paper/`)
- Dependencies at root instead of `environment/` (e.g., `requirements.txt`, `environment.yml`, `pyproject.toml` at root)
- Supplementary materials outside `supplementary/` (e.g., `know-how.md` at root)
- Severity: `warning` for misplaced files (the repo works, but the structure is inconsistent)

**File paths:**
- Every path in AGENTS.md Repository Map must resolve to a real file or directory
- Every path in README must resolve
- Every path in `supplementary/` references must resolve
- Relative paths should be relative to the repo root

**Commands:**
- Figure generation commands should be syntactically valid (parseable by the shell)
- Install commands should reference real package files (e.g., `environment/requirements.txt` exists)
- Don't run heavy commands — just check they parse and reference real files

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
- Version in frontmatter matches the git tag (if released)

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
- AGENTS.md identity section must explicitly state the paper is the ground truth
- Supplementary materials section must note they are secondary
- If skills are present, the Skills section should note they are tools, not claims
