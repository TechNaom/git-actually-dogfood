# Mission 12: Staging Deploy Gate

**Module 4 — Full DevOps Pipeline**

## Goal

Deploy something real to GitHub Pages, gated behind the `staging`
environment from Mission 11.

## Steps

1. **Enable Pages first** (one-time, if you haven't): Settings → Pages →
   Source → **GitHub Actions**. (Your repo must be Public for this to
   work — see the note in `README.md` if you skipped that.)
2. Add a `deploy-staging` job to a new workflow,
   `.github/workflows/deploy-pages.yml`:
   ```yaml
   name: Deploy

   on:
     push:
       branches: [main]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   jobs:
     deploy-staging:
       runs-on: ubuntu-latest
       environment:
         name: staging
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with: { python-version: "3.12" }
         - run: pip install -e .
         - name: Build staging site
           env:
             RELEASE_TOKEN: ${{ secrets.RELEASE_TOKEN }}
           run: |
             mkdir -p site
             relnotes render --format markdown > /tmp/changelog.md 2>/dev/null || echo "No entries yet." > /tmp/changelog.md
             echo "<html><body><h1>relnotes -- STAGING</h1><pre>$(cat /tmp/changelog.md)</pre></body></html>" > site/index.html
         - uses: actions/configure-pages@v5
         - uses: actions/upload-pages-artifact@v3
           with: { path: site }
         - id: deployment
           uses: actions/deploy-pages@v4
   ```
3. Push, then check the run's summary for the live URL — it'll be
   `https://<you>.github.io/<your-repo-name>/`.

## What's checked

A real deployment to the `staging` environment exists and succeeded (via
the deployment API, not just checking the current live page — by the
time you're on Mission 13, production will have overwritten it).

## If it doesn't pass

`deploy-pages` fails with a plan-limit error → your repo is private,
make it public. Nothing happens at all → confirm Pages is enabled with
source set to "GitHub Actions," not "Deploy from a branch."
