# {{project_name}}

Minimal bounded {{language}} CLI scaffold for `{{project_id}}`.

## Engineering Quality Requirements

This target inherits the control-plane engineering quality contract from `templates/requirements/engineering_quality.yaml`.

- KISS / minimal design is required.
- Non-trivial code must state expected time and space complexity.
- Validation must remain deterministic and reproducible.
- Network access, secrets, and protected repository access are prohibited unless explicitly allowed.
- Claims and non-claims must be evidence-based.

## Validation

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```
