# KISS and Algorithmic Efficiency Governance

This repository uses two complementary governance rules for agentic development.

## KISS Engineering

Agents should prefer simple, bounded, reviewable changes.

A proposed implementation should be challenged when it introduces:

- new frameworks
- new services
- new plugin systems
- large refactors
- unnecessary schemas
- speculative abstractions
- hidden automation
- distributed workflows for local problems

The preferred default is a small, explicit, testable change that matches the current task.

## Algorithmic Efficiency

Agents should reason about data size, hot paths, and repeated work before implementing data-processing logic.

A proposed implementation should be challenged when it contains:

- avoidable nested scans
- repeated parsing of the same data
- unbounded memory growth
- unnecessary full-directory scans
- repeated sorting
- unindexed matching
- concurrency added before bottleneck analysis

The preferred default is to choose appropriate data structures, bound memory and IO, and validate performance claims.

## Combined rule

KISS and efficiency are not opposites.

The target is:

- simple enough to review
- efficient enough for expected scale
- explicit enough to debug
- bounded enough to operate safely
- validated enough to trust
