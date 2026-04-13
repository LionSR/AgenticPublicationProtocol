---
name: find-paper-resources
description: Search for resources associated with a paper — code repositories, author blog posts, and OpenReview reviews/rebuttals. Works with any loaded paper (arXiv or GitHub). Only runs when the user explicitly asks.
---

# Find Paper Resources

Search for resources associated with a paper that aren't in the paper's own repo — code on GitHub, author blog posts, and OpenReview reviews/rebuttals.

Works on any paper in `papers/`, whether loaded from arXiv or GitHub. This skill is designed to be invoked after loading a paper with `/load-paper-agent`, or standalone when the user already has a paper and wants to find what's around it.

## Triggering

User says something like:
- "Find code for this paper"
- "Look for reviews of 2301.07041"
- "Find associated resources for the paper"
- "Is there a blog post about this paper?"
- "Find code, blogs, and reviews for this paper"

## Steps

### 1. Identify the paper

Determine which paper the user is asking about. Use one of:
- An arXiv ID (e.g. `2301.07041`)
- A paper title (from AGENTS.md or provided by the user)
- A path to a loaded paper in `papers/`

If the paper is already loaded, read its AGENTS.md (or PDF) to get the title, authors, and arXiv ID. If the user provides just an arXiv ID or title without a loaded paper, work with that directly.

### 2. Search for resources

Spawn three parallel subagents — one for each resource type:

#### 2a. Code repositories

Use a tiered approach — run the first tier in parallel, fall back only if needed:

**Tier 1 (run in parallel):**
1. **Papers with Code**: Fetch `https://paperswithcode.com/api/v1/papers/?arxiv_id=ARXIV_ID` — most reliable aggregated source (requires arXiv ID)
2. **Links in the PDF**: If the paper PDF is available locally, scan it for GitHub/GitLab URLs — catches repos not yet indexed

**Tier 2 (only if Tier 1 finds nothing, run in parallel):**
3. **GitHub search**: Search for the arXiv ID or paper title (`site:github.com ARXIV_ID` or `site:github.com "PAPER_TITLE"`)
4. **Semantic Scholar**: Fetch `https://api.semanticscholar.org/graph/v1/paper/ArXiv:ARXIV_ID?fields=externalIds` (requires arXiv ID)

If code is found:
- Report the repo URL(s) to the user
- Ask if they want to clone it via `/load-paper-agent`
- If the repo has an AGENTS.md, note that it's APP-compliant

If no code is found, report that clearly.

#### 2b. Author blog posts

Search the web for blog posts by the authors about this paper:
- Search for `"PAPER_TITLE" blog` or `"FIRST_AUTHOR" "PAPER_TITLE" blog`
- Check common platforms: author's personal site, Medium, Towards Data Science, distill.pub, the institution's blog
- Look for Twitter/X threads by the authors discussing the paper

Report any blog posts or threads found with URLs. Don't editorialize — just provide the links and a one-line description of each.

#### 2c. OpenReview rebuttals and reviews

Search for the paper on OpenReview:
- Search `https://openreview.net/search?term=PAPER_TITLE` (or use web search: `site:openreview.net "PAPER_TITLE"`)
- If found, report:
  - The OpenReview forum URL
  - The venue (e.g. ICLR 2024, NeurIPS 2023)
  - Number of reviews available
  - Whether author responses/rebuttals are present
- If the paper has reviews, offer to fetch and summarize them

If not found on OpenReview, report that — not all papers go through OpenReview.

### 3. Present findings

After all subagent searches complete, present a consolidated summary:

```
## Associated Resources for "PAPER TITLE"

**Code**: [found/not found] — URL if found
**Blog posts**: [found/not found] — URLs if found
**OpenReview**: [found/not found] — URL and venue if found

Would you like me to:
- Clone the code repo into the paper directory?
- Fetch and summarize the OpenReview reviews?
```

Let the user decide what to do next. Don't automatically clone or fetch anything — present options and wait.

## Integration with other skills

- If a code repo is found and the user wants to load it, hand off to `/load-paper-agent` with the repo URL
- If the user wants to publish their own version of the paper, hand off to `/publish-paper`
