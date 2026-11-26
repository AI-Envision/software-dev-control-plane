# Governance

LinkedIn: https://www.linkedin.com/in/levkantorovich

## Hard-truth boundary

Every task must state:

- what is already proven
- what is not proven
- what remains unknown
- what the task may claim on success
- what the task must never claim

## Anti-micro-step rule

A normal task must unlock a new, end-to-end, reviewer-visible capability.
A proposal should be folded into a larger milestone when it only:

- adds a wrapper around existing behavior
- renames or repackages existing artifacts
- adds a schema with no active consumer
- adds documentation without enabling operation
- creates another report over unchanged evidence

Small tasks are allowed only for blocking defects, security fixes, or narrowly
bounded corrections that prevent a larger milestone.

## Evidence gate

Completion requires:

- exact commands
- exit status
- test summary
- produced artifacts
- target commit SHA when applicable
- final repository status
- explicit limitations
- reality-check conclusion

## Stop conditions

The implementation must stop when:

- required work escapes allowed repositories or files
- credentials or secret-bearing paths would be required unexpectedly
- acceptance criteria conflict
- two focused correction attempts fail in the same area
- deterministic validation cannot be constructed
- evidence does not support the requested completion claim

## Provider-agnostic orchestration and cost governance (adopted 2026-11-26)

For meaningful AI-assisted tasks, inspect current instructions, available skills,
provider capabilities, data permissions and approved budget. Select the least
costly option meeting acceptance criteria; record the routing rationale or why
no delegation is needed. Prefer capability-based adapters and compliant fallback
rather than vendor lock-in. Preserve human review boundaries and existing skills.

- Default paid API budget is zero; explicit authorization is required for any
  nonzero spend. Fail closed on uncertain cost or data authorization.
- Bound retries, recursion, delegation depth and elapsed time. Never bypass
  provider limits or terms.
- Protect credentials and confidential data; review and pin external skills and
  tools. Store generated media as files and pass paths when practical.
- Measure cost per verified outcome, including retries and review. Separate
  measured API charges, subscription consumption, local costs and estimates.
- Verify results independently where warranted; report unverified claims as such.
- Before rollout, integrate these rules into the actual global instruction and
  installer mechanism; test offline routing, fallback, budget/privacy rejection,
  secret handling, bounded execution, regression and fresh-session discovery.
- Check policy version and availability at project handoff; record drift and
  missing capabilities. Policy documentation alone is not runtime enforcement.

Implementation and acceptance tracking: [issue #3](https://github.com/AI-Envision/software-dev-control-plane/issues/3).
Status: policy adopted; implementation and machine rollout pending.
