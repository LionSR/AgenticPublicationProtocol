---
name: validate-publication
description: Validate whether a publication repo or publication-staging tree is compliant with the Agentic Publication Protocol. Use after major steps in /publish-paper or standalone to check APP structure, reproducibility, privacy, consistency, and reader-agent usability.
---

# Validate Publication

Automated APP compliance checks for publication repos or `publication-staging/` candidate release trees. The goal is to make sure the paper-as-agent can help a reader understand and reproduce the paper smoothly, and that the publication contains the information APP requires.

This skill is not a referee report. Do not judge novelty, writing style, scientific importance, or whether the paper is "good." Restrict factual checks to clear APP-relevant inconsistencies: conflicting stated numbers, commands that do not run, missing files, unreproducible figures/tables, broken links, privacy issues, or documentation that would mislead a reader agent.

When called by `/publish-paper` or its modular step skills, treat `publication-staging/` as the effective repository root. Do not validate paths against the private parent working repo. A staged candidate passes only if a reader agent could use the staging tree on its own.

## When to use

- Called by `/publish-paper` as a sub-skill at validation checkpoints
- Standalone to audit an existing publication repo
- Standalone to audit a local `publication-staging/` tree before publication
- Before tagging a new release of an existing publication

## Stages

Invoke with `--stage <name>` to validate specific artifacts. Omit for a full validation.

| Stage | When | What's checked |
|-------|------|----------------|
| `structure` | After organizing files (phase 3) | Folder structure, file paths, sensitive files, data links, `.gitignore` |
| `agents-md` | After creating AGENTS.md (phase 4) | APP metadata, ground-truth hierarchy, canonical pointers, reader-help behavior, clear factual consistency |
| `full` | Step 4 of `/publish-paper`, pre-release review, or standalone | All of the above + README consistency, confidentiality sweep, validation report consistency, local reader-agent usability, and release manifest verification when validating a public tagged release |

## Before full validation: settle the publication identity

When `--stage full` runs ahead of a planned real publication, first settle the publication identity with the author, so it is validated here rather than changed after validation (any post-validation change forces a costly full re-validation):

1. The target public repo: an existing repo, or a name for a new one. No required naming convention; suggest candidates such as `<papername>.app` (dots are valid in GitHub repo names) and let the author choose. Only the name is needed now; creating the repo can wait until release.
2. The exact release tag. Per `PROTOCOL.md`, a publication is `(repo URL, tag)` and the tag is predictable before release, while the commit SHA is not. Ensure `AGENTS.md` `version` matches the tag under the normalization rule.
3. Whether the paper cites the publication. If yes, the author adds the link to the source manuscript now — the repo URL, or preferably the tag URL `https://github.com/<owner>/<repo>/releases/tag/<tag>`; never a commit URL — and the staged copy of the paper is re-imported and recompiled before validation runs.

Skip this section for dev-sandbox runs and for read-only audits of an existing tagged release, where the identity already exists. When validating before tagging a **new** release of an already-published repo, run it: a new version is a new identity, so settle the new tag (and any link updates) the same way.

## Process

### 1. Gather context

Read the publication repo or staging tree to understand what's being validated:

- `AGENTS.md` — the agent's instructions (if it exists yet)
- The paper source — whatever format is designated as ground truth
- `README.md`
- `supplementary/` — know-how, authors-note, sessions, materials
- `skills/` — any author-published skills
- `data/README.md` — dataset provenance, access, and download instructions when the publication uses any dataset, local or external
- `supplementary/validation-report.md` — prior validation report, if this is a final/revalidation pass
- `supplementary/paper-agent-test.md` — fresh staging-root paper-agent smoke test, required during final `/publish-paper` validation
- `APP_PUBLICATION.json` release asset — only when auditing a public tagged release, not when validating `publication-staging/`

When running `--stage full` as Step 4 of the modular `/publish-paper` workflow, perform or ensure the fresh staging-root paper-agent smoke test before declaring full validation passed. Save it as `supplementary/paper-agent-test.md`. The smoke test must include at least one primary-benchmark/result-check question when the paper has a headline numerical or benchmark claim. If staged cached plotted data, notebooks, tables, logs, or generated summaries exist for that claim, the tested agent should report an observed value, ratio, count, ordering, or explicit ambiguity from those staged artifacts; a generic reproduction plan is not enough. If the environment cannot launch a fresh agent session, write or require a `paper-agent-test: not performed` note and classify it as a release-outcome blocker rather than treating a documentation review as a smoke test.

### 2. Run APP validation checks

You may use parallel agents internally when useful, but the user-facing output is a validation report, not inline review comments. Do not edit files to insert validation markers.

**Check 1: APP factual consistency**

Compare APP-facing claims in `AGENTS.md`, `README.md`, supplementary materials, and skills against the paper and runnable artifacts.

Flag only clear inconsistencies or unsupported operational claims, such as:

