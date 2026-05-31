"""End-to-end self-test of the PTY harness.

Drives a child Claude Code session, forces it to ask an `AskUserQuestion`
multiple-choice question, answers it by simulated keyboard navigation, and
verifies the child registered the chosen answer. This proves the core
mechanism (operating another agent and answering its questions, including
multiple choice) independently of the publish-paper protocol.

Run:  IS_SANDBOX=1 python3 selftest_color.py
Exits non-zero on failure.
"""

import sys
import tempfile

from pty_agent import PtyAgent
from responder import Rule, Scenario, drive

PROMPT = (
    "Use the AskUserQuestion tool right now to ask me exactly one question: "
    "my favorite color, with options Red, Green, and Blue. Do nothing else "
    "first. After I answer, reply on its own line with exactly: PICKED=<color>."
)
CHOICE = "Green"


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="pty-selftest-")
    transcript = tempfile.mktemp(prefix="pty-selftest-", suffix=".log")
    print(f"workdir={workdir}\ntranscript(raw)={transcript}")

    agent = PtyAgent(cwd=workdir, transcript_path=transcript)
    with agent:
        # Clear any startup menus, then reach the prompt box.
        agent.wait_for_menu(timeout=20)
        scenario_startup = Scenario(rules=[])
        drive(agent, scenario_startup, max_turns=8, idle_turns_to_stop=2,
              on_event=print)

        # Ask the child to pose the multiple-choice question.
        agent.send_text(PROMPT)

        scenario = Scenario(rules=[
            Rule(["favorite color", "Green"], select=CHOICE, name="pick-color"),
        ])
        result = drive(
            agent, scenario, max_turns=40, idle_turns_to_stop=6,
            on_event=print,
            stop_when=lambda s: f"PICKED={CHOICE}" in s,
        )

    final = result["final_screen"]
    ok_fired = "pick-color" in result["fired"]
    ok_ack = f"PICKED={CHOICE}".lower() in final.lower() or CHOICE.lower() in final.lower()

    print("\n===== RESULT =====")
    print("fired rules :", result["fired"])
    print("picked acked:", ok_ack)
    print("----- final screen tail -----")
    print("\n".join(final.splitlines()[-12:]))

    if ok_fired and ok_ack:
        print("\nSELFTEST PASS")
        return 0
    print("\nSELFTEST FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
