"""Mission 00 -- Setup: relnotes installs and its own CI passes."""

from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    sha = context["sha"]
    runs = gh_api.workflow_runs_for_sha(repo, sha, workflow_name="CI")

    if not runs:
        return False, (
            "No CI run found yet for this commit. Give it a few seconds and re-run "
            "this check (Actions tab -> Mission Check -> Run workflow), or push again."
        )

    run = runs[0]
    if run.status != "completed":
        return False, f"CI is still running ({run.status}). Check back shortly."
    if run.conclusion != "success":
        return False, (
            f"CI finished but didn't pass (conclusion: {run.conclusion}). "
            "Fix the failing job, commit, and push again."
        )

    return True, (
        "relnotes installs and its test suite passes in CI. Setup complete -- on to Mission 01."
    )
