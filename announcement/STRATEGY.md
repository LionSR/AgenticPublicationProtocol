# APP Announcement Strategy

Working notes for announcing the Agentic Publication Protocol (APP). This is
internal planning material, not part of the protocol specification.

## Goal

Introduce APP to two distinct audiences without diluting the message for either:

1. **Researchers / authors** — potential publishers. They decide based on whether
   APP solves a real pain in their research workflow and whether it is credible
   enough to adopt. They live on arXiv, X/Twitter, and in their labs.
2. **The agent / tooling ecosystem** — Claude Code, Codex, `agents.md`-aware
   agents, plugin marketplaces. They care about the spec itself and integration.

A single channel cannot reach both. The plan below uses complementary channels.

## Decisions (settled)

- **Write an arXiv paper**, positioned as a **position / vision paper** (not a
  benchmark-driven empirical paper).
- **Dogfood**: publish *this* repository as a verified APP publication, so the
  strongest demo is "clone the APP paper and talk to it with an agent."
- **Case study**: use one of our own papers, run it end-to-end through
  `publish-paper`, and report the experience in the paper.
- Pair the arXiv drop with a blog / X long-post aimed at the tooling ecosystem.

## Why arXiv (even though it is "just a protocol")

The value of arXiv here is not technical novelty. It is:

- A **citable, permanent anchor** for an idea, in the language the target
  audience already uses. We are pitching "a new way to publish" *to* academics,
  so we should speak academic.
- **Credibility**: a position + spec on arXiv reads as a proposal worth
  discussing and citing, where a bare GitHub repo reads as just a tool.
- A natural **dogfooding** opportunity: the paper announcing APP can itself be
  an APP publication.

## Channels and artifacts

| Channel | Artifact | Audience | Status |
|---------|----------|----------|--------|
| arXiv | Position paper (PDF + abstract) | Researchers | outline drafted |
| GitHub (this repo) | Verified APP release of the paper repo | Both | planned |
| Blog / X long-post | Short narrative + demo GIF/video | Tooling ecosystem | planned |
| Plugin marketplaces | Already shipped (Claude Code, Codex) | Tooling ecosystem | done |
| HN / Reddit / lab talks | Link + framing | Mixed | opportunistic |

## Sequencing

1. **Finalize the spec** at a taggable state (v0.1.0 → consider v0.1.0 release).
2. **Run the case study**: take our own paper through `publish-paper`, capture
   the real workflow, screenshots, and what the reader-agent can do. This
   produces the most persuasive section of the paper, so do it before writing
   the results-ish sections.
3. **Write the position paper** from the outline.
4. **Dogfood**: structure the paper's own repo as an APP publication
   (`AGENTS.md`, `paper/`, manifest), so readers can interact with the paper.
5. **Coordinated drop**: arXiv submission + blog/X post + repo release on the
   same day. Cross-link all three.
6. **Follow-up**: respond to discussion, collect early adopters, iterate spec
   toward v0.2.0 based on real publications.

## Risks / things to be honest about in the announcement

- Verification (manifest + validation) proves *structure and approval*, not
  scientific *correctness*. Say so plainly.
- Agent hallucination risk; the Faithfulness principle is a mitigation, not a
  guarantee.
- Author burden / incentives: why would authors do the extra work? The case
  study should speak to effort honestly.
- Maintenance and longevity of published agents.

Addressing these directly raises credibility far more than ignoring them.
