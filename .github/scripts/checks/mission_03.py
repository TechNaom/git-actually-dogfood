"""Mission 03 -- Handle a real merge conflict.

Checks for two things that only happen if a genuine conflict was
resolved by hand: a real (2+ parent) merge commit in main's history --
not just a fast-forward -- and CONFLICT_PRACTICE.md changed from its
seed content.
"""

from lib import git_inspect

SEED_MARKER = "Current status: not started."


def check(context: dict) -> tuple[bool, str]:
    if not git_inspect.any_merge_commit("origin/main"):
        return False, (
            "No real merge commit found on main yet. Create two branches that both "
            "edit the same line of CONFLICT_PRACTICE.md, merge the first cleanly, "
            "then merge the second -- git will report a conflict. Resolve it by "
            "hand, `git add` the file, and finish the merge with `git commit`."
        )

    if git_inspect.file_contains("CONFLICT_PRACTICE.md", SEED_MARKER):
        return False, (
            "Found a merge commit, but CONFLICT_PRACTICE.md still has its original "
            "seed text -- make sure the branches you merged actually changed it."
        )

    return True, "Real merge conflict, resolved by hand. On to Mission 04 -- opening a real PR."
