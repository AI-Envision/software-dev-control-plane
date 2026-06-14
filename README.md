# Software Development Control Plane

A clean-room, reusable control plane for AI-assisted software development.

The repository provides a deterministic, human-controlled workflow around
AI coding tools:

- explicit project and repository boundaries
- architecture before implementation
- large capability milestones rather than artificial micro-tasks
- separate architect, product, implementation, validation, security, and
  reality-check responsibilities
- generated task handoffs
- dry-run manifests
- test and evidence gates
- explicit non-goals and stop conditions
- truth-preserving completion reports

## What this repository is

This is a generic software-development governance and orchestration layer.
It is designed to sit beside a target software repository rather than contain
the target product itself.

## What this repository is not

- It is not a copy of any private production repository.
- It contains no arbitrage implementation, trading logic, credentials, or
  proprietary employer code.
- It does not automatically execute AI agents.
- It does not claim that passing unit tests proves production readiness.
- It does not require LangChain or LangGraph.

## Public-review purpose

This repository is intentionally suitable for technical review. Reviewers can
inspect:

1. `docs/ARCHITECTURE.md`
2. `docs/GOVERNANCE.md`
3. `docs/REVIEWER_GUIDE.md`
4. `agents/`
5. `schemas/`
6. `projects/example_project/`
7. `tests/`

The control plane can be linked from a take-home repository through a
`CONTROL_PLANE.md` file.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q

sdcp validate-project projects/example_project/project.yaml
sdcp validate-task projects/example_project/tasks/EX-001.yaml
sdcp prepare-run \
  --project projects/example_project/project.yaml \
  --task projects/example_project/tasks/EX-001.yaml
```

## Design principles

- Human approval remains explicit.
- Every task identifies what it proves and what it does not prove.
- Claims require evidence.
- Missing evidence remains missing evidence.
- Agents may not widen scope silently.
- Stop conditions are first-class.
- A task should unlock a reviewable capability, not merely add wrappers,
  schemas, or documentation.
- Product code stays in the target repository.
- Generated artifacts stay reproducible and inspectable.
