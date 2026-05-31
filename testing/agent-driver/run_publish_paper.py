"""Drive `/publish-paper --mode dev-sandbox` against the toy-paper fixture.

This is the protocol-level integration test: it operates a child Claude Code
session through the PTY harness, invokes the real APP `publish-paper` skill in
developer-sandbox mode, and answers the publication interview with simulated
keyboard input — scripted where the decision points are known, autopilot +
canned free-text replies elsewhere.

Developer-sandbox mode is used on purpose: it exercises the same prepare and
validate standards as a real publication but creates no public repo and writes
no APP compliance records (see PROTOCOL.md and skills/publish-paper/SKILL.md).

Usage:
    IS_SANDBOX=1 python3 run_publish_paper.py [--minutes 8]

The run is time-boxed; the full six-phase workflow is long, so by default this
demonstrates that the harness loads the skill and answers the early interview
rounds, capturing a transcript for inspection. Increase --minutes to let it go
further.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time

from pty_agent import PtyAgent
from responder import Rule, Scenario, drive

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIXTURE = os.path.join(HERE, "fixtures", "toy-paper")


def setup_child_config() -> str:
    """Isolated CLAUDE_CONFIG_DIR with the APP plugin installed locally."""
    config_dir = tempfile.mkdtemp(prefix="publish-paper-config-")
    env = dict(os.environ, CLAUDE_CONFIG_DIR=config_dir)
    # Seed onboarding so interactive mode uses the managed provider, not login.
    import json
    json.dump({"hasCompletedOnboarding": True, "theme": "dark"},
              open(os.path.join(config_dir, ".claude.json"), "w"))
    for cmd in (
        ["claude", "plugin", "marketplace", "add", REPO_ROOT],
        ["claude", "plugin", "install", "paper-protocol@paper-protocol"],
    ):
        subprocess.run(cmd, env=env, check=True,
                       capture_output=True, text=True)
    print(f"plugin installed into {config_dir}")
    return config_dir


def setup_workdir() -> str:
    """Fresh copy of the fixture so the committed one is never mutated."""
    workdir = tempfile.mkdtemp(prefix="publish-paper-work-")
    dest = os.path.join(workdir, "toy-paper")
    shutil.copytree(FIXTURE, dest)
    # Make it a git repo, as a real working repo would be.
    subprocess.run(["git", "init", "-q"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
    # Disable commit signing: throwaway repo, and signing may be unavailable.
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "-c", "commit.gpgsign=false",
                    "commit", "-qm", "fixture"], cwd=dest, check=True)
    return dest


def build_scenario() -> Scenario:
    """Known decision points in the publish-paper interview.

    Wording is model-generated and may drift; anything not matched here is
    handled by autopilot. These rules just nudge the common choices.
    """
    return Scenario(rules=[
        # Decline editor/LSP/tooling install offers that interrupt the flow.
        Rule(["LSP"], select="No, not now", name="decline-lsp", once=False),
        Rule(["install", "lsp"], select="No, not now",
             name="decline-lsp2", once=False),
        # New publication rather than a revision of an existing release.
        Rule(["new", "revision"], select="new", name="new-vs-revision"),
        # Keep going past summaries/file lists shown for confirmation.
        Rule(["proceed"], select="proceed", name="proceed"),
        Rule(["looks good"], select="looks good", name="looks-good"),
        Rule(["continue"], select="continue", name="continue"),
        Rule(["approve"], select="approve", name="approve"),
        Rule(["yes"], select="yes", name="generic-yes", once=False),
    ])


def idle_replies() -> list[str]:
    """Free-text answers for open-ended interview questions, in rough order."""
    return [
        "This is a test fixture. The key result: the sum of the first N "
        "integers equals N(N+1)/2, verified numerically (exact agreement for "
        "N=1..100). Figure 1 is reproduced by src/generate_fig1.py using "
        "matplotlib. No datasets, no heavy compute. Use your best judgment "
        "and keep moving through the dev-sandbox workflow.",
        "Audience: people verifying the publication tooling. License: MIT for "
        "code, CC-BY for the manuscript. Include the manuscript, the figure, "
        "and the figure-reproduction script. Proceed.",
        "Looks good. Continue to the next phase.",
        "Yes, that is correct. Please proceed.",
        "Approved for the dev-sandbox run. Continue.",
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=8.0)
    args = ap.parse_args()

    if not shutil.which("claude"):
        print("claude CLI not found on PATH", file=sys.stderr)
        return 2

    config_dir = setup_child_config()
    workdir = setup_workdir()
    transcript = os.path.join(os.getcwd(), "publish_paper_transcript.bin")
    print(f"workdir={workdir}\nconfig={config_dir}\ntranscript(raw)={transcript}")

    deadline = time.time() + args.minutes * 60
    agent = PtyAgent(cwd=workdir, config_dir=config_dir,
                     transcript_path=transcript, timeout=int(args.minutes * 60) + 120)
    try:
        agent.start()
        # Clear startup menus and reach the prompt box.
        agent.wait_for_menu(timeout=25)
        drive(agent, Scenario(rules=[]), max_turns=8, idle_turns_to_stop=2,
              on_event=print)

        # Invoke the real skill in developer-sandbox mode.
        agent.send_text("/publish-paper --mode dev-sandbox")

        result = drive(
            agent, build_scenario(),
            max_turns=400, idle_turns_to_stop=10, turn_pump=2.5,
            autopilot=True, idle_replies=idle_replies(), idle_reply_after=3,
            on_event=print,
            stop_when=lambda s: time.time() > deadline
            or "implementation test result" in s.lower()
            or "phase 6 complete" in s.lower(),
        )
    finally:
        final = agent.screen_text()
        agent.close()
        shutil.rmtree(os.path.dirname(workdir), ignore_errors=True)
        shutil.rmtree(config_dir, ignore_errors=True)

    print("\n===== RUN SUMMARY =====")
    print("fired:", result["fired"])
    print("----- final screen -----")
    print("\n".join(final.splitlines()[-20:]))
    print(f"\nraw transcript: {transcript}")
    # Success here means "the harness drove the skill and answered prompts",
    # not "a publication was produced" — the run is time-boxed.
    drove = any(f for f in result["fired"]
                if f not in ("trust-folder", "bypass-accept"))
    print("\nHARNESS DROVE THE SKILL" if drove else "\nHARNESS DID NOT PROGRESS")
    return 0 if drove else 1


if __name__ == "__main__":
    sys.exit(main())
