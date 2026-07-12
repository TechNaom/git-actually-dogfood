"""
git_inspect.py -- local git state introspection for mission checkers.

Every function shells out to a real `git` command against the checked-out
repo (mission-check.yml runs actions/checkout@v4 with fetch-depth: 0
first, so full history is available). Nothing here is mocked -- these
functions report exactly what a learner's real repo looks like.
"""

from __future__ import annotations

import subprocess


class GitInspectError(Exception):
    """Raised when a git command fails unexpectedly (not just returns non-zero)."""


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise GitInspectError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def current_branch() -> str:
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def branch_exists(name: str, remote: bool = True) -> bool:
    ref = f"refs/remotes/origin/{name}" if remote else f"refs/heads/{name}"
    result = subprocess.run(["git", "show-ref", "--verify", "--quiet", ref])
    return result.returncode == 0


def commit_count(ref: str = "HEAD", since_ref: str | None = None) -> int:
    rev_range = f"{since_ref}..{ref}" if since_ref else ref
    output = run_git("rev-list", "--count", rev_range)
    return int(output)


def commit_messages(ref: str = "HEAD", n: int = 20) -> list[str]:
    output = run_git("log", f"-{n}", "--pretty=%s", ref, check=False)
    return output.splitlines() if output else []


def is_ancestor(maybe_ancestor: str, ref: str) -> bool:
    result = subprocess.run(["git", "merge-base", "--is-ancestor", maybe_ancestor, ref])
    return result.returncode == 0


def has_merge_commit(ref: str = "HEAD", since_ref: str = "origin/main") -> bool:
    rev_range = f"{since_ref}..{ref}"
    output = run_git("log", "--merges", "--pretty=%H", rev_range, check=False)
    return bool(output.strip())


def any_merge_commit(ref: str = "origin/main") -> bool:
    """True if `ref`'s history contains at least one real (2+ parent) merge commit."""
    output = run_git("log", "--merges", "--pretty=%H", "-1", ref, check=False)
    return bool(output.strip())


def remote_branches(exclude: tuple[str, ...] = ("origin/main", "origin/HEAD")) -> list[str]:
    """List remote branch names (without the 'origin/' prefix), excluding main/HEAD."""
    output = run_git("branch", "-r", check=False)
    names = []
    for line in output.splitlines():
        name = line.strip()
        if not name or "->" in name:
            continue
        if name in exclude:
            continue
        names.append(name.removeprefix("origin/"))
    return names


def file_contains(path: str, substring: str) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            return substring in f.read()
    except FileNotFoundError:
        return False


def yaml_file_contains_key_path(path: str, *key_path: str) -> bool:
    """
    Check a YAML file (e.g. a workflow) has a nested key path, e.g.
    yaml_file_contains_key_path("ci.yml", "jobs", "test", "strategy", "matrix").
    """
    import yaml

    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError):
        return False

    node = data
    for key in key_path:
        if not isinstance(node, dict) or key not in node:
            return False
        node = node[key]
    return True
