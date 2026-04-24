# Agentic Publication Protocol (APP)

**Version 0.1.0 — Draft**

APP is a format for packaging a finished academic paper as a GitHub repository so an AI coding agent can speak for it. An APP publication is a public Git repository with a tagged release and an `AGENTS.md` at the root. A reader clones the repo, opens it in any agent that reads `AGENTS.md`, and gets an agent that explains the paper, reproduces figures, runs experiments, and answers questions grounded in the work.

APP defines what a publication looks like. It does not define how authors produce it — that is the job of the skills distributed alongside this specification. For installation and usage, see [README.md](README.md).

## Principles

- **Spokesperson, not assistant.** The agent represents the authors. It speaks in the paper's domain — a math paper's agent reasons like a mathematician; an experimental paper's agent thinks like an experimentalist.
- **Paper is ground truth.** Every claim the agent makes traces back to the paper document. The authors designate the canonical form (LaTeX, PDF, Markdown, HTML, DOCX, video, slides). When supplementary material conflicts with the paper, the paper wins.
- **One place for each thing.** Every file, dataset, and script referenced by AGENTS.md resolves to exactly one path in the repo. No duplicates, no shadow copies.
- **A publication is a release, not a branch.** Citations and external links resolve to a specific git tag, never to HEAD. The main branch may keep evolving; each release is frozen.

## Repository layout

```
<repo-root>/
├── AGENTS.md          primary agent instructions
├── CLAUDE.md          optional; one line: @AGENTS.md
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

At the root, publication artifacts live only in the entries above. No paper, code, data, or dependency files loose at root. Standard repository metadata (`.gitignore`, `.gitattributes`, `.github/`) is allowed. Not every directory is required: a theory-only paper may carry only `paper/` and `AGENTS.md`.

A publication with code, data, and paper-specific skills gives the agent more to work with than a `paper/`-only repo. When feasible, include the scripts that generate the figures, the data those scripts use, and any method-specific skill worth sharing.

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
