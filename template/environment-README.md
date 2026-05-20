# Environment

This file is the source of truth for recreating the computational environment for this APP publication.

## Summary

- Tested platform: <!-- OS, architecture, date -->
- Primary toolchain: <!-- Python / Julia / R / Node / MATLAB / Mathematica / TeX / other -->
- Environment required: <!-- yes/no; if no, explain -->
- External/proprietary requirements: <!-- GPU, VASP, MATLAB toolbox, Mathematica paclet, licensed solver, credentials, pseudopotential library, cluster module, etc. -->

## Dependency Files

List the files committed to this repository that recreate the environment.

- `environment/requirements.txt` — <!-- Python dependencies, if applicable -->
- `pyproject.toml` / `uv.lock` — <!-- Python project/lock, if applicable -->
- `code/Project.toml` / `code/Manifest.toml` — <!-- Julia project/lock, if applicable -->
- `environment/environment.yml` — <!-- conda/mamba environment, if applicable -->
- `package.json` / lockfile — <!-- Node dependencies, if applicable -->
- `renv.lock` — <!-- R dependencies, if applicable -->

## Setup From Repository Root

Replace this with the actual setup commands. Do not leave unused examples in the final publication.

### Python Example

```sh
python -m venv .venv
.venv/bin/pip install -r environment/requirements.txt
```

Run Python commands with:

```sh
.venv/bin/python <script>
```

### Julia Example

```sh
JULIA_DEPOT_PATH=.julia_depot julia --project=code -e 'using Pkg; Pkg.instantiate()'
```

Run Julia commands with:

```sh
JULIA_DEPOT_PATH=.julia_depot julia --project=code <script>
```

### MATLAB / Octave Example

```sh
octave <script.m>
# or
matlab -batch "<command>"
```

State the MATLAB release, required toolboxes, and whether Octave was tested.

## External Or Licensed Software

If reproducing the paper requires software that is not bundled with this repository and cannot be installed automatically, document it here even if the current agent could not run it.

| Software | Version | Required components | Access/license | Expected command | Tested here? | Notes |
|----------|---------|---------------------|----------------|------------------|--------------|-------|
| <!-- VASP / MATLAB / Mathematica / COMSOL / Gaussian / solver --> | <!-- version --> | <!-- toolboxes, paclets, pseudopotentials, modules --> | <!-- license/credentials/manual install --> | <!-- command or executable --> | <!-- yes/no --> | <!-- blocker or alternative --> |

## Gitignored Local Environment Artifacts

The following local environment directories/caches are intentionally not committed. Recreate them with the setup commands above.

- `.venv/`
- `.julia_depot/`
- `node_modules/`
- `.cache/`

## Validation Evidence

Record setup and verification commands attempted during staging.

| Command | Working directory | Result | Notes |
|---------|-------------------|--------|-------|
| <!-- command --> | <!-- repo root --> | <!-- passed/blocked --> | <!-- versions/errors --> |
