# Session Output Formats

Templates and formatting guidance for the three output levels in extract-context.

## Know-how (default — `supplementary/know-how.md`)

Thematic summary of all sessions. Organize by topic, not by session.

```markdown
# Know-How

## Methodology decisions
- [Why we chose approach X over Y — from session Z]
- [What didn't work and why]

## What worked well
- [Approaches, tools, configurations that were particularly effective]
- [Why they worked — what made them the right choice]

## Key insights during development
- [Insight 1]
- [Insight 2]

## Dead ends and alternatives tried
- [Approach that was attempted but abandoned, and why]

## Tacit knowledge
- [Things the researcher knows from experience that are not in the paper]
- [E.g., "feature X is sensitive to batch size in ways the paper doesn't explore"]
- [E.g., "the loss landscape has a plateau around epoch 30 that is not a bug"]

## Known limitations and future ideas
- [Limitation the researcher is aware of]
- [Idea that didn't make it into the paper]
```

Adapt the sections to fit the actual content — these are starting points, not a rigid structure. A paper heavy on debugging might have a "Bugs and fixes" section; a theory paper might have "Proof strategies attempted."

## Cleaned sessions (`supplementary/sessions/`)

One file per session. Each session is curated: typos fixed, tangents removed, long agent responses summarized, but the reasoning is preserved.

```markdown
# Session: [descriptive title]

Date: YYYY-MM-DD
Topic: [what this session was about]

## Key decisions
- [Decision 1 — what was decided and why]
- [Decision 2]

## Conversation

**Researcher:** [cleaned-up message — fix typos, remove tangents, keep substance]

**Agent:** [summarized response — keep the key information, trim verbose output]

**Researcher:** [next message]

...
```

When curating with the researcher:
- Show them the raw conversation
- Help them decide per exchange: keep, summarize, or skip
- Clean up messages for readability while preserving reasoning
- Summarize long agent responses to their key points
- The "Key decisions" header at the top should capture what came out of the session

## Full history (`supplementary/sessions/`)

One file per session. Minimal processing — convert from JSON to readable markdown, strip system tags, format readably. Don't heavily edit content.
