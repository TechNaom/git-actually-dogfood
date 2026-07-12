# Contributing to git-actually

This is for people improving **this repo** (the template itself) — if
you're working through the missions in your own copy, see `GUIDE.md`
and `missions/` instead; this file isn't for you.

## Project layout

- `src/relnotes/` — the practice app learners branch/PR against
- `tests/` — its test suite
- `missions/` — the 16 mission instruction docs
- `.github/scripts/` — the mission checker (`check_mission.py`,
  `checks/mission_NN.py`, `lib/git_inspect.py`, `lib/gh_api.py`)
- `.github/workflows/` — `ci.yml` and `deploy-pages.yml` (the pipeline
  learners extend across missions) plus `mission-check.yml` (the checker
  dispatcher, which only runs in *templated copies*, not this repo
  itself — see its `if:` guard)

## Working on the practice app

Standard Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -v
ruff check .
```

Keep `relnotes` genuinely small — its whole job is to have a few honest,
fillable gaps for missions to target, not to be feature-complete.

## Working on a mission checker

Each `checks/mission_NN.py` exports one function:
`check(context: dict) -> tuple[bool, str]`, where `context` has `repo`
(a PyGithub `Repository`), `sha`, `ref`, and `state` (the persisted
`.mission-state.json` dict — checkers may write extra keys into it, e.g.
`state["feature_branch"]`, for later missions to read).

When changing a checker, test it against real state, not just by
reading the code:

```bash
GITHUB_TOKEN=$(gh auth token) GITHUB_REPOSITORY="<owner>/<repo>" \
  python3 -c "
import sys; sys.path.insert(0, '.github/scripts')
from lib import gh_api
import importlib
repo = gh_api.get_repo()
mod = importlib.import_module('checks.mission_NN')
print(mod.check({'repo': repo, 'sha': '', 'ref': '', 'state': {}}))
"
```

Test both the pass and fail path against real repo state where
possible — a checker that only ever returns `True` isn't actually
checking anything.

## Changing the CI/CD pipeline missions cover

If you change the "solved" shape of `ci.yml` or `deploy-pages.yml`
(the target state missions 08-14 build toward), re-verify the whole
chain works live on a real repo before updating the mission docs —
GitHub Environments, Pages, and required-reviewer approvals can't be
fully verified any other way (no local Actions runner reproduces them
faithfully).

## Style

Match the existing tone in `missions/*.md`: concrete commands, a short
"what's checked" section, and a short "if it doesn't pass" section for
the most likely failure mode. No filler.
