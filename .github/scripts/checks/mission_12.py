"""Mission 12 -- Staging deploy gate.

Checks the deployment API's history for the 'staging' environment
(not the live site's current content) -- by the time a learner gets to
Mission 13, production may have already overwritten what's live.
"""


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    deployments = list(repo.get_deployments(environment="staging"))
    if not deployments:
        return False, (
            "No deployment to the 'staging' environment found yet. Wire up a "
            "deploy-staging job gated by the staging environment and push."
        )

    latest = deployments[0]
    statuses = list(latest.get_statuses())
    if not statuses or statuses[0].state != "success":
        return False, "Found a staging deployment, but it hasn't succeeded yet."

    return True, "A real deployment to staging succeeded. On to Mission 13 -- the production gate."
