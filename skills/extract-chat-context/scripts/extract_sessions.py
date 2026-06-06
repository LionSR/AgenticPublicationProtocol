"""Extract conversation sessions from Claude Code and Codex CLI history.

Reads session logs from:
  - Claude Code: ~/.claude/projects/<project-key>/*.jsonl
      where <project-key> is the working-directory path with '/' replaced by '-'.
  - Codex CLI:   ~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl
      (archived sessions live under ~/.codex/archived_sessions; pass
       --sessions-root ~/.codex/archived_sessions to read those.)

Both Codex on-disk formats are supported: the current 'session_meta'/'response_item'
layout and the legacy top-level 'message' layout.

By default 'list' is scoped to the current working directory (Claude by project key,
Codex by the directory each session recorded). Use --project all to list every
session, or --project <path-or-key> to target a specific one.

Usage:
  python extract_sessions.py list --source claude [--project all|<key>]
  python extract_sessions.py list --source codex  [--project all|<path>]
  python extract_sessions.py extract --source claude --session <id>
  python extract_sessions.py extract --source codex  --session <id>

Based on the approach from QuantumBFS/sci-brain (MIT license).
"""
import argparse
import json
import re
import sys
from pathlib import Path


def _extract_text(content):
    """Extract human-readable text from message.content (string or array)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") in ("text", "input_text", "output_text"):
                parts.append(block.get("text", ""))
        return "\n".join(parts).strip()
    return ""


_SYSTEM_TAGS = (
    "system-reminder", "environment_context", "command-message",
    "command-name", "INSTRUCTIONS", "instructions", "user_instructions",
    "user-prompt-submit-hook", "context",
)


def _strip_system_tags(text):
    """Remove known XML-style system tags from text."""
    result = text
    for tag in _SYSTEM_TAGS:
        result = re.sub(rf"<{tag}>.*?</{tag}>", "", result, flags=re.DOTALL)
    return result.strip()


def _is_system_preamble(text):
    """Check if text is entirely system/environment tags with no real user content."""
    stripped = _strip_system_tags(text)
    if len(stripped) == 0:
        return True
    if re.match(r"^# (AGENTS|CLAUDE|GEMINI)\.md\b", stripped):
        return True
    return False


def _truncate(text, max_chars=500):
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def _cwd_to_project_key(cwd):
    """Convert filesystem path to Claude's project directory key format."""
    return cwd.replace("/", "-")


# --- Claude Code ---

def list_claude_sessions(projects_root, project_filter=None):
    root = Path(projects_root)
    if not root.exists():
        return []

    sessions = []
    if project_filter:
        project_dirs = [root / project_filter] if (root / project_filter).is_dir() else []
    else:
        project_dirs = [p for p in root.iterdir() if p.is_dir()]

    for project_dir in project_dirs:
        for jsonl_file in project_dir.glob("*.jsonl"):
            if jsonl_file.parent != project_dir:
                continue
            session_id = jsonl_file.stem
            timestamp = None
            preview = ""
            try:
                with jsonl_file.open() as f:
                    for raw in f:
                        raw = raw.strip()
                        if not raw:
                            continue
                        try:
                            rec = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        if rec.get("type") == "user":
                            text = _extract_text(rec.get("message", {}).get("content", ""))
                            if text and not _is_system_preamble(text):
                                if timestamp is None:
                                    timestamp = rec.get("timestamp", "")
                                preview = " ".join(text.split())[:80]
                                break
                        if timestamp is None:
                            timestamp = rec.get("timestamp", "")
            except OSError:
                continue
            sessions.append({
                "session_id": session_id,
                "project": project_dir.name,
                "timestamp": timestamp or "",
                "preview": preview,
                "path": str(jsonl_file),
            })

    sessions.sort(key=lambda s: s["timestamp"], reverse=True)
    return sessions


def extract_claude_turns(lines):
    records = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") not in ("user", "assistant"):
            continue
        msg = rec.get("message", {})
        if "content" not in msg:
            continue
        text = _extract_text(msg["content"])
        if text:
            records.append({"role": rec["type"], "text": text})

    turns = []
    idx = 0
    i = 0
    while i < len(records):
        r = records[i]
        if r["role"] == "user":
            if _is_system_preamble(r["text"]):
                i += 1
                continue
            user_text = _strip_system_tags(r["text"]) or r["text"]
            assistant_parts = []
            i += 1
            while i < len(records) and records[i]["role"] == "assistant":
                assistant_parts.append(records[i]["text"])
                i += 1
            idx += 1
            assistant_text = "\n".join(assistant_parts) if assistant_parts else "[no response]"
            turns.append({
                "index": idx,
                "user": user_text,
                "assistant": _truncate(assistant_text),
            })
        else:
            i += 1
    return turns


