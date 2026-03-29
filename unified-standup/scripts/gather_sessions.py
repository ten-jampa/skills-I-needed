#!/usr/bin/env python3
"""
gather_sessions.py - Extract today's activity from Claude and Codex sessions.

Usage:
    python3 gather_sessions.py [--date YYYY-MM-DD]

Output: Markdown summary of all activity for the given day, printed to stdout.
"""

import argparse
import json
import os
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today)")
    return parser.parse_args()


def get_target_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return datetime.now().date()


# ── Claude sessions ──────────────────────────────────────────────────────────

def gather_claude_activity(target_date):
    """Read ~/.claude/history.jsonl and return prompts for target_date grouped by project."""
    history_path = Path.home() / ".claude" / "history.jsonl"
    if not history_path.exists():
        return {}

    projects = defaultdict(list)
    with open(history_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Timestamp is epoch milliseconds
            ts = entry.get("timestamp", 0)
            entry_date = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).date()
            if entry_date != target_date:
                continue

            project = entry.get("project", "unknown")
            display = entry.get("display", "").strip()
            if display:
                projects[project].append(display)

    return dict(projects)


# ── Codex sessions ────────────────────────────────────────────────────────────

def extract_codex_user_messages(session_file):
    """Extract user messages from a Codex JSONL session file."""
    messages = []
    cwd = None
    with open(session_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            payload = entry.get("payload", {})

            if entry_type == "session_meta" and isinstance(payload, dict):
                cwd = payload.get("cwd")

            elif entry_type == "response_item" and isinstance(payload, dict):
                role = payload.get("role")
                content = payload.get("content", [])
                if role == "user" and isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "input_text":
                            text = block.get("text", "").strip()
                            # Skip system-injected pseudo-user messages
                            SKIP_PREFIXES = (
                                "# AGENTS.md", "<INSTRUCTIONS>", "<environment_context>",
                                "<turn_aborted>", "<subagent_notification>", "<user_shell_command>",
                                "<skill>", "<SYSTEM>",
                                # Subagent orchestration instructions
                                "You are researching Phase", "Plan Phase", "Review the Phase",
                                "Execute Phase", "Review the current", "Give a concise implementation",
                            )
                            if text and not any(text.startswith(p) for p in SKIP_PREFIXES):
                                messages.append(text)

    return cwd, messages


def gather_codex_activity(target_date):
    """Return Codex activity for target_date grouped by cwd."""
    year = target_date.strftime("%Y")
    month = target_date.strftime("%m")
    day = target_date.strftime("%d")
    sessions_dir = Path.home() / ".codex" / "sessions" / year / month / day

    if not sessions_dir.exists():
        return {}

    # Track seen messages per project to deduplicate (subagents re-inject full history)
    projects = defaultdict(list)
    seen = defaultdict(set)

    for session_file in sorted(sessions_dir.glob("*.jsonl")):
        try:
            cwd, messages = extract_codex_user_messages(session_file)
        except Exception:
            continue
        key = cwd or str(session_file.stem)
        for msg in messages:
            if msg not in seen[key]:
                seen[key].add(msg)
                projects[key].append(msg)

    return dict(projects)


# ── Git commits ───────────────────────────────────────────────────────────────

def get_git_commits_for_date(repo_path, target_date):
    """Return list of commit summaries from a git repo for the target date."""
    date_str = target_date.strftime("%Y-%m-%d")
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--no-merges",
             f"--after={date_str} 00:00:00",
             f"--before={date_str} 23:59:59",
             "--author-date-is-committer-date"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return lines
    except Exception:
        return []


def find_git_repos_from_projects(all_project_paths):
    """Given a set of directory paths, find which are (or are in) git repos."""
    repos = set()
    for path_str in all_project_paths:
        p = Path(path_str)
        # Walk up to find .git
        current = p
        for _ in range(5):
            if (current / ".git").exists():
                repos.add(str(current))
                break
            if current.parent == current:
                break
            current = current.parent
    return repos


def gather_git_activity(project_paths, target_date):
    """Return dict of repo -> [commits] for all repos touched today."""
    repos = find_git_repos_from_projects(project_paths)
    result = {}
    for repo in repos:
        commits = get_git_commits_for_date(repo, target_date)
        if commits:
            result[repo] = commits
    return result


# ── PROGRESS.md ───────────────────────────────────────────────────────────────

def read_progress_files(project_paths):
    """Find and read PROGRESS.md files in any project worked on today."""
    found = {}
    for path_str in project_paths:
        p = Path(path_str) / "PROGRESS.md"
        if p.exists():
            try:
                content = p.read_text().strip()
                if content:
                    found[path_str] = content[:2000]  # cap length
            except Exception:
                pass
    return found


# ── Formatting ────────────────────────────────────────────────────────────────

def format_output(target_date, claude_activity, codex_activity, git_activity, progress_files):
    lines = [f"# Raw Activity for {target_date}\n"]

    # Claude
    lines.append("## Claude Code Sessions\n")
    if claude_activity:
        for project, prompts in claude_activity.items():
            proj_name = Path(project).name if project != "unknown" else "unknown"
            lines.append(f"### {proj_name} (`{project}`)")
            for p in prompts:
                snippet = p.replace("\n", " ")[:200]
                lines.append(f"- {snippet}")
            lines.append("")
    else:
        lines.append("_No Claude sessions found._\n")

    # Codex
    lines.append("## Codex Sessions\n")
    if codex_activity:
        for project, prompts in codex_activity.items():
            proj_name = Path(project).name if project else "unknown"
            lines.append(f"### {proj_name} (`{project}`)")
            for p in prompts:
                snippet = p.replace("\n", " ")[:200]
                lines.append(f"- {snippet}")
            lines.append("")
    else:
        lines.append("_No Codex sessions found._\n")

    # Git
    lines.append("## Git Commits\n")
    if git_activity:
        for repo, commits in git_activity.items():
            repo_name = Path(repo).name
            lines.append(f"### {repo_name} (`{repo}`)")
            for c in commits:
                lines.append(f"- {c}")
            lines.append("")
    else:
        lines.append("_No commits found._\n")

    # PROGRESS.md
    if progress_files:
        lines.append("## PROGRESS.md Files\n")
        for path, content in progress_files.items():
            lines.append(f"### {Path(path).name}")
            lines.append(content)
            lines.append("")

    return "\n".join(lines)


def main():
    args = parse_args()
    target_date = get_target_date(args.date)

    claude_activity = gather_claude_activity(target_date)
    codex_activity = gather_codex_activity(target_date)

    # Collect all project paths for git + PROGRESS.md lookup
    all_projects = set(claude_activity.keys()) | set(codex_activity.keys())

    git_activity = gather_git_activity(all_projects, target_date)
    progress_files = read_progress_files(all_projects)

    output = format_output(target_date, claude_activity, codex_activity, git_activity, progress_files)
    print(output)


if __name__ == "__main__":
    main()
