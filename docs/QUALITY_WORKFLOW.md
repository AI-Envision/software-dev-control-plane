# Quality Workflow

Developed by Lev Kantorovich.

LinkedIn: https://www.linkedin.com/in/levkantorovich

Agent-produced code should be small enough to review, directly related to the task, tested where practical, understandable by the next engineer, consistent with existing project conventions, and explicit about limitations.

## Comments

Comments should explain why something exists, not restate obvious syntax.

Good comments explain tradeoffs, constraints, safety checks, algorithmic choices, and edge cases.

## Review checklist

- Does the diff match the task?
- Are there unrelated changes?
- Are validation commands documented?
- Is the code simpler than the first proposed design?
- Are data structures appropriate?
- Are comments useful?
- Can another engineer continue from the handoff?
