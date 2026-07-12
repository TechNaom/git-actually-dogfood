"""Mission 08 -- Matrix builds: the test job runs across multiple Python versions."""

import yaml


def check(context: dict) -> tuple[bool, str]:
    try:
        with open(".github/workflows/ci.yml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return False, "No .github/workflows/ci.yml found."

    jobs = data.get("jobs", {})
    test_job = jobs.get("test")
    if not test_job:
        return False, "No 'test' job found in ci.yml."

    matrix = (test_job.get("strategy") or {}).get("matrix") or {}
    versions = matrix.get("python-version")
    if not versions or len(versions) < 2:
        return False, (
            "The 'test' job doesn't have a Python version matrix with at least 2 "
            "versions yet. Add a `strategy.matrix.python-version` list."
        )

    return True, (
        f"Test job runs across {len(versions)} Python versions: {versions}. On to Mission 09."
    )
