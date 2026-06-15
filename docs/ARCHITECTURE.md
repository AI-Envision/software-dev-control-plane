# Architecture

Developed by Lev Kantorovich.

LinkedIn: https://www.linkedin.com/in/levkantorovich

## Core model

The control plane has five persistent objects:

1. **Project profile** — target repository, languages, test commands,
   boundaries, disclosure policy, and project-specific guards.
2. **Task specification** — one capability milestone with factual state,
   non-goals, allowed files, evidence requirements, and stop conditions.
3. **Generated prompt** — an operator-reviewable execution handoff.
4. **Run manifest** — immutable record of what task, project, branch, prompt,
   and validation state were prepared.
5. **Completion handoff** — evidence, tests, commit identifiers, limitations,
   and reality-check conclusion.

## Separation from target repositories

The control-plane repository never becomes the implementation repository.
A project profile points to a target repository. Product changes occur only
inside that target repository and only under task-declared boundaries.

## Agent roles

- Architect: component boundaries, interfaces, risks, non-goals.
- Product Engineer: minimum coherent reviewer-visible capability.
- Implementation Engineer: implementation within approved scope.
- Validation Engineer: deterministic tests and negative cases.
- Security Reviewer: secrets, permissions, unsafe behavior, disclosure.
- Reality-Check Reviewer: verifies that the claimed capability actually exists.

## State transitions

```text
draft
  -> architecture_reviewed
  -> ready
  -> prompt_generated
  -> dry_run_prepared
  -> implementation_in_progress
  -> validation_pending
  -> reality_check_pending
  -> completed | blocked | superseded
```

Automatic agent execution is intentionally outside the initial core.
