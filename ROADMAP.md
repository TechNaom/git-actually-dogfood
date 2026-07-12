# Roadmap

16 missions across 5 modules. No prior git knowledge assumed — Module 1
starts from `git init`. Each mission's completion is checked against real
repo state (a real commit, a real PR, a real deployment), not a
self-reported checkbox.

| Module | Missions | Covers |
|---|---|---|
| **1. Git Foundations** | 00 Setup · 01 First real commit · 02 Branch & merge · 03 Handle a real merge conflict | init/add/commit, branching, fast-forward vs. real merge, hand-resolving a genuine conflict |
| **2. GitHub Collaboration** | 04 Push & open a real PR · 05 CI runs on your PR · 06 Real code review · 07 Merge & clean up | PR template, watching real CI on a real PR, leaving and addressing a genuine review comment, merge + branch cleanup |
| **3. CI Essentials** | 08 Matrix builds · 09 Caching + a second check | multi-version test matrix, pip caching, adding a type-check/format job |
| **4. Full DevOps Pipeline** | 10 Build artifacts · 11 Environments & secrets · 12 Staging deploy gate · 13 Production deploy gate · 14 Reusable workflow | a needs-gated build job, a real GitHub Environment with a secret, a real GitHub Pages deploy behind an environment gate, a production environment with a required reviewer you approve yourself, refactoring into a `workflow_call` reusable workflow |
| **5. Capstone** | 15 Ship a real feature end-to-end | the full loop unassisted: issue → branch → atomic commits → PR → CI green → review → merge → staging deploy → approved production deploy → cleanup |

See each `missions/NN-*.md` file for the actual step-by-step instructions.
