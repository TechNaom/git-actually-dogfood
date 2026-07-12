# Mission 13: Production Deploy Gate

**Module 4 — Full DevOps Pipeline**

## Goal

Add a production deployment that requires your own explicit approval
before it runs — the actual mechanic behind real staging→production
promotion gates.

## Steps

1. **Settings → Environments → New environment**, name it `production`.
2. On that environment's page, check **Required reviewers**, and add
   yourself. (Yes — approving your own deployment is normal, expected
   behavior for environment protection. It's a different mechanism from
   PR self-review restrictions, which don't apply here.)
3. Add a `deploy-production` job to `deploy-pages.yml`, after
   `deploy-staging`:
   ```yaml
     deploy-production:
       needs: [deploy-staging]
       runs-on: ubuntu-latest
       environment:
         name: production
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with: { python-version: "3.12" }
         - run: pip install -e .
         - name: Build production site
           run: |
             mkdir -p site
             relnotes render --format markdown > /tmp/changelog.md 2>/dev/null || echo "No entries yet." > /tmp/changelog.md
             echo "<html><body><h1>relnotes -- PRODUCTION</h1><pre>$(cat /tmp/changelog.md)</pre></body></html>" > site/index.html
         - uses: actions/configure-pages@v5
         - uses: actions/upload-pages-artifact@v3
           with: { path: site }
         - id: deployment
           uses: actions/deploy-pages@v4
   ```
   **One real gotcha**: `upload-pages-artifact` names its artifact
   `github-pages` by default. Since both jobs now run in the *same*
   workflow run, that's a naming collision. Give the staging job's
   artifact a distinct name and tell `deploy-pages` which one to use:
   ```yaml
   # in deploy-staging:
   - uses: actions/upload-pages-artifact@v3
     with: { name: github-pages-staging, path: site }
   - id: deployment
     uses: actions/deploy-pages@v4
     with: { artifact_name: github-pages-staging }
   ```
4. Push. Watch the Actions run — `deploy-production` will pause with a
   "Review deployments" prompt. Click it, approve, and watch production
   actually deploy.

## What's checked

The `production` environment has a required-reviewer rule configured,
and a deployment to it has succeeded (meaning you actually approved it —
a pending, unapproved deployment doesn't count).

## If it doesn't pass

Job never pauses for approval → double check you actually added a
required reviewer in Settings, not just created the environment. Deploy
fails with "Multiple artifacts named 'github-pages'" → you hit the
naming collision above; give each job's artifact a distinct name.
