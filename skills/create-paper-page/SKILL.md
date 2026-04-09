---
name: create-paper-page
description: Create a GitHub Pages project page for a paper — a public landing page with title, authors, abstract, highlights, figures, links to code/data, and optionally an embedded agent chat. Use when a researcher wants a web presence for their paper beyond just a GitHub repo.
---

# Create Paper Page

Generate a GitHub Pages site for a published paper. This is the "project homepage" that many ML and CS papers have — but automated and structured.

## When to use

- After `/publish-paper` to add a web presence
- Standalone when a researcher wants a project page for an existing paper
- When preparing for a conference submission or public release

## What the page includes

A single-page site with:

1. **Title and authors** — with affiliations and links
2. **Abstract** — from the paper
3. **Highlights / Key results** — 3-5 bullet points with figures
4. **Figures** — key figures from the paper, displayed large
5. **Links** — paper PDF, arXiv, code repo, data
6. **BibTeX** — copy-to-clipboard citation block
7. **Agent badge** — indicates this paper has an AI agent (links to AGENTS.md)

## Process

### 1. Gather content

Read the paper source and AGENTS.md (if it exists) to extract:
- Title, authors, affiliations
- Abstract
- Key results / highlights (from AGENTS.md "Key Results" or paper's introduction)
- 3-5 best figures (ask the researcher which ones to feature)
- arXiv ID, DOI, or other paper links
- BibTeX citation

Ask the researcher:
- Which figures should be on the landing page?
- Any specific highlights they want to emphasize?
- Do they have author photos or logos to include?
- Preferred color scheme? (or use a clean default)

### 2. Generate the site

Create a `docs/` directory (GitHub Pages default) with a static site:

```
docs/
├── index.html        ← the landing page
├── style.css         ← styling
└── assets/
    ├── figures/      ← featured figures (copied from paper/figures/)
    └── ...           ← any other assets (logos, photos)
```

**The HTML should be:**
- Self-contained — no build step, no JavaScript framework, no npm
- Clean and readable — academic style, not startup landing page
- Mobile-friendly — responsive layout
- Fast — just HTML + CSS + images, no heavy dependencies

**Structure of index.html:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Paper Title]</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>[Paper Title]</h1>
        <p class="authors">
            <a href="[url]">Author One</a><sup>1</sup>,
            <a href="[url]">Author Two</a><sup>2</sup>
        </p>
        <p class="affiliations">
            <sup>1</sup>Institution A,
            <sup>2</sup>Institution B
        </p>
        <nav class="links">
            <a href="[arxiv-url]">Paper</a>
            <a href="[repo-url]">Code</a>
            <a href="[data-url]">Data</a>
            <a href="AGENTS.md">🤖 Paper Agent</a>
        </nav>
    </header>

    <section id="abstract">
        <h2>Abstract</h2>
        <p>[abstract text]</p>
    </section>

    <section id="highlights">
        <h2>Highlights</h2>
        <ul>
            <li>[Key result 1]</li>
            <li>[Key result 2]</li>
            <li>[Key result 3]</li>
        </ul>
    </section>

    <section id="figures">
        <h2>Key Results</h2>
        <figure>
            <img src="assets/figures/fig1.png" alt="[description]">
            <figcaption>Figure 1: [caption]</figcaption>
        </figure>
        <!-- more figures -->
    </section>

    <section id="citation">
        <h2>Citation</h2>
        <pre id="bibtex">[bibtex block]</pre>
        <button onclick="navigator.clipboard.writeText(
            document.getElementById('bibtex').textContent
        )">Copy BibTeX</button>
    </section>

    <footer>
        <p>This paper is published with an
        <a href="https://github.com/LionSR/AgenticPublicationProtocol">
        AI agent</a> — clone the repo and talk to it.</p>
    </footer>
</body>
</html>
```

**Styling (style.css):**
- Clean serif font for body, sans-serif for headings
- Max-width ~800px, centered
- Figures displayed at full width with captions
- Muted colors, academic feel — not flashy
- Print-friendly

### 3. Copy figures

Copy the featured figures from `paper/figures/` (or wherever they live) into `docs/assets/figures/`. Use web-friendly formats:
- Convert PDF figures to PNG or SVG if needed
- Optimize image sizes (no 10MB PNGs)
- Keep original filenames for traceability

### 4. Enable GitHub Pages

Check if the repo has GitHub Pages enabled:

```bash
gh api repos/{owner}/{repo}/pages 2>/dev/null
```

If not enabled, enable it:

```bash
gh api repos/{owner}/{repo}/pages -X POST -f source.branch=main -f source.path=/docs
```

Or tell the researcher to go to Settings → Pages → Source: Deploy from branch → `main` → `/docs`.

The page will be available at `https://{username}.github.io/{repo-name}/`.

### 5. Verify

- Open the page URL and check everything renders
- Test on mobile (responsive?)
- Check all links work (paper PDF, arXiv, code repo)
- Verify figures display correctly
- Test the BibTeX copy button

### 6. Update README and AGENTS.md

Add the page URL to:
- README.md: `[Project Page](https://{username}.github.io/{repo-name}/)`
- AGENTS.md frontmatter: add `page_url: "https://..."`
- AGENTS.md body: mention the project page exists

### Customization

The researcher may want:
- **Different figures** — swap them in `docs/assets/figures/`
- **Video or demo** — embed a YouTube/video link in the highlights section
- **More sections** — method overview, comparison tables, acknowledgments
- **Custom domain** — they can configure this in GitHub Pages settings
- **Different style** — they can edit `style.css` directly

Keep the base simple. The researcher can customize after generation.
