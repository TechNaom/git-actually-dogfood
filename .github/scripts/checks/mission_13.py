"""Mission 13 -- Production deploy gate: a required reviewer, approved for real."""

from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]

    if not gh_api.environment_has_required_reviewer(repo, "production"):
        return False, (
            "'production' environment doesn't have a required reviewer configured "
            "yet. Add yourself as a required reviewer in Settings -> Environments."
        )

    deployments = list(repo.get_deployments(environment="production"))
    if not deployments:
        return False, (
            "No deployment to 'production' found yet. Push a change and approve the "
            "pending deployment when it appears on the Actions run."
        )

    latest = deployments[0]
    statuses = list(latest.get_statuses())
    if not statuses or statuses[0].state != "success":
        return False, (
            "Found a production deployment, but it hasn't succeeded yet -- did you "
            "approve it in the Actions run's 'Review deployments' button?"
        )

    return True, "Production deployment approved and live. On to Mission 14 -- a reusable workflow."
