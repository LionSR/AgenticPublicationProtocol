# Working notes (fixture)

These are informal author notes, the kind of context a real working repo
carries before publication. They exist so the `publish-paper` interview has
material to draw on when driven by the harness.

- **Key result.** The sum of the first N integers equals N(N+1)/2, verified
  numerically to exact agreement for N = 1..100.
- **Figure.** `paper/figures/fig1.png` is produced by `src/generate_fig1.py`.
  It needs only matplotlib.
- **Audience.** This is a test fixture; treat the intended audience as
  "people verifying the publication tooling," not a real research community.
- **Scope.** Single short LaTeX manuscript, one figure, one tiny script. No
  datasets. No heavy compute (runs in well under a second).
- **License intent.** MIT for code, CC-BY for the manuscript is fine.
