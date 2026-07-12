# Mission 07: Merge & Clean Up

**Module 2 — GitHub Collaboration**

## Goal

Merge your PR for real, and clean up after yourself.

## Steps

1. Merge the PR (GitHub UI's "Merge pull request" button, or
   `gh pr merge`). Either merge commit or squash is fine.
2. Delete the branch — GitHub usually offers a "Delete branch" button
   right after merging; if you skip it, do it from the terminal:
   ```bash
   git push origin --delete feature/list-category-filter
   ```
3. Sync your local `main`:
   ```bash
   git switch main
   git pull
   git branch -d feature/list-category-filter   # delete your local copy too
   ```

## What's checked

Your PR shows as merged, and the branch no longer exists on GitHub.

## If it doesn't pass

"Merged" but branch still exists → you skipped the delete step, run the
`git push origin --delete` command above.
