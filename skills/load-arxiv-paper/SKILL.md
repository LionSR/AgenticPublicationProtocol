---
name: load-arxiv-paper
description: Load a paper directly from arXiv by ID or URL. Fetches metadata, prefers arXiv source when available, falls back to PDF only when needed, and downloads associated public GitHub code when found. Author blog posts and OpenReview material remain optional extra searches.
---

# Load Paper from arXiv

Load an arXiv paper into your project by its ID or URL. Fetch metadata directly from arXiv, load the arXiv source package when available, fall back to PDF only when source is unavailable or unusable, download associated public GitHub code when found, and generate a protocol-shaped local import. This is useful for bootstrapping a publication or pulling in a paper for reference.

## Triggering

User says something like:
- "Load arXiv paper 2301.07041"
- "Load this paper from arXiv: https://arxiv.org/abs/2301.07041"
- "Fetch the arXiv paper at 2301.07041v2"
- "Load arxiv 2301.07041 and find associated code and reviews"

## Steps

### 1. Parse the arXiv identifier

Accept any of these formats and extract the arXiv ID:
- Bare ID: `2301.07041` or `2301.07041v2`
- Abstract URL: `https://arxiv.org/abs/2301.07041`
- PDF URL: `https://arxiv.org/pdf/2301.07041`

Normalize to the bare ID (e.g. `2301.07041`). If a version suffix is given (e.g. `v2`), preserve it.

### 2. Fetch metadata and source first

Run metadata and source requests concurrently. Do not download the PDF in the default path:

```bash
mkdir -p papers/arxiv-ARXIV_ID/paper
curl -s "https://export.arxiv.org/api/query?id_list=ARXIV_ID" -o /tmp/arxiv_response.xml &
curl -L "https://arxiv.org/e-print/ARXIV_ID" -o /tmp/arxiv-ARXIV_ID-source &
wait
```

**From the metadata** (Atom XML), extract:
- **Title**
- **Authors** (names and affiliations if available)
- **Abstract**
- **Categories** (e.g. cs.CL, stat.ML)
- **Published date** and **updated date**
- **Links** — PDF link, DOI link if present, any related links

If the API returns no results or an error, inform the user and ask them to verify the ID.

Inspect `/tmp/arxiv-ARXIV_ID-source`:

- Extract tar archives into `papers/arxiv-ARXIV_ID/paper/`.
- Decompress a gzip-compressed single TeX file to `papers/arxiv-ARXIV_ID/paper/main.tex`.
- Copy an already-plain TeX file to `papers/arxiv-ARXIV_ID/paper/main.tex`.
- Verify that `papers/arxiv-ARXIV_ID/paper/` contains at least one `*.tex` file. If several candidates exist, identify the likely main file by looking for `\documentclass`; if ambiguous, note that in `AGENTS.md`.

If source is unavailable or unusable, then download the PDF:

```bash
curl -L "https://arxiv.org/pdf/ARXIV_ID" -o papers/arxiv-ARXIV_ID/paper/paper.pdf
```

Verify `paper/paper.pdf` exists and is >0 bytes, retry once if needed, and report that this import used the PDF fallback. Do not create `paper.pdf` when usable source was loaded.

### 3. Find and download associated code

Code discovery is part of the default arXiv-loading workflow. Do not wait for a separate user request before checking for code.

Create:

```bash
mkdir -p papers/arxiv-ARXIV_ID/code/external
mkdir -p papers/arxiv-ARXIV_ID/supplementary
```

Run the first two checks in parallel:

1. Search the imported paper source for GitHub URLs. If this import fell back to PDF, search the PDF text instead.
2. Fetch `https://paperswithcode.com/api/v1/papers/?arxiv_id=ARXIV_ID`.

If neither gives a credible repository, search GitHub for the arXiv ID and exact title. You may also fetch `https://api.semanticscholar.org/graph/v1/paper/ArXiv:ARXIV_ID?fields=externalIds`.

For each candidate repository:

- Prefer repositories explicitly named in the paper source, PDF, or arXiv metadata.
- Resolve GitHub redirects and renamed repositories.
- Check whether the repository is public and reachable.
- Record the evidence linking it to the paper.
- Record the canonical URL, clone URL, default branch, commit SHA, pushed date, approximate size, language summary, license field, and whether `AGENTS.md` exists.

Download credible public GitHub repositories only. If GitHub reports a repository as larger than 100 MB, record it but do not download it. If a credible non-GitHub repository is found, record it but do not download it in this default workflow.

```bash
curl -L "https://api.github.com/repos/OWNER/REPO/tarball/COMMIT_SHA" \
  -o "papers/arxiv-ARXIV_ID/code/external/OWNER-REPO-COMMIT.tar.gz"
```

Verify the archive and, when it is small enough, extract it:

```bash
tar -tzf "papers/arxiv-ARXIV_ID/code/external/OWNER-REPO-COMMIT.tar.gz" | head
tar -xzf "papers/arxiv-ARXIV_ID/code/external/OWNER-REPO-COMMIT.tar.gz" \
  -C "papers/arxiv-ARXIV_ID/code/external"
```

If download or extraction fails, retry once. If it still fails, keep the failure in the provenance record and continue with the import.

Write a code provenance file:

```text
papers/arxiv-ARXIV_ID/supplementary/code-provenance.md
```

The provenance file must list:

- repositories found and evidence linking each to the paper;
- canonical URL, commit SHA, archive path, and extracted path when downloaded;
- repositories skipped because they are non-GitHub, too large, private, or unreachable;
- download or extraction failures;
- whether each downloaded repository appears agent-readable, APP-structured, or neither.

