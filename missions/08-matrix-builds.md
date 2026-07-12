# Mission 08: Matrix Builds

**Module 3 — CI Essentials**

## Goal

Make the `test` job in `.github/workflows/ci.yml` run across multiple
Python versions in parallel, instead of just one.

## Steps

Open `.github/workflows/ci.yml` and add a `strategy.matrix` block to the
`test` job:

```yaml
jobs:
  test:
    name: Test (Python ${{ matrix.python-version }})
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest -v
```

`fail-fast: false` matters: without it, one Python version failing
cancels the others mid-run, which hides real information about which
versions are actually broken.

Commit and push directly to `main`, or through another small PR — your
call from here on.

## What's checked

The `test` job's `strategy.matrix.python-version` list has at least 2
entries.

## If it doesn't pass

Check your YAML indentation — `strategy` and `matrix` need to be nested
correctly under the `test` job, not at the top level of the file.
