# Phase 4 — Paper-Agent Docs

The **author's voice** principle declared in [`SKILL.md`](SKILL.md) is especially load-bearing in this phase.

All files in this phase are created inside `publication-staging/`. Run commands and validation from the staging root, and write all paths as if `publication-staging/` were the repository root.

## 4.1 Create `AGENTS.md`

Tell the researcher you're drafting `publication-staging/AGENTS.md` now, drawing on everything from phases 1-2.

The schema — every required frontmatter field, every required and optional body section — is defined in [PROTOCOL.md § AGENTS.md](../../PROTOCOL.md#agentsmd). Read it before drafting. Do not paraphrase or re-derive the schema here. The guidance below is about *how to fill the schema well*, not *what the schema is*.

Use [`template/AGENTS.md`](../../template/AGENTS.md) as a starting skeleton.

**AGENTS.md guidance — things easy to get wrong:**

- **Paper Summary.** Before drafting, ask the researcher: "What's the core message you want someone to take away from this paper?" Their answer sets the direction — do not draft from your own reading first. Use the researcher's own words from phase 2 and any extracted context as the foundation. This section is what the agent will rely on most; make it substantive, not generic.
- **Repository Structure.** Don't just list files — explain what each does and how they connect. Mark the canonical paper file as `(GROUND TRUTH)`. Group by function: paper source, figure reproduction, experiments, data, config. Include `code/figure-reproduction/README.md` as the authoritative figure/table reproduction map when the paper has generated figures/tables. Use paths relative to the staging root. For external data (Hugging Face, Zenodo, Figshare, ...), briefly name the dataset and point to `data/README.md`; keep the URL, exact download command, local destination, size, and required/optional status in `data/README.md`.
- **What You Can Do.** Real, copy-pasteable commands — no placeholders. The figure-reproduction section must point to `code/figure-reproduction/README.md` and summarize every figure/table status. For "Run experiments" and "Extend the work," the goal is that a reader can answer "what if I change X?" by running something concrete.
- **Figure Reproduction.** If `code/figure-reproduction/README.md` exists, `AGENTS.md` must include a "Figure Reproduction" or "Reproduce figures" section that names it as authoritative. The summary table in `AGENTS.md` must include at least: figure/table, paper artifact, script, status, and runtime/requirements. Do not hide blocked figures; summarize the blocker and refer to the README map for details. If a figure mapping required researcher clarification, summarize the confirmed mapping rather than the agent's earlier guess.
- **License.** If `LICENSE` exists, include it in Repository Structure and state that licensing/reuse questions should be answered from `LICENSE`. If the run is developer-sandbox-only and licensing was explicitly deferred, do not imply public reuse permission; state that licensing is unresolved and the candidate is not public-release-ready until `LICENSE` is added.
- **Validation Status.** Keep this section current with `supplementary/validation-report.md` and `code/figure-reproduction/README.md`. State what was tested, what passed, and what remains blocked/manual. Remove stale placeholders such as "commands not yet validated" after validation has run, and do not say "fully validated" when blockers remain.
- **Computational Requirements.** Classify every task (figure generation, individual experiments, full reproduction) by time, hardware, and memory. Note the platform tested on (OS, language version). The agent MUST warn before running anything heavy.
- **Identity.** Keep the spokesperson framing — the agent represents *these authors' work*, not a generic assistant. Domain voice matters: a math paper's agent reasons like a mathematician; an experimental paper's agent thinks like an experimentalist.

Also create `publication-staging/CLAUDE.md` — one line: `@AGENTS.md`. You can copy [`template/CLAUDE.md`](../../template/CLAUDE.md) verbatim.

**Self-check before showing the researcher:**

- Verify every file path in Repository Structure exists inside `publication-staging/`.
- Verify `code/figure-reproduction/README.md` exists for papers with generated figures/tables and is referenced from `AGENTS.md`.
- Run every `code/figure-reproduction/` command marked `reproduced`; confirm generated outputs exist.
- Confirm computational requirements are accurate.

Fix any mechanical issues found.

### AGENTS.md validation

Invoke `/validate-publication --stage agents-md` with `publication-staging/` as the effective repository root — checks APP metadata, path validity, privacy, clear factual consistency, and reader-agent usability. Fix any errors. Show the validation report summary to the researcher before the iteration step — they can address both validation findings and their own feedback together.

## 4.2 Iterate on `AGENTS.md` with the researcher

Show the draft and discuss it. This is not a rubber-stamp review — it is a conversation about what the agent should convey.

Walk through `AGENTS.md` **one section at a time**, not as a wall of review. For each section, ask a focused question:

- **Paper Summary.** "Does this capture what makes your work distinctive? What would you change?"
- **Key Results.** "Are these the results you're most proud of, or just the easiest to describe? If someone remembers one thing from this paper, what should it be?"
- **What You Can Do / Extend the work.** "What questions do you wish people would ask about this work? What variations would be interesting?"

If the researcher says "looks good" without engaging with specifics, gently probe one concrete aspect — e.g. "I want to make sure the summary captures your intent. The first paragraph says [X] — does that match how you'd describe it?"

After walking through sections, ask:

- "Is there anything the agent should say that isn't in the paper itself — context, motivation, what you tried that didn't work?"

Revise `AGENTS.md` based on their feedback. Go back and forth until the researcher is satisfied that the agent represents their **intent**, not just their words.

## 4.3 Create `README.md`

Copy [`template/README.md`](../../template/README.md) to `publication-staging/README.md` and fill in each placeholder using information from phases 1-2 and the finalized `AGENTS.md`. The figure table should point to `code/figure-reproduction/README.md` and use the same status/script information as the `AGENTS.md` figure-reproduction summary, so the files stay checkable against each other.

The publication `README.md` is for readers who want to use the paper agent; it is not a copy of the working repo's README.

Show the README draft to the researcher and iterate on it before finalising.

## Handoff

`publication-staging/AGENTS.md`, `publication-staging/CLAUDE.md`, and `publication-staging/README.md` drafted and approved. Next: [`release.md`](release.md).
