# Reviewer Guide

Developed by Lev Kantorovich.

LinkedIn: https://www.linkedin.com/in/levkantorovich

This repository demonstrates the engineering process used around an
AI-assisted take-home project.

## Suggested review path

1. Read `README.md`.
2. Read `docs/GOVERNANCE.md`.
3. Inspect role boundaries in `agents/`.
4. Inspect the example project and task.
5. Run `pytest -q`.
6. Run the example validation and dry-run commands.
7. Inspect the generated manifest under `shared/runs/`.

## Important disclosure statement

This repository was created as a clean-room generic framework. It does not
contain source code, prompts, task history, domain logic, credentials, or
artifacts copied from private development repositories.

## What reviewers should evaluate

- Are task boundaries explicit?
- Are implementation claims evidence-backed?
- Are negative cases and stop conditions present?
- Is human control preserved?
- Can the workflow be reproduced without external API keys?
- Is the framework useful without being overengineered?
