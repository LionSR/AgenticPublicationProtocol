# Phase 4 — Draft

The **author's voice** principle declared in [`SKILL.md`](SKILL.md) is especially load-bearing in this phase.

## 4.1 Create `AGENTS.md`

Tell the researcher you're drafting `AGENTS.md` now, drawing on everything from phases 1–2.

The schema — every required frontmatter field, every required and optional body section — is defined in [PROTOCOL.md § AGENTS.md](../../PROTOCOL.md#agentsmd). Read it before drafting. Do not paraphrase or re-derive the schema here. The guidance below is about *how to fill the schema well*, not *what the schema is*.

Use [`template/AGENTS.md`](../../template/AGENTS.md) as a starting skeleton.

**Drafting guidance — things easy to get wrong:**

- **Paper Summary.** Before drafting, ask the researcher: "What's the core message you want someone to take away from this paper?" Their answer sets the direction — do not draft from your own reading first. Use the researcher's own words from phase 2 and any extracted context as the foundation. This section is what the agent will rely on most; make it substantive, not generic.
- **Repository Structure.** Don't just list files — explain what each does and how they connect. Mark `paper/`, `code/`, and `data/` as ground truth for the work. Group by function: paper source, figure generation, experiments, data, config. Use paths relative to the repo root. For datasets — local or external — put the detail (URL, download command, local destination, required-for-default-workflow flag) in `data/README.md`. `AGENTS.md` Repository Structure carries only a one-liner pointer (e.g. `data/README.md — dataset documentation`).
- **What You Can Do.** Real, copy-pasteable commands — no placeholders. The figure-reproduction table covers every figure in the paper as a 1:1 mapping — one script per figure. For "Run experiments" and "Extend the work," the goal is that a reader can answer "what if I change X?" by running something concrete.
- **Computational Requirements.** Classify every task (figure generation, individual experiments, full reproduction) by time, hardware, and memory. Note the platform tested on (OS, language version). The agent MUST warn before running anything heavy.
- **Identity.** Keep the spokesperson framing — the agent represents *these authors' work*, not a generic assistant. The Identity section must state that the paper manuscript, code, and data are the ground truth for all claims. Domain voice matters: a math paper's agent reasons like a mathematician; an experimental paper's agent thinks like an experimentalist.

Also create `CLAUDE.md` — one line: `@AGENTS.md`. You can copy [`template/CLAUDE.md`](../../template/CLAUDE.md) verbatim.

**Self-check before showing the researcher:**

- Verify every file path in Repository Structure exists in the publication repo.
- Run every command in the figure generation table.
- Confirm computational requirements are accurate.

Fix any mechanical issues found.

### AGENTS.md validation

Invoke `/validate-publication --stage agents-md` — checks factuality against the paper, path validity, privacy, and substance. Fix any errors. Show warnings to the researcher before the iteration step — they can address both validation findings and their own feedback together.

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

Copy [`template/README.md`](../../template/README.md) to the publication repo root and fill in each placeholder using information from phases 1–2 and the finalized `AGENTS.md`. The figure table uses the same schema as the `AGENTS.md` "Reproduce figures" table — `Figure | Command | Data | Time` — so the two tables stay checkable against each other.

The publication `README.md` is for readers who want to use the paper agent; it is not a copy of the working repo's README.

Show the README draft to the researcher and iterate on it before finalising.

## Handoff

`AGENTS.md`, `CLAUDE.md`, and `README.md` drafted and approved. Next: [`release.md`](release.md).
