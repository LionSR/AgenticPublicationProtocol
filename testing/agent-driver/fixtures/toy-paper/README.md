# Toy paper (harness fixture)

A deliberately tiny "working repo" used to exercise the `publish-paper`
workflow under the PTY harness. It is **not** an APP publication itself — it
is the messy author-side input that `publish-paper` reorganizes into a
`publication-staging/` tree.

Contents:

- `paper/main.tex` — a one-page manuscript with a single result and figure.
- `paper/figures/fig1.png` — the figure used by the manuscript.
- `src/generate_fig1.py` — reproduces the figure (needs only matplotlib).
- `requirements.txt` — the lone dependency.
- `notes.md` — informal author context for the publication interview.

Reproduce the figure:

```bash
pip install -r requirements.txt
python src/generate_fig1.py   # -> paper/figures/fig1.png
```
