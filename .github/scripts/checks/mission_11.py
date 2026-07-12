"""Mission 11 -- Environments & secrets: a real staging environment with a secret."""

from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]

    if not gh_api.environment_exists(repo, "staging"):
        return False, (
            "No 'staging' environment found yet. Create one in Settings -> "
            "Environments, then add a secret to it (e.g. RELEASE_TOKEN)."
        )

    if not gh_api.environment_has_secret(repo, "staging", "RELEASE_TOKEN"):
        return False, "'staging' environment exists, but has no RELEASE_TOKEN secret yet."

    return True, (
        "'staging' environment exists with a real secret. On to Mission 12 -- deploying to it."
    )
