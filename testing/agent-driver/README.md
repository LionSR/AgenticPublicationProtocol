# Agent driver — testing the protocol by operating an agent via a TTY

This harness drives an **interactive Claude Code session through a real
pseudo-terminal (PTY)** and answers its prompts with simulated keyboard
input — including the `AskUserQuestion` multiple-choice and multi-select
menus. It lets one agent operate another agent end to end, so the questions a
human would normally answer during an APP `publish-paper` interview can be
answered by a script instead.

The motivation: to test the Agentic Publication Protocol you want to run the
real skills the way a researcher would, but the interesting interactions are
**interactive TUI widgets**, not plain text. Piping stdin to headless
`claude -p` never renders those menus. A PTY does, so the harness reads the
rendered screen and presses arrow keys / Enter / Tab like a person.

## What's here

| File | Purpose |
|------|---------|
| `pty_agent.py` | Core mechanism. Spawns `claude` in a PTY, renders the TUI with `pyte`, parses numbered menus, and selects options by **label or position** with cursor verification. Handles single-select, multi-select (checkbox) submit, free-text, and raw keys. |
| `responder.py` | Scenario-driven loop. Declarative `Rule`s map on-screen text to an answer (select / multi-select / type / key). Built-in defaults clear startup menus. Optional **autopilot** (pick the first non-destructive option) and **idle replies** (canned free-text answers) carry a long workflow past prompts you didn't script. |
| `selftest_color.py` | Proves the single-select path: forces an `AskUserQuestion`, answers "Green", verifies the child registered it. |
| `selftest_multiselect.py` | Proves the multi-select path: toggles two checkboxes, tabs to Submit, submits, verifies. |
| `run_publish_paper.py` | Protocol-level integration test: installs the APP plugin into an isolated config, drives `/publish-paper --mode dev-sandbox` against the toy fixture, and answers the interview. Time-boxed. |
| `fixtures/toy-paper/` | A tiny "working repo" (one-page LaTeX paper + one reproducible figure) used as `publish-paper` input. |

## Requirements

- `claude` CLI on `PATH` (tested with v2.1.x).
- Python 3.11+, then `pip install -r requirements.txt` (`pexpect`, `pyte`).
- Authentication: the child session must be able to authenticate. In a
  managed environment (e.g. Claude Code on the web) the managed-host provider
  supplies credentials automatically once onboarding is marked complete — the
  harness seeds an isolated `CLAUDE_CONFIG_DIR` to do exactly that, so it does
  **not** touch your global `~/.claude.json`. On a normal machine, a logged-in
  `claude` works too (point `config_dir` at your real config, or let the
  harness seed a fresh one if your auth is global).
- Running as **root** requires `IS_SANDBOX=1` for `bypassPermissions` (Claude
  Code blocks dangerous-skip-permissions for root otherwise). All commands
  below set it; drop it if you run as a non-root user.

## Run it

```bash
pip install -r requirements.txt

# Prove the mechanism (≈1–2 min each):
IS_SANDBOX=1 python3 selftest_color.py
IS_SANDBOX=1 python3 selftest_multiselect.py

# Drive the real publish-paper skill in dev-sandbox mode (time-boxed):
IS_SANDBOX=1 python3 run_publish_paper.py --minutes 8
```

`--mode dev-sandbox` is used on purpose: it exercises the same prepare and
validate standards as a real publication but creates **no public repo** and
writes **no APP compliance records** (see `PROTOCOL.md` and
`skills/publish-paper/SKILL.md`).

## How selection works (and why it's careful)

Menus render one option per line. The highlighted row carries a `❯` cursor
*before* the number:

```
❯ 1. Yes, I accept
  2. No, exit
```

The driver **never assumes** option 1 or a blind Enter is safe — some menus
(the bypass-permissions warning) default the cursor to a destructive choice
like "No, exit". Instead it:

1. Renders the screen and parses options + the `❯` cursor position.
2. Finds the target by label (truncation/whitespace-tolerant) or by position.
3. Moves the cursor one row at a time, **re-reading the cursor after each
   keypress**, and only presses Enter once `❯` is verified on the target.

Multi-select (`multiSelect`) questions are different: Enter **toggles** a
checkbox rather than submitting. The driver toggles the desired boxes, presses
**Tab** to advance through question tabs to the review/Submit step, then
selects **"Submit answers"**.

## Empirical findings (Claude Code v2.1.x interactive TUI)

These were discovered by probing a live session and are what the harness
depends on:

- **Auth vs. onboarding.** Headless `claude -p` authenticates via the
  managed-host provider, but interactive mode shows a "Select login method"
  screen until onboarding is marked complete. Setting
  `hasCompletedOnboarding: true` in an isolated `CLAUDE_CONFIG_DIR` lets the
  managed provider authenticate interactive mode without touching global
  config and without a browser login.
- **Startup menus are conditional.** Folder-trust and bypass-permissions
  acceptance appear only when not already remembered, so they're handled
  reactively, not as a fixed sequence.
- **Menu format** is stable across kinds (login, trust, bypass, single- and
  multi-select `AskUserQuestion`): `❯`-cursor + numbered options, with a
  footer like `Enter to select · ↑/↓ to navigate · Esc to cancel`.
- **Plugin availability.** A child session gets `/publish-paper` by installing
  the repo as a local marketplace into its isolated config
  (`claude plugin marketplace add <repo>` → `claude plugin install
  paper-protocol@paper-protocol`); the harness does this automatically.

## What the integration run demonstrated

Driving `/publish-paper --mode dev-sandbox` against `fixtures/toy-paper`, the
harness autonomously:

- cleared startup menus, then answered the multi-round interview — single
  choice, **multi-select checkboxes**, and free-text — choosing a repo name,
  license, audience, reader goals, and supplementary handling;
- let the skill build `publication-staging/`, set up a virtualenv, **reproduce
  the figure** (exact agreement, `max abs difference … : 0`), and run
  **`validate-publication`** ("Structure is clean").

i.e. the protocol's own workflow runs to completion under a fully automated,
no-human-in-the-loop agent driver.

## Limitations & extension notes

- **Long, line-wrapped option labels** are matched leniently and, for
  autopilot, selected by position; very long custom labels can still be hard
  to match by text — prefer `select_index` / position when scripting those.
- **Autopilot is a smoke-test convenience**, not a faithful researcher: it
  picks the first non-destructive option and submits multi-selects with a
  single default checkbox. For meaningful publication content, script explicit
  `Rule`s (and `idle_replies`) per decision point instead.
- The full six-phase `publish-paper` run is long; `run_publish_paper.py` is
  time-boxed and is intended to prove the harness *drives the protocol*, not to
  produce a finished publication.
- Same approach should port to **Codex** (also reads `AGENTS.md`); only the
  spawn command, auth, and menu glyphs would need adapting in `pty_agent.py`.
- The harness reads model/CLI output from external processes. Treat captured
  transcripts as untrusted text; they are gitignored by default.