- stated numbers that conflict between the paper, `AGENTS.md`, README, or figures/tables;
- a claim that a command reproduces a figure/table when the command is missing or fails;
- a described dataset, experiment, or artifact that is absent or named differently;
- supplementary notes or skills that contradict the ground-truth paper;
- a skill description that promises a workflow the staged repo cannot support.

Do not flag generic language merely because it is stylistically weak. Do not evaluate novelty, significance, or paper quality.

Only run at stages: `agents-md`, `full`.

**Check 2: Path, structure, and command validity**

- Verify every file path in `AGENTS.md` exists in the repo.
- Verify every file path in README exists.
- Check that commands in the figure/table reproduction sections are syntactically valid.
- For papers with generated figures/tables, verify `code/figure-reproduction/README.md` exists, is referenced from `AGENTS.md`, and is compatible with README.
- Verify every paper figure/table is listed in `code/figure-reproduction/README.md`; every listed script exists; every `reproduced` item has run evidence or a generated output path; every blocked/manual item has a concrete reason.
- Verify every figure/table status is in the allowed final enum from `validation-criteria.md`. Flag `not-yet-run`, `todo`, `unknown`, blank, or other temporary statuses as final-validation errors.
- For papers with headline numerical or benchmark claims, verify the canonical reproduction/data docs
  include quick claim checks, or equivalent reader-facing check entries, for the primary claim(s).
  These entries should identify the paper anchor, direct staged artifact, lightweight command or
  inspection path, expected observed signature, evidence level, and exact blocker/ambiguity when
  the headline check is not available.
- If a staged primary-claim artifact contains parseable numeric evidence, do not accept a
  quick check whose expected signature is only that files exist. Require an observed value,
  ratio, threshold, count, ordering, or explicit statement that no such partial audit is possible.
- If a primary benchmark check requires combining multiple staged artifacts, parsing a notebook, or
  computing ratios/counts from cached files, verify there is a single obvious read-only entry point
  for a reader agent, such as a lightweight script, command, or compact code block in the canonical
  docs. Do not accept "inspect the notebook/data" alone when the computation is nontrivial.
