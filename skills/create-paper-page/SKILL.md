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
5. **Links** — paper PDF/arXiv, the publication repo (the primary link), data
6. **BibTeX** — copy-to-clipboard citation block
7. **Agent badge** — indicates this paper has an AI agent. It links to the
   publication repo on GitHub, and the page states the usable action: clone
   the repo and open it in an AI coding agent. Never link the raw `AGENTS.md`
   file — see the linking rules below.

## Page vs README — what goes where

The page and the README serve different readers, so they must not be the same
document. The page is for someone who has **not** cloned anything and is
deciding in ~30 seconds whether the paper is interesting; the README is for
someone who **has** cloned the repo and wants to work with it. Rule of thumb:
the page sells and routes, the README operates.

On the page:
- Title, authors, abstract, 3-5 highlights, key figures
- Links out: arXiv/PDF, publication repo, agent badge
- BibTeX
- One sentence on what the agent is and how to use it (clone + open)

Not on the page (README/repo territory):
- Repository layout and per-file descriptions
- Reproduction commands, environment setup, toolchain versions
- Reproduction status detail, validation reports, provenance
- License text, agent behavioral instructions

If a detail matters to someone who has not cloned the repo (e.g. "results
reproduce from committed data on a laptop"), state it as a one-line highlight
and link to the repo for the rest. If the generated page reads like the
README with styling, cut it down.

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

Create the site under `supplementary/page/` in the publication tree:

```
supplementary/page/
├── index.html        ← the landing page
├── style.css         ← styling
└── assets/
    ├── figures/      ← web-optimized derivatives of featured figures
    └── ...           ← any other assets (logos, photos)
```

**Protocol consistency:** `supplementary/` is part of the APP layout
(PROTOCOL.md), so the page ships inside the publication tree and is
versioned with the tagged release; it is supplementary material, not ground
truth. Two rules still hold: never add non-protocol fields such as
`page_url` to the `AGENTS.md` frontmatter — the page URL goes in
`README.md` (step 6) — and do not commit exact duplicates of canonical
files. Page figures are web-optimized derivatives (PNG/SVG conversions),
and the paper PDF is linked (arXiv, or the rendered `blob/{tag}` URL, which
GitHub shows in a PDF viewer) rather than copied into the site.

**The HTML should be:**
- Self-contained — no build step, no JavaScript framework, no npm
- Clean and readable — academic style, not startup landing page
- Mobile-friendly — responsive layout
- Fast — just HTML + CSS + images, no heavy dependencies

**Linking rules — the live site serves only `supplementary/page/`:**

The published site lives at `https://{username}.github.io/{repo-name}/` and
serves only the deployed artifact, i.e. the contents of
`supplementary/page/`. Relative links that escape it
(`../../paper/...`, `../../AGENTS.md`) 404 on the live site.
Pages also does not render markdown — a link to a `.md` file shows raw text
or downloads the file, which is not usable (a downloaded `AGENTS.md` on its
own does nothing; the agent works by opening the cloned repo).

- The primary link target is the **publication repo on GitHub**
  (`https://github.com/{owner}/{repo}`) — readers get the rendered README,
  the code, and the clone URL in one place.
- Figures — web-optimized derivatives in the site's `assets/` linked
  relatively. The paper PDF — link arXiv or the rendered `blob/{tag}` URL
  (GitHub shows PDFs in a viewer); do not duplicate it into the site.
- A specific repo file worth pointing at (e.g. a computations README) — use
  the rendered GitHub URL, pinned to the release tag:
  `https://github.com/{owner}/{repo}/blob/{tag}/...`. PROTOCOL.md says
  external references should point to a specific tag, and tag URLs are
  immutable; do not hardcode a branch name (not every repo's default branch
  is `main`).
- Agent badge → the publication repo URL, never a `.md` file.
- Local preview: serve the staging/repo root and open
  `/supplementary/page/` — in-site assets resolve as on the live site. In a
  dev-sandbox preview (no public repo yet), relative links escaping the
  page directory are acceptable for browsing, but every such link must be
  rewritten per these rules before a real release.

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
            <a href="[arxiv-url]">Paper</a>          <!-- arXiv, or the rendered blob/{tag} PDF URL -->
            <a href="[repo-url]">Code</a>            <!-- the publication repo on GitHub -->
            <a href="[data-url]">Data</a>            <!-- only if data lives elsewhere -->
            <a href="[repo-url]">🤖 Paper Agent</a>  <!-- repo URL, never AGENTS.md -->
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
        <p>This paper has an AI agent: clone
        <a href="[repo-url]">the publication repo</a> and open it in an
        AI coding agent (Claude Code, Codex, ...) — the agent reads
        <code>AGENTS.md</code> and answers questions about the paper.
        Published with the
        <a href="https://github.com/LionSR/AgenticPublicationProtocol">
        Agentic Publication Protocol</a>.</p>
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

Copy the featured figures from `paper/figures/` (or wherever they live) into `supplementary/page/assets/figures/` as web-optimized derivatives. Use web-friendly formats:
- Convert PDF figures to PNG or SVG if needed
- Optimize image sizes (no 10MB PNGs)
- Keep original filenames for traceability

### 4. Deploy with the GitHub Actions Pages source

GitHub Pages is GitHub's free static hosting. Its branch-based deployment
can only serve the repo root or `/docs` — neither exists in the APP layout —
so the page is deployed with the **GitHub Actions** source instead, which
can publish any directory. PROTOCOL.md allows `.github/`, so commit
`.github/workflows/paper-page.yml`:

```yaml
name: Deploy paper page
on:
  push:
    branches: [main]   # adjust if the default branch has another name
    paths: ['supplementary/page/**']
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: supplementary/page
      - id: deployment
        uses: actions/deploy-pages@v4
```

One precondition worth stating to a researcher who has not used Pages
before: the repo must be public (private repos need a paid plan).

Check the current Pages configuration:

```bash
gh api repos/{owner}/{repo}/pages 2>/dev/null
```

Three cases:

- Not enabled (404) — enable with the Actions source:

  ```bash
  gh api repos/{owner}/{repo}/pages -X POST -f build_type=workflow
  ```

- Enabled with a branch source (`.build_type` is `"legacy"` in the
  response — e.g. a leftover `main` + `/docs` setup) — switch it, or the
  workflow deploys will never be served:

  ```bash
  gh api repos/{owner}/{repo}/pages -X PUT -f build_type=workflow
  ```

- Already `workflow` — nothing to do.

Or walk the researcher through the manual path: repo page on github.com →
Settings → Pages → under "Build and deployment" choose Source: GitHub
Actions.

Trigger the first deploy by pushing the page (or `workflow_dispatch`). The
page will be available at `https://{username}.github.io/{repo-name}/` after
the run completes (a minute or two, visible in the repo's Actions tab).
Pushes that touch `supplementary/page/**` redeploy automatically, and the
tagged release snapshots the page source with the rest of the publication.

### 5. Verify

- Open the page URL and check everything renders
- Click every link **from the live Pages URL** — nothing may 404 or download
  raw markdown; the agent badge must land on the publication repo
- Test on mobile (responsive?)
- Verify figures display correctly
- Test the BibTeX copy button

### 6. Add the page link to README

Add the page URL to `README.md` on the default branch:
`[Project Page](https://{username}.github.io/{repo-name}/)`

Do not touch `AGENTS.md` for this: `page_url` is not a field in the
PROTOCOL.md frontmatter schema, and validation checks the frontmatter
against that schema. The README link is the canonical pointer to the page.

### Customization

The researcher may want:
- **Different figures** — swap them in `supplementary/page/assets/figures/`
- **Video or demo** — embed a YouTube/video link in the highlights section
- **More sections** — method overview, comparison tables, acknowledgments
- **Custom domain** — they can configure this in GitHub Pages settings
- **Different style** — they can edit `style.css` directly

Keep the base simple. The researcher can customize after generation.
