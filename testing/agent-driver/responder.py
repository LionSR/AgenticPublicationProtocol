"""Scenario-driven responder: answer an agent's prompts from a script.

A scenario is an ordered list of rules. On each turn the driver renders the
screen and, if a menu is present, picks the first rule whose trigger text is
on screen and applies its answer (select an option by label, type text, or
press a key). Startup menus (folder-trust, bypass acceptance) are handled by
built-in default rules so scenarios only describe the interesting choices.

This keeps the "what would a human answer" logic declarative and separate
from the PTY mechanics in `pty_agent.py`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

from pty_agent import KEY_ENTER, PtyAgent


@dataclass
class Rule:
    """When `triggers` all appear on screen, apply `answer`."""

    triggers: list[str]
    # Exactly one of these describes the answer:
    select: str | None = None          # menu option label to choose
    multi_select: list[str] | None = None  # checkbox labels to toggle on + submit
    type_text: str | None = None       # text to type into the prompt box
    key: bytes | None = None           # raw key to send
    once: bool = True                  # fire at most once
    name: str = ""

    _fired: bool = field(default=False, init=False)

    def matches(self, screen_text: str) -> bool:
        if self.once and self._fired:
            return False
        return all(t.lower() in screen_text.lower() for t in self.triggers)

    def apply(self, agent: PtyAgent) -> str:
        self._fired = True
        if self.multi_select is not None:
            agent.answer_multiselect(self.multi_select)
            return f"multi-selected {self.multi_select!r}"
        if self.select is not None:
            agent.select(self.select)
            return f"selected {self.select!r}"
        if self.type_text is not None:
            agent.send_text(self.type_text)
            return f"typed {self.type_text!r}"
        if self.key is not None:
            agent.send_key(self.key)
            return f"sent key {self.key!r}"
        return "no-op"


DEFAULT_STARTUP_RULES = [
    Rule(["trust this folder"], select="Yes, I trust this folder",
         once=False, name="trust-folder"),
    Rule(["Bypass Permissions mode", "Yes, I accept"], select="Yes, I accept",
         once=False, name="bypass-accept"),
]


@dataclass
class Scenario:
    rules: list[Rule]
    include_startup_defaults: bool = True

    def all_rules(self) -> list[Rule]:
        if self.include_startup_defaults:
            return [*DEFAULT_STARTUP_RULES, *self.rules]
        return list(self.rules)


# Labels an autopilot must never auto-select (destructive / negative defaults).
_UNSAFE = ("exit", "cancel", "no,", "quit", "abort", "discard", "reject",
           "don't", "do not", "skip", "delete")


def _safe_autopilot_index(options) -> int | None:
    """Index of the first option that is not destructive or a meta-action."""
    for i, o in enumerate(options):
        low = o.label.lower()
        if any(bad in low for bad in _UNSAFE):
            continue
        if low.startswith("type something") or low.startswith("chat about"):
            continue
        return i
    return None


def drive(
    agent: PtyAgent,
    scenario: Scenario,
    *,
    max_turns: int = 80,
    idle_turns_to_stop: int = 6,
    turn_pump: float = 2.0,
    on_event: Callable[[str], None] | None = None,
    stop_when: Callable[[str], bool] | None = None,
    autopilot: bool = False,
    idle_replies: list[str] | None = None,
    idle_reply_after: int = 3,
) -> dict:
    """Run the scenario against the agent until it stalls or `stop_when` hits.

    Beyond the scripted rules:

    * ``autopilot`` — on a menu with no matching rule, select the first
      non-destructive option instead of stopping. Useful for smoke-testing a
      long workflow where not every prompt is known in advance.
    * ``idle_replies`` — canned free-text answers, sent one at a time when the
      agent has been waiting at an empty prompt box (no menu) for
      ``idle_reply_after`` turns. Mimics a human answering an open-ended
      interview question.

    Returns a summary dict with the fired rules and the final screen text.
    """
    rules = scenario.all_rules()
    pending_replies = list(idle_replies or [])
    log: list[str] = []
    fired: list[str] = []

    def emit(msg: str):
        log.append(msg)
        if on_event:
            on_event(msg)

    idle = 0
    prev_sig = None
    for turn in range(max_turns):
        agent._pump(turn_pump)
        if not agent.alive():
            emit(f"[turn {turn}] agent exited")
            break

        screen = agent.screen_text()
        if stop_when and stop_when(screen):
            emit(f"[turn {turn}] stop condition met")
            break

        # Is the agent actively producing output? Compare the screen minus the
        # bottom status/footer rows (which animate even when idle). Only a
        # stable screen with no menu means the agent is waiting for us.
        sig = "\n".join(screen.splitlines()[:-2])
        screen_changed = sig != prev_sig
        prev_sig = sig

        acted = False
        if agent.has_menu():
            for rule in rules:
                if not rule.matches(screen):
                    continue
                try:
                    result = rule.apply(agent)
                except (LookupError, RuntimeError) as exc:
                    # Trigger text matched but the option isn't selectable here
                    # (absent, or a wrapped label the cursor can't land on).
                    # Let autopilot or a later rule handle it; never crash.
                    rule._fired = False
                    emit(f"[turn {turn}] rule '{rule.name}' skipped: {exc}")
                    continue
                label = rule.name or (rule.select or rule.type_text or "key")
                emit(f"[turn {turn}] rule '{label}': {result}")
                fired.append(rule.name or label)
                acted = True
                idle = 0
                break
            if not acted:
                opts, _ = agent.parse_menu()
                if autopilot:
                    try:
                        if agent.is_multiselect():
                            # Toggle a default choice and submit, rather than
                            # looping forever toggling the same checkbox.
                            ok = agent.answer_multiselect(None)
                            emit(f"[turn {turn}] AUTOPILOT multi-select submit "
                                 f"(ok={ok}) from {[o.label for o in opts]}")
                            if ok:
                                fired.append("autopilot:multiselect")
                                acted = True
                                idle = 0
                        else:
                            idx = _safe_autopilot_index(opts)
                            if idx is not None:
                                agent.select_index(idx)
                                emit(f"[turn {turn}] AUTOPILOT chose "
                                     f"'{opts[idx].label}' (#{idx+1}) "
                                     f"from {[o.label for o in opts]}")
                                fired.append(f"autopilot:{opts[idx].label[:30]}")
                                acted = True
                                idle = 0
                    except (LookupError, RuntimeError) as exc:
                        emit(f"[turn {turn}] AUTOPILOT could not act: {exc}")
                if not acted:
                    emit(f"[turn {turn}] UNHANDLED MENU: {[o.label for o in opts]}")
                    idle += 1
        elif screen_changed:
            # Agent is still streaming output; wait, don't interrupt.
            idle = 0
        else:
            idle += 1
            # Stable screen, no menu: the agent is waiting for free-text input.
            if idle >= idle_reply_after and pending_replies:
                reply = pending_replies.pop(0)
                agent.send_text(reply)
                emit(f"[turn {turn}] idle-reply: {reply!r}")
                fired.append("idle-reply")
                idle = 0
                acted = True

        if idle >= idle_turns_to_stop:
            emit(f"[turn {turn}] idle for {idle} turns; stopping")
            break
        time.sleep(0.4)

    return {
        "fired": fired,
        "log": log,
        "final_screen": agent.screen_text(),
        "alive": agent.alive(),
        "unsent_replies": pending_replies,
    }
