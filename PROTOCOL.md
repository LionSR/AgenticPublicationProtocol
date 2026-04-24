# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

APP is a format for packaging a finished academic paper as a GitHub repository, enabling an AI agent to present and explain the work interactively. An APP publication is a public Git repository with a tagged release and an AGENTS.md file at the root. A reader can clone the repository, open it in any agent that supports AGENTS.md, and immediately access an agent that acts as a representative of the authors. This agent can explain the paper, reproduce figures, run experiments, and answer questions grounded in the work.

The goal of APP is to transform the format of academic publication. Rather than serving as a static record of research results, an APP publication becomes an interactive and dynamic medium that significantly lowers the cost of understanding, reproducing, and building upon the work. APP defines what an agentic publication looks like; it does not prescribe how authors should create one. That aspect is handled by the skills distributed alongside this specification. For installation and usage, see [README.md](README.md).

## Principles

- **Faithfulness to Ground Truth.**  
  The agent **MUST** base its responses on the authoritative contents of the publication, defined as the manuscript and primary code included in the repository. When multiple sources are present, the agent **MUST** prioritize these over supplementary materials or external knowledge. If the authors’ claims differ from mainstream views, the agent **SHOULD** present the authors’ perspective accurately and explicitly. The agent **MAY** provide additional context but **MUST** clearly distinguish it from the authors’ claims.

- **Reproducibility.**  
  An APP publication **SHOULD** include all artifacts necessary to reproduce the main results of the work, including figures, tables, and key experiments. The repository **MUST** provide executable instructions (via `AGENTS.md` or scripts) that allow an agent to run these reproductions. Dependencies, environments, and expected outputs **SHOULD** be specified to minimize ambiguity.

- **Transparency and Provenance.**  
  The agent **SHOULD** make the origin of its responses clear by linking claims to specific files, code, or sections of the manuscript when possible. This ensures that users can verify, trace, and build upon the work with confidence.

- **Canonical Structure and Referencing.**  
  Each dataset, script, and artifact **MUST** have a single canonical location within the repository. The agent **SHOULD** reference resources by explicit paths. Duplicate or conflicting versions of files **SHOULD NOT** be included, in order to avoid ambiguity and ensure consistent interpretation.

- **Versioned Publication.**  
  A published APP **MUST** correspond to a tagged GitHub release, which defines an immutable snapshot of the work. The main branch **MAY** continue to evolve, but agents and users **SHOULD** default to interacting with a specific release to ensure consistency and reproducibility.

