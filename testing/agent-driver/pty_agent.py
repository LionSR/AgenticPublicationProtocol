"""Drive an interactive Claude Code session through a pseudo-terminal.

The harness launches `claude` inside a real PTY, renders the TUI with a
terminal emulator (`pyte`), and reacts to whatever is on screen the way a
human would: typing into the prompt box and answering interactive menus —
including `AskUserQuestion` multiple-choice prompts — with simulated
keyboard input (arrow keys + Enter).

This is the mechanism the protocol-testing scenarios build on: it lets one
agent operate another agent end to end, so the questions a human would
normally answer in a `publish-paper` interview can be answered by a script.

Empirical notes (Claude Code v2.1.x interactive TUI), gathered by probing a
live session, that this module depends on:

* Menus render one option per line as ``❯ 1. Label`` for the highlighted row
  and ``  2. Label`` for the others. The ``❯`` cursor glyph appears *before*
  the number, so option parsing must tolerate a leading cursor/indent.
* The highlighted option is the one whose line contains ``❯``. Selection is
  done by moving the cursor with Up/Down and pressing Enter — pressing a
  number key is not relied upon.
* NEVER press Enter on a menu without first confirming the cursor is on the
  intended label. Some menus (e.g. the bypass-permissions warning) default
  the cursor to a destructive option such as "No, exit".
* Startup menus (folder-trust, bypass-permissions acceptance) appear
  *conditionally* depending on prior state, so they are handled reactively
  rather than as a fixed sequence.
* Auth: a child `claude` authenticates through the managed-host provider
  even with an isolated ``CLAUDE_CONFIG_DIR``, as long as onboarding is
  marked complete in that config. Interactive mode otherwise shows a login
  screen. Running as root in a sandbox requires ``IS_SANDBOX=1`` for
  ``--permission-mode bypassPermissions``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import time
from dataclasses import dataclass, field

import pexpect
import pyte

# Key sequences for the TUI.
KEY_DOWN = b"\x1b[B"
KEY_UP = b"\x1b[A"
KEY_ENTER = b"\r"
KEY_ESC = b"\x1b"
KEY_TAB = b"\t"

# A menu option line, with an optional leading cursor glyph before the number.
# Examples that must match:  "❯ 1. Red"  "  2. Green"  "❯ 1. No, exit"
_OPTION_RE = re.compile(r"^[\s❯>›*]*?(?P<num>\d+)\.\s+(?P<label>\S.*)$")


_CHECKBOX_RE = re.compile(r"^\[(?P<mark>.)\]\s*(?P<text>.*)$")


@dataclass
class Option:
    num: int
    label: str
    current: bool  # is the cursor (❯) on this row?

    @property
    def checkbox(self) -> bool:
        """True if this option is a multi-select checkbox like ``[ ] Foo``."""
        return bool(_CHECKBOX_RE.match(self.label))

    @property
    def checked(self) -> bool:
        m = _CHECKBOX_RE.match(self.label)
        return bool(m) and m.group("mark").strip() not in ("", " ")

    @property
    def text(self) -> str:
        """Label with any checkbox prefix stripped, for content matching."""
        m = _CHECKBOX_RE.match(self.label)
        return m.group("text").strip() if m else self.label


@dataclass
class PtyAgent:
    """A live interactive `claude` session behind a PTY."""

    cwd: str
    rows: int = 40
    cols: int = 120
    timeout: int = 240
    permission_mode: str = "bypassPermissions"
    transcript_path: str | None = None
    extra_args: list[str] = field(default_factory=list)
    config_dir: str | None = None  # isolated CLAUDE_CONFIG_DIR; created if None

    _child: pexpect.spawn = field(init=False, default=None)
    _raw_path: str = field(init=False, default=None)
    _owns_config_dir: bool = field(init=False, default=False)

    # ---- lifecycle -------------------------------------------------------

    def start(self) -> "PtyAgent":
        env = dict(os.environ)
        env["TERM"] = "xterm-256color"
        # Required so a root user in a sandbox may use bypassPermissions.
        env.setdefault("IS_SANDBOX", "1")

        if self.config_dir is None:
            self.config_dir = tempfile.mkdtemp(prefix="pty-agent-config-")
            self._owns_config_dir = True
        self._seed_config(self.config_dir)
        env["CLAUDE_CONFIG_DIR"] = self.config_dir

        self._raw_path = self.transcript_path or tempfile.mktemp(
            prefix="pty-agent-raw-", suffix=".bin"
        )
        args = ["--permission-mode", self.permission_mode, *self.extra_args]
        self._child = pexpect.spawn(
            "claude",
            args=args,
            cwd=self.cwd,
            env=env,
            encoding=None,  # bytes; the TUI emits raw ANSI
            dimensions=(self.rows, self.cols),
            timeout=self.timeout,
        )
        self._child.logfile_read = open(self._raw_path, "wb")
        return self

    @staticmethod
    def _seed_config(config_dir: str) -> None:
        """Mark onboarding complete so interactive mode skips the login UI."""
        os.makedirs(config_dir, exist_ok=True)
        cfg_path = os.path.join(config_dir, ".claude.json")
        cfg = {}
        if os.path.exists(cfg_path):
            try:
                cfg = json.load(open(cfg_path))
            except Exception:
                cfg = {}
        cfg.setdefault("hasCompletedOnboarding", True)
        cfg.setdefault("theme", "dark")
        json.dump(cfg, open(cfg_path, "w"))

    def close(self) -> None:
        if self._child is not None and self._child.isalive():
            try:
                self._child.sendcontrol("c")
                time.sleep(0.3)
                self._child.terminate(force=True)
            except Exception:
                pass
        try:
            self._child.logfile_read.close()
        except Exception:
            pass
        if self._owns_config_dir and self.config_dir:
            shutil.rmtree(self.config_dir, ignore_errors=True)

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.close()

    # ---- low-level IO ----------------------------------------------------

    def _pump(self, seconds: float) -> bool:
        """Read everything the TUI emits for `seconds`. False on EOF."""
        end = time.time() + seconds
        while time.time() < end:
            try:
                self._child.read_nonblocking(size=65536, timeout=0.3)
            except pexpect.TIMEOUT:
                pass
            except pexpect.EOF:
                return False
        return True

    def alive(self) -> bool:
        return self._child is not None and self._child.isalive()

    def screen(self) -> list[str]:
        """Render the current terminal viewport as a list of text rows."""
        s = pyte.Screen(self.cols, self.rows)
        stream = pyte.ByteStream(s)
        self._child.logfile_read.flush()
        with open(self._raw_path, "rb") as f:
            stream.feed(f.read())
        return [line.rstrip() for line in s.display]

    def screen_text(self) -> str:
        return "\n".join(line for line in self.screen() if line.strip())

    def send_text(self, text: str, enter: bool = True, pace: float = 0.02) -> None:
        """Type text into the prompt box (optionally submitting with Enter)."""
        self._child.send(text.encode())
        time.sleep(max(pace * len(text), 0.3))
        self._pump(0.4)
        if enter:
            self._child.send(KEY_ENTER)
            self._pump(0.4)

    def send_key(self, key: bytes) -> None:
        self._child.send(key)
        self._pump(0.25)

    # ---- menu handling ---------------------------------------------------

    def parse_menu(self) -> tuple[list[Option], int | None]:
        """Parse the numbered-option menu currently on screen.

        Returns (options, cursor_index). cursor_index is the position in the
        returned list whose row carries the ``❯`` cursor, or None.
        """
        options: list[Option] = []
        for line in self.screen():
            stripped = line.strip()
            m = _OPTION_RE.match(stripped)
            if not m:
                continue
            options.append(
                Option(
                    num=int(m.group("num")),
                    label=m.group("label").strip(),
                    current="❯" in line,
                )
            )
        cursor = next((i for i, o in enumerate(options) if o.current), None)
        return options, cursor

    def wait_for_menu(self, timeout: float = 30.0, stable: float = 0.8):
        """Wait until a numbered menu is on screen and has stopped changing."""
        deadline = time.time() + timeout
        last = None
        last_change = time.time()
        while time.time() < deadline:
            self._pump(0.3)
            options, cursor = self.parse_menu()
            sig = tuple((o.num, o.label, o.current) for o in options)
            if options and sig == last:
                if time.time() - last_change >= stable:
                    return options, cursor
            else:
                last = sig
                last_change = time.time()
        return self.parse_menu()

    @staticmethod
    def _norm(s: str) -> str:
        # Drop a trailing ellipsis (the TUI truncates long labels) and collapse
        # whitespace / non-breaking spaces so matching survives re-rendering.
        s = s.lower().replace("\xa0", " ").strip()
        for tail in ("…", "..."):
            if s.endswith(tail):
                s = s[: -len(tail)].strip()
        return " ".join(s.split())

    def _find_option(self, options: list[Option], want: str) -> int | None:
        w = self._norm(want)
        candidates = [(i, self._norm(o.text), self._norm(o.label))
                      for i, o in enumerate(options)]
        # Exact, then prefix-either-way (handles truncation), then substring.
        for matcher in (
            lambda v: v == w,
            lambda v: bool(v) and (v.startswith(w) or w.startswith(v)) and
            min(len(v), len(w)) >= 4,
            lambda v: w in v,
        ):
            for i, text, label in candidates:
                if matcher(text) or matcher(label):
                    return i
        return None

    def goto(self, want: str, max_steps: int = 20) -> int:
        """Position the menu cursor on the option matching `want`.

        Returns the option index. Navigates one row at a time, re-reading the
        cursor after each key so it self-corrects, and never presses Enter —
        callers decide whether to confirm (single-select) or toggle (checkbox).
        """
        options, cursor = self.wait_for_menu()
        target = self._find_option(options, want)
        if target is None:
            raise LookupError(
                f"option matching {want!r} not found; on screen: "
                f"{[o.label for o in options]}"
            )
        if cursor is None:
            cursor = 0
        steps = 0
        while cursor != target and steps < max_steps:
            self.send_key(KEY_DOWN if target > cursor else KEY_UP)
            steps += 1
            options, cursor = self.parse_menu()
            new_target = self._find_option(options, want)
            if new_target is not None:
                target = new_target
            if cursor is None:
                cursor = 0
        if cursor != target:
            raise RuntimeError(
                f"could not place cursor on {want!r} after {steps} steps"
            )
        return target

    def goto_index(self, target: int, max_steps: int = 20) -> int:
        """Position the cursor on option position `target` (0-based).

        Navigates by re-reading the ``❯`` cursor each step, so it is robust to
        label truncation/wrapping — useful when the *position* is known but the
        label text is too long to match reliably.
        """
        options, cursor = self.wait_for_menu()
        if not options:
            raise RuntimeError("no menu on screen")
        target = max(0, min(target, len(options) - 1))
        if cursor is None:
            cursor = 0
        steps = 0
        while cursor != target and steps < max_steps:
            self.send_key(KEY_DOWN if target > cursor else KEY_UP)
            steps += 1
            _, cursor = self.parse_menu()
            if cursor is None:
                cursor = 0
        if cursor != target:
            raise RuntimeError(f"could not place cursor on index {target}")
        return target

    def select(self, want: str, settle_after: float = 4.0, max_steps: int = 20) -> bool:
        """Move the cursor onto the option matching `want` and press Enter.

        For single-select menus this confirms the choice. Refuses to confirm a
        wrong (possibly destructive) default because it verifies the cursor is
        on the target before pressing Enter.
        """
        self.goto(want, max_steps=max_steps)
        self.send_key(KEY_ENTER)
        self._pump(settle_after)
        return True

    def select_index(self, target: int, settle_after: float = 4.0) -> bool:
        """Select the option at position `target` (0-based) by cursor nav."""
        self.goto_index(target)
        self.send_key(KEY_ENTER)
        self._pump(settle_after)
        return True

    def is_multiselect(self) -> bool:
        """True if the current menu is a checkbox (multi-select) question."""
        options, _ = self.parse_menu()
        return any(o.checkbox for o in options)

    def answer_multiselect(
        self,
        wanted: list[str] | None = None,
        max_tabs: int = 8,
        settle_after: float = 4.0,
    ) -> bool:
        """Answer a (possibly multi-question) multi-select AskUserQuestion.

        For each checkbox question tab: toggle the desired options on (Enter),
        then press Tab to advance. On the review/Submit tab, choose
        "Submit answers". If `wanted` is None, ensures at least one box per
        question is checked (picks the first non-meta option) so the form can
        be submitted — useful for autopilot smoke tests.
        """
        for _ in range(max_tabs):
            options, _ = self.wait_for_menu()
            # Reached the review/submit step?
            if any("submit answers" in o.text.lower() for o in options):
                self.select("Submit answers", settle_after=settle_after)
                return True
            if not any(o.checkbox for o in options):
                # Not a checkbox tab and no submit option: bail to caller.
                return False

            targets = self._desired_checkboxes(options, wanted)
            for label in targets:
                idx = self.goto(label)
                opts_now, _ = self.parse_menu()
                if 0 <= idx < len(opts_now) and not opts_now[idx].checked:
                    self.send_key(KEY_ENTER)  # toggle on
            self.send_key(KEY_TAB)  # advance to next question / submit
            self._pump(1.5)
        return False

    @staticmethod
    def _desired_checkboxes(options: list[Option], wanted: list[str] | None):
        meta = ("type something", "chat about", "submit", "cancel")
        real = [o for o in options if o.checkbox
                and not any(m in o.text.lower() for m in meta)]
        if wanted:
            chosen = []
            for w in wanted:
                for o in real:
                    if w.lower() in o.text.lower():
                        chosen.append(o.label)
            if chosen:
                return chosen
        # Default: first real option, so the form has a valid answer.
        return [real[0].label] if real else []

    # ---- waiting on output ----------------------------------------------

    def wait_for_text(self, needle: str, timeout: float = 60.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            self._pump(0.5)
            if needle in self.screen_text():
                return True
            if not self.alive():
                return needle in self.screen_text()
        return False

    def has_menu(self) -> bool:
        options, _ = self.parse_menu()
        return len(options) >= 2
