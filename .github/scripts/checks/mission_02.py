"""Mission 02 -- Branch & merge: your Mission 01 branch is merged into main."""

from lib import git_inspect


def check(context: dict) -> tuple[bool, str]:
    branch = context["state"].get("feature_branch")
    if not branch:
        return False, "Complete Mission 01 first so I know which branch to look for."

    if not git_inspect.branch_exists(branch, remote=True):
        return False, f"'origin/{branch}' isn't on the remote (yet)."

    if not git_inspect.is_ancestor(f"origin/{branch}", "origin/main"):
        return False, (
            f"'{branch}' hasn't been merged into main yet. Merge it locally "
            "(fast-forward is fine here) and push main."
        )

    return True, f"'{branch}' is merged into main. On to Mission 03 -- a real merge conflict."
