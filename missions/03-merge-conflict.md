# Mission 03: Handle a Real Merge Conflict

**Module 1 — Git Foundations**

## Goal

Make git report a real conflict, and resolve it by hand.

## Steps

1. Create two branches from `main`, both editing the same line of
   `CONFLICT_PRACTICE.md`:
   ```bash
   git switch main && git pull
   git switch -c practice/conflict-a
   # edit CONFLICT_PRACTICE.md -- change "Current status: not started."
   #   to something like "Current status: in progress (branch A)."
   git add CONFLICT_PRACTICE.md
   git commit -m "Update conflict practice status from branch A"
   git push -u origin practice/conflict-a

   git switch main
   git switch -c practice/conflict-b
   # edit the SAME line to something different, e.g.
   #   "Current status: in progress (branch B)."
   git add CONFLICT_PRACTICE.md
   git commit -m "Update conflict practice status from branch B"
   git push -u origin practice/conflict-b
   ```
2. Merge the first branch cleanly:
   ```bash
   git switch main
   git merge practice/conflict-a
   git push
   ```
3. Merge the second — this is where the real conflict happens:
   ```bash
   git merge practice/conflict-b
   ```
   Git will stop and mark the conflicting section in
   `CONFLICT_PRACTICE.md` with `<<<<<<<`, `=======`, `>>>>>>>` markers.
4. Open the file, decide what the line should actually say, delete the
   conflict markers, then finish the merge:
   ```bash
   git add CONFLICT_PRACTICE.md
   git commit
   git push
   ```

## What's checked

`main`'s history contains a real (2+ parent) merge commit, and
`CONFLICT_PRACTICE.md` no longer contains its original seed text.

## If it doesn't pass

If you got scared and ran `git merge --abort`, that's fine — it's a
legitimate command, but it means you haven't resolved anything yet.
Run the second `git merge` again and this time work through the
conflict instead of backing out of it.
