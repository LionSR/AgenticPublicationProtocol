# TODO

Work items deferred past the current draft of the Agentic Publication Protocol.

## Documentation

- **Workflow diagram.** Add a diagram to `PROTOCOL.md` or `README.md` showing the flow: working repo → `/publish-paper` → publication repo (tagged release) → reader's agent.
- **Example publication.** Add a fully populated example APP publication under `examples/`, beyond the minimal `template/` skeleton — a real paper's worth of structure that readers can reference.

## Skills

- **Split `skills/publish-paper/SKILL.md`.** The orchestrator is a single ~560-line file covering six phases. Split into four sub-skills at the natural user-facing checkpoints already present in the workflow (no new pauses, just naming the pauses that exist):
  - `publish-paper-gather` — phases 1–2. Read the working repo, check `.publications.md` for prior versions, interview the researcher, optionally extract context. Output: a publication plan (scope, file list, title, version).
  - `publish-paper-build` — phase 3. Create the publication repo, copy and organize approved files, verify code runs with new paths. Output: a working publication repo before authoring.
  - `publish-paper-draft` — phase 4. Draft AGENTS.md and README, iterate with the researcher. Output: drafted publication ready for final review.
  - `publish-paper-release` — phases 5–6. Final validation sweep, checklist walk-through, commit, tag, push, record in `.publications.md`. Output: a tagged public release.

  `publish-paper` stays as a thin user-facing orchestrator — shows the roadmap, dispatches to each sub-skill in order, carries cross-phase state. Each sub-skill is also invokable standalone for targeted re-runs (e.g. redo just the AGENTS.md draft).

  Shared content currently in the orchestrator (pace principle, author's voice, structured-question guidance, handling different paper types) inlines into the sub-skill where it applies, or moves to a shared reference file the sub-skills link.

## Protocol

- **Conformance automation.** A lightweight checker (CLI or GitHub Action) that validates an APP publication against `PROTOCOL.md` — paths resolve, frontmatter is well-formed, tag matches `version`. Could be packaged as a companion tool to `/validate-publication`.
