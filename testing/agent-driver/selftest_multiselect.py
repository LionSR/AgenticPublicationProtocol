"""Self-test for the multi-select (checkbox) AskUserQuestion path.

Forces a `multiSelect` question, toggles two specific options by label, tabs
to the Submit step, submits, and verifies the child registered both choices.

Run:  IS_SANDBOX=1 python3 selftest_multiselect.py
"""

import sys
import tempfile

from pty_agent import PtyAgent
from responder import Rule, Scenario, drive

PROMPT = (
    "Use the AskUserQuestion tool with multiSelect=true to ask which pizza "
    "toppings I want, options Cheese, Mushroom, Onion. Ask only that. After I "
    "answer, reply on its own line with exactly: TOPPINGS=<comma-separated "
    "sorted lowercase>."
)
WANT = ["Mushroom", "Onion"]


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="pty-msel-")
    transcript = tempfile.mktemp(prefix="pty-msel-", suffix=".log")
    agent = PtyAgent(cwd=workdir, transcript_path=transcript)
    with agent:
        agent.wait_for_menu(timeout=20)
        drive(agent, Scenario(rules=[]), max_turns=8, idle_turns_to_stop=2,
              on_event=print)
        agent.send_text(PROMPT)

        # Stop only on the answer-confirmation line, where the question text
        # and "→ <values>" appear on the SAME line (the menu renders them on
        # separate lines, so a per-line check avoids a false early stop).
        def answered(s: str) -> bool:
            for line in s.splitlines():
                low = line.lower()
                if "toppings do you want" in low and "→" in line \
                        and "comma-separated" not in low:
                    return True
            return False

        result = drive(
            agent,
            Scenario(rules=[
                Rule(["pizza toppings", "Submit"], multi_select=WANT,
                     name="toppings"),
                Rule(["pizza toppings", "[ ]"], multi_select=WANT,
                     name="toppings2"),
            ]),
            max_turns=40, idle_turns_to_stop=8, on_event=print,
            stop_when=answered,
        )

    # Verify the confirmation line lists exactly the wanted toppings.
    confirm = ""
    for line in result["final_screen"].splitlines():
        if "→" in line and ("mushroom" in line.lower() or "onion" in line.lower()
                             or "cheese" in line.lower()):
            confirm = line.lower()
    picked = confirm.split("→", 1)[-1] if "→" in confirm else ""
    ok = ("toppings" in result["fired"]
          and "mushroom" in picked and "onion" in picked
          and "cheese" not in picked)

    print("\n===== RESULT =====")
    print("fired:", result["fired"])
    print("confirmation line:", confirm.strip() or "(none)")
    print("\nMULTISELECT SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
