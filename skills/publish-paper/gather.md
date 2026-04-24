# Phases 1–2 — Understand and Discuss

## Phase 1 — Understand

### 1.1 Check for previous versions

First, check the **working repo** for a `.publications.md` file — `release.md` creates this after each release and tracks all publication repos from this working repo.

**If `.publications.md` exists:**

- Read it to find the previous publication repo URL, version, and date.
- Clone or locate that publication repo.
- Read its `AGENTS.md`, `README.md`, `supplementary/`, and `skills/` thoroughly.
- Most content already exists and just needs updating.
- The researcher's interview (phase 2) should focus on **what changed** — "What's new or different in this version?"
- Carry forward anything that hasn't changed rather than re-creating it.
- In phase 4, start from the previous `AGENTS.md` and modify it, rather than drafting from scratch.
- When creating the new version, update the `version` field in `AGENTS.md` frontmatter and tag a new release (e.g. `v2.0.0`).

**If `.publications.md` does not exist**, ask the researcher: "Is this the first version, or is there a previous publication repo?" If a previous version exists, get the repo URL and follow the same process.

This saves significant time and avoids losing good content that was already reviewed and approved.

### 1.2 Understand the paper

Read the working repo thoroughly before asking the researcher anything. Build a mental model. For format-specific guidance — theory papers, notebooks, video — see [`paper-types.md`](paper-types.md).

**Paper source.** Find the main document (`*.tex`, `*.md`, `*.docx`, `*.pdf`, `*.html`, `*.pptx`, video files). Note all candidates if multiple exist — you'll ask the researcher which is canonical in phase 2. Read it — title, abstract, key claims, structure. Find figures: where they're stored, which source files generate them.

**Code.** Language, framework, entry point. Dependency manifests (`setup.py`, `pyproject.toml`, `requirements.txt`, `environment.yml`, `package.json`, `Cargo.toml`). What the code does — simulation, data analysis, model, proof script. Figure-generating scripts. Config files that control parameters.

**Data.** Is there data in the repo? How large? Raw, processed, or both? External data references — Hugging Face (`huggingface.co/datasets/…`), Zenodo (`zenodo.org/record/…`), Figshare, Dryad, Materials Project, Google Drive / Dropbox. For each external dataset, note URL and download command. Check whether a `data/README.md` already exists in the working repo — the spec requires one in the publication whenever `data/` has files. If the working repo doesn't have one, record that it must be authored with the researcher in phase 3.

**Environment.** Platform developed on (OS-specific code), GPU requirements, cluster job scripts, Dockerfiles.

**Supplementary materials.** Slides, talks, posters, tutorials, conversation logs, research notes already in the repo.

**Script→figure mapping.** For each figure in the paper:

1. Find the figure reference in the paper source (`\includegraphics`, filenames).
2. Find the script that generates it (`savefig`, `plt.save`, output paths).
3. Identify the data the script reads.

The spec requires one reproduction script per figure. Flag figures whose script also produces other figures — these need to be split in phase 3, or the overlap explicitly documented if splitting is impractical.

Note anything you cannot figure out by reading — these become targeted questions for phase 2.

**Tell the researcher what you found.** Present your understanding of the repo structure, the paper, and the code. Show them the script→figure mapping. This demonstrates you did the homework and gives them a chance to correct misunderstandings early.

## Phase 2 — Discuss

### 2.1 Interview the researcher

Ask **1–3 questions per round**, wait for answers, then move to the next round. Do not dump all questions at once — researchers have limited attention and will miss things in a wall of text. Lead with what you can't figure out from reading; skip questions you already know the answer to.

**Within each round:** if the researcher answers some questions but not others, follow up on the unanswered ones specifically. Do not move to the next round until the current one is resolved — either answered or explicitly deferred.

**Round 1 — The paper.** Foundation; start here.

- If multiple paper-like documents exist: "Which of these is the canonical paper?" (show the candidates you found).
- "In your own words, what are the key results and the main contribution?"

**Round 2 — The code.** Only what you couldn't determine from phase 1.

- Show the script→figure mapping you built and ask the researcher to confirm or correct it.
- For any multi-figure scripts flagged in phase 1, ask whether to split them or keep as-is; record the decision.
- "What's the main experiment and how do you run it?"
- If anything looked fragile or slow, ask about it specifically.

**Round 3 — What to publish.**

- Present the file list with a structured choice for each: include / exclude / ask me later.
- "What should the publication repo be called?"

**Round 4 — The reader's perspective.**

- "What do you wish someone had told you before reading this paper?"
- "What would a reader most likely want to do?" Offer options: reproduce figures, extend the work, understand the math/theory, run with different inputs.

**Round 5 — Supplementary materials and skills** (optional — skip if the researcher is low on time).

- "Do you have slides, talks, posters, or tutorials? Do you have permission to share them?"
- "Are there specific workflows you'd like readers to run through the agent?"

**After all rounds — gap check.** If any of these crucial items are still missing, ask again explicitly:

- the canonical paper document;
- the key results;
- the include/exclude file list;
- the repo name.

These four are required to proceed. Everything else can be filled in later or inferred.

### 2.2 Extract research context (optional)

Ask the researcher if they want to include research context from their conversation history. Offer a structured choice:

- **Yes — extract from sessions** (recommended). Captures reasoning, decisions, dead ends from Claude Code / Codex history. By default all project sessions are included and a thematic summary is produced. The researcher can optionally publish more detailed session transcripts too.
- **Yes — I'll write notes manually.** The researcher provides context themselves.
- **No — skip this.** No research context in the publication.

This context is valuable for writing `AGENTS.md` in phase 4, because the agent can answer "why did you do X?" from real reasoning rather than guessing.

If extracting from sessions, run `/extract-context` in the **working repo** (that's where the sessions are). The output will be copied into the publication repo later in phase 3. `/extract-context` runs its own confidentiality screening; phase 4 checks again when incorporating context into `AGENTS.md`.

## Handoff

Summarise the publication plan to the researcher. Next: [`build.md`](build.md).
