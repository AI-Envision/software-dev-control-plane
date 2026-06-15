# How To Use This Control Plane

Developed by Lev Kantorovich.

LinkedIn: https://www.linkedin.com/in/levkantorovich

Run from the repository root:

    pytest -q
    sdcp validate-project projects/example_project/project.yaml
    sdcp validate-task projects/example_project/tasks/EX-001.yaml
    python -m control_plane.skills --root .

## Intended workflow

1. Define a project.
2. Define a task.
3. Load relevant skills.
4. Execute the task in a bounded branch.
5. Run quality gates.
6. Produce a handoff.
7. Review and merge.
