"""Mission 07 -- Merge & clean up: PR merged, branch deleted on GitHub."""


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    pr_number = context["state"].get("pr_number")
    if not pr_number:
        return False, "Complete Missions 04-06 first."

    pr = repo.get_pull(pr_number)
    if not pr.merged:
        return False, f"PR #{pr_number} isn't merged yet."

    branch = pr.head.ref
    try:
        repo.get_git_ref(f"heads/{branch}")
        branch_still_exists = True
    except Exception:
        branch_still_exists = False

    if branch_still_exists:
        return False, (
            f"PR #{pr_number} is merged, but '{branch}' still exists on GitHub. "
            f"Delete it: `git push origin --delete {branch}` (or the Delete branch "
            "button on the PR page)."
        )

    return True, f"PR #{pr_number} merged and branch cleaned up. On to Mission 08 -- matrix builds."
