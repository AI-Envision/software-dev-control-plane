# Skills

This directory contains compact procedural skills for the Universal Software Development Control Plane.

Each skill lives in:

    skills/<skill-name>/SKILL.md

Each SKILL.md starts with metadata:

    ---
    name: example-skill
    description: Load when ...
    ---

Validate with:

    python -m control_plane.skills --root .
    pytest -q
