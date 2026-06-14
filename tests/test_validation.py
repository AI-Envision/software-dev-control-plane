from pathlib import Path

import pytest

from control_plane.validation import (
    ValidationError,
    load_yaml,
    validate_project,
    validate_task,
)


ROOT = Path(__file__).resolve().parents[1]


def test_example_project_is_valid():
    data = load_yaml(ROOT / "projects/example_project/project.yaml")
    validate_project(data)


def test_example_task_is_valid():
    data = load_yaml(ROOT / "projects/example_project/tasks/EX-001.yaml")
    validate_task(data)


def test_protected_target_is_rejected():
    data = load_yaml(ROOT / "projects/example_project/project.yaml")
    data["target_repo"] = "/home/lev/ai-dev-platform"
    with pytest.raises(ValidationError, match="protected path"):
        validate_project(data)


def test_capability_requires_capability_output():
    data = load_yaml(ROOT / "projects/example_project/tasks/EX-001.yaml")
    data["capability_unlocked"] = []
    with pytest.raises(ValidationError, match="capability_unlocked"):
        validate_task(data)
