---
name: load-arxiv-paper
description: Load a paper directly from arXiv by ID or URL. Fetches metadata, prefers arXiv LaTeX/source when available, and falls back to PDF only when source is unavailable. Optionally searches for associated code repos, author blog posts, and OpenReview rebuttals when the user explicitly asks.
---

# Load Paper from arXiv

Load an arXiv paper into your project by its ID or URL. Fetch metadata directly from arXiv, load the arXiv source package when available, fall back to PDF only when source is unavailable or unusable, and generate a starter AGENTS.md. This is useful for bootstrapping a publication or pulling in a paper for reference.

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

### 3. Generate a starter AGENTS.md

Create `papers/arxiv-ARXIV_ID/AGENTS.md` following the structure defined in [PROTOCOL.md](../../PROTOCOL.md#agentsmd), populated with the fetched metadata. Use the YAML frontmatter fields from the protocol (`protocol`, `protocol_version`, `title`, `authors`, `arxiv_id`, `paper_format`, `version`, `domain`, `tags`).

This creates an APP-structured local import, not a verified APP publication. It has no public tagged release, no validation manifest, and no `app_publication_id`.

Set `paper_format` according to the imported artifact:

- `latex` when the arXiv source package produced TeX files.
- `pdf` only when source import failed and the workflow fell back to PDF.

Since this is an import (not an author publication), fill in what the metadata provides and mark the rest as placeholders:
- **Paper Summary**: Use the arXiv abstract (note it's not an author-written agent summary)
- **Key Results**: Leave as placeholder — the abstract doesn't enumerate contributions clearly enough
- **Repository Structure**: List `paper/` and the likely main TeX file as the ground truth document when source was loaded. List `paper/paper.pdf` only for PDF fallback imports.
- **Citation**: Generate a BibTeX entry from the metadata
- Other required sections: populate with sensible defaults per the protocol

### 4. Report to the user

Present:
- Paper title and authors
- Abstract (first 3-4 sentences)
- arXiv categories
- Where files were saved
- Whether LaTeX source was loaded or the workflow had to fall back to PDF
- That this is an arXiv import — no code or structured publication repo is included unless associated resources are found separately. If they want full APP capabilities, they'll need to find or create a publication repo.

### 5. Find associated resources (ONLY when explicitly asked)

**Do NOT do this by default.** Only proceed if the user explicitly requests it — e.g. "also find code", "look for reviews", "find everything related to this paper", "find associated resources".

When the user asks, spawn three parallel subagents for 5a, 5b, and 5c:

#### 5a. Code repositories

Use a tiered approach — run the first tier in parallel, fall back only if needed:

**Tier 1 (run in parallel):**
1. **Papers with Code**: Fetch `https://paperswithcode.com/api/v1/papers/?arxiv_id=ARXIV_ID` — most reliable aggregated source
2. **Links in the imported paper**: Search the downloaded LaTeX source under `papers/arxiv-ARXIV_ID/paper/` for GitHub/GitLab URLs. If this import fell back to PDF, read `papers/arxiv-ARXIV_ID/paper/paper.pdf` instead — catches repos not yet indexed

**Tier 2 (only if Tier 1 finds nothing, run in parallel):**
3. **GitHub search**: Search GitHub for the arXiv ID (`site:github.com ARXIV_ID`)
4. **Semantic Scholar**: Fetch `https://api.semanticscholar.org/graph/v1/paper/ArXiv:ARXIV_ID?fields=externalIds`

If code is found:
- Report the repo URL(s) to the user
- Ask if they want to clone it into the paper directory (via `/load-paper-agent`)
- If the repo has an AGENTS.md, note only that it is agent-readable. Use `/load-paper-agent` to classify whether it is an APP-structured candidate or a verified APP publication.

If no code is found, report that clearly.

#### 5b. Author blog posts

Search the web for blog posts by the authors about this paper:
- Search for `"PAPER_TITLE" blog` or `"FIRST_AUTHOR" "PAPER_TITLE" blog`
- Check common platforms: author's personal site, Medium, Towards Data Science, distill.pub, the institution's blog
- Look for Twitter/X threads by the authors discussing the paper

Report any blog posts or threads found with URLs. Don't editorialize — just provide the links and a one-line description of each.

#### 5c. OpenReview rebuttals and reviews

Search for the paper on OpenReview:
- Search `https://openreview.net/search?term=PAPER_TITLE` (or use web search: `site:openreview.net "PAPER_TITLE"`)
- If found, report:
  - The OpenReview forum URL
  - The venue (e.g. ICLR 2024, NeurIPS 2023)
  - Number of reviews available
  - Whether author responses/rebuttals are present
- If the paper has reviews, offer to fetch and summarize them

If not found on OpenReview, report that — not all papers go through OpenReview.

#### 5d. Present findings

After all subagent searches complete, present a consolidated summary:

```
## Associated Resources for "PAPER TITLE"

**Code**: [found/not found] — URL if found
**Blog posts**: [found/not found] — URLs if found
**OpenReview**: [found/not found] — URL and venue if found

Would you like me to:
- Clone the code repo into the paper directory?
- Fetch and summarize the OpenReview reviews?
- Load this as a full paper agent (if code repo exists)?
```

Let the user decide what to do next. Don't automatically clone or fetch anything — present options and wait.

## Integration with other skills

- If a code repo is found and the user wants to load it, hand off to `/load-paper-agent` with the repo URL
- If the user wants to publish their own version of the paper, hand off to `/publish-paper`
- The generated AGENTS.md is a starter — if the user is the author, they should flesh it out with `/publish-paper`
