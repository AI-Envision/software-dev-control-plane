from pathlib import Path

import pytest

from control_plane.validation import (
    ValidationError,
    load_yaml,
    validate_evidence,
    validate_engineering_quality_requirements,
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
    data["target_repo"] = "/home/a/ai-dev-platform"
    with pytest.raises(ValidationError, match="protected path"):
        validate_project(data)


def test_capability_requires_capability_output():
    data = load_yaml(ROOT / "projects/example_project/tasks/EX-001.yaml")
    data["capability_unlocked"] = []
    with pytest.raises(ValidationError, match="capability_unlocked"):
        validate_task(data)


def test_engineering_quality_requirements_template_is_valid():
    data = load_yaml(ROOT / "templates/requirements/engineering_quality.yaml")
    validate_engineering_quality_requirements(data)


def test_evidence_quality_review_fields_accept_string_or_string_list():
    data = load_yaml(ROOT / "projects/leetcode_rotated_search/evidence/LEET-001.yaml")
    data["quality_review"] = "Minimal implementation."
    data["complexity_review"] = ["O(log n) time.", "O(1) extra space."]
    validate_evidence(data)


def test_evidence_quality_review_fields_reject_non_string_values():
    data = load_yaml(ROOT / "projects/leetcode_rotated_search/evidence/LEET-001.yaml")
    data["test_review"] = {"status": "invalid"}
    with pytest.raises(ValidationError, match="test_review must be a string or list of strings"):
        validate_evidence(data)
