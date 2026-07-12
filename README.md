# git-actually

Practice real git, real GitHub, and a real CI/CD pipeline — inside your own
repo, for free, with a bot that checks your work as you go.

No fake local simulations, no read-only tutorials. You fork a real repo,
branch, commit, open real pull requests, watch real CI runs, and deploy
through a real GitHub Pages staging → production gate — and a checker
workflow tells you, mission by mission, whether you actually did it.

📖 **New here? Read [`GUIDE.md`](GUIDE.md) first** — the full walkthrough:
what you'll actually gain, the loop you'll repeat for each mission, and
troubleshooting for the most common snags.

## How to get your own copy (do this first)

1. Click **Use this template** → **Create a new repository** at the top of
   this page (not *Fork* — a template gives you a clean, independent repo
   with no shared history).
2. **Set the visibility to Public.** GitHub Pages (used in Missions 12-13)
   only works on public repos on the free plan. If you create it private,
   the deploy missions will fail with a plan-limit error, not a bug in your
   workflow.
3. Clone your new repo locally:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```
4. Install the practice app and its dev dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # .venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   pytest -v                      # confirm it's green before you start
   ```
5. Push anything (even an empty commit) to `main` once. That first push is
   what wakes up the mission-check bot and creates your **Mission Control**
   issue — that issue is where you'll see pass/fail feedback from here on.
   ```bash
   git commit --allow-empty -m "Start git-actually"
   git push
   ```
6. Open `missions/00-setup.md` and start there. `ROADMAP.md` has the full
   16-mission map if you want to see where it's going first.

If the bot doesn't comment on your Mission Control issue within a minute
of pushing, check **Settings → Actions → General → Workflow permissions**
and make sure it's set to **Read and write permissions** — personal
accounts sometimes default this to read-only, which silently blocks the
bot from commenting or committing progress.

## Do's and don'ts

**Do:**
- Work through missions in order — later checkers assume earlier missions'
  real repo state exists (a branch, a PR, an environment).
- Read the failure message when a check doesn't pass — it names the exact
  gap, not just "failed."
- Use `workflow_dispatch` (Actions tab → Mission Check → Run workflow) to
  manually re-check your progress any time, not just after a push.
- Do the actual GitHub UI steps missions 11-13 ask for yourself (creating
  Environments, adding a secret, clicking Approve) — no script can do
  those for you, and they're the actual point of those missions.
- Keep your repo public for the duration — Pages deployments (Missions
  12-13) will keep failing on a private repo regardless of how correct
  your workflow YAML is.

**Don't:**
- Don't force-push or amend commits once a PR is open and someone (even
  a future-you doing self-review) has fetched that branch — Mission 06's
  checker specifically looks for a *new* commit after feedback, not a
  rewritten one, and this is also just how you'd treat genuinely shared
  history on a real team.
- Don't edit `.mission-state.json` or `PROGRESS.md` by hand — they're
  bot-owned; a hand-edit will be overwritten (or worse, desync your real
  progress) on the next check.
- Don't skip Mission 00 assuming `pip install -e .` "obviously works" —
  the checker confirms your specific fork's CI is green, not just that
  the upstream template was fine.
- Don't panic if a deploy mission fails the first time — read the actual
  Actions run log, not just the checker's summary; GitHub Pages/Actions
  errors are usually specific and fixable (see the note about visibility
  above for the most common one).

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for the full 5-module, 16-mission map —
from your first commit through a real staging → production deploy gate to
a final capstone where you ship a feature completely unassisted.

## The practice app: `relnotes`

A small, real, pip-installable changelog/release-note CLI is what you'll
actually be branching and opening PRs against — see `src/relnotes/`. It
ships with a couple of missing features on purpose; some early missions
have you build them.

## License

MIT — see [`LICENSE`](LICENSE).
