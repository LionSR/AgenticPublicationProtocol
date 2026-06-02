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

If an AI-written derivation could help readers, default to proposing it as optional context under `supplementary/`. Explain:

- `paper/` is ground truth: material there is treated as part of the paper.
- `supplementary/` is optional additional context: useful, but secondary to the paper.

If the derivation seems essential for understanding the work, tell the author why and ask whether they want to revise the paper or keep the derivation supplementary. The author decides placement. Never silently add AI-written derivations to `paper/`.

Record checked steps, uncertainty, and author decisions in `working/reproduction/reproduction-report.md`.

