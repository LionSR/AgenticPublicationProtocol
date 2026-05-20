# Phase 3 Support — Environment Setup

Use this file from [`build.md`](build.md) whenever the publication includes runnable code, generated figures/tables, notebooks, a compilable manuscript with nontrivial tooling, or external software needed for reproduction.

## Create `environment/README.md`

If the publication includes executable artifacts or nontrivial tooling, create:

```text
publication-staging/environment/README.md
```

Use [`template/environment-README.md`](../../template/environment-README.md) as a starting point, but remove unused examples before final validation. If the publication has no executable artifacts, omit `environment/` or include a short README saying no computational environment is required.

Installed environments are normally **not** publication artifacts. Gitignore local environment directories and caches such as `.venv/`, `.julia_depot/`, `node_modules/`, `.Rproj.user/`, `.renv/` package caches, `.matlab/`, `.wolfram/`, `.cache/`, and tool-specific build caches unless the researcher explicitly identifies a small file as source material. The published repo must instead include enough recipes and pinned dependency files to recreate the environment.

## Detect Toolchains

Detect the relevant toolchain from the source tree and staged files:

- Python: `pyproject.toml`, `uv.lock`, `requirements.txt`, `environment.yml`, imports, notebooks.
- Julia: `Project.toml`, `Manifest.toml`.
- R: `renv.lock`, `DESCRIPTION`, `install.R`.
- Node/JavaScript: `package.json`, npm/pnpm/yarn lockfiles.
- MATLAB/Octave: `.m` files, required toolboxes/packages, Octave compatibility.
- Mathematica/Wolfram: `.nb`, `.wl`, required paclets/kernel version.
- Licensed or manually installed scientific software: VASP, COMSOL, Gaussian, commercial solvers, domain-specific binaries, cluster modules, pseudopotential libraries, license servers, and wrapper scripts.
- TeX and document tools: `latexmkrc`, `.sty`, BibTeX/Biber, `pandoc`, `make`.
- System tools: `make`, `cmake`, `ffmpeg`, solvers, CUDA/GPU drivers, compilers.

## Required Contents

`environment/README.md` must record:

- supported platform(s) and versions actually tested, or "not tested";
- dependency recipe files included in the repo, such as `environment/requirements.txt`, `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`, `environment.yml`, `package-lock.json`, or `renv.lock`;
- exact setup commands from the staging root;
- exact command prefixes readers/agents should use, such as `.venv/bin/python`, `uv run`, `JULIA_DEPOT_PATH=.julia_depot julia --project=code`, `Rscript`, `octave`, `matlab -batch`, or `wolframscript`;
- what local generated environment directories are intentionally gitignored and how to recreate them;
- heavyweight, proprietary, credentialed, platform-specific, or manually installed requirements;
- required external software that cannot be bundled or installed by the agent, including software name, version if known, license/access requirement, required modules/toolboxes/paclets/pseudopotentials, expected executable/command, and what was or was not tested;
- setup commands attempted during staging and their result.

Also make `AGENTS.md` and `README.md` contain the same setup information in concise form; `environment/README.md` is the detailed source of truth.

## Dependency Installation Policy

Before marking a figure/table or validation command `blocked-dependency`, make a reasonable attempt to prepare the needed execution environment when it is safe and authorized in the host environment.

Safe install attempts include project-local or environment-scoped installs from explicit dependency files, such as:

- `python -m venv .venv && .venv/bin/pip install -r environment/requirements.txt`
- `uv sync`
- `npm ci` or `npm install`
- `JULIA_DEPOT_PATH=.julia_depot julia --project=code -e 'using Pkg; Pkg.instantiate()'`
- `Rscript`/`renv` restore commands
- TeX package manager commands
- conda/mamba environment creation when those tools are already available

Prefer installs that are reproducible, logged, and scoped to the staged project or a disposable environment.

Do not commit installed environments such as `.venv/`, `.julia_depot/`, `node_modules/`, conda env directories, or package caches. Commit the dependency manifests, lockfiles, and setup instructions needed to recreate them.

Ask the researcher before installing or cloning anything when:

- the platform requires approval or the current agent lacks authorization;
- the install would modify global system state, consume substantial disk/network/compute, require credentials, accept a license, or run untrusted external code;
- the dependency is proprietary, commercial, platform-specific, unusually large, or likely to affect the user's machine beyond the current project.

If authorization is already available and the install is low-risk, try it and record the command and result in `environment/README.md` and later in `supplementary/validation-report.md`. If authorization is absent, unclear, denied, or the dependency cannot be safely installed, ask for permission or record the precise blocker.

A `blocked-dependency` entry must say whether a safe install was attempted, skipped for authorization/safety reasons, or impossible because of licensing/platform constraints.

## Verification From Staging Root

During `build.md` phase 3.5, if `environment/README.md` exists:

- run documented setup or verification commands when safe;
- verify tool versions;
- verify commands use the intended environment (`.venv/bin/python`, `uv run`, project-local Julia depot, conda env, MATLAB/Octave, Wolfram, etc.);
- if setup is unsafe, unavailable, proprietary, credentialed, or too heavy, record the precise blocker.

Record results in `environment/README.md` and later in `publication-staging/supplementary/validation-report.md`.
