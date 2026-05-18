# Contributing to APP

Contributions are welcome. This repository is the home for the Agentic Publication Protocol specification, the reference templates, and the official skills that help authors create, validate, load, and publish APP publications.

## What Belongs Here

Good contributions to this repository include:

- clarifications or corrections to `PROTOCOL.md`
- improvements to the reference templates in `template/`
- fixes or focused improvements to official workflow skills in `skills/`
- validation checks that enforce existing protocol requirements
- documentation, examples, and test cases that help authors publish or readers load APP publications

This repository should stay focused on the APP publication format and its official workflows. Reusable writing, proofreading, journal-specific, or field-specific skills usually belong in separate skill repositories and can be referenced by APP publications through `recommended_external_skills` or `app_extensions`.

## External Skills

Third-party skills do not need to live in this repository. A lab, field community, or individual researcher can publish a normal Agent Skill in their own repository and point APP publications directly to the skill directory containing `SKILL.md`.

External skills may be proposed for inclusion here when they are broadly useful to APP itself rather than to one field, venue, or author's workflow. For example, a general validation helper may belong here; a quantum-information proofreading skill probably belongs in a field-maintained repository.

## Changing the Protocol

Protocol changes should be conservative. A proposal that changes `PROTOCOL.md` should explain:

- the problem the change solves
- whether the change is required or optional
- how existing APP publications continue to work
- how agents should behave when they do not support the new capability
- whether validation needs to change

Prefer optional, gracefully degrading additions over new required fields. Avoid adding new file formats unless the existing `AGENTS.md`, Agent Skills, or repository structure cannot express the need clearly.

## Changing Official Skills

Changes to official skills should preserve the distinction between:

- author-approved publication contents
- validation results
- supplementary context
- third-party or external recommendations

When editing skills, keep behavior grounded in the protocol and avoid making the skill depend on one agent provider unless that dependency is clearly documented.

## Review Checklist

Before opening a pull request, check:

- Markdown links and paths resolve.
- New requirements use RFC 2119 language (`MUST`, `SHOULD`, `MAY`) when they are normative.
- Optional capabilities state fallback behavior.
- External skills are not described as publication ground truth.
- Template changes remain minimal and easy for authors to fill in.

For code or script changes, include the command you ran to test them. For documentation-only changes, a short explanation of the intended behavior is enough.