# --- Codex CLI ---
#
# Codex has two on-disk session formats:
#   Format A (legacy): a header record {id, timestamp, instructions, git} with no
#     "type", followed by top-level message records {type:"message", role, content}.
#     The working directory is not stored directly; it appears inside an injected
#     <environment_context> user message, and the repo URL is in the header's "git".
#   Format B (current): a {type:"session_meta", payload:{cwd, git, ...}} header,
#     followed by {type:"response_item", payload:{type:"message", role, content}}.

# The working directory appears inside an injected environment_context message as
# either prose ("Current working directory: /path") or an XML tag (<cwd>/path</cwd>).
_CWD_RE = re.compile(r"Current working directory:\s*(.+)")
_CWD_TAG_RE = re.compile(r"<cwd>(.*?)</cwd>", re.DOTALL)


def _cwd_from_text(text):
    """Best-effort working directory parsed from an environment_context message."""
    if not text:
        return None
    m = _CWD_RE.search(text) or _CWD_TAG_RE.search(text)
    return m.group(1).strip() if m else None


def _codex_role_content(rec):
    """Return (role, content) for a Codex message record, spanning both formats."""
    if rec.get("type") == "response_item":           # Format B
        payload = rec.get("payload") or {}
        return payload.get("role"), payload.get("content")
    if rec.get("type") == "message":                 # Format A
        return rec.get("role"), rec.get("content")
    return None, None


def _codex_header_location(rec):
    """Extract (cwd, repo_url) hints from a Codex header/meta record, if present."""
    if rec.get("type") == "session_meta":            # Format B
        payload = rec.get("payload") or {}
        return payload.get("cwd"), (payload.get("git") or {}).get("repository_url")
    if "type" not in rec and "instructions" in rec:  # Format A header
        return None, (rec.get("git") or {}).get("repository_url")
    return None, None


def _codex_location(lines):
    """Best-effort (cwd, repo_url) for the directory a Codex session ran in."""
    cwd = repo = None
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(rec, dict):
            continue
        if cwd is None or repo is None:
            h_cwd, h_repo = _codex_header_location(rec)
            cwd = cwd or h_cwd
            repo = repo or h_repo
        if cwd is None:
            role, content = _codex_role_content(rec)
            if role == "user":
                cwd = _cwd_from_text(_extract_text(content))
        if cwd and repo:
            break
    return cwd, repo


def list_codex_sessions(sessions_root, cwd_filter=None):
    root = Path(sessions_root)
    if not root.exists():
        return []

    sessions = []
    for jsonl_file in root.rglob("rollout-*.jsonl"):
        session_id = jsonl_file.stem
        timestamp = None
        preview = ""
        cwd = repo = None
        try:
            with jsonl_file.open() as f:
                for raw in f:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        rec = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(rec, dict):
                        continue
                    if timestamp is None:
                        timestamp = rec.get("timestamp", "")
                    if cwd is None or repo is None:
                        h_cwd, h_repo = _codex_header_location(rec)
                        cwd = cwd or h_cwd
                        repo = repo or h_repo
                    role, content = _codex_role_content(rec)
                    if role == "user":
                        text = _extract_text(content)
                        if cwd is None:
                            cwd = _cwd_from_text(text)
                        if text and not _is_system_preamble(text):
                            preview = " ".join(text.split())[:80]
                            break
        except OSError:
            continue

        if cwd_filter and cwd_filter != "all":
            target = cwd_filter.rstrip("/")
            if not (cwd and (cwd == target or cwd.startswith(target + "/"))):
                continue

        sessions.append({
            "session_id": session_id,
            "timestamp": timestamp or "",
            "preview": preview,
            "cwd": cwd or "",
            "repo": repo or "",
            "path": str(jsonl_file),
        })

    sessions.sort(key=lambda s: s["timestamp"], reverse=True)
    return sessions


