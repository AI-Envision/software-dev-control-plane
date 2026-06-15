# Skills

This directory contains compact procedural skills for the Universal Software Development Control Plane.

Each skill lives in:

    skills/<skill-name>/SKILL.md

Each SKILL.md starts with metadata:

    ---
    name: example-skill
    description: Load when ...
    ---

The description is a routing trigger. The body contains procedure, checks, gotchas, and validation guidance.

## Current skills

- repository-safety
- task-execution
- quality-gates
- agent-handoff
- context-management
- kiss-engineering
- algorithmic-efficiency

## Validation

Run:

    python -m control_plane.skills --root .
    pytest -q
