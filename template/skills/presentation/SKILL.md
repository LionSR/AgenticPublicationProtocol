---
name: presentation
description: Generate a slide presentation summarizing the paper. Use when asked to create slides, a talk, or a presentation.
---

# Presentation Generation

Create a slide deck summarizing the paper.

## Approach

1. Read the paper source in `paper/` to understand the full content
2. Structure the presentation as:
   - Title slide (title, authors, affiliations, date)
   - Motivation / Problem statement (1-2 slides)
   - Key ideas / Methods (2-4 slides)
   - Main results (2-3 slides, include figures from `paper/figures/`)
   - Conclusions and future work (1 slide)

3. For each figure included, reference the source file in `paper/figures/`

## Output Format

Generate the presentation as:
- LaTeX Beamer (if the user uses LaTeX)
- Markdown slides (if the user prefers)
- Plain text outline (as a starting point)

Ask the user which format they prefer.

## Customization

The user may request:
- A short version (5 minutes / 5 slides)
- A long version (20 minutes / 15-20 slides)
- Focus on specific sections
- A particular style or template
