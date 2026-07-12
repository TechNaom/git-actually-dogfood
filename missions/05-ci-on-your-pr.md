# Mission 05: CI Runs on Your PR

**Module 2 — GitHub Collaboration**

## Goal

Watch real CI run on your PR, and if it's red, fix it for real.

## Steps

1. Open your PR's **Checks** tab (or scroll down on the PR page) and
   watch the CI workflow run.
2. If it's green already, you're done — move to Mission 06.
3. If it's red: click into the failing job, read the actual error in the
   log (not just the red X), fix it locally, commit, and push:
   ```bash
   # make the fix
   git add -A
   git commit -m "Fix ruff lint error in list command"
   git push
   ```
   Pushing to the same branch automatically updates the same PR — you
   don't need to open a new one.

## What's checked

The CI workflow run for your PR's latest commit has completed with
conclusion `success`.

## If it doesn't pass

CI still running → wait, it usually takes under a minute. CI failing on
something unrelated to your change → check you're not on a stale branch;
`git switch main && git pull && git switch feature/list-category-filter
&& git merge main` to pick up anything new.
