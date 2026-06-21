# Generators

LinkedIn: https://www.linkedin.com/in/levkantorovich

The control-plane CLI can now render two deterministic Markdown artifacts from project/task metadata and review evidence.

## Implementation prompt

Generate an implementation prompt with:

```bash
sdcp render-prompt \
  --project projects/leetcode_rotated_search/project.yaml \
  --task projects/leetcode_rotated_search/tasks/LEET-001.yaml \
  --output shared/generated_prompts/LEET-001-prompt.md
```

The prompt includes the task identity, target repository and branch, strict boundaries, allowed files, current state, required outputs, stop conditions, reality checks, validation commands, and final handoff requirements.

## Review packet

Generate a review packet with:

```bash
sdcp render-review-packet \
  --project projects/leetcode_rotated_search/project.yaml \
  --task projects/leetcode_rotated_search/tasks/LEET-001.yaml \
  --evidence projects/leetcode_rotated_search/evidence/LEET-001.yaml \
  --output shared/generated_prompts/LEET-001-review.md
```

The review packet is deterministic Markdown built from the task metadata plus evidence about commits, validation, implemented files, supported claims, non-claims, boundary review, and final status.

## LEET-001 relationship

`projects/leetcode_rotated_search/` remains the local example fixture from the completed LEET-001 manual demo cycle. The new generators let that fixture produce the same bounded implementation prompt and a reviewer-facing packet without touching the demo repository itself.

## Still manual

The generators do not execute work, collect commits automatically, run tests automatically, or decide whether claims are justified. The actual implementation, evidence gathering, final review, and any push or merge decisions remain intentionally manual.
