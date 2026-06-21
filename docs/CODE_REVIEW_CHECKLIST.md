# Code Review Checklist

LinkedIn: https://www.linkedin.com/in/levkantorovich

## Checklist

- Readability: Can a reviewer follow the implementation quickly without unnecessary indirection?
- Module cohesion: Do files and modules each have a clear, cohesive responsibility?
- Function size: Are functions kept small enough to review, or is any larger function justified by local clarity?
- Naming: Are names explicit, stable, and aligned with domain meaning?
- Complexity hot spots: Are non-trivial paths accompanied by clear time/space complexity expectations?
- Unnecessary allocations/copies: Does the implementation avoid avoidable allocations, copies, repeated parsing, repeated scans, and accidental quadratic behavior?
- Hidden I/O/network calls: Is all filesystem, shell, or network behavior explicit and justified?
- Deterministic tests: Are tests reproducible without network, credentials, timing luck, or external services?
- Generated artifacts: Do generated outputs remain concise, deterministic, and reviewable?
- Comments/docstrings: Do comments explain non-obvious reasoning without repeating the code?
- Evidence and validation commands: Do the review artifacts include concrete validation commands, supported claims, and explicit non-claims?
