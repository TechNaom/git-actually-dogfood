# Mission 09: Caching & a Second Check

**Module 3 — CI Essentials**

## Goal

Speed up CI with dependency caching, and add a second kind of check
beyond tests.

## Steps

1. Add pip caching to your `setup-python` step(s):
   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: ${{ matrix.python-version }}
       cache: "pip"
       cache-dependency-path: requirements-dev.txt
   ```
   Run CI twice and compare timings in the Actions log — the second run's
   "Install dependencies" step should be visibly faster.
2. Add a third job for a second kind of check — pick one:
   - `mypy` for type checking
   - `black --check .` for formatting
   - anything else genuinely useful beyond lint + tests

   Example:
   ```yaml
   typecheck:
     name: Type check
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v4
       - uses: actions/setup-python@v5
         with: { python-version: "3.12" }
       - run: pip install mypy
       - run: mypy src/relnotes
   ```

## What's checked

At least one `setup-python` step has `cache: "pip"`, and `ci.yml` has at
least 3 jobs total.

## If it doesn't pass

Caching not detected → make sure `cache: "pip"` is under a real
`setup-python` step's `with:` block, not floating elsewhere in the file.
