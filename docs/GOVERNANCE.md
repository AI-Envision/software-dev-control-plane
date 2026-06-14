# Governance

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
