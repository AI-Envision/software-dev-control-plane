---
name: context-management
description: Load when an agent must choose what context to load, summarize, omit, or defer. Use to control context cost and keep large workflows navigable.
---

# Context Management Skill

Use this skill when managing large context, long tasks, or multi-step workflows.

Principles:
- Put routing information in short descriptions.
- Put durable procedure in SKILL.md.
- Put long references in separate files.
- Load heavy references only when needed.
- Keep gotchas close to the workflow they protect.

Gotchas:
- More context can make the agent worse if it distracts from the task.
- Repeated instructions should become a skill, test, or checklist.
- If an agent repeatedly fails the same way, add a gotcha or validation gate.
