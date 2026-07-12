# Mission 14: Reusable Workflow

**Module 4 — Full DevOps Pipeline**

## Goal

Extract your lint+test logic into a reusable workflow, called via
`workflow_call` — the pattern real teams use to avoid copy-pasting the
same CI steps across every repo (or every job in one repo).

## Steps

1. Create `.github/workflows/reusable-lint-test.yml` from scratch:
   ```yaml
   name: Reusable Lint & Test

   on:
     workflow_call:
       inputs:
         python-version:
           required: true
           type: string

   jobs:
     lint-and-test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: ${{ inputs.python-version }}
             cache: "pip"
             cache-dependency-path: requirements-dev.txt
         - run: pip install -e ".[dev]"
         - run: ruff check .
         - run: pytest -v
   ```
2. Replace your `ci.yml`'s `test` job (and fold `lint` into it, since the
   reusable workflow now does both) with a call to it:
   ```yaml
   jobs:
     test:
       strategy:
         fail-fast: false
         matrix:
           python-version: ["3.11", "3.12", "3.13"]
       uses: ./.github/workflows/reusable-lint-test.yml
       with:
         python-version: ${{ matrix.python-version }}

     build:
       needs: [test]
       # ... unchanged from Mission 10
   ```
3. Push and confirm CI still passes — same behavior, less duplication.

## What's checked

`ci.yml` calls a local workflow via `uses:` referencing
`reusable-lint-test.yml`, and that file exists with a real
`on: workflow_call` trigger.

## If it doesn't pass

YAML parses the bare `on:` key as the boolean `true` in some parsers —
a real, well-known YAML gotcha, not a typo on your part. Make sure your
file actually has `on:` (not `On:` or `"on":`, both of which also work,
but a stray extra colon or indentation slip won't).
