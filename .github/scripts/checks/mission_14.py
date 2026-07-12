"""Mission 14 -- Reusable workflow: ci.yml calls a real workflow_call workflow."""

import yaml


def check(context: dict) -> tuple[bool, str]:
    try:
        with open(".github/workflows/ci.yml", encoding="utf-8") as f:
            ci_data = yaml.safe_load(f)
    except FileNotFoundError:
        return False, "No .github/workflows/ci.yml found."

    jobs = ci_data.get("jobs", {})
    calls_reusable = any(
        isinstance(job, dict) and "reusable-lint-test.yml" in str(job.get("uses") or "")
        for job in jobs.values()
    )
    if not calls_reusable:
        return False, (
            "ci.yml doesn't call a reusable workflow yet. Create "
            ".github/workflows/reusable-lint-test.yml with `on: workflow_call`, move "
            "your lint+test steps into it, and call it from ci.yml with `uses:`."
        )

    try:
        with open(".github/workflows/reusable-lint-test.yml", encoding="utf-8") as f:
            reusable_data = yaml.safe_load(f)
    except FileNotFoundError:
        return False, "ci.yml references a reusable workflow file that doesn't exist yet."

    # PyYAML parses the bare `on:` key as the boolean True (a classic YAML 1.1
    # gotcha very relevant to Actions files) -- handle both forms.
    on_block = reusable_data.get(True, reusable_data.get("on", {})) or {}
    if "workflow_call" not in on_block:
        return False, "reusable-lint-test.yml exists but isn't triggered by `workflow_call`."

    return True, "ci.yml now calls a real reusable workflow. On to Mission 15 -- the capstone."
