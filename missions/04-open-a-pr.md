# Mission 04: Push & Open a Real PR

**Module 2 — GitHub Collaboration**

Missions 00-03 merged straight to `main` — that's normal for solo local
git work. From here on, changes go through a real pull request instead.

## Goal

Open a real PR, using the repo's PR template properly.

## Steps

1. Branch and make another small, real improvement to `relnotes` — a good
   pick: wire up the `--category` filter flag on `relnotes list` (the CLI
   doesn't expose it yet, even though `core.list_entries()` already
   supports it).
   ```bash
   git switch main && git pull
   git switch -c feature/list-category-filter
   # make the change
   git add -A
   git commit -m "Expose --category filter on the list subcommand"
   git push -u origin feature/list-category-filter
   ```
2. Open a PR against `main` (GitHub UI, or `gh pr create`). The PR
   template pre-fills three required sections — fill them in for real,
   don't delete them:
   - **What changed**
   - **Why**
   - **How to test**

## What's checked

An open PR exists whose description contains all three headings.

## If it doesn't pass

If you used `gh pr create --fill`, it may skip the template — open the
PR on GitHub and edit the description in by hand instead.
