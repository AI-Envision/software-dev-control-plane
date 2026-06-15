---
name: code-quality-comments
description: Load when an agent writes or reviews source code, tests, scripts, or documentation intended for handoff. Use to improve readability, maintainability, naming, comments, and review quality.
---

# Code Quality and Comments Skill

Developed by Lev Kantorovich as part of the Universal Software Development Control Plane.

Core rule: code should be understandable by the next engineer without requiring the original agent conversation.

Required checks:
- Does the code match the task?
- Is the naming clear?
- Is the control flow easy to follow?
- Are edge cases handled explicitly?
- Are errors reported clearly?
- Are comments useful and durable?
- Are tests or validation commands included?
- Is the implementation smaller than a speculative architecture?

Comment guidance:
- Explain why, not obvious syntax.
- Document constraints and tradeoffs.
- Explain non-obvious algorithms or data structures.
- Mark intentional limitations.
- Avoid comments that duplicate the code.

Avoid:
- clever code without explanation
- broad refactors without need
- comments that will become stale quickly
- generic docstrings with no useful information
- hiding unclear code behind excessive comments
