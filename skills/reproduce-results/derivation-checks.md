# Analytic Derivation Checks

Use this for theory papers and for computational papers with nontrivial formulas, theorems, scaling laws, bounds, or derivations.

## What to Check

- Identify theorems, propositions, lemmas, derivations, formulas, and assumptions that support key results.
- Verify included derivation steps when feasible.
- Check that symbols, assumptions, limiting cases, and cited results are consistent with the paper.
- Distinguish:
  - derivations present in the paper;
  - derivations quoted from literature;
  - derivations that seem necessary but absent;
  - derivations too long or specialized to verify in the session.

## Author Control

If a more detailed derivation of key steps would help readers or future agents, write a detailed note in Markdown or LaTeX and inform the author. Add the note to `supplementary/` by default. Explain:

- `paper/` is ground truth: material there is treated as part of the paper.
- `supplementary/` is optional additional context: useful, but secondary to the paper.

If the derivation seems essential for understanding the work, tell the author why. If they want the note to become part of the paper itself, they should move or adapt it into `paper/`. The author decides placement. Never silently add agent-written derivations to `paper/`.

Record checked steps, uncertainty, and author decisions in `working/reproduction/reproduction-report.md`.
