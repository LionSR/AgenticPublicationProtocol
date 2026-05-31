# testing/

Tooling for exercising the Agentic Publication Protocol with real agents.

- [`agent-driver/`](agent-driver/) — a PTY harness that operates an
  interactive Claude Code session and answers its prompts (including
  `AskUserQuestion` multiple-choice and multi-select menus) with simulated
  keyboard input. Used to drive `/publish-paper --mode dev-sandbox` against a
  toy fixture with no human in the loop. See its README for details.