def extract_codex_turns(lines):
    records = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(rec, dict):
            continue
        role, content = _codex_role_content(rec)
        if role not in ("user", "assistant"):
            continue
        text = _extract_text(content)
        if not text or (role == "user" and _is_system_preamble(text)):
            continue
        records.append({"role": role, "text": text})

    turns = []
    idx = 0
    i = 0
    while i < len(records):
        r = records[i]
        if r["role"] == "user":
            user_text = _strip_system_tags(r["text"]) or r["text"]
            assistant_parts = []
            i += 1
            while i < len(records) and records[i]["role"] == "assistant":
                assistant_parts.append(records[i]["text"])
                i += 1
            idx += 1
            assistant_text = "\n".join(assistant_parts) if assistant_parts else "[no response]"
            turns.append({
                "index": idx,
                "user": user_text,
                "assistant": _truncate(assistant_text),
            })
        else:
            i += 1
    return turns


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Extract dialog from Claude Code and Codex sessions")
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List available sessions")
    list_p.add_argument("--source", choices=["claude", "codex"], required=True)
    list_p.add_argument(
        "--project",
        help="Scope the list. Default: the current working directory "
             "(Claude by project key, Codex by each session's recorded directory). "
             "Use 'all' for every session, or target a specific repo "
             "(Codex: a directory path; Claude: the dash-encoded project key).",
    )
    list_p.add_argument("--projects-root", default=str(Path.home() / ".claude" / "projects"))
    list_p.add_argument("--sessions-root", default=str(Path.home() / ".codex" / "sessions"))

    ext_p = sub.add_parser("extract", help="Extract dialog from a session")
    ext_p.add_argument("--source", choices=["claude", "codex"], required=True)
    ext_p.add_argument("--session", required=True, help="Session ID")
    ext_p.add_argument("--projects-root", default=str(Path.home() / ".claude" / "projects"))
    ext_p.add_argument("--sessions-root", default=str(Path.home() / ".codex" / "sessions"))

    args = parser.parse_args()

    if args.command == "list":
        if args.source == "claude":
            project_filter = None if (args.project == "all") else (args.project or _cwd_to_project_key(str(Path.cwd())))
            sessions = list_claude_sessions(args.projects_root, project_filter=project_filter)
        else:
            cwd_filter = None if (args.project == "all") else (args.project or str(Path.cwd()))
            sessions = list_codex_sessions(args.sessions_root, cwd_filter=cwd_filter)

        for i, s in enumerate(sessions, 1):
            ts = s["timestamp"][:16].replace("T", " ") if s.get("timestamp") else "unknown"
            if args.source == "codex":
                loc = s.get("cwd") or s.get("repo") or "?"
                loc = loc.rstrip("/").split("/")[-1].replace(".git", "") or loc
                print(f'[{i}] {ts} | {loc} | {s["session_id"]} | "{s.get("preview", "")}"')
            else:
                print(f'[{i}] {ts} | {s["session_id"]} | "{s.get("preview", "")}"')

        if args.source == "codex" and not sessions and args.project != "all":
            scope = args.project or str(Path.cwd())
            print(
                f"# No Codex sessions found for {scope}. Run with --project all "
                f"to list every session, or --project <path> to target the repo where "
                f"the research happened.",
                file=sys.stderr,
            )

    elif args.command == "extract":
        session_file = None
        timestamp = None

        if args.source == "claude":
            for candidate in Path(args.projects_root).rglob(f"{args.session}.jsonl"):
                if "subagents" not in candidate.parts:
                    session_file = candidate
                    break
        else:
            for candidate in Path(args.sessions_root).rglob("*.jsonl"):
                if args.session in candidate.stem:
                    session_file = candidate
                    break

        if session_file is None:
            print(f"Session '{args.session}' not found.", file=sys.stderr)
            sys.exit(1)

        with session_file.open() as f:
            lines = f.readlines()

        for raw in lines:
            raw = raw.strip()
            if not raw:
                continue
            try:
                timestamp = json.loads(raw).get("timestamp", "")
                break
            except json.JSONDecodeError:
                continue

        if args.source == "claude":
            turns = extract_claude_turns(lines)
            project = session_file.parent.name
        else:
            turns = extract_codex_turns(lines)
            cwd, repo = _codex_location(lines)
            project = cwd or repo or ""

        json.dump({
            "source": args.source,
            "session_id": args.session,
            "project": project,
            "timestamp": timestamp or "",
            "turns": turns,
        }, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
