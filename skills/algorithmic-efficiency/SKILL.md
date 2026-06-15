---
name: algorithmic-efficiency
description: Load when an agent designs loops, data processing, searches, matching, scheduling, telemetry pipelines, replay systems, or performance-sensitive code. Use to prevent avoidable CPU, memory, IO, and latency problems.
---

# Algorithmic Efficiency Skill

Use this skill when code may process non-trivial amounts of data or run repeatedly.

Core rule:
Choose data structures and algorithms deliberately before scaling the workflow.

Required checks:
- What is the expected input size now?
- What input size is plausible later?
- Is the hot path obvious?
- Are loops nested unnecessarily?
- Can lookups use a dict, set, index, heap, or sorted structure?
- Is the code repeatedly parsing, scanning, sorting, or loading the same data?
- Can processing stream records instead of materializing everything?
- Are memory, IO, and latency bounded?

Default preferences:
- O(n) scans over O(n^2) nested matching when possible.
- Sets and dictionaries for membership and lookup.
- Streaming or chunking for large logs and telemetry.
- Clear ordering and indexing for replay/debug workflows.
- Early filtering to reduce downstream work.
- Measurements for performance claims.

Avoid:
- Repeated full-directory scans inside loops.
- Re-reading large files for each item.
- Sorting repeatedly when one sort is enough.
- Loading unbounded logs into memory without reason.
- Adding concurrency before understanding the bottleneck.
- Optimizing cold paths while ignoring hot paths.

Gotchas:
- Do not prematurely micro-optimize small, one-time setup code.
- Big-O is not enough; IO, serialization, process startup, and network calls may dominate.
- The best optimization is often changing the data flow, not tweaking syntax.
