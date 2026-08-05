#!/usr/bin/env python3
"""Discussion-list bot helper for APP papers.

Given a free-form comment (+ optional Copilot JSON), verify candidate releases
and propose:
  - an updated Discussion body (append next numbered entry), and/or
  - a reply to the commenter.

The Discussion body is the list of record for now (no registry PR).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any

GITHUB_API = "https://api.github.com"
USER_AGENT = "app-discussion-bot/1.0"
PROTOCOL = "agentic-publication-protocol"


def http_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {body[:400]}") from e


def http_bytes(url: str, token: str | None = None) -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/octet-stream"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} for {url}: {body[:400]}") from e


def extract_json(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {}
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else {}
    except json.JSONDecodeError:
        pass
    a, b = text.find("{"), text.rfind("}")
    if a >= 0 and b > a:
        try:
            obj = json.loads(text[a : b + 1])
            return obj if isinstance(obj, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def parse_ref(text: str) -> tuple[str, str] | None:
    text = text.strip().strip("<>")
    patterns = [
        r"https?://github\.com/([^/]+)/([^/]+)/releases/tag/([^/\s#?]+)",
        r"https?://github\.com/([^/]+)/([^/]+)/releases/download/([^/\s#?]+)/",
        r"https?://github\.com/([^/]+)/([^/\s#?]+)/tree/([^/\s#?]+)",
        r"https?://github\.com/([^/]+)/([^/\s#?]+)/?$",
    ]
    for i, pat in enumerate(patterns):
        m = re.search(pat, text)
        if not m:
            continue
        owner, repo = m.group(1), m.group(2).removesuffix(".git")
        if i < 3:
            return f"{owner}/{repo}", m.group(3)
        return f"{owner}/{repo}", ""
    m = re.match(r"^([^/\s]+)/([^/\s@]+)(?:@|\s+)(v?[0-9][\w.\-]*)$", text)
    if m:
        return f"{m.group(1)}/{m.group(2)}", m.group(3)
    return None


def candidates_from_parsed(parsed: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for c in parsed.get("candidates") or []:
        if not isinstance(c, dict):
            continue
        target = (
            (c.get("release_url") or c.get("repo_url") or c.get("owner_repo") or "")
            .strip()
        )
        tag = (c.get("tag") or "").strip()
        if not target:
            continue
        # Prefer structured fields over string-smashing so full release URLs parse cleanly.
        if tag and not re.search(r"/releases/tag/", target):
            ref = parse_ref(target)
            if ref:
                out.append((ref[0], tag or ref[1]))
                continue
        ref = parse_ref(target)
        if not ref:
            continue
        owner_repo, parsed_tag = ref
        out.append((owner_repo, tag or parsed_tag))
    return out


def candidates_from_comment(comment: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for m in re.finditer(r"https?://github\.com/[^\s<>)\]\"']+", comment or ""):
        ref = parse_ref(m.group(0).rstrip(".,;"))
        if ref and ref[1]:
            out.append(ref)
    return out


def resolve_commit_tree(owner_repo: str, tag: str, token: str | None) -> tuple[str, str]:
    ref = http_json(f"{GITHUB_API}/repos/{owner_repo}/git/ref/tags/{tag}", token)
    obj = ref["object"]
    if obj["type"] == "tag":
        tag_obj = http_json(
            f"{GITHUB_API}/repos/{owner_repo}/git/tags/{obj['sha']}", token
        )
        commit_sha = tag_obj["object"]["sha"]
    else:
        commit_sha = obj["sha"]
    commit = http_json(
        f"{GITHUB_API}/repos/{owner_repo}/git/commits/{commit_sha}", token
    )
    return commit_sha, commit["tree"]["sha"]


def download_manifest(owner_repo: str, tag: str, token: str | None) -> dict[str, Any]:
    release = http_json(f"{GITHUB_API}/repos/{owner_repo}/releases/tags/{tag}", token)
    for a in release.get("assets") or []:
        if a.get("name") == "APP_PUBLICATION.json":
            url = a.get("browser_download_url") or a.get("url")
            return json.loads(http_bytes(url, token).decode("utf-8"))
    raise RuntimeError(f"No APP_PUBLICATION.json on {owner_repo}@{tag}")


def normalize_id(value: str) -> str:
    value = value.strip()
    if value.startswith("app-v1:sha256:"):
        return value
    if re.fullmatch(r"[0-9a-f]{64}", value):
        return f"app-v1:sha256:{value}"
    return value


def recompute_id(manifest: dict[str, Any]) -> str:
    payload = dict(manifest)
    payload.pop("app_publication_id", None)
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return "app-v1:sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


def fetch_agents_bits(owner_repo: str, tag: str, token: str | None) -> dict[str, Any]:
    url = f"https://raw.githubusercontent.com/{owner_repo}/{tag}/AGENTS.md"
    try:
        text = http_bytes(url, token).decode("utf-8", errors="replace")
    except Exception:
        return {}
    meta: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm, body = parts[1], parts[2]
            for key in ("title", "domain", "arxiv_id"):
                m = re.search(rf"^{key}:\s*[\"']?(.*?)[\"']?\s*$", fm, re.M)
                if m and m.group(1).strip():
                    meta[key] = m.group(1).strip()
            authors = []
            for block in re.split(r"\n\s*-\s+name:\s*", fm)[1:]:
                nm = re.match(r"[\"']?(.*?)[\"']?\s*(?:\n|$)", block)
                am = re.search(r"affiliation:\s*[\"']?(.*?)[\"']?\s*(?:\n|$)", block)
                if nm:
                    authors.append(
                        {
                            "name": nm.group(1).strip(),
                            "affiliation": am.group(1).strip() if am else "",
                        }
                    )
            if authors:
                meta["authors"] = authors
            tm = re.search(r"^tags:\s*\[(.*?)\]\s*$", fm, re.M | re.S)
            if tm:
                meta["tags"] = [
                    t.strip().strip("\"'")
                    for t in tm.group(1).split(",")
                    if t.strip()
                ]
            sm = re.search(
                r"##\s*Paper Summary\s*\n+(.*?)(?=\n##\s|\Z)", body, re.S | re.I
            )
            if sm:
                meta["summary"] = sm.group(1).strip()
    return meta


def verify(owner_repo: str, tag: str, token: str | None) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest = download_manifest(owner_repo, tag, token)
        commit, tree = resolve_commit_tree(owner_repo, tag, token)
    except Exception as e:
        return {"ok": False, "errors": [str(e)]}

    if manifest.get("protocol") != PROTOCOL:
        errors.append(f"protocol is {manifest.get('protocol')!r}")
    pub = manifest.get("publication_type")
    if pub is not None and pub != "app-publication":
        errors.append(f"publication_type is {pub!r}")
    expected_repo = f"https://github.com/{owner_repo}"
    m_repo = str(manifest.get("repo_url", "")).rstrip("/").removesuffix(".git")
    if m_repo != expected_repo:
        errors.append(f"repo_url mismatch ({m_repo})")
    if manifest.get("tag") != tag:
        errors.append("tag mismatch")
    if manifest.get("commit") != commit:
        errors.append("commit mismatch")
    if manifest.get("tree") != tree:
        errors.append("tree mismatch")
    val = manifest.get("validation") or {}
    if val.get("stage") != "full" or val.get("result") != "passed":
        errors.append("validation not full/passed")
    ha = manifest.get("human_approval") or {}
    if ha.get("approved") is not True:
        errors.append("not human-approved")
    mid = normalize_id(str(manifest.get("app_publication_id", "")))
    if mid != recompute_id(manifest):
        errors.append("app_publication_id recompute failed")

    if errors:
        return {"ok": False, "errors": errors, "owner_repo": owner_repo, "tag": tag}

    agents = fetch_agents_bits(owner_repo, tag, token)
    return {
        "ok": True,
        "errors": [],
        "owner_repo": owner_repo,
        "tag": tag,
        "app_publication_id": mid,
        "release_url": f"https://github.com/{owner_repo}/releases/tag/{tag}",
        "title": agents.get("title") or manifest.get("title") or owner_repo,
        "authors": agents.get("authors")
        or [
            {"name": a, "affiliation": ""}
            for a in (manifest.get("authors") or [])
            if isinstance(a, str)
        ],
        "field": agents.get("domain"),
        "arxiv_id": agents.get("arxiv_id") or manifest.get("arxiv_id"),
        "tags": agents.get("tags") or [],
        "summary": agents.get("summary") or "",
    }


def format_authors(authors: list[Any]) -> str:
    bits = []
    for a in authors:
        if isinstance(a, dict):
            name = a.get("name", "")
            aff = a.get("affiliation") or ""
            bits.append(f"**{name}**" + (f" ({aff})" if aff else ""))
        else:
            bits.append(f"**{a}**")
    # Discussion style for multi-author: "A, B (shared aff)" sometimes; keep one per line if affs differ
    if len(bits) == 1:
        return bits[0]
    # If same affiliation, compact
    if all(isinstance(a, dict) for a in authors):
        affs = {(a.get("affiliation") or "") for a in authors}
        if len(affs) == 1 and next(iter(affs)):
            names = ", ".join(a.get("name", "") for a in authors)
            return f"**{names}** ({next(iter(affs))})"
    return "\n".join(bits)


def format_entry(n: int, paper: dict[str, Any]) -> str:
    lines = [f"### {n}. {paper['title']}", ""]
    if paper.get("authors"):
        lines.append(format_authors(paper["authors"]))
        lines.append("")
    meta = []
    if paper.get("arxiv_id"):
        aid = paper["arxiv_id"]
        meta.append(f"arXiv: [{aid}](https://arxiv.org/abs/{aid})")
    if paper.get("field"):
        meta.append(f"Field: `{paper['field']}`")
    meta.append(f"Release: [{paper['tag']}]({paper['release_url']})")
    if paper.get("tags"):
        meta.append("Tags: " + ", ".join(paper["tags"]))
    lines.append("\n".join(meta))
    lines.append("")
    if paper.get("summary"):
        lines.append(paper["summary"].strip())
        lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def next_index(body: str) -> int:
    nums = [int(x) for x in re.findall(r"^###\s+(\d+)\.", body, re.M)]
    return (max(nums) + 1) if nums else 1


def already_listed(body: str, owner_repo: str, tag: str, pub_id: str) -> bool:
    """Prefer release URL match; avoid false positives from a shared tag like v1.0.0."""
    body_l = body.lower()
    release = f"github.com/{owner_repo.lower()}/releases/tag/{tag.lower()}"
    if release in body_l:
        return True
    # Also match without scheme/host variants already normalized above
    if f"{owner_repo.lower()}/releases/tag/{tag.lower()}" in body_l:
        return True
    if pub_id and pub_id in body:
        return True
    return False


def insert_entry(body: str, entry_md: str) -> str:
    footer = (
        "Published a paper with APP? Reply with the link to your release "
        "and we will add it here."
    )
    idx = body.find(footer)
    if idx >= 0:
        return body[:idx] + entry_md + body[idx:]
    return body.rstrip() + "\n\n" + entry_md


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--comment-file", type=argparse.FileType("r"), required=True)
    ap.add_argument("--parsed-file", type=argparse.FileType("r"))
    ap.add_argument("--discussion-body-file", type=argparse.FileType("r"), required=True)
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    ap.add_argument("--out", type=argparse.FileType("w"), default=sys.stdout)
    args = ap.parse_args()

    comment = args.comment_file.read()
    parsed = extract_json(args.parsed_file.read() if args.parsed_file else "")
    body = args.discussion_body_file.read()

    msg = (parsed.get("message") or parsed.get("ask_clarification") or "").strip()
    cands = candidates_from_parsed(parsed)
    # Always allow a plain release URL if Copilot missed it
    if not cands:
        cands = candidates_from_comment(comment)

    action = (parsed.get("action") or "").strip()
    if not action:
        intent = parsed.get("intent") or ""
        action = {
            "submit_paper": "submit",
            "question": "question",
            "not_relevant": "ignore",
            "unclear": "question",
        }.get(intent, "")
    if not action:
        action = "submit" if cands else "ignore"
    # URL present ⇒ treat as submit even if model said ignore
    if cands and action == "ignore":
        action = "submit"

    # Dedupe keys
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for owner_repo, tag in cands:
        key = f"{owner_repo.lower()}@{tag}"
        if key not in seen:
            seen.add(key)
            unique.append((owner_repo, tag))

    results: list[dict[str, Any]] = []
    new_body = body
    added: list[dict[str, Any]] = []
    replies: list[str] = []

    if action == "ignore" and not unique:
        out = {
            "should_update": False,
            "should_reply": False,
            "reply": "",
            "new_body": body,
            "results": [],
            "action": "ignore",
        }
        json.dump(out, args.out, indent=2, ensure_ascii=False)
        args.out.write("\n")
        return 0

    if action == "question" and not unique:
        out = {
            "should_update": False,
            "should_reply": True,
            "reply": msg
            or (
                "Please share a public GitHub Release URL for the APP paper "
                "(e.g. https://github.com/org/repo/releases/tag/v1.0.0)."
            ),
            "new_body": body,
            "results": [],
            "action": "question",
        }
        json.dump(out, args.out, indent=2, ensure_ascii=False)
        args.out.write("\n")
        return 0

    if not unique:
        out = {
            "should_update": False,
            "should_reply": True,
            "reply": msg
            or (
                "I couldn't find a GitHub release link in your comment. "
                "Please include something like "
                "https://github.com/org/repo/releases/tag/v1.0.0."
            ),
            "new_body": body,
            "results": [],
            "action": action or "submit",
        }
        json.dump(out, args.out, indent=2, ensure_ascii=False)
        args.out.write("\n")
        return 0

    for owner_repo, tag in unique:
        vr = verify(owner_repo, tag, args.token)
        results.append(vr)
        if not vr["ok"]:
            replies.append(
                f"**{owner_repo}@{tag}**: not added — "
                + "; ".join(vr.get("errors") or ["verification failed"])
            )
            continue
        if already_listed(new_body, owner_repo, tag, vr.get("app_publication_id", "")):
            replies.append(
                f"**{owner_repo}@{tag}**: already on the list — thanks!"
            )
            continue
        n = next_index(new_body)
        entry = format_entry(n, vr)
        new_body = insert_entry(new_body, entry)
        added.append(vr)
        replies.append(
            f"**{owner_repo}@{tag}**: verified APP publication — added as **#{n}** "
            f"({vr.get('title')})."
        )

    if msg and action == "question":
        replies.insert(0, msg)

    out = {
        "should_update": len(added) > 0,
        "should_reply": True,
        "reply": "\n\n".join(replies) if replies else "No action taken.",
        "new_body": new_body,
        "added_count": len(added),
        "results": results,
        "action": action,
    }
    json.dump(out, args.out, indent=2, ensure_ascii=False)
    args.out.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
