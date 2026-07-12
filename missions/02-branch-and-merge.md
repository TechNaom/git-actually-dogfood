# Mission 02: Branch & Merge

**Module 1 — Git Foundations**

## Goal

Merge your Mission 01 branch into `main` for real.

## Steps

```bash
git switch main
git pull
git merge feature/add-category-field
git push
```

A fast-forward merge is completely fine here — you're not trying to
force a merge commit yet (that's Mission 03).

## What's checked

Your Mission 01 branch's tip commit is an ancestor of `origin/main` —
i.e. it's genuinely merged in, not just sitting on its own branch.

## If it doesn't pass

If `git merge` reports "Already up to date" but the checker still says
it's not merged, double check you pushed `main` afterward — `git push`
with no arguments only pushes your current branch.
