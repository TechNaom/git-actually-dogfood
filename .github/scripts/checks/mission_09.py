"""Mission 09 -- Caching & a second check: pip caching plus a third CI job."""

import yaml


def _has_pip_cache_step(steps: list) -> bool:
    for step in steps or []:
        if str(step.get("uses", "")).startswith("actions/setup-python"):
            if (step.get("with") or {}).get("cache") == "pip":
                return True
    return False


def check(context: dict) -> tuple[bool, str]:
    try:
        with open(".github/workflows/ci.yml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return False, "No .github/workflows/ci.yml found."

    jobs = data.get("jobs", {})
    has_cache = any(_has_pip_cache_step(job.get("steps")) for job in jobs.values())

    # A later mission (14) may have moved lint+test into a reusable
    # workflow -- check there too so this stays correct regardless of
    # whether that's happened yet.
    if not has_cache:
        try:
            with open(".github/workflows/reusable-lint-test.yml", encoding="utf-8") as f:
                reusable_data = yaml.safe_load(f)
            for job in (reusable_data.get("jobs") or {}).values():
                if _has_pip_cache_step(job.get("steps")):
                    has_cache = True
        except FileNotFoundError:
            pass

    if not has_cache:
        return False, 'No pip caching found yet. Add `cache: "pip"` to a setup-python step.'

    if len(jobs) < 3:
        return False, (
            f"Only {len(jobs)} job(s) found (lint, test). Add a third job for a "
            "second check -- e.g. mypy or black --check."
        )

    return True, (
        f"Caching enabled and {len(jobs)} jobs running. On to Mission 10 -- build artifacts."
    )

