"""Mission 15 -- Capstone: ship a real feature end-to-end, unassisted.

A composite check: a fresh merged PR (not the one from Missions 04-07),
issue-linked, branch cleaned up. Some parts of the capstone (commit
message quality, review depth, the honest retrospective) are
inherently human-judged -- see missions/15-capstone.md's checklist.
"""

from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    prior_pr = context["state"].get("pr_number")

    merged_prs = [pr for pr in gh_api.all_pulls(repo) if pr.merged and pr.number != prior_pr]
    if not merged_prs:
        return False, (
            "No new merged PR found yet beyond the one from Missions 04-07. The "
            "capstone is a full, fresh loop: issue -> branch -> commits -> PR -> "
            "CI green -> review -> merge -> staging -> approved production -> cleanup."
        )

    pr = merged_prs[0]
    body = (pr.body or "").lower()
    if "closes #" not in body and "fixes #" not in body:
        return False, f"PR #{pr.number} is merged, but doesn't reference a 'Closes #N' issue."

    try:
        repo.get_git_ref(f"heads/{pr.head.ref}")
        branch_cleaned_up = False
    except Exception:
        branch_cleaned_up = True

    if not branch_cleaned_up:
        return False, f"PR #{pr.number} merged, but branch '{pr.head.ref}' wasn't cleaned up."

    return True, (
        f"Capstone complete: PR #{pr.number} shipped a real feature end-to-end, "
        "issue-linked, reviewed, merged, and cleaned up. Self-score against the "
        "checklist in missions/15-capstone.md -- that part's on you to judge honestly."
    )
