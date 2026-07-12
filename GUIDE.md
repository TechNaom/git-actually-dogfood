# User Guide: How to Use git-actually

This is the step-by-step walkthrough. `README.md` has the quickstart;
this is the longer version — what to expect, what you'll actually gain,
and what to do when something doesn't work.

## Who this is for

Anyone who can write basic Python and has never (or barely) used git for
real — students, career-switchers, self-taught developers about to
interview, or anyone whose git knowledge is "I know `add`, `commit`,
`push` and get nervous about everything else." No prior GitHub or CI/CD
experience assumed.

## What you'll actually walk away with

By Mission 15 you will have, for real, on your own GitHub account:

- Resolved a real merge conflict by hand (not watched someone else do it)
- Opened, reviewed, and merged real pull requests
- Written a GitHub Actions pipeline from a single lint+test job up to a
  multi-version test matrix, build artifacts, and a staging→production
  deployment gate with a real required-approval step
- A real, public repo with real commit history and real Actions runs you
  can point to in an interview or portfolio — "I did this" instead of
  "I read about this"

## Step 1: Get your own copy

1. On this repo's GitHub page, click **Use this template → Create a new
   repository**. (Not *Fork* — a template gives you clean, independent
   history with no ties back to this repo.)
2. Name it whatever you like, and **set it to Public**. This matters:
   GitHub Pages (Missions 12-13) only works on public repos on the free
   plan. If you pick Private, everything works until the deploy missions,
   which will fail with a plan-limit error that has nothing to do with
   your workflow YAML.
3. Clone it locally and install the practice app:
   ```bash
   git clone https://github.com/<you>/<your-repo-name>.git
   cd <your-repo-name>
   python3 -m venv .venv
   source .venv/bin/activate      # .venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   pytest -v                      # should be green before you touch anything
   ```
4. Wake the bot up with one push:
   ```bash
   git commit --allow-empty -m "Start git-actually"
   git push
   ```
5. Wait about a minute, then check your repo's **Issues** tab. You should
   see a new issue titled **Mission Control** — that's the bot's home
   base from here on. It'll say whether Mission 00 passed yet.

If no issue appears after a couple minutes: go to **Settings → Actions →
General → Workflow permissions** and switch it to **Read and write
permissions**, then re-run the check manually (next section covers how).

## Step 2: The loop you'll repeat 16 times

Every mission follows the same shape:

1. **Read** `missions/NN-<name>.md` for that mission's instructions.
2. **Do the real work** in your terminal / GitHub's UI — write code, run
   git commands, open a PR, click buttons in Settings. Nothing here is
   simulated; every action is the real thing.
3. **Push** (or take the manual UI action a mission calls for, like
   approving a deployment).
4. **Check your progress**: either wait for the automatic check to run
   after your push, or trigger it yourself any time —
   **Actions tab → Mission Check → Run workflow**.
5. **Read the result** on the Mission Control issue or in that run's Job
   Summary. A failed check names the exact gap — not just "failed," but
   what specifically is missing or wrong. Fix that one thing and repeat
   step 3-4.
6. On a pass, the bot commits an updated `PROGRESS.md` and unlocks the
   next mission automatically — no waiting on anyone.

## Step 3: Working through the modules

Follow `ROADMAP.md` for the full map. Roughly:

- **Missions 00-03** are pure local git — no GitHub features needed yet,
  just you, the terminal, and a real merge conflict to resolve by hand.
- **Missions 04-07** move onto GitHub itself: your first real pull
  request, watching CI run on it, a real review comment, and a real
  merge.
- **Missions 08-09** deepen the CI pipeline itself: a test matrix, then
  caching and a second check.
- **Missions 10-14** are the "full DevOps pipeline" stretch: build
  artifacts, a real Environment with a secret, a staging deploy, a
  production deploy gated behind your own approval, and a refactor into
  a reusable workflow.
- **Mission 15** is unassisted: the entire loop, start to finish, with no
  mission doc holding your hand — that's the point.

## Troubleshooting

**The bot never comments / never creates Mission Control.**
Check Settings → Actions → Workflow permissions (see Step 1). This is
the single most common snag and it's a one-click fix, not a bug in your
work.

**A deploy mission (12 or 13) fails immediately.**
Confirm your repo is Public (Settings → General → Danger Zone → Change
visibility) and that GitHub Pages is enabled with source set to "GitHub
Actions" (Settings → Pages).

**The checker says "not yet" but you're sure you did it.**
Read the message closely — it's checking a specific, narrow thing (e.g.
"a commit *after* the review comment's timestamp," not just "any
commit"). Re-read the mission doc's exact requirement before assuming
it's the bot's fault.

**You want to double check something without waiting for a push.**
Actions tab → Mission Check → Run workflow → pick your branch → Run.
This re-checks your current progress on demand.

## When you finish

Mission 15's Mission Control comment will say the capstone is complete.
At that point:

- Your repo is real, public, and portfolio-ready as-is — link it directly.
- Consider doing Mission 15 a second time on a genuinely different
  feature (the stretch goal every capstone-style project benefits from —
  repetition is what makes the loop automatic).
- If you want to keep practicing GitHub collaboration specifically
  (not just solo missions), `first-contributions`-style repos are a good
  next step now that you have real PR/review muscle memory.
