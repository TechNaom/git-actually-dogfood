"""Mission 10 -- Build artifacts: a needs-gated build job that uploads one."""

import yaml
from lib import gh_api


def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]

    try:
        with open(".github/workflows/ci.yml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return False, "No .github/workflows/ci.yml found."

    jobs = data.get("jobs", {})
    build_job = jobs.get("build")
    if not build_job:
        return False, "No 'build' job found in ci.yml yet."

    if not build_job.get("needs"):
        return False, "'build' job exists but doesn't `needs:` the test job(s) yet."

    artifacts = gh_api.latest_artifacts(repo)
    if not artifacts:
        return False, "No workflow artifacts found yet. Push to main and let the build job run."

    return True, (
        f"Build job runs after tests and uploads an artifact ({artifacts[0]}). On to Mission 11."
    )
