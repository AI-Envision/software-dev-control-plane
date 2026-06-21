# Target Templates

LinkedIn: https://www.linkedin.com/in/levkantorovich

## Purpose

Language-aware target templates let the control plane initialize a minimal bounded target repository from stable data files under `templates/project_types/<template_id>/`. The core logic stays language-extensible: each template contributes metadata in `template.yaml` plus UTF-8 text files in `files/`.

## Initialize A Python Target

```bash
sdcp init-target \
  --template python_package \
  --project-id demo_python_project \
  --name demo-python-project \
  --package-name demo_python_project \
  --target-repo /tmp/ucp006-demo-python-target \
  --force
```

This creates a small Python package scaffold with `pyproject.toml`, a single package module, one smoke test, and bounded control-plane notes.

## Initialize A C++ Target

```bash
sdcp init-target \
  --template cpp_cli \
  --project-id demo_cpp_project \
  --name demo-cpp-project \
  --package-name demo_cpp_project \
  --target-repo /tmp/ucp006-demo-cpp-target \
  --force
```

This creates a small C++17 CLI scaffold with `CMakeLists.txt`, a tiny executable, and an `assert()`-based smoke test registered with CTest.

## Generate Project And Task YAML

`init-target` can also emit control-plane metadata alongside the target scaffold:

```bash
sdcp init-target \
  --template python_package \
  --project-id demo_python_project \
  --name demo-python-project \
  --target-repo /tmp/ucp006-demo-python-target \
  --output-project-yaml /tmp/ucp006-demo-python-project.yaml \
  --output-task-yaml /tmp/ucp006-demo-python-task.yaml \
  --force
```

The generated `project.yaml` uses the template language, default validation commands, default allowed files, and fixed protected-path / disclosure boundaries. The generated `task.yaml` includes the template allowed files plus explicit engineering-quality outputs, non-goals, reality checks, and stop conditions.

## Engineering Quality Inheritance

Generated `README.md` and `CONTROL_PLANE.md` explicitly reference `templates/requirements/engineering_quality.yaml`. The generated task skeleton also carries the same language-neutral quality contract:

- KISS / minimal design
- Time and space complexity for non-trivial code
- Deterministic validation
- Security and disclosure boundaries
- Evidence-based claims and non-claims

## Intentionally Manual

`init-target` does not run project builds, install external toolchains, collect evidence automatically, or decide whether later implementation claims are justified. The command only creates a bounded starter repository plus optional control-plane YAML.

## Add Future Language Templates

Add a new directory under `templates/project_types/<template_id>/` with:

- `template.yaml`
- `files/`

Keep `template.yaml` small and stable. It must define:

- `id`
- `language`
- `description`
- `default_validation`
- `default_allowed_files`
- `generated_ignore`
- `files`

Template files may use these placeholders:

- `{{project_id}}`
- `{{project_name}}`
- `{{package_name}}`
- `{{target_repo}}`
- `{{language}}`

No external template engine is used; rendering is simple placeholder replacement only.
