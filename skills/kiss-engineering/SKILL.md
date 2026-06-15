---
name: kiss-engineering
description: Load when an agent proposes architecture, abstractions, frameworks, new services, schemas, or broad refactors. Use to keep solutions simple, minimal, reviewable, and proportional to the task.
---

# KISS Engineering Skill

Use this skill to prevent over-engineering in agentic software development.

Core rule:
Prefer the simplest design that satisfies the current validated requirement.

Required checks:
- Is this change solving the task that was actually requested?
- Can the same result be achieved with fewer moving parts?
- Is a new abstraction justified by at least two real use cases?
- Is a new service, dependency, queue, database, or framework truly necessary?
- Can this be a small function, config file, script, test, or documentation update instead?
- Will the next human reviewer understand this quickly?

Default preferences:
- Small patches over large rewrites.
- Explicit code over clever indirection.
- Existing project conventions over new patterns.
- Deterministic scripts over hidden automation.
- Local validation over distributed complexity.
- Clear handoff notes over speculative future-proofing.

Reject or challenge:
- Architecture introduced before a concrete requirement.
- Generic plugin systems without real plugins.
- Complex inheritance or dependency injection for simple flows.
- New infrastructure to avoid writing a small amount of direct code.
- Large refactors bundled with small feature requests.

Gotchas:
- KISS does not mean sloppy. It means minimal, correct, testable, and maintainable.
- Simplicity should reduce operational risk, not hide it.
- Do not use KISS to avoid necessary validation, security checks, or error handling.
