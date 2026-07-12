"""Mission 04 -- Push & open a real PR.

Missions 01-03 merged straight to main (no PR needed for local git
practice). This mission starts a fresh cycle: a new branch, a new
change, and this time a real pull request using the repo's PR template.
"""

from lib import gh_api

REQUIRED_HEADERS = ["what changed", "why", "how to test"]


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    pr = gh_api.latest_pull(repo)

    if pr is None:
        return False, "No pull request found yet. Push a new branch and open a PR against main."

    body = (pr.body or "").lower()
    missing = [h for h in REQUIRED_HEADERS if h not in body]
    if missing:
        return False, (
            f"Found PR #{pr.number}, but its description is missing: {', '.join(missing)}. "
            "Use the PR template's sections (What changed / Why / How to test)."
        )

    context["state"]["pr_number"] = pr.number
    return True, (
        f"PR #{pr.number} opened with a real description. "
        "On to Mission 05 -- watching CI run on it."
    )
