# Mission 06: Real Code Review

**Module 2 — GitHub Collaboration**

## Goal

Leave a genuine review comment on your PR, then address it with a new
commit — not an amend, not a force-push.

## Steps

1. On your PR, leave a comment (yourself is fine, solo — or use a second
   account if you have one) that follows this shape:
   - **Name the issue** — what specifically is off?
   - **Explain why** — why does it matter?
   - **Suggest a fix** — what would you actually change?

   Example: *"The `--category` filter doesn't validate its input before
   passing it to `list_entries()` — an unknown category silently returns
   zero results instead of erroring. Consider validating against
   `VALID_CATEGORIES` the same way `add` does."*
2. Address it with a **new commit** (this matters — see below):
   ```bash
   # make the fix for real
   git add -A
   git commit -m "Validate --category against VALID_CATEGORIES"
   git push
   ```

## What's checked

At least one comment or review exists on the PR, and at least one commit
was pushed **after** that comment's timestamp.

## Why "new commit, not amend" matters

The moment someone else (even a future-you doing review) has seen a
commit, treat it as shared history. Amending or force-pushing over it
erases the exact thing a reviewer just looked at — on a real team this
breaks the reviewer's diff view and can silently drop their in-progress
comments. A fresh commit keeps the trail honest.

## If it doesn't pass

If you amended instead of adding a new commit, undo it:
`git reset --soft HEAD~1`, then `git commit` again as a separate commit
on top instead of replacing the old one.
