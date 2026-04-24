# Agentic Publication Protocol — Vision

Ideas and directions beyond the core protocol.

## Quick follow-up without reproduction

The biggest value is speed. Today, building on someone's paper means days of reproducing their setup — installing dependencies, figuring out undocumented scripts, debugging platform differences. With a paper agent, you clone the repo, load the agent, and immediately say "try this with different parameters" or "what happens if we change assumption X?" The agent knows the code, the data, and the methodology. It can run things for you or explain why something won't work on your machine.

## Multi-agent discussion

Two paper agents can discuss with each other. Load both as sub-agents in your project and ask them to compare approaches. Or put multiple paper agents in a Slack channel — each responds when @-mentioned, and they can build on each other's points. No new protocol is needed for this; existing agent platforms already support sub-agents and messaging. The interesting part is what emerges when paper agents with different perspectives interact — they can identify connections, contradictions, and potential syntheses that a human might miss.

## Minimal publications

Not every paper has code. A theoretical paper, a review, or a set of small results that don't warrant a full paper — all valid. The minimal publication is `paper/<document>` plus the always-required root files `AGENTS.md`, `README.md`, and `LICENSE`; `code/`, `data/`, and `environment/` can all be absent. The agent explains and discusses the content. The protocol scales down to "just a paper with an agent to chat about it" and scales up to full reproducible computational pipelines.

## Environment awareness

When code is included, the agent should understand the computational environment it was developed in. If a reader runs it on a different OS or without a GPU, the agent should be able to explain why something fails and suggest adaptations — not just silently hang or produce cryptic errors. This means documenting not just what dependencies are needed, but what platform the code was tested on and what resources heavy computations require.

## Protocol as a published artifact

`PROTOCOL.md` is itself a description of a publication format. A natural next step is to publish the protocol as a paper of its own — bundling the specification, motivating examples, and design rationale — and archive it alongside other scientific artifacts. The protocol can be cited and versioned the way any other publication is.

## A home for APP publications

Today, APP publications sit as independent GitHub repositories cross-linked from arXiv ancillary material or personal pages. A hosted index — searchable by metadata, domain, or tag, with optional inline chat — would let readers discover and consult published agents without cloning. The protocol does not mandate such a platform; it is compatible with one, and such a platform would scale across many publications without requiring coordination between authors.

## Native repository-host agents

Repository hosts (GitHub, GitLab, and others) are adding agents that chat about a repo directly in the browser. When those integrations read `AGENTS.md`, an APP publication becomes chattable without any local setup — clone-free reading for shorter questions, with local cloning reserved for code execution and heavier exploration. This is orthogonal to APP but a natural distribution channel.

## Future work

- Paper agents as MCP servers for runtime tool access
- Benchmark integration (cf. Terminal Bench Science)
- Automated figure verification using vision models
- Cross-platform environment adaptation
