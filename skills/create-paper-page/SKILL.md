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

Build the site in a scratch directory outside the publication tree (a temp
dir or the private working repo). It is published from an orphan `gh-pages`
branch in step 4 — never committed into the publication tree itself:

```
paper-page/
├── index.html        ← the landing page
├── style.css         ← styling
└── assets/
    ├── figures/      ← featured figures (copied from paper/figures/)
    └── ...           ← any other assets (logos, photos)
```

**Protocol consistency:** the APP repository layout (PROTOCOL.md) does not
include a `docs/` directory, and the tagged release tree must stay exactly
protocol-shaped. The page therefore lives on a separate orphan `gh-pages`
branch, not on `main`. Likewise, never add non-protocol fields such as
`page_url` to the `AGENTS.md` frontmatter — the page URL goes in `README.md`
(step 6).

**The HTML should be:**
- Self-contained — no build step, no JavaScript framework, no npm
- Clean and readable — academic style, not startup landing page
- Mobile-friendly — responsive layout
- Fast — just HTML + CSS + images, no heavy dependencies

**Linking rules — the live site serves only the `gh-pages` branch:**

The published site lives at `https://{username}.github.io/{repo-name}/` and
can serve only files committed to the `gh-pages` branch. Relative links into
the publication tree (`../paper/...`, `../AGENTS.md`) 404 on the live site.
Pages also does not render markdown — a link to a `.md` file shows raw text
or downloads the file, which is not usable (a downloaded `AGENTS.md` on its
own does nothing; the agent works by opening the cloned repo).

- The primary link target is the **publication repo on GitHub**
  (`https://github.com/{owner}/{repo}`) — readers get the rendered README,
  the code, and the clone URL in one place.
- Files that should display in the browser (paper PDF, figures) — copy them
  into the site's `assets/` and link relatively.
- A specific repo file worth pointing at (e.g. a computations README) — use
  the rendered GitHub URL, pinned to the release tag:
  `https://github.com/{owner}/{repo}/blob/{tag}/...`. PROTOCOL.md says
  external references should point to a specific tag, and tag URLs are
  immutable; do not hardcode a branch name (not every repo's default branch
  is `main`).
- Agent badge → the publication repo URL, never a `.md` file.
- For a local dev-sandbox preview (no public repo yet), relative links into
  the staging tree are acceptable for browsing — but the preview must not
  remain inside the staging tree at validation/release time (delete it or
  keep it untracked), and every link must be rewritten per these rules
  before a real release.

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
            <a href="[arxiv-url]">Paper</a>          <!-- or assets/paper.pdf copied into the site -->
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

Copy the featured figures from `paper/figures/` (or wherever they live) into the site's `assets/figures/`. Use web-friendly formats:
- Convert PDF figures to PNG or SVG if needed
- Optimize image sizes (no 10MB PNGs)
- Keep original filenames for traceability

### 4. Publish to `gh-pages` and enable GitHub Pages

GitHub Pages is GitHub's free static hosting. The site lives on an orphan
`gh-pages` branch — a branch with no shared history with `main` — so the
publication tree and its tagged release stay protocol-shaped. Use exactly
the branch name `gh-pages` (the conventional Pages branch); do not invent
repo-specific variants. One precondition worth stating to a researcher who
has not used Pages before: the repo must be public (private repos need a
paid plan).

Publish the site directory **from a fresh temporary clone, never from the
working clone**: untracked files and gitignored artifacts in a working clone
survive `git rm -rf .` and `git add -A` would sweep them into the public
branch.

First publish (no `gh-pages` branch exists yet):

```bash
git clone <repo-url> /tmp/paper-page-publish
cd /tmp/paper-page-publish
git checkout --orphan gh-pages
git rm -rf .
cp -R <scratch-dir>/paper-page/. .
git add -A
git commit -m "Project page"
git push origin gh-pages
cd - && rm -rf /tmp/paper-page-publish
```

Later updates (a `gh-pages` branch already exists — the orphan flow would
fail to push against it; check out the existing branch instead):

```bash
git clone --branch gh-pages <repo-url> /tmp/paper-page-publish
cd /tmp/paper-page-publish
git rm -rf .
cp -R <scratch-dir>/paper-page/. .
git add -A
git commit -m "Update project page"
git push
cd - && rm -rf /tmp/paper-page-publish
```

Check the current Pages configuration:

```bash
gh api repos/{owner}/{repo}/pages 2>/dev/null
```

Three cases:

- Not enabled (404) — enable it on the new branch:

  ```bash
  gh api repos/{owner}/{repo}/pages -X POST -f 'source[branch]=gh-pages' -f 'source[path]=/'
  ```

- Enabled but with a different source (check `.source` in the response —
  e.g. a leftover `main` + `/docs` setup) — switch it, or the new branch
  will never be served:

  ```bash
  gh api repos/{owner}/{repo}/pages -X PUT -f 'source[branch]=gh-pages' -f 'source[path]=/'
  ```

- Already `gh-pages` + `/` — nothing to do.

Or walk the researcher through the manual path: repo page on github.com →
Settings → Pages → under "Build and deployment" choose Source: Deploy from a
branch → branch `gh-pages`, folder `/ (root)` → Save.

The page will be available at `https://{username}.github.io/{repo-name}/`
after a build that takes a minute or two (visible in the repo's Actions tab).
Later page updates are pushes to `gh-pages` only — they never touch the
default branch or the tagged release.

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
- **Different figures** — swap them in `assets/figures/` on the `gh-pages` branch
- **Video or demo** — embed a YouTube/video link in the highlights section
- **More sections** — method overview, comparison tables, acknowledgments
- **Custom domain** — they can configure this in GitHub Pages settings
- **Different style** — they can edit `style.css` directly

Keep the base simple. The researcher can customize after generation.