- Verify `data/README.md` exists whenever the publication uses any dataset; verify every dataset documented there resolves, with local files present or external links reachable via `curl -sIL`.
- Check that each figure/table reproduction entry maps to a distinct script when feasible; flag duplicate scripts as warnings unless the figure map explicitly marks the script as a grouped wrapper and lists every artifact/output it covers.
- When validating `publication-staging/`, verify commands and paths work with staging as the current working directory, and flag references to private parent-repo files.
- Test external data links with `curl -sIL <url>` when appropriate; flag non-2xx responses or mark authentication-limited links as needing manual verification.
- Check that `supplementary/` references point to real files.
- Check folder structure conformance against the layout defined in [PROTOCOL.md](../../PROTOCOL.md#repository-layout). See `validation-criteria.md` for the detailed checklist of what to flag.
- Check for hidden or generated artifacts that should not be staged as source-of-truth files, including `.ipynb_checkpoints/`, notebook execution caches, hidden generated folders, stale `results/`, stale `figures/`, and build outputs not intentionally documented as paper artifacts or reproduction outputs.

Run at all stages.

**Check 3: Privacy and confidentiality**

Scan all files in the repo — not just supplementary materials, but also the paper source, code files, code comments, notebook outputs, config files, and README. Flag:

- API keys, tokens, credentials (`sk-...`, `ghp_...`, `Bearer ...`, `key=...`)
- Email addresses, phone numbers, physical addresses
- File paths revealing private directory structure (`/Users/name/...`)
- Internal URLs, private repo references
- Names of people not listed as authors
- Access-controlled dataset identifiers

See `validation-criteria.md` for the full pattern list and `../extract-chat-context/confidentiality-checklist.md` for the extended reference.

Run at all stages.

**Check 4: APP completeness and reader-agent usability**

Cross-check information across files:

- `AGENTS.md` paper summary vs README description — should be compatible.
- Figure/table reproduction pointers in AGENTS.md and README should both lead to the canonical figure map when generated figures/tables exist.
- Figure/table reproduction information in README vs `code/figure-reproduction/README.md` — the code README is authoritative. AGENTS.md should point to that README rather than duplicate its detailed status table.
- Validation/reproduction status language in README, `code/figure-reproduction/README.md`, and the validation report should agree. If AGENTS.md includes validation or reproduction status despite the concise-template guidance, it must also agree. Flag stale phrases such as "not yet validated" when validation evidence says commands were run, and overly strong statements such as "fully validated" when blockers remain.
- Citation in `AGENTS.md` vs README — should be identical when both exist.
- At stage `full` only, when a real release is planned: `AGENTS.md` `version` matches the release tag settled in the pre-validation identity step, and any in-paper publication link matches the settled repo URL or tag URL exactly. Flag a mismatch as an error; it would otherwise surface as a post-validation change at the release gate. Skip this item at `agents-md`, where the identity may not be settled yet.
- Computational requirements vs actual code — for example, do not claim "runs on any laptop" if the code requires CUDA.
- Ground truth hierarchy explicitly stated in `AGENTS.md` identity section.
- Required APP files exist for the current validation stage.
- `data/README.md` exists whenever the publication uses any dataset, local or external.
- During full modular `/publish-paper` validation, `supplementary/paper-agent-test.md` exists and records a fresh agent session launched with the staged repo as its working directory. It should include representative Q&A showing the agent can identify ground truth, summarize the paper, point to real reproduction commands, and accurately report blockers. If this is missing or only a documentation review, classify it as a release-outcome blocker.
- The paper-agent smoke test includes a primary-benchmark/result-check question when the paper has
  a headline numerical or benchmark claim. Passing answers should inspect staged artifacts when
  available and report observed values, ratios, counts, orderings, or explicit ambiguities rather
  than only pointing to a plan or saying full rerun is blocked.
- Setup, data access, and reproduction instructions are complete enough for a reader agent to know what can be run, what data is required, and what requires manual/human steps.

This is a completeness/usability check, not a prose-quality review. Do not flag wording only because it sounds generic; flag missing information only when it blocks APP use.

Only run at stages: `agents-md`, `full`.

**Check 5: Verified release manifest**

Only run this check when validating a public tagged release or an already-published repo. Do not require `APP_PUBLICATION.json` during `/publish-paper` staging validation; the manifest is created in the real publication final-outcome step after the public commit exists.

For a public tagged release:

- Download `APP_PUBLICATION.json` from the GitHub Release asset for the current tag.
- Verify manifest fields match the current checkout: `repo_url`, `tag`, `commit`, and `tree`.
- Recompute `app_publication_id` from the manifest payload excluding `app_publication_id`; it must equal the manifest ID.
- Verify `validation.stage == "full"` and `validation.result == "passed"`.
- Verify the `validation.validation_report_sha256` matches `supplementary/validation-report.md` if that report is committed, or the validation report release asset if the report is distributed as an asset.
- Verify `human_approval.approved == true` and approving authors are listed.

If any manifest check fails, report the repo as not fully verified APP-compliant. It may still be an APP-structured candidate.

### 3. Collect and classify results

Classify findings with:

- **Passed checks**: APP requirements that were checked and passed.
- **Issues needing changes**: concrete changes required or recommended.
- **Public-release blockers**: error-level issues or explicit sandbox deferrals that prevent real APP publication, even if a dev-sandbox run can be recorded.
- **Sandbox-only deferrals**: items the researcher intentionally deferred for implementation testing, such as missing `LICENSE`; these must not be described as full APP compliance.
- **Manual verification needed**: items the agent could not verify, such as authenticated data links or commands too heavy to run.

For each issue include:

- **Severity**: `error` (must fix before release), `warning` (should fix), `note` (consider)
- **File** and **location** (line number or section when available)
- **Description**
- **Suggested fix**

### 4. Validate error-level issues

Before reporting an `error`, independently confirm it by rereading the relevant files or rerunning the lightweight check. Filter out anything that does not validate.

This reduces false blocking errors. Warnings and notes can be reported with lower confidence if clearly labeled.

### 5. Report results

Do not write inline comments or modify files. Produce a validation report in the terminal/chat output.

The report should include both what passed and what needs work:

```text
## Publication validation (stage: agents-md)

### Passed
- Required APP files for this stage are present.
- Paths listed in AGENTS.md resolve from the staging root.
- README and AGENTS.md cite the same paper title and authors.

### Issues needing changes
Errors (2)
1. AGENTS.md:45 — Path `code/scripts/fig3.py` does not exist.
   Suggested fix: update the path or copy the missing script into staging.
2. README.md:34 — Figure 4 command differs from AGENTS.md.
   Suggested fix: make both tables use the same command.

Warnings (1)
1. supplementary/know-how.md:12 — Contains an email address for a non-author.
   Suggested fix: remove or anonymize before release.

### Manual verification needed
- External data link requires authentication; researcher should confirm it is accessible to intended readers.

### Public-release blockers
- None.

### Sandbox-only deferrals
- None.

### Brief summary for chat
Validation found two release-blocking APP issues: a missing figure script and inconsistent Figure 4 commands. The rest of the checked structure, paths, and metadata passed.
```

If no issues are found, say clearly:

```text
No APP compliance issues found. Checked structure, paths, privacy, clear factual consistency, README/AGENTS.md consistency, and reader-agent usability for the requested stage.
```

## Standalone usage

When used outside `/publish-paper` (e.g., auditing an existing publication repo or local staging tree):

```text
/validate-publication
```

This runs `--stage full` by default. The agent reads the entire repo, runs the APP validation checks, and reports passed checks, issues needing changes, and manual verification items.
