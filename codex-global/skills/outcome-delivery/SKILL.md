---
name: outcome-delivery
description: Use for multi-step engineering or product-development work where the user states a desired outcome and wants Codex to own planning, bounded implementation, verification, and handoff rather than stop after the first patch.
---

# Outcome delivery

Use this for a substantial result, not a trivial one-line edit.

1. Identify the current source of truth: real repository/worktree, applicable AGENTS.md, task-relevant contracts and current test state. Protect dirty work.
2. Express a concise contract: user outcome, acceptance evidence, constraints, scope, human gates, cost/time budget, and blocked stop conditions.
3. Plan the shortest evidence-producing route; reuse existing code and tests. Decide whether separate read-only research, engineering, or QA passes benefit the task. Use independent worktrees for overlapping changes.
4. Implement reversible scoped fixes; capture observed before/after evidence when possible. Avoid expanding product architecture to satisfy process requests.
5. Test at the appropriate level: deterministic tests, integration, adversarial review, and user-visible UI or real-world acceptance as applicable. Do not infer pass from mock/synthetic data.
6. If criteria fail, choose the highest-impact next bounded hypothesis and try again without bypassing gates. Stop for an actual blocker, missing owner decision, budget limit, or repeated failures.
7. End only with a verified outcome or an explicit incomplete/blocked state. Record commands, outputs, changed paths, branch, limitations, remaining work and the smallest owner action.

When the client supports persistent `/goal`, offer it for a clearly measurable multi-step objective; do not claim it globally persists or assume it is present in every Codex client.
