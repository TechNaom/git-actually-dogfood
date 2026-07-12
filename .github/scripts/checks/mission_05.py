"""Mission 05 -- CI runs on your PR (fix a red check)."""

from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    pr_number = context["state"].get("pr_number")
    if not pr_number:
        return False, "Complete Mission 04 first."

    pr = repo.get_pull(pr_number)
    head_sha = pr.head.sha
    runs = gh_api.workflow_runs_for_sha(repo, head_sha, workflow_name="CI")

    if not runs:
        return False, "No CI run found yet for your PR's latest commit. Give it a minute."

    run = runs[0]
    if run.status != "completed":
        return False, f"CI is still running on PR #{pr_number} ({run.status})."
    if run.conclusion != "success":
        return False, (
            f"CI failed on PR #{pr_number} (conclusion: {run.conclusion}). Open the "
            "Checks tab on your PR, fix what's red, commit, and push -- watch the PR update."
        )

    return True, f"CI is green on PR #{pr_number}. On to Mission 06 -- a real code review."
