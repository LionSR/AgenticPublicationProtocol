# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

APP is a format for packaging a finished academic paper as a GitHub repository, enabling an AI agent to present and explain the work interactively. An APP publication is a public Git repository with a tagged release, an AGENTS.md file at the root, and a verifiable APP publication manifest attached to the release. A reader can clone the repository, open it in any agent that supports AGENTS.md, and immediately access an agent that acts as a representative of the authors. This agent can explain the paper, reproduce figures, run experiments, and answer questions grounded in the work.

The goal of APP is to transform the format of academic publication. Rather than serving as a static record of research results, an APP publication becomes an interactive and dynamic medium that significantly lowers the cost of understanding, reproducing, and building upon the work. APP defines what an agentic publication looks like; it does not prescribe how authors should create one. That aspect is handled by the skills distributed alongside this specification. For installation and usage, see [README.md](README.md).

## Principles

- **Faithfulness to Ground Truth.**  
  The agent **MUST** base its responses on the authoritative contents of the publication, defined as the manuscript, code, and data included in the repository. When multiple sources are present, the agent **MUST** prioritize these over supplementary materials or external knowledge. If the authors’ claims differ from mainstream views, the agent **SHOULD** present the authors’ perspective accurately and explicitly. The agent **MAY** provide additional context but **MUST** clearly distinguish it from the authors’ claims.

- **Reproducibility.**  
  An APP publication **SHOULD** include all artifacts necessary to reproduce the main results of the work, including figures, tables, and key experiments. The repository **MUST** provide executable instructions (via `AGENTS.md` or scripts) that allow an agent to run these reproductions. Dependencies, environments, and expected outputs **SHOULD** be specified to minimize ambiguity.

- **Transparency and Provenance.**  
  The agent **SHOULD** make the origin of its responses clear by linking claims to specific files, code, or sections of the manuscript when possible. This ensures that users can verify, trace, and build upon the work with confidence.

- **Canonical Structure and Referencing.**  
  Each dataset, script, and artifact **MUST** have a single canonical location within the repository. The agent **SHOULD** reference resources by explicit paths. Duplicate or conflicting versions of files **SHOULD NOT** be included, in order to avoid ambiguity and ensure consistent interpretation.

- **Versioned Publication.**  
  A published APP **MUST** correspond to a tagged GitHub release, which defines an immutable snapshot of the work. The main branch **MAY** continue to evolve, but agents and users **SHOULD** default to interacting with a specific release to ensure consistency and reproducibility.

