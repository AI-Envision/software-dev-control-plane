---
name: quality-gates
description: Load when validating agent-generated code or documentation. Use for tests, linting, schema validation, diff review, and explicit acceptance criteria.
---

# Quality Gates Skill

Use this skill before handoff, commit, or pull request.

Common gates:
- `pytest -q`
- `git diff --check`
- `git status --short`
- `sdcp validate-project projects/example_project/project.yaml`
- `sdcp validate-task projects/example_project/tasks/EX-001.yaml`
- `python -m control_plane.skills --root .`

Acceptance criteria:
- Relevant tests pass.
- The diff is understood.
- No unrelated files changed.
- Working tree state is intentional.
- Residual risk is explained.
