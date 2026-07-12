# Mission 10: Build Artifacts

**Module 4 — Full DevOps Pipeline**

## Goal

Add a job that builds a real installable package and uploads it as a
workflow artifact — gated behind the test job(s) passing first.

## Steps

Add a `build` job to `ci.yml`:

```yaml
build:
  name: Build package
  needs: [test]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: "3.12" }
    - run: pip install build
    - run: python -m build
    - uses: actions/upload-artifact@v4
      with:
        name: relnotes-dist
        path: dist/
```

`needs: [test]` is the important part — it means `build` won't even
start until `test` succeeds. Push, then check the Actions run's summary
page for a downloadable artifact.

## What's checked

A `build` job exists with a `needs` field, and at least one workflow
artifact exists on a recent run.

## If it doesn't pass

No artifact appears → check the `build` job actually ran (it won't if an
earlier job it `needs` failed) and that `python -m build` succeeded —
check the job log for the actual build error if not.
