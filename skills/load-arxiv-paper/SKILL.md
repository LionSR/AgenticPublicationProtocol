---
name: load-arxiv-paper
description: Load a paper directly from arXiv by ID or URL. Fetches the PDF, extracts metadata, and sets up a local paper directory. Optionally searches for associated code repos, author blog posts, and OpenReview rebuttals when the user explicitly asks.
---

# Load Paper from arXiv

Load an arXiv paper into your project by its ID or URL. Fetches the PDF and metadata directly from arXiv, sets up a local directory, and generates a starter AGENTS.md — useful for bootstrapping a publication or pulling in a paper for reference.

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

### 2. Fetch metadata and download PDF (in parallel)

Run both requests concurrently — they are independent:

```bash
mkdir -p papers/arxiv-ARXIV_ID
curl -s "https://export.arxiv.org/api/query?id_list=ARXIV_ID" -o /tmp/arxiv_response.xml &
curl -L "https://arxiv.org/pdf/ARXIV_ID" -o papers/arxiv-ARXIV_ID/paper.pdf &
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

**For the PDF**, verify the download succeeded (file exists and is >0 bytes). If it failed, retry once, then report the error.

### 3. Generate a starter AGENTS.md

Create `papers/arxiv-ARXIV_ID/AGENTS.md` from the fetched metadata:

```yaml
---
protocol: agentic-publication-protocol
protocol_version: "0.1.0"
title: "PAPER TITLE"
authors:
  - name: "Author Name"
    affiliation: "Institution"  # if available from API
arxiv_id: "ARXIV_ID"
paper_format: "pdf"
version: "1.0.0"
domain: "PRIMARY_CATEGORY"
tags: ["category1", "category2"]
---
```

Fill in the required sections using the metadata:
- **Identity**: Standard spokesperson framing, referencing the paper title and authors
- **Paper Summary**: Use the abstract as the initial summary (note that this is the arXiv abstract, not an author-written agent summary)
- **Key Results**: Leave as placeholder — the abstract doesn't usually enumerate individual contributions clearly enough
- **Repository Structure**: List `paper.pdf` as the ground truth document, plus any other files added
- **What You Can Do**: Explain the paper (from the PDF), note that code reproduction requires additional setup
- **Computational Requirements**: Unknown — note this
- **Citation**: Generate a BibTeX entry from the metadata

### 4. Report to the user

Present:
- Paper title and authors
- Abstract (first 3-4 sentences)
- arXiv categories
- Where files were saved
- That this is a PDF-only import — no code, no structured repo. If they want full APP capabilities, they'll need to either find or create a publication repo.

### 5. Find associated resources (ONLY when explicitly asked)

**Do NOT do this by default.** Only proceed if the user explicitly requests it — e.g. "also find code", "look for reviews", "find everything related to this paper", "find associated resources".

When the user asks, spawn three parallel subagents for 5a, 5b, and 5c:

#### 5a. Code repositories

Use a tiered approach — run the first tier in parallel, fall back only if needed:

**Tier 1 (run in parallel):**
1. **Papers with Code**: Fetch `https://paperswithcode.com/api/v1/papers/?arxiv_id=ARXIV_ID` — most reliable aggregated source
2. **Links in the PDF**: Read the paper PDF and look for GitHub/GitLab URLs — catches repos not yet indexed

**Tier 2 (only if Tier 1 finds nothing, run in parallel):**
3. **GitHub search**: Search GitHub for the arXiv ID (`site:github.com ARXIV_ID`)
4. **Semantic Scholar**: Fetch `https://api.semanticscholar.org/graph/v1/paper/ArXiv:ARXIV_ID?fields=externalIds`

If code is found:
- Report the repo URL(s) to the user
- Ask if they want to clone it into the paper directory (via `/load-paper-agent`)
- If the repo has an AGENTS.md, note that it's APP-compliant

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