- **Agent Skills (Optional but Recommended).**  
  If possible, authors **SHOULD** provide reusable “skills” defined according to the Agent Skills Protocol (https://agentskills.io/home). These skills encapsulate procedures, workflows, or domain-specific expertise that go beyond what is explicitly described in the manuscript. While not mandatory, providing skills is strongly recommended, as they enable the agent to perform meaningful tasks such as reproducing experiments, analyzing outputs, and adapting explanations to different audiences.





## Repository layout

```
<repo-root>/
├── AGENTS.md          primary agent instructions
├── CLAUDE.md          one line: @AGENTS.md
├── README.md          human-facing README for readers
├── LICENSE
├── .gitignore         standard repo metadata; .gitattributes and .github/ are also allowed
├── paper/             paper source, figures, compiled PDF
├── code/              source and scripts
├── data/              shipped datasets; external datasets are documented in AGENTS.md
├── environment/       requirements.txt, environment.yml, Dockerfile, or equivalent
├── supplementary/     optional supplementary files such as authors' notes, slides, chat sessions, etc.
└── skills/            optional: author-published SKILL.md capabilities
```

### `paper/`

The `paper/` directory contains the manuscript and all files required to read it, including the main document, compiled output, figures, and bibliography. Exactly one document **MUST** be designated as the canonical paper. Its format **MUST** be declared in the `paper_format` field of the `AGENTS.md` frontmatter, and its path **MUST** be listed in the Repository Structure section of `AGENTS.md`. The contents of `paper/` are considered ground truth for the work.

### `code/`

The `code/` directory contains source code distributed with the publication. Typical subdivisions include `code/src/` for libraries, `code/scripts/` for entry points, `code/notebooks/` for notebooks, and `code/configs/` for configuration files. Paths used by scripts **MUST** resolve relative to the repository root and **MUST NOT** depend on absolute paths from the authors' machines. The directory **MUST** include scripts that reproduce all data figures in the paper, with each figure generated by a separate script. The contents of `code/` are considered ground truth for the work.

### `data/`

The `data/` directory contains datasets small enough to be stored comfortably in git, typically no more than a few tens of megabytes each. A `data/README.md` **MUST** describe each dataset, including what it is, how it was produced, and which figures or scripts use it. Large datasets **SHOULD** remain on external hosts such as Hugging Face, Zenodo, or Figshare; `data/README.md` **MUST** record the URL, exact download command, local destination, and whether the dataset is required for the default workflow. `AGENTS.md` **SHOULD** describe the data and how to access any external data. The contents of `data/` are considered ground truth for the work.

### `environment/`

The `environment/` directory contains the files required to recreate the runtime environment, such as `requirements.txt`, `pyproject.toml`, `environment.yml`, `package.json`, `Dockerfile`, or an equivalent specification. If multiple dependency specifications are present, such as both pip and conda files, `AGENTS.md` **MUST** identify the canonical environment specification.

### `supplementary/`

The optional `supplementary/` directory contains materials that provide additional context for understanding the work but are not part of the ground truth. Paper appendices that are necessary for understanding the paper **SHOULD** be included in `paper/` rather than `supplementary/`. Typical files include:

- `supplementary/know-how.md` — methodology decisions, tacit insights, practical knowledge from the research process.
- `supplementary/authors-note.md` — what the authors want readers to know beyond the paper.
- `supplementary/sessions/` — curated human-AI and/or human-human conversation transcripts from development, if the authors decide to share that.
- `supplementary/materials/` — slides, talks, posters, tutorials.

### `skills/`

The optional `skills/` directory contains agent capabilities shipped with the paper, following the [Agent Skills Protocol](https://agentskills.io/home). Each skill **MUST** be a directory `skills/<name>/` containing a `SKILL.md` file with `name` and `description` in YAML frontmatter and step-by-step instructions in the body. A typical skill exposes a paper-specific computation so that a reader or agent can invoke the paper's method directly.

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

#### Required sections

- **Identity** — who the agent is and how it should behave. References the paper title, authors, and domain. States that the paper manuscript, code, and data are the ground truth for all claims.
- **Paper Summary** — 2–4 paragraphs covering the problem, the approach, the results, and the implications. In the authors' own words.
- **Key Results** — numbered list of the main contributions, phrased as the authors want them cited.
- **Repository Structure** — every important file with its path and purpose, grouped by function. External datasets include URL, download command, and local destination.
- **What You Can Do** — concrete capabilities: *explain the paper* (what to read for what), *reproduce figures* (a table mapping each figure to its command, data, and runtime), *run experiments* (real commands, real parameters), *extend the work* (what to vary).
- **Computational Requirements** — time, hardware, and memory for each class of task; platform tested. The agent warns before running anything heavy.
- **Citation** — full BibTeX entry.

#### Optional sections

- **Supplementary Materials** — pointers to `supplementary/`. One line per item, noting what it is and that it is secondary to the paper.
- **Skills** — list of `skills/<name>/` entries, each with a one-line description.

### `README.md`

Each APP publication **MUST** include a `README.md` file at the root of the repository. The README is the human-facing entry point for readers and **SHOULD** summarize the paper, identify the authors, and link to the canonical public record when available, such as arXiv, DOI, or PDF.

The README **SHOULD** explain that the repository is an APP publication and that readers can clone the repository and open it in an AI coding agent that reads `AGENTS.md`. It **SHOULD** provide practical instructions for interacting with the paper through supported agents, reproducing figures or results, setting up the environment, and citing the work. The README **MAY** duplicate high-level commands from `AGENTS.md` for reader convenience, but `AGENTS.md` remains the canonical instruction file for agents.

### `LICENSE`

Each APP publication **MUST** include a `LICENSE` file at the root of the repository that clearly specifies the terms under which the contents of the publication may be used, modified, and redistributed. The license **SHOULD** cover all relevant components, including the manuscript, code, data, and any auxiliary materials, or explicitly state if different components are distributed under different licenses. If any part of the repository is subject to additional restrictions (e.g., third-party data, proprietary dependencies), these **MUST** be clearly indicated. The agent **SHOULD** be able to reference and communicate the licensing terms to users when relevant.

## Versioning

A publication is the pair `(repo URL, tag)`. Tags are immutable; the main branch is not. The recommended tag format is `vMAJOR.MINOR.PATCH` ([semver](https://semver.org)); other immutable tag names are allowed. Every tag corresponds to a GitHub Release. When the tag uses the recommended `vMAJOR.MINOR.PATCH` form, the `version` field in AGENTS.md matches the tag without the leading `v` (tag `v1.0.0` → `version: "1.0.0"`); otherwise, `version` matches the tag exactly. External references — citations, arXiv ancillary links, personal pages — should always point to a specific tag.


## License

This specification is released under CC-BY-4.0.
