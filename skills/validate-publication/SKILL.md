---
name: validate-publication
description: Validate a publication repo for factuality, privacy, consistency, and completeness. Use after major steps in /publish-paper or standalone to audit an existing publication. Launches parallel specialized agents to check different aspects and leaves inline comments in files.
---

# Validate Publication

Automated quality checks for publication repos. Launches parallel agents to independently check factuality, privacy, file integrity, and substance, then leaves inline comments directly in the files for the researcher to resolve.

Modeled on the code-review pattern: parallel specialized agents, high-signal filtering, independent validation of flagged issues.

## When to use

- During `/publish-paper` at validation checkpoints (after steps 5, 7, 9, and 10)
- Standalone to audit an existing publication repo
- Before tagging a new release of an existing publication

## Stages

Invoke with `--stage <name>` to validate specific artifacts. Omit for a full validation.

| Stage | When | What's checked |
|-------|------|----------------|
| `structure` | After step 5 (copy/organize) | Folder structure, file paths, sensitive files, data links, .gitignore |
| `agents-md` | After step 7 (AGENTS.md created) | Factuality, paths, ground truth, substance, commands |
| `readme` | After step 9 (README created) | Consistency with AGENTS.md, links, figure table |
| `full` | Step 10 or standalone | All of the above + confidentiality sweep + checklist |

## Process

### 1. Gather context

Read the publication repo to understand what's being validated:
- `AGENTS.md` — the agent's instructions (if it exists yet)
- The paper source — whatever format is designated as ground truth
- `README.md`
- `supplementary/` — know-how, authors-note, sessions, materials
- `skills/` — any author-published skills
- `supplementary/checklist.md` — the publication checklist (if it exists)

### 2. Launch parallel validation agents

Launch these agents in parallel. Each returns a list of issues with severity, location, and suggested fix.

**Agent 1: Factuality**
Compare every claim in AGENTS.md (paper summary, key results, "What You Can Do") against the actual paper source. Also check supplementary materials:
- Flag anything in AGENTS.md that isn't grounded in the paper
- Flag claims in `supplementary/know-how.md` or `supplementary/authors-note.md` that contradict the paper
- Flag skills that make claims about the paper's results
- Check that the paper summary uses specific language, not generic filler

Only run at stages: `agents-md`, `full`.

**Agent 2: Path & structure validator**
- Verify every file path in AGENTS.md Repository Map exists in the repo
- Verify every file path in README exists
- Check that commands in the figure generation table are syntactically valid
- Test external data links with `curl -sIL <url>` (flag non-2xx responses)
- Check that `supplementary/` references point to real files
- **Check folder structure conformance** — the publication repo should follow the convention from `/publish-paper` step 5:
  - Paper source in `paper/`, not loose at root or in `src/`
  - Code in `code/` (with `src/`, `scripts/`, `configs/`, `notebooks/` as relevant)
  - Data in `data/`
  - Dependencies/setup in `environment/`
  - Supplementary materials in `supplementary/`
  - Skills in `skills/<name>/SKILL.md`
  - Root should only contain `AGENTS.md`, `CLAUDE.md`, `README.md`, `LICENSE`, `.gitignore`, and the top-level directories — flag other root-level files
  - Flag files that look misplaced (e.g., `.py` scripts at root, `requirements.txt` at root instead of `environment/`, paper PDF at root instead of `paper/build/`)

Run at all stages.

**Agent 3: Privacy & confidentiality**
Scan ALL files in the repo — not just supplementary materials, but also the paper source, code files, code comments, notebook outputs, config files, and README. Flag:
- API keys, tokens, credentials (`sk-...`, `ghp_...`, `Bearer ...`, `key=...`)
- Email addresses, phone numbers, physical addresses
- File paths revealing private directory structure (`/Users/name/...`)
- Internal URLs, private repo references
- Names of people not listed as authors
- Access-controlled dataset identifiers

See `validation-criteria.md` for the full pattern list and `../extract-context/confidentiality-checklist.md` for the extended reference.

Run at all stages.

**Agent 4: Consistency & substance**
Cross-check information across files:
- AGENTS.md paper summary vs README description — should be consistent
- Figure table in AGENTS.md vs README — should match
- Citation in AGENTS.md vs README — should be identical
- Computational requirements vs actual code (e.g., GPU mentioned but no GPU code)
- Ground truth hierarchy explicitly stated in AGENTS.md identity section
- Paper summary is substantive — flag generic phrases like "novel method", "we propose", "state-of-the-art" without specifics
- Key results are concrete — flag vague results like "improved performance"

Only run at stages: `agents-md`, `readme`, `full`.

### 3. Collect and classify issues

Each agent returns issues with:
- **Severity**: `error` (must fix before release), `warning` (should fix), `note` (consider)
- **File** and **location** (line number or section)
- **Description** of the issue
- **Suggested fix**

### 4. Validate error-level issues

For each `error`-level issue, launch a validation subagent to independently confirm it's real. The validator reads the relevant files fresh and checks whether the issue actually exists. Filter out any issues that don't validate.

This reduces false positives — the cost of a false error is high (blocks the researcher), so we validate before reporting.

### 5. Write inline comments

For every validated issue, write a comment directly in the file:

```
<!-- REVIEW: error — The paper summary states "we achieve 95% accuracy" but the paper (Section 4.2) reports 93.7%. Fix: update to match paper. -->
```

```
<!-- REVIEW: warning — Generic language: "we propose a novel method." What specifically is novel? -->
```

```
<!-- REVIEW: note — Consider adding the runtime for Figure 3 to the computational requirements. -->
```

The `REVIEW:` prefix is a short, scannable marker — it doesn't refer to the skill name. Place the comment immediately above or next to the problematic content. The researcher resolves each by fixing the issue and removing the `<!-- REVIEW: -->` marker.

For code files, use the appropriate comment syntax:
```python
# REVIEW: warning — This path `/Users/john/data/` should be relative.
```

### 6. Report to terminal

Output a summary:

```
## Publication validation (stage: agents-md)

### Errors (2)
1. AGENTS.md:23 — Paper summary claims "95% accuracy"; paper reports 93.7%
2. AGENTS.md:45 — Path `code/scripts/fig3.py` does not exist

### Warnings (3)
1. AGENTS.md:18 — Generic language: "novel method" — be specific
2. supplementary/know-how.md:12 — Contains email address: john@university.edu
3. README.md:34 — Figure table missing Fig 4 (present in AGENTS.md)

### Notes (1)
1. AGENTS.md:67 — Computational requirements don't mention GPU; code imports torch.cuda

Inline comments placed in 3 files. Search for `<!-- REVIEW:` to find them.
```

If no issues found: "No issues found. Checked factuality, privacy, paths, and consistency."

## Standalone usage

When used outside `/publish-paper` (e.g., auditing an existing publication repo):

```
/validate-publication
```

This runs `--stage full` by default. The agent reads the entire repo, runs all four validation agents, and reports findings with inline comments.
