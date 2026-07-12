# Mission 15: Capstone — Ship a Real Feature, Unassisted

**Module 5 — Capstone**

## Goal

Run the entire loop, start to finish, with no mission doc holding your
hand: issue → branch → atomic commits → PR → CI green → review →
merge → staging deploy → approved production deploy → cleanup.

## What to build

Pick one real gap in `relnotes` you haven't already fixed. Good
candidates:
- `render.py` has no `format_html()` yet, and the CLI's `--format` choice
  list doesn't include `html` — a genuinely useful feature to add
- Anything else you've noticed while working through the earlier missions

## The loop (no code samples this time — you've done each step before)

1. **File a real issue** describing the gap, what's expected vs. actual,
   and why it's worth fixing.
2. **Branch**, and make **atomic commits** — each one a coherent,
   reviewable step, not one giant "did the feature" commit.
3. **Open a PR** using the template, referencing `Closes #N`.
4. Get **CI green**.
5. Do a **genuine review** — find at least one real thing worth
   commenting on, not a rubber stamp.
6. **Address it with a new commit.**
7. **Merge**, deploy to **staging**, then **approve production**.
8. **Clean up** — delete the branch, both locally and on GitHub.

## What's checked

A new merged PR (distinct from your Mission 04-07 one), issue-linked via
`Closes #N` or `Fixes #N`, with its branch cleaned up.

## Self-assessment (the checker can't judge this part — you have to)

**Git mechanics:**
- [ ] Commits are atomic and each has a message explaining *why*
- [ ] The branch name is descriptive
- [ ] Feedback was addressed with a new commit, not a rewrite
- [ ] The merge was explicit (merge commit or squash — your call, but a
      deliberate one)
- [ ] The branch was deleted both locally and on GitHub

**Process and communication quality:**
- [ ] The issue is realistic — a real gap, not manufactured
- [ ] The PR description is complete, not "fixed it"
- [ ] At least one review comment names the issue, explains why, and
      suggests a fix — not just "LGTM"
- [ ] You'd be comfortable showing this PR to an interviewer as proof of
      how you work, not just what you built

## When you're done

Your repo is real and portfolio-ready. Link it directly — the commit
history, the PR, the Actions runs, and the deployed site are all real
proof, not a claim on a resume.
