---
name: repository-safety
description: Load when an agent will inspect, modify, branch, commit, push, or otherwise operate on a Git repository. Use to prevent cross-repo edits, destructive commands, secret exposure, and unsafe workspace assumptions.
---

# Repository Safety Skill

Use this skill before working inside a source repository.

Required checks:
- Confirm repository root.
- Confirm current branch.
- Check `git status --short`.
- Confirm intended task scope.
- Avoid touching unrelated repositories.
- Never expose secrets, tokens, customer data, or proprietary employer material.

Safe default commands:
- `pwd`
- `git rev-parse --show-toplevel`
- `git branch --show-current`
- `git status --short`

Gotchas:
- Do not assume the current directory is the repo root.
- Do not modify sibling repositories.
- Do not commit caches, virtualenvs, logs, or local credentials.
- Do not claim a push or deployment succeeded unless it actually succeeded.
