# Environment Setup

Create `publication-staging/environment/README.md` whenever the candidate has runnable code, notebooks, figure/table scripts, compilable paper tooling, or external software requirements.

Use `template/environment-README.md` as the starting point. Remove unused examples.

## Detect

Look for Python, Julia, R, Node, MATLAB/Octave, Wolfram, TeX, system tools, cluster scripts, CUDA/GPU requirements, and licensed/proprietary tools.

## Document

`environment/README.md` must record:

- tested platform/version or "not tested";
- dependency files included in `environment/`;
- exact setup commands from staging root;
- exact runner prefix, such as `.venv/bin/python`, `uv run`, `julia --project=code`, `Rscript`, `octave`, `matlab -batch`, or `wolframscript`;
- local environment/cache directories intentionally gitignored;
- heavy, credentialed, proprietary, platform-specific, or manual requirements;
- setup commands attempted and their result.

`AGENTS.md` and README later include the same setup information in concise form.

## Install Policy

Attempt safe project-scoped installs from explicit dependency files when authorized. Ask before global, risky, proprietary, credentialed, unusually large, or system-invasive installs.

Never commit installed environments such as `.venv/`, `.julia_depot/`, `node_modules/`, conda env folders, package caches, or notebook caches.

