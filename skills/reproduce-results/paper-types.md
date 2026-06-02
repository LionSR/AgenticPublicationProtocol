# Paper Type Guidance

Consult this when the paper is not a default LaTeX-plus-code computational paper.

## Theory-only

Focus on canonical manuscript, assumptions, theorem/proof structure, and derivation checks. `code/`, `data/`, and `environment/` may be absent in the final APP staging tree.

## Computational

Map scripts/notebooks to key results, figures, and tables. Record data and environment requirements. Do not run heavy experiments without author approval; record exact blockers.

## Experimental

Reproduce analysis and figures when possible. Make clear that the physical experiment cannot be rerun by the agent unless the necessary lab setup exists.

## Notebooks

Map notebooks to figures/results and execution order. Consider wrapper scripts for final staging, but do not change the scientific content.

## Video / Slideware / PDF-only

Identify the canonical object and provide enough text summary or transcript context for the future paper agent, while keeping the original object as ground truth.