- **Agent Skills** (optional but recommended).
  Authors **SHOULD** provide reusable “skills” defined according to the Agent Skills Protocol (https://agentskills.io). These skills encapsulate procedures, workflows, or domain-specific expertise that go beyond what is explicitly described in the manuscript. While not mandatory, providing skills is strongly recommended, as they enable the agent to perform meaningful tasks such as reproducing experiments, analyzing outputs, and adapting explanations to different audiences.


## Repository layout

```
<repo-root>/
├── AGENTS.md          primary agent instructions
├── CLAUDE.md          one line: @AGENTS.md
├── README.md          human-facing README for readers
├── LICENSE
├── .gitignore         standard repo metadata; .gitattributes and .github/ are also allowed
├── paper/             paper source, figures, compiled PDF
├── code/              source and scripts, including figure reproduction code
├── data/              shipped datasets; external datasets are documented in data/README.md
├── environment/       README.md plus requirements.txt, environment.yml, Dockerfile, or equivalent
├── supplementary/     optional supplementary files such as authors' notes, slides, chat sessions, etc.
└── skills/            optional: author-published SKILL.md capabilities
```

`AGENTS.md`, `README.md`, `LICENSE`, and `paper/` are required for every publication. `code/`, `data/`, `environment/`, `supplementary/`, and `skills/` **MAY** be omitted when not applicable — for example, a theory-only paper with no code or data can ship only `paper/` plus the required root files. If the publication includes executable code, figure/table reproduction scripts, notebooks, or nontrivial build tools, `environment/README.md` **MUST** be included.

### `paper/`

The `paper/` directory contains the manuscript and all files required to read it, including the main document, compiled output, figures, and bibliography. Exactly one document **MUST** be designated as the canonical paper. Its format **MUST** be declared in the `paper_format` field of the `AGENTS.md` frontmatter, and its path or containing directory **MUST** be listed in the Where to Look section of `AGENTS.md`. The contents of `paper/` are considered ground truth for the work.

### `code/`

The `code/` directory contains source code distributed with the publication. It **MAY** be omitted for publications without code, such as theory-only papers. When present, typical subdivisions include `code/src/` for libraries, `code/scripts/` for entry points, `code/notebooks/` for notebooks, and `code/configs/` for configuration files. Paths used by scripts **MUST** resolve relative to the repository root and **MUST NOT** depend on absolute paths from the authors' machines. The contents of `code/` are considered ground truth for the work.

For papers with figures or tables generated from data or computation, `code/` **MUST** include an authoritative figure/table reproduction area:

```text
code/figure-reproduction/
  README.md
  fig01_<short-name>.py
  fig02_<short-name>.py
  ...
```

`code/figure-reproduction/README.md` is the source of truth for mapping each paper figure/table to reproduction code. It **MUST** list every paper figure/table, the paper artifact path, the reproduction script, inputs, generated output path, status, and notes. Generated reproduction outputs **SHOULD** be local run artifacts written under `code/figure-reproduction/generated/` unless the figure map documents a stronger local convention. They **SHOULD NOT** be committed by default, and the generated-output directory **SHOULD** be listed in `.gitignore`. Commit generated reproduction outputs only when they are intentional publication artifacts, validation evidence, or otherwise not cheaply reproducible; in that case, `code/figure-reproduction/README.md` **MUST** explain why they are included and how they were generated. The publication **SHOULD** provide one direct script per figure/table. A grouped wrapper that produces multiple figures or tables is allowed when this is the clearest direct entry point, but the README **MUST** say it is a grouped wrapper and list every artifact and generated output it covers. If a figure/table cannot be directly reproduced, the README **MUST** document the attempted source scripts/notebooks, the attempted command, and the concrete blocker such as missing data, heavy compute, external dependency/network failure, manual post-processing, or a failing command. Final statuses **MUST** be explicit reproduction states or blockers; temporary statuses such as `not-yet-run` are not valid for a release candidate.

### `data/`

The `data/` directory contains datasets small enough to be stored comfortably in git, typically no more than a few tens of megabytes each. Whenever a publication uses any dataset — local or external — `data/README.md` **MUST** exist and describe each dataset, including what it is, how it was produced, and which figures or scripts use it. Large datasets **SHOULD** remain on external hosts such as Hugging Face, Zenodo, or Figshare; `data/README.md` **MUST** record the URL, exact download command, local destination, and whether the dataset is required for the default workflow. The contents of `data/` are considered ground truth for the work.

### `environment/`

The `environment/` directory contains the files required to recreate the runtime environment, such as `README.md`, `requirements.txt`, `pyproject.toml`, `uv.lock`, `Project.toml`, `Manifest.toml`, `renv.lock`, `environment.yml`, `package.json`, lockfiles, `Dockerfile`, or an equivalent specification. If multiple dependency specifications are present, such as both pip and conda files, `environment/README.md` **MUST** identify the canonical environment specification.

When `environment/` is present, `environment/README.md` **MUST** describe the tested platform, dependency files, exact setup commands, and the command prefix that readers and agents should use to run code, such as `.venv/bin/python`, `uv run`, `JULIA_DEPOT_PATH=.julia_depot julia --project=code`, `Rscript`, `octave`, `matlab -batch`, or `wolframscript`. `AGENTS.md` and README **MUST** point to `environment/README.md` for these details instead of becoming independent sources of setup truth.

Installed environments and package caches, such as `.venv/`, `.julia_depot/`, `node_modules/`, conda environment directories, and tool caches, **SHOULD NOT** be committed. They **SHOULD** be listed in `.gitignore` and recreated from the dependency manifests, lockfiles, and commands committed to the repository. If external software is required but cannot be bundled or installed by the agent, including licensed/proprietary/manual tools such as VASP, MATLAB, Mathematica, COMSOL, Gaussian, or commercial solvers, `environment/README.md` **MUST** still document the requirement: software name, version if known, required modules/toolboxes/paclets/pseudopotentials/licenses, expected executable or command, what was tested, and any open alternative or reason no alternative is available.

### `supplementary/`

The optional `supplementary/` directory contains materials that provide additional context for understanding the work but are not part of the ground truth. Paper appendices that are necessary for understanding the paper **SHOULD** be included in `paper/` rather than `supplementary/`. Typical files include:

- `supplementary/know-how.md` — methodology decisions, tacit insights, practical knowledge from the research process.
- `supplementary/authors-note.md` — what the authors want readers to know beyond the paper.
- `supplementary/sessions/` — curated human-AI and/or human-human conversation transcripts from development, if the authors decide to share that.
- `supplementary/materials/` — slides, talks, posters, tutorials.

### `skills/`

The optional `skills/` directory contains agent capabilities shipped with the paper, following the [Agent Skills Protocol](https://agentskills.io). Each skill **MUST** be a directory `skills/<name>/` containing a `SKILL.md` file with `name` and `description` in YAML frontmatter and step-by-step instructions in the body. A typical skill exposes a paper-specific computation so that a reader or agent can invoke the paper's method directly.

### `AGENTS.md`

`AGENTS.md` is the file an agent reads first when the repository is opened. It **MUST** be standard Markdown compatible with [agents.md](https://agents.md), and it **MUST** contain two parts: YAML frontmatter and a Markdown body. An example is provided in `template/AGENTS.md`.

#### Frontmatter

```yaml
---
protocol: agentic-publication-protocol
protocol_version: "0.1.0"
title: "Your Paper Title"
authors:
  - name: "Author Name"
    affiliation: "Institution"
arxiv_id: "XXXX.XXXXX"       # optional
paper_format: "latex"          # latex, docx, markdown, html, video, pptx, pdf
version: "1.0.0"               # matches the git tag, without the leading v
domain: "your-field"
tags: ["keyword1", "keyword2"]
recommended_external_skills:
  - id: "org.example/proofread-paper"     # optional; reverse-DNS or org/name namespace
    version: "1.2.0"                      # optional; exact release/tag preferred
    source: "https://github.com/example/app-skills/tree/v1.2.0/proofread-paper"
    purpose: "Proofread manuscript prose before APP staging."
app_extensions:
  - id: "org.example/field-publishing"
    version: "0.1.0"
    source: "https://github.com/example/app-extensions/tree/v0.1.0/field-publishing"
    required: false
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `protocol` | yes | Always the literal string `agentic-publication-protocol`. |
| `protocol_version` | yes | APP version this publication targets. |
| `title` | yes | Paper title. |
| `authors` | yes | List of `{name, affiliation}` entries. |
| `arxiv_id` | no | arXiv identifier, if applicable. |
| `paper_format` | yes | Format of the canonical document in `paper/`. |
| `version` | yes | Publication version. Matches the git tag, without the leading `v` (tag `v1.0.0` → `"1.0.0"`). |
| `domain` | yes | Short field tag (e.g. `condensed-matter`, `nlp`, `combinatorics`). |
| `tags` | no | Free-form keyword list. |
| `recommended_external_skills` | no | External Agent Skills that may help readers, authors, or agents work with the publication. These are recommendations only and are not author-approved ground truth unless bundled into the release and explicitly identified as such. |
| `app_extensions` | no | Optional APP-related extensions supported or recommended by this publication. Extensions **MUST** be optional unless `required: true` is explicitly set; if required, the publication **MUST** describe fallback behavior or the reason no fallback is possible. |

#### Required sections

- **Identity** — who the agent is and how it should behave. References the paper title, authors, and domain. States that the paper manuscript, code, and data are the ground truth for all claims.
- **Paper Summary** — 1–2 concise paragraphs covering the problem, approach, main results, and implications. In the authors' own words.
- **Key Results** — numbered list of the main contributions, phrased as the authors want them cited.
- **Where to Look** — concise pointers to canonical files and directories with their roles. Detailed setup, data, figure/table reproduction, validation, and license information belongs in the dedicated README or report files rather than being duplicated in `AGENTS.md`.
- **Reader-Help Operating Mode** — concrete behavior for helping readers: answer science questions first, inspect direct staged evidence when useful, cite specific files/sections/scripts/data, use canonical reproduction/setup/data docs, warn before heavy or risky commands, and distinguish evidence levels such as paper claim, staged artifact, locally reproduced, newly checked, inferred, or blocked.
- **Citation** — full BibTeX entry.

#### Optional sections

- **Supplementary Materials** — pointers to `supplementary/`. One line per item, noting what it is and that it is secondary to the paper.
- **Skills** — list of `skills/<name>/` entries, each with a one-line description.
- **External Skills and Extensions** — optional list of skills or extensions hosted outside the publication repository, including source URL, version or tag when available, purpose, and trust status.

### External skills and extensions

APP deliberately keeps the core publication format small. Reusable writing, proofreading, journal-response, field-specific, or workflow-specific capabilities **SHOULD** usually be distributed as external Agent Skills or APP extensions rather than added to the APP core specification. This follows the same separation as other agent protocols: the core protocol defines the stable artifact, while optional extensions evolve independently.

External skills and extensions are declared in the `recommended_external_skills` and `app_extensions` frontmatter fields. The optional **External Skills and Extensions** section of `AGENTS.md` may provide human-readable context for those declarations, but it should not be the only place machine-actionable external references appear. These references let a publication point to a separate APP skills repository, a field-specific repository, or an individual contributor's repository without copying the skill into the publication release.

External skill and extension identifiers **SHOULD** be namespaced to avoid collisions. Recommended formats are:

- reverse-DNS style: `edu.example/latex-proofreader`, `org.lab/quantum-code-review`
- host-scoped style: `github.com/owner/repo/skill-name`
- organization style: `app/validate-publication`, reserved for official APP-maintained skills

Each external entry **SHOULD** include:

- `id` — stable namespaced identifier.
- `source` — repository URL, registry URL, or immutable release/tag URL.
- `version` — exact version, tag, or commit when known.
- `purpose` — one sentence saying when an agent should use it.
- `required` — for extensions only; defaults to `false`.

External skill sources **SHOULD** point directly to a skill directory containing `SKILL.md`, preferably at a stable tag or commit. The APP protocol does not define a separate index or registry format for reusable skills. A protocol-maintained collection, a field-maintained collection, and an individual researcher's repository can all be valid sources as long as referenced entries have stable identifiers, stable source URLs, and clear licensing.

External skills and extensions **MUST NOT** be treated as part of the publication's scientific ground truth merely because they are referenced. The paper, code, and data bundled in the tagged APP release remain authoritative. A third-party skill may help proofread, analyze, reproduce, or explain, but it cannot alter the authors' claims unless the authors incorporate the resulting changes into a new APP release.

If a skill is necessary for representing the paper's own method or reproducing paper-specific results, authors **SHOULD** bundle it under `skills/` in the publication repository. If a skill is reusable across papers, journals, disciplines, or authoring workflows, authors **SHOULD** publish it externally and reference it from `AGENTS.md`.

Agents loading a publication **SHOULD** gracefully degrade when an external skill or extension is unavailable. They may explain that an optional capability was recommended but not installed, then continue using the bundled APP contents. Agents **SHOULD** attempt safe, reproducible dependency installation when the host environment authorizes it, especially project-local installs from bundled dependency files. Agents **MUST** ask for user approval before installing, cloning, or running untrusted external code when the host environment requires such approval or when the action may affect the user's filesystem, network, credentials, licenses, or substantial compute/network/disk resources. When a dependency is not installed, the agent should record whether installation was attempted, skipped for lack of authorization, or blocked by licensing/platform constraints.

### `README.md`

Each APP publication **MUST** include a `README.md` file at the root of the repository. The README is the human-facing entry point for readers and **SHOULD** summarize the paper, identify the authors, and link to the canonical public record when available, such as arXiv, DOI, or PDF.

The README **SHOULD** explain that the repository is an APP publication and that readers can clone the repository and open it in an AI coding agent that reads `AGENTS.md`. It **SHOULD** provide practical instructions for interacting with the paper through supported agents, reproducing figures or results, setting up the environment, and citing the work. When an executable environment is needed, README and `AGENTS.md` **MUST** point to `environment/README.md` for detailed environment notes. The README **MAY** include a short human-facing quickstart, but detailed setup commands, runner prefixes, data access, figure/table status maps, runtimes, and blockers should live in their canonical docs to avoid stale duplicates.

### `LICENSE`

Each APP publication **MUST** include a `LICENSE` file at the root of the repository that clearly specifies the terms under which the contents of the publication may be used, modified, and redistributed. The license **SHOULD** cover all relevant components, including the manuscript, code, data, and any auxiliary materials, or explicitly state if different components are distributed under different licenses. If any part of the repository is subject to additional restrictions (e.g., third-party data, proprietary dependencies), these **MUST** be clearly indicated. The agent **SHOULD** be able to reference and communicate the licensing terms to users when relevant.

## Versioning

A publication is the pair `(repo URL, tag)`. Tags **MUST** be immutable; the main branch **MAY** continue to evolve. The recommended tag format is `vMAJOR.MINOR.PATCH` ([semver](https://semver.org)); other immutable tag names **MAY** be used. Every tag **MUST** correspond to a GitHub Release. When the tag uses the recommended `vMAJOR.MINOR.PATCH` form, the `version` field in AGENTS.md **MUST** match the tag without the leading `v` (tag `v1.0.0` → `version: "1.0.0"`); otherwise, `version` **MUST** match the tag exactly. External references — citations, arXiv ancillary links, personal pages — **SHOULD** point to a specific tag.

## Verified APP publication manifest

An `AGENTS.md` file makes a repository agent-readable, but it does not by itself prove that the repository is a validated APP publication. A fully verified APP publication **MUST** have an APP publication manifest associated with the public release.

The manifest is a JSON object distributed as a GitHub Release asset named `APP_PUBLICATION.json`. It **MAY** also be copied into the annotated tag message or another public registry, but the release asset is the canonical location for verification.

The manifest **MUST** include:

```json
{
  "protocol": "agentic-publication-protocol",
  "protocol_version": "0.1.0",
  "manifest_version": "1",
  "publication_type": "app-publication",
  "repo_url": "https://github.com/user/paper-repo",
  "tag": "v1.0.0",
  "commit": "<git-commit-sha>",
  "tree": "<git-tree-sha>",
  "app_publication_id": "app-v1:sha256:<hex-digest>",
  "validation": {
    "validated_by": "validate-publication",
    "validator_protocol_version": "0.1.0",
    "stage": "full",
    "result": "passed",
    "validated_at": "YYYY-MM-DD",
    "validation_report_sha256": "<sha256>"
  },
  "human_approval": {
    "approved": true,
    "approved_at": "YYYY-MM-DD",
    "approved_by": ["Author Name"],
    "approval_statement": "The listed authors approved this release as an APP publication."
  }
}
```

The `app_publication_id` **MUST** be computed from a canonical JSON payload that excludes `app_publication_id` itself and includes at least:

- `protocol`
- `protocol_version`
- `manifest_version`
- `publication_type`
- `repo_url`
- `tag`
- `commit`
- `tree`
- `validation.validation_report_sha256`
- `validation.result`
- `human_approval.approved`
- `human_approval.approved_at`
- `human_approval.approved_by`

The recommended identifier format is:

```text
app-v1:sha256:<sha256(canonical-json-payload)>
```

The manifest is valid only for the exact `(repo_url, tag, commit, tree)` it names. A loader verifies APP status by downloading the release manifest, checking that the local checkout matches the manifest commit and tree, recomputing `app_publication_id`, and confirming that validation passed and human approval is recorded.

Repositories without a valid manifest can still be useful:

- `AGENTS.md` present, no APP frontmatter: agent-readable repository.
- `AGENTS.md` with `protocol: agentic-publication-protocol`, no valid manifest: APP-structured candidate.
- Valid release manifest matching the checkout: verified APP publication.


## License

This specification is released under CC-BY-4.0.
