# Mission 01: First Real Commit

**Module 1 — Git Foundations**

## Goal

Make a real change to `relnotes` on a real branch, with a commit message
that explains *why*, not just *what*.

## Steps

1. Create a branch:
   ```bash
   git switch -c feature/add-category-field
   ```
2. Make a small, real change. A good first pick: `relnotes.core` doesn't
   validate that `category` is lowercase before checking it against
   `VALID_CATEGORIES` — try adding a normalization step, or pick any
   other small, honest improvement.
3. Commit it with a message that says *why* the change matters, not just
   what changed:
   ```bash
   git add -A
   git commit -m "Normalize category casing so 'Added' and 'added' both work"
   ```
   Avoid placeholder messages like "wip", "update", or "fix" — the
   checker specifically rejects those.
4. Push the branch:
   ```bash
   git push -u origin feature/add-category-field
   ```

## What's checked

A remote branch (other than `main`) exists, with at least one commit
ahead of `main`, and that commit's message isn't a placeholder.

## If it doesn't pass

Rewrite your commit message to explain the reasoning, not just restate
the diff: `git commit --amend -m "..."` then `git push --force-with-lease`
(force-pushing your *own*, not-yet-shared branch is fine here — this
isn't the "don't rewrite shared history" rule yet, that comes later).
