"""
check_mission.py -- dispatcher for git-actually's mission checkers.

Run from mission-check.yml inside the learner's own repo. Reads the
current mission number from .mission-state.json on `main` (via the API,
never the local checkout -- a feature branch or PR may have forked
before the state file's last update, which would otherwise make
progress look reverted), runs that mission's check function against
real repo/API state, and reports pass/fail -- persisting progress back
to .mission-state.json and PROGRESS.md on `main` on a pass, and always
writing a job summary for immediate feedback in the Actions tab.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib import gh_api  # noqa: E402

STATE_PATH = ".mission-state.json"
PROGRESS_PATH = "PROGRESS.md"
TOTAL_MISSIONS = 16  # missions 00-15

MISSION_NAMES = {
    0: "Setup",
    1: "First real commit",
    2: "Branch & merge",
    3: "Handle a real merge conflict",
    4: "Push & open a real PR",
    5: "CI runs on your PR",
    6: "Real code review",
    7: "Merge & clean up",
    8: "Matrix builds",
    9: "Caching & a second check",
    10: "Build artifacts",
    11: "Environments & secrets",
    12: "Staging deploy gate",
    13: "Production deploy gate",
    14: "Reusable workflow",
    15: "Capstone: ship a real feature",
}


def load_state(repo) -> dict:
    content = gh_api.read_repo_file(repo, STATE_PATH, ref="main")
    if content is None:
        return {"current_mission": 0, "completed": []}
    return json.loads(content)


def save_state(repo, state: dict) -> None:
    content = json.dumps(state, indent=2, sort_keys=True) + "\n"
    gh_api.write_repo_file(repo, STATE_PATH, content, "mission-bot: update progress [skip ci]")


def update_progress_md(repo, state: dict) -> None:
    lines = ["# Progress", "", "Bot-updated -- don't hand-edit the checkmarks.", ""]
    for n in range(TOTAL_MISSIONS):
        mark = "x" if n in state["completed"] else " "
        lines.append(f"- [{mark}] Mission {n:02d}: {MISSION_NAMES[n]}")
    content = "\n".join(lines) + "\n"
    gh_api.write_repo_file(repo, PROGRESS_PATH, content, "mission-bot: update progress [skip ci]")


def run_checker(mission: int, context: dict) -> tuple[bool, str]:
    module = __import__(f"checks.mission_{mission:02d}", fromlist=["check"])
    return module.check(context)


def write_job_summary(mission: int, passed: bool, message: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    status = "PASSED" if passed else "NOT YET"
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(f"## Mission {mission:02d}: {MISSION_NAMES[mission]} -- {status}\n\n{message}\n")


MISSION_CONTROL_TITLE = "Mission Control"


def sync_mission_control_issue(repo, state: dict, mission: int, passed: bool, message: str) -> None:
    body_lines = [
        "This issue tracks your progress through git-actually. The bot edits it "
        "in place -- don't worry about it growing into a spam thread.",
        "",
        f"**Last checked:** Mission {mission:02d} -- {MISSION_NAMES[mission]} "
        f"-- {'PASSED' if passed else 'NOT YET'}",
        "",
        f"> {message}",
        "",
        "## Progress",
        "",
    ]
    for n in range(TOTAL_MISSIONS):
        mark = "x" if n in state["completed"] else " "
        body_lines.append(f"- [{mark}] Mission {n:02d}: {MISSION_NAMES[n]}")
    body = "\n".join(body_lines) + "\n"

    issues = repo.get_issues(state="open")
    existing = next((i for i in issues if i.title == MISSION_CONTROL_TITLE), None)

    if existing is None:
        repo.create_issue(title=MISSION_CONTROL_TITLE, body=body)
    else:
        existing.edit(body=body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", type=int, default=None)
    args = parser.parse_args()

    repo = gh_api.get_repo()
    state = load_state(repo)
    mission = args.mission if args.mission is not None else state["current_mission"]

    if mission >= TOTAL_MISSIONS:
        print("All missions complete.")
        return 0

    context = {
        "repo": repo,
        "sha": os.environ.get("GITHUB_SHA", ""),
        "ref": os.environ.get("GITHUB_REF", ""),
        "state": state,
    }

    passed, message = run_checker(mission, context)
    write_job_summary(mission, passed, message)
    print(f"Mission {mission:02d} ({MISSION_NAMES[mission]}): {'PASS' if passed else 'NOT YET'}")
    print(message)

    if passed:
        if mission not in state["completed"]:
            state["completed"].append(mission)
        state["current_mission"] = mission + 1

    save_state(repo, state)
    update_progress_md(repo, state)
    sync_mission_control_issue(repo, state, mission, passed, message)

    return 0


if __name__ == "__main__":
    sys.exit(main())
