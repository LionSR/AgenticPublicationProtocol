# Handling different paper types

The paper can be in any format — LaTeX, DOCX, Markdown, HTML, video, PPTX, PDF. Adapt the process accordingly. Consult this file whenever the paper is not a standard LaTeX-plus-code computational paper.

## Theory-only paper (no code)

- Minimal layout: `paper/`, `supplementary/checklist.md`, plus the always-required root files `AGENTS.md`, `README.md`, and `LICENSE`. `code/`, `data/`, `environment/` can all be absent.
- Focus the agent on: explaining the theorems, the proof strategy, the assumptions.
- The agent's value is discussing the ideas and connecting them to related work.
- The phase 4 figure-reproduction table may be empty or absent; flag this in `AGENTS.md` rather than leaving a stub table.

## Computational paper

- Full Repository Structure, figure table, experiment commands.
- Extra care on environment specification — computational papers are the hardest to reproduce.
- Document cluster/GPU requirements clearly in `AGENTS.md` Computational Requirements.
- In phase 3.3, actually run the main experiments at least once on a clean checkout.

## Experimental paper (wet lab, etc.)

- Code is typically analysis scripts, not the experiment itself.
- Focus on data-analysis reproduction and figure generation.
- The agent explains the experimental setup but cannot re-run it — make that limit explicit in `AGENTS.md` Computational Requirements ("the experiment cannot be re-run without lab equipment; the agent can walk through the analysis").

## Paper with notebooks

- Map notebooks to figures/results: "notebook X produces figure Y".
- Note execution order when it matters.
- Consider extracting key cells into standalone scripts for easier reproduction; this is a phase 3 judgment call per researcher preference.

## Video / slideware paper

- The video or `.pptx` is the ground truth document.
- The agent should be able to discuss contents and reference specific sections or timestamps.
- Supplementary materials may include a transcript or text summary to support the agent in answering questions — but the video/slides remain the authoritative reference.
