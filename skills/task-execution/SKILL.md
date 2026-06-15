---
name: task-execution
description: Load when executing a structured software-development task from project/task YAML. Use for task decomposition, implementation sequencing, validation, and final handoff.
---

# Task Execution Skill

Use this skill when executing a defined engineering task.

Execution pattern:
1. Read the task.
2. Identify the smallest useful change.
3. Inspect the existing implementation.
4. Make a minimal patch.
5. Run targeted tests.
6. Run broader tests if risk warrants it.
7. Produce a handoff with files changed, commands run, and remaining risks.

Rules:
- Prefer small, reviewable changes.
- Preserve existing behavior unless the task explicitly changes it.
- Do not invent requirements.
- Do not add frameworks, services, queues, databases, or abstractions unless clearly justified.