Do not classify a downloaded code repository as a verified APP publication unless a matching public tagged release manifest is actually verified. A normal GitHub repository with paper code is only associated code.

### 4. Generate a protocol-shaped local import

Create a local tree that follows the APP repository layout as far as a third-party arXiv import can. It is not a verified APP publication, but it should be easy for a reader agent to use.

Create the remaining protocol directories:

```bash
mkdir -p papers/arxiv-ARXIV_ID/data
mkdir -p papers/arxiv-ARXIV_ID/environment
```

Required files:

- `AGENTS.md` — APP-shaped reader-agent instructions.
- `CLAUDE.md` — one line: `@AGENTS.md`.
- `README.md` — human-facing summary of the local import.
- `LICENSE` — explain the wrapper license and the status of imported third-party materials.
- `.gitignore` — ignore local caches, build outputs, credentials, and extracted dependency folders.
- `paper/` — arXiv source files, or `paper/paper.pdf` when the workflow fell back to PDF.
- `code/external/` — downloaded associated public GitHub repositories, if any.
- `supplementary/import-provenance.md` — metadata, fetch outcomes, source/PDF fallback status, and limitations.
- `supplementary/code-provenance.md` — associated-code search and download record.
- `data/README.md` and `environment/README.md` — present even when no data or environment was imported, with that limitation stated explicitly.

Use root-relative paths throughout. Do not reference temporary files or parent-repo paths from `AGENTS.md`, README, or provenance files.

Populate `AGENTS.md` following [PROTOCOL.md](../../PROTOCOL.md#agentsmd). Use the YAML frontmatter fields from the protocol (`protocol`, `protocol_version`, `title`, `authors`, `arxiv_id`, `paper_format`, `version`, `domain`, `tags`).

This creates an APP-structured local import, not a verified APP publication. It has no public tagged release, no validation manifest, and no `app_publication_id`. State that explicitly in `AGENTS.md` and README.

Set `paper_format` according to the imported artifact:

- `latex` when the arXiv source package produced TeX files.
- `pdf` only when source import failed and the workflow fell back to PDF.

Since this is an import (not an author publication), fill in what the metadata provides and mark the rest as placeholders:
- **Paper Summary**: Use the arXiv abstract (note it's not an author-written agent summary)
- **Key Results**: Leave as placeholder — the abstract doesn't enumerate contributions clearly enough
- **Repository Structure**: List `paper/` and the likely main TeX file as the ground truth document when source was loaded. List `paper/paper.pdf` only for PDF fallback imports. List downloaded associated repositories under `code/external/`.
- **What You Can Do**: distinguish reading the paper from inspecting or running downloaded code. Include setup/build commands from downloaded repository READMEs only when they are present and path-correct from the import root.
- **Computational Requirements**: state what can be read locally, what can be inspected, and what has not been run. Warn before heavy downloads, builds, or external dataset access.
- **Citation**: Generate a BibTeX entry from the metadata
- Other required sections: populate with conservative defaults per the protocol

### 5. Report to the user

Present:
- Paper title and authors
- Abstract (first 3-4 sentences)
- arXiv categories
- Where files were saved
- Whether LaTeX source was loaded or the workflow had to fall back to PDF
- Associated public code repositories found, downloaded, and extracted, including local paths and commit SHAs.
- Any code repositories searched for but not found, not reachable, too large, or not downloaded.
- That this is a local arXiv import, not an author-approved or verified APP publication. Downloaded code improves the local import, but it does not by itself create APP verification.

### 6. Find non-code associated resources (ONLY when explicitly asked)

Code search and code download are already part of the default load path. Do not repeat them here unless the user asks for a deeper code search.

Search for author blog posts, OpenReview rebuttals, reviews, social-media threads, slides, and talks only when the user explicitly asks — e.g. "look for reviews", "find everything related to this paper", "find associated resources", or "find author commentary".

When the user asks for non-code resources, spawn parallel subagents for the relevant searches.

#### 6a. Author blog posts

Search the web for blog posts by the authors about this paper:
- Search for `"PAPER_TITLE" blog` or `"FIRST_AUTHOR" "PAPER_TITLE" blog`
- Check common platforms: author's personal site, Medium, Towards Data Science, distill.pub, the institution's blog
- Look for Twitter/X threads by the authors discussing the paper

Report any blog posts or threads found with URLs. Don't editorialize — just provide the links and a one-line description of each.

#### 6b. OpenReview rebuttals and reviews

Search for the paper on OpenReview:
- Search `https://openreview.net/search?term=PAPER_TITLE` (or use web search: `site:openreview.net "PAPER_TITLE"`)
- If found, report:
  - The OpenReview forum URL
  - The venue (e.g. ICLR 2024, NeurIPS 2023)
  - Number of reviews available
  - Whether author responses/rebuttals are present
- If the paper has reviews, offer to fetch and summarize them

If not found on OpenReview, report that — not all papers go through OpenReview.

#### 6c. Present findings

After all subagent searches complete, present a consolidated summary:

```
## Associated Resources for "PAPER TITLE"

**Blog posts**: [found/not found] — URLs if found
**OpenReview**: [found/not found] — URL and venue if found

Would you like me to:
- Fetch and summarize the OpenReview reviews?
- Inspect downloaded code more deeply?
```

Let the user decide what to do next for these non-code resources.

## Integration with other skills

- If a downloaded code repo has `AGENTS.md`, hand off to `/load-paper-agent` to classify that repository as agent-readable, APP-structured, or verified APP.
- If the user wants to publish their own version of the paper, hand off to `/publish-paper`
- The generated AGENTS.md is a starter — if the user is the author, they should flesh it out with `/publish-paper`
