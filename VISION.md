# Agentic Publication Protocol — Vision

Ideas and directions beyond the core protocol.

## Quick follow-up without reproduction

The biggest value is speed. Today, building on someone's paper means days of reproducing their setup — installing dependencies, figuring out undocumented scripts, debugging platform differences. With a paper agent, you clone the repo, load the agent, and immediately say "try this with different parameters" or "what happens if we change assumption X?" The agent knows the code, the data, and the methodology. It can run things for you or explain why something won't work on your machine.

## Multi-agent discussion

Two paper agents can discuss with each other. Load both as sub-agents in your project and ask them to compare approaches. Or put multiple paper agents in a Slack channel — each responds when @-mentioned, and they can build on each other's points. No new protocol is needed for this; existing agent platforms already support sub-agents and messaging. The interesting part is what emerges when paper agents with different perspectives interact — they can identify connections, contradictions, and potential syntheses that a human might miss.

## Minimal publications

Not every paper has code. A theoretical paper, a review, or a set of small results that don't warrant a full paper — all valid. A repo with just `AGENTS.md` and a PDF works. The agent explains and discusses the content. The protocol scales down to "just a paper with an agent to chat about it" and scales up to full reproducible computational pipelines.

## Environment awareness

When code is included, the agent should understand the computational environment it was developed in. If a reader runs it on a different OS or without a GPU, the agent should be able to explain why something fails and suggest adaptations — not just silently hang or produce cryptic errors. This means documenting not just what dependencies are needed, but what platform the code was tested on and what resources heavy computations require.

## Future work

- Paper agents as MCP servers for runtime tool access
- Benchmark integration (cf. Terminal Bench Science)
- GitHub Pages landing page with embedded chat
- Automated figure verification using vision models
- Cross-platform environment adaptation
