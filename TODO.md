# TODO

Work items deferred past the current draft of the Agentic Publication Protocol.

## Documentation

- **Workflow diagram.** Add a diagram to `PROTOCOL.md` or `README.md` showing the flow: working repo → `/publish-paper` → publication repo (tagged release) → reader's agent.
- **Example publication.** Add a fully populated example APP publication under `examples/`, beyond the minimal `template/` skeleton — a real paper's worth of structure that readers can reference.

## Skills

- **Split `skills/publish-paper/SKILL.md`.** The orchestrator is currently a single long file covering six phases. Candidate split:
  - `understand-repo` — phase 1 (read the working repo, check for previous versions).
  - `interview-researcher` — phase 2 (structured interview, extract context).
  - `build-repo` — phase 3 (create publication repo, copy and organize files, verify code runs).
  - `draft-agents-md` — phase 4 (draft `AGENTS.md` and `README.md`, iterate with researcher).
  - `final-review` — phase 5 (final validation, checklist walk-through).
  - `release` — phase 6 (commit, tag, push, record in `.publications.md`).
  `publish-paper` stays the user-facing entry point and calls these in order.

## Protocol

- **Conformance automation.** A lightweight checker (CLI or GitHub Action) that validates an APP publication against `PROTOCOL.md` — paths resolve, frontmatter is well-formed, tag matches `version`. Could be packaged as a companion tool to `/validate-publication`.
