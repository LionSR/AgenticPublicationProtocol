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
├── paper/             paper source (ground truth), figures, compiled PDF
├── code/              source and scripts
├── data/              shipped datasets; external datasets are documented in AGENTS.md
├── environment/       requirements.txt, environment.yml, Dockerfile, or equivalent
├── supplementary/     optional: know-how, authors' note, slides, sessions, checklist
└── skills/            optional: author-published SKILL.md capabilities
```

At the root, publication artifacts live only in the entries above. No paper, code, data, or dependency files loose at root. Standard repository metadata (`.gitignore`, `.gitattributes`, `.github/`) is allowed. Not every top-level directory is required: a minimal theory-only publication contains `paper/`, `supplementary/checklist.md`, plus the always-required root files `AGENTS.md`, `README.md`, and `LICENSE` (with `CLAUDE.md` recommended).

The agent's value scales with what the repo contains: code makes figures reproducible, data makes experiments runnable, and paper-specific skills let a reader invoke the paper's methods directly. A `paper/`-only publication is valid but gives the agent nothing to do beyond discussing the text.

For a concrete starter, see [`template/`](template/) — example `AGENTS.md`, `CLAUDE.md`, and publication-checklist files that conform to this layout.

### `paper/`

The paper itself plus everything needed to read it: the main document, any compiled output, figure files, bibliography. Exactly one document is the canonical paper; its format is declared in the AGENTS.md frontmatter (`paper_format`) and its path is listed in the Repository Structure section of AGENTS.md. Everything in `paper/` is ground truth.

### `code/`

Source code that ships with the publication. Typical subdivisions are `code/src/` for libraries, `code/scripts/` for entry points, `code/notebooks/` for notebooks, `code/configs/` for configuration files. Paths inside scripts resolve relative to the repo root — no absolute paths from the authors' machines.

### `data/`

Datasets small enough to live comfortably in git (under a few tens of megabytes each). A `data/README.md` describes each dataset — what it is, how it was produced, which figures or scripts use it. Large datasets stay on external hosts (Hugging Face, Zenodo, Figshare, …); AGENTS.md records the URL, exact download command, local destination, and whether the dataset is needed for the default workflow.

### `environment/`

Whatever recreates the runtime: `requirements.txt`, `pyproject.toml`, `environment.yml`, `package.json`, `Dockerfile`, or equivalent. If multiple dependency files are present (e.g. pip and conda), AGENTS.md names the canonical one.

### `supplementary/`

Secondary material. Everything here is subordinate to `paper/` — it adds context, never overrides. Typical files:

- `supplementary/know-how.md` — methodology decisions, tacit insights, practical knowledge from the research process.
- `supplementary/authors-note.md` — what the authors want readers to know beyond the paper.
- `supplementary/sessions/` — curated conversation transcripts from development.
- `supplementary/materials/` — slides, talks, posters, tutorials.
- `supplementary/checklist.md` — the publication checklist (see below).

### `skills/`

Optional agent capabilities shipped with the paper. Each skill is a directory `skills/<name>/` containing a `SKILL.md` file with `name` and `description` in YAML frontmatter and step-by-step instructions in the body. A typical use is to expose a paper-specific computation — a reader can invoke the skill and the agent walks through it using the paper's method.

Skills are tools, not claims. Running a skill does not override the paper's findings.

### `AGENTS.md`

The file an agent reads first when the repo is opened. Standard Markdown, compatible with [agents.md](https://agents.md). Two parts: YAML frontmatter and the body.

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

- **Identity** — who the agent is and how it should behave. References the paper title, authors, and domain. States that the paper is the ground truth for all claims.
- **Paper Summary** — 2–4 paragraphs covering the problem, the approach, the results, and the implications. In the authors' own words.
- **Key Results** — numbered list of the main contributions, phrased as the authors want them cited.
- **Repository Structure** — every important file with its path and purpose, grouped by function. External datasets include URL, download command, and local destination.
- **What You Can Do** — concrete capabilities: *explain the paper* (what to read for what), *reproduce figures* (a table mapping each figure to its command, data, and runtime), *run experiments* (real commands, real parameters), *extend the work* (what to vary).
- **Computational Requirements** — time, hardware, and memory for each class of task; platform tested. The agent warns before running anything heavy.
- **Citation** — full BibTeX entry.

#### Optional sections

- **Supplementary Materials** — pointers to `supplementary/`. One line per item, noting what it is and that it is secondary to the paper.
- **Skills** — list of `skills/<name>/` entries, each with a one-line description.

## Versioning

A publication is the pair `(repo URL, tag)`. Tags are immutable; the main branch is not. The recommended tag format is `vMAJOR.MINOR.PATCH` ([semver](https://semver.org)); other immutable tag names are allowed. Every tag corresponds to a GitHub Release. When the tag uses the recommended `vMAJOR.MINOR.PATCH` form, the `version` field in AGENTS.md matches the tag without the leading `v` (tag `v1.0.0` → `version: "1.0.0"`); otherwise, `version` matches the tag exactly. External references — citations, arXiv ancillary links, personal pages — always point to a specific tag.

When publishing a new version, start from the previous version's AGENTS.md, supplementary materials, and skills, then update only what changed.

## Publication checklist

Every publication includes a completed checklist at `supplementary/checklist.md`. `supplementary/` itself stays optional: a publication that ships no other supplementary material still includes `supplementary/checklist.md` as its only entry.

The checklist records that the authors explicitly confirmed at least the following. Items that do not apply can be marked N/A.

- The paper in `paper/` is the canonical, up-to-date source.
- Every path referenced in AGENTS.md resolves in the repo.
- Every external data link is reachable.
- No private credentials, internal URLs, or unpublished data are in the repo.
- The license in `LICENSE` is what the authors intend.
- The git tag and the AGENTS.md `version` field match.

The reference template at [`template/publication-checklist.md`](template/publication-checklist.md) expands these into per-topic subchecks.

## Using a published paper

Clone the repo at a given tag and open it in any agent that reads `AGENTS.md`. No special runtime or server is needed. For parallel use, multiple publications can sit side-by-side as subdirectories of a working project; each nested `AGENTS.md` is picked up by the parent agent.

## License

This specification is released under CC-BY-4.0.
