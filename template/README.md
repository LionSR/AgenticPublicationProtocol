# [Paper Title]

[Authors, affiliations]

[1–2 sentence summary of the paper]

[Link to arXiv / DOI / PDF if available]

## Talk to this paper

This paper is published with an AI agent ([Agentic Publication Protocol](https://github.com/LionSR/AgenticPublicationProtocol)). Clone this repo and open it in an AI coding agent to ask questions, reproduce figures, and explore the work.

**Claude Code:** clone and open — it reads `AGENTS.md` automatically. Or use `/load-paper https://github.com/<owner>/<repo>`.

**Codex or other agents:** clone and open — any agent that reads `AGENTS.md` picks up the paper context.

## Figures

Authoritative figure reproduction map: `code/figure-reproduction/README.md`.

| Figure | Paper artifact | Script | Status | Time |
|--------|----------------|--------|--------|------|
| Fig 1 (description) | `paper/figures/fig1.png` | `python code/figure-reproduction/fig01_example.py` | reproduced | ~5s |
| Fig 2 (description) | `paper/figures/fig2.png` | `python code/figure-reproduction/fig02_example.py` | reproduced | ~10s |

## Reproducing results

### Setup

[copy the concise setup from AGENTS.md; point to `environment/README.md` for details when present]

Example Python layout:

```sh
python -m venv .venv
.venv/bin/pip install -r environment/requirements.txt
```

Run Python commands with `.venv/bin/python ...`. The `.venv/` directory is intentionally gitignored and should be recreated locally from the included dependency files.

### Run figures

[Use the commands in `code/figure-reproduction/README.md`. Run them with the environment prefix documented above and in `environment/README.md`. Generated outputs are written under `code/figure-reproduction/generated/` unless the figure map says otherwise. They are local run artifacts and are gitignored by default unless the figure map explicitly documents that generated outputs are intentionally committed.]

### Full experiment

[how to run from scratch, if applicable]

## Citation

```bibtex
[bibtex entry]
```

## License

See `LICENSE` for reuse terms.
