# TODO

Work items deferred past the current draft of the Agentic Publication Protocol.

## Documentation

- **Workflow diagram.** Add a diagram to `PROTOCOL.md` or `README.md` showing the flow: working repo → `/publish-paper` → publication repo (tagged release) → reader's agent.
- **Example publication.** Add a fully populated example APP publication under `examples/`, beyond the minimal `template/` skeleton — a real paper's worth of structure that readers can reference.

## Protocol

- **Conformance automation.** A lightweight checker (CLI or GitHub Action) that validates an APP publication against `PROTOCOL.md` — paths resolve, frontmatter is well-formed, tag matches `version`. Could be packaged as a companion tool to `/validate-publication`.
