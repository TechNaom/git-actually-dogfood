# Mission 11: Environments & Secrets

**Module 4 — Full DevOps Pipeline**

This one is manual UI setup, no code — and it matters. Environments and
secrets are how real teams gate deployments and keep credentials out of
their YAML.

## Goal

Create a real GitHub Environment with a real secret scoped to it.

## Steps

1. Go to **Settings → Environments → New environment**, name it
   `staging`.
2. Inside that environment's page, click **Add secret**, name it
   `RELEASE_TOKEN`, and give it any placeholder value (it's not a real
   credential — this is purely to prove the mechanism).
3. That's it for this mission — you'll actually *use* this secret in
   Mission 12.

## What's checked

A `staging` environment exists, with a secret named `RELEASE_TOKEN`
attached to it.

## Why this matters

Environment-scoped secrets are only visible to jobs that explicitly
target that environment (`environment: staging` on the job) — unlike
repo-level secrets, which any workflow in the repo can read. That
scoping is what makes environments a real access-control boundary, not
just an organizational label.
