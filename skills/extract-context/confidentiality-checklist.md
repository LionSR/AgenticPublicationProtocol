# Confidentiality and Privacy Screening

This checklist is used in step 5 of the extract-context process. All output files (`supplementary/know-how.md`, `supplementary/authors-note.md`, any session files in `supplementary/sessions/`, and any files in `supplementary/materials/`) must be screened before publishing.

## Patterns to flag

**Credentials and secrets:**
- API keys, tokens, passwords (patterns like `sk-...`, `ghp_...`, `Bearer ...`, `key=...`)
- Environment variables with secret values
- Database connection strings

**Personal information:**
- Email addresses, phone numbers, physical addresses
- Names of people not listed as paper authors (collaborators, reviewers, students mentioned in passing)

**Internal infrastructure:**
- Internal URLs (company intranets, staging servers, private endpoints)
- File paths that reveal private directory structure (e.g., `/Users/name/...`, `C:\Users\name\...`)
- References to private repos, internal tools, or unreleased work
- IP addresses of internal servers

**Data and access:**
- Dataset paths or identifiers that might be access-controlled
- License keys or subscription identifiers
- References to data the researcher doesn't have permission to redistribute

**Tone and content:**
- Profanity, casual remarks, or off-topic tangents the researcher wouldn't want public
- Negative comments about specific people, institutions, or competing work
- Draft text the researcher might not want attributed to them publicly

## Procedure

For each flagged item, present the researcher with:
- The exact text and its location (file + line)
- A suggested action:
  - **Redact** — remove or replace with a placeholder (e.g., `[REDACTED]`, `[internal-url]`)
  - **Keep** — the researcher confirms it's fine to publish
  - **Rephrase** — rewrite to remove the sensitive part while keeping the insight

Do NOT silently remove content — always show the researcher what was flagged and let them decide.

Err on the side of flagging too much rather than too little. A false positive costs the researcher a few seconds; a missed leak can't be taken back.

After the researcher resolves all flags, do a final pass over all output files to confirm nothing was missed.
