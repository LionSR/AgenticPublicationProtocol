# APP Position Paper — Outline

Working outline for the arXiv position paper announcing the Agentic Publication
Protocol. Positioning: **position / vision paper** with a reference
implementation and a self-dogfooded case study. Internal planning material.

**Working title (candidates):**

- "Publish an Agent, Not Just a Paper: The Agentic Publication Protocol"
- "Agentic Publications: An Interactive Format for Scientific Work"
- "From Static Manuscripts to Agentic Publications"

**Target length:** ~8–12 pages, two-column or arXiv preprint style.

---

## Abstract (~150–200 words)

Static papers lose author know-how and impose high reproduction cost. AI agents
let us publish an interactive representative of the work alongside the paper. We
introduce APP, a format that packages a finished paper as a Git repository with
`AGENTS.md`, a tagged release, and a verifiable manifest, so any `agents.md`-aware
agent can explain the work, reproduce figures, run experiments, and answer
questions grounded in the artifacts. We describe the design principles, the
specification, a reference implementation of authoring/validation skills, and a
case study publishing our own paper. This paper is itself an APP publication.

## 1. Introduction / Motivation

- The static-paper problem: incomplete information, high reproduction cost,
  missing tacit know-how. (Reuse README "Motivation".)
- The agent-era opportunity: "publish an agent, not just a paper."
- Thesis: publications should become an **interactive, dynamic medium** that
  lowers the cost of understanding, reproducing, and building upon the work.
- Contributions list (bullet form):
  1. The concept of an *agentic publication*.
  2. APP: a concrete, minimal, verifiable format.
  3. A reference implementation (authoring + validation skills).
  4. A self-dogfooded case study.

## 2. What is an Agentic Publication

- Definition: repo + `AGENTS.md` + tagged release + verifiable manifest.
- The reader experience: clone, open in Claude Code / Codex / any agents.md
  agent, and the agent "speaks for the paper."
- Key distinction: APP defines *what an agentic publication looks like*; it does
  **not** prescribe *how* to create one (that is the skills' job). Protocol vs.
  tooling separation.
- Figure: publication repository structure (reuse `assets/readme/`).

## 3. Design Principles

Lift the six principles from `PROTOCOL.md`, each as a short subsection with the
rationale and the failure mode it prevents:

1. **Faithfulness to ground truth** — manuscript/code/data are authoritative;
   author claims preserved; external context clearly distinguished. (Mitigates
   hallucination / misrepresentation.)
2. **Reproducibility** — executable instructions, figure-reproduction map,
   pinned environment.
3. **Transparency and provenance** — link claims to files/sections.
4. **Canonical structure and referencing** — one canonical location per
   artifact.
5. **Versioned publication** — `(repo, tag)` immutable snapshot.
6. **Agent skills** — optional reusable capabilities (Agent Skills Protocol).

## 4. Specification Overview

Condensed from `PROTOCOL.md`; full spec lives in the repo.

- Repository layout (`paper/`, `code/`, `data/`, `environment/`,
  `supplementary/`, `skills/`) and what is required vs. optional.
- `AGENTS.md`: frontmatter fields + required sections (Identity, Paper Summary,
  Key Results, Repository Structure, What You Can Do, Computational
  Requirements, Citation).
- Versioning: `(repo URL, tag)`, immutable tags, GitHub releases.
- **Verified manifest**: `APP_PUBLICATION.json`, `app_publication_id` derivation,
  the three trust tiers (agent-readable / APP-structured candidate / verified).
  This is a genuinely novel bit worth a clear diagram.

## 5. Reference Implementation

- The official skills: `publish-paper`, `validate-publication`,
  `extract-chat-context`, `create-paper-page`, `load-paper`.
- Authoring workflow figure (reuse `assets/readme/publish_workflow.png`).
- Validation: structure, paths, privacy, factual consistency, reader-agent
  usability, manifest verification.
- External skills / extensions mechanism: keeping the core small, letting
  field-specific capabilities evolve independently.

## 6. Case Study (our own paper)

The most persuasive section. Take one of our own papers through `publish-paper`
and report honestly:

- What the working repo looked like before.
- The authoring session(s): what the skill asked, what we approved, effort spent.
- The resulting APP publication structure.
- **Demonstrated reader-agent capabilities**: explain a result, reproduce a
  specific figure end-to-end (show the command + output match), run a small
  experiment, answer a grounded question with provenance.
- What worked, what was awkward, what we would improve in the spec.

> TODO: pick which of our papers; gather screenshots / transcripts; record exact
> reproduction commands and runtimes.

## 7. Related Work

Position APP relative to (and distinguish from):

- **Agent / doc standards**: `agents.md`, Agent Skills Protocol, MCP.
- **Reproducibility & artifacts**: ACM Artifact Review & Badging, Papers with
  Code, Code Ocean, MyBinder / Binder, Jupyter, Whole Tale, Research Objects /
  RO-Crate.
- **Open-science principles**: FAIR data principles.
- **Living / executable documents**: executable papers, computational
  notebooks.
- Key differentiator: APP ships an *interactive agent grounded in the artifacts*
  with a *verifiable release manifest*, not just runnable code or richer
  metadata.

> TODO: gather citations; verify current names/links before submission.

## 8. Limitations and Threats to Validity

Be explicit (raises credibility):

- Verification proves structure + author approval, **not** scientific
  correctness.
- Hallucination risk despite the Faithfulness principle.
- Author burden and incentive alignment.
- Maintenance / longevity of published agents and their dependencies.
- Dependence on the evolving agent ecosystem.

## 9. Governance and Roadmap

- How the protocol evolves; semantic versioning of the spec.
- Extension mechanism for fields/journals/workflows.
- Path from v0.1.0 draft toward v0.2.0 informed by real publications.
- Call for adoption and contribution.

## 10. Conclusion

Restate the thesis; the paper-you-are-reading is itself an APP publication;
invite readers to clone it and talk to it.

---

## Production checklist

- [ ] Decide working title.
- [ ] Run case study end-to-end; capture artifacts.
- [ ] Collect and verify related-work citations.
- [ ] Draft prose section by section.
- [ ] Structure the paper's own repo as an APP publication (dogfood).
- [ ] Prepare blog / X long-post for coordinated drop.
- [ ] Internal review pass focused on the honesty of §8.
