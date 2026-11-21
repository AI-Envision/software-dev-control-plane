---
name: evidence-learning
description: Use after recurring agent execution errors, repeated QA defects, or retrospective findings to propose small, evidence-backed improvements to AGENTS.md, reusable skills, tests, or task templates.
---

# Evidence-based workflow improvement

1. Collect observed evidence (reproduced failure, tests, dates, changed files, corrected outcome). Separate evidence from opinions and speculation.
2. Ask which layer owns the lesson: deterministic test, repo-specific AGENTS.md, global policy, reusable SKILL.md, template, or handoff note. Prefer the narrowest durable owner.
3. Do not encode one-off task details or private project facts in public global files.
4. Make a small proposed patch with trigger conditions and expected benefit. Preserve existing safeguards and instruction hierarchy.
5. Check the patch against a successful scenario and a negative/regression case. Do not claim general improvement without actual evaluation.
6. Changes to global instructions and safety/cost/approval gates require explicit owner review. No silent autonomous self-modification.
