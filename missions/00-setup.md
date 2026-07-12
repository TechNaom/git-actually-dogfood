# Mission 00: Setup

**Module 1 — Git Foundations**

## Goal

Get `relnotes` installed and its test suite passing in CI, on your own
copy of this repo.

## Steps

1. If you haven't already: clone your repo and install the practice app.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # .venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   pytest -v
   ```
   All tests should pass locally before you do anything else.
2. Push something — even an empty commit — to wake up Mission Check.
   ```bash
   git commit --allow-empty -m "Start git-actually"
   git push
   ```
3. Wait about a minute, then check the **Actions** tab for a "CI" run on
   your push, and check your **Issues** tab for a new "Mission Control"
   issue.

## What's checked

The bot looks for a completed **CI** workflow run on your latest commit
with conclusion `success`. If CI hasn't run yet, wait a minute and
re-check (Actions tab → Mission Check → Run workflow).

## If it doesn't pass

- No Mission Control issue appears at all → Settings → Actions → General
  → Workflow permissions → set to **Read and write permissions**.
- CI is red → open the failing job's log, read the actual error (usually
  a missing dependency or a test failure), fix it, commit, push again.
