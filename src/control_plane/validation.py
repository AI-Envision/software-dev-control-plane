from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_REQUIRED = {
    "project_id",
    "target_repo",
    "default_branch",
    "languages",
    "test_commands",
    "boundaries",
}

TASK_REQUIRED = {
    "id",
    "title",
    "project",
    "type",
    "status",
    "strategic_goal",
    "current_factual_state",
    "capability_unlocked",
    "non_goals",
    "allowed_files",
    "required_outputs",
    "stop_conditions",
    "reality_check",
}

TASK_TYPES = {"capability", "blocking_hotfix", "security_fix", "investigation"}

TASK_STATES = {
    "draft",
    "architecture_reviewed",
    "ready",
    "prompt_generated",
    "dry_run_prepared",
    "implementation_in_progress",
    "validation_pending",
    "reality_check_pending",
    "completed",
    "blocked",
    "superseded",
}


class ValidationError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"File does not exist: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError(f"Expected YAML mapping: {path}")
    return data


def _require(data: dict[str, Any], required: set[str], kind: str) -> None:
    missing = sorted(required - set(data))
    if missing:
        raise ValidationError(f"{kind} is missing required fields: {', '.join(missing)}")


def validate_project(data: dict[str, Any]) -> None:
    _require(data, PROJECT_REQUIRED, "Project")
    boundaries = data["boundaries"]
    if not isinstance(boundaries, dict):
        raise ValidationError("Project boundaries must be a mapping")
    for key in ("protected_paths", "allow_network", "allow_secrets", "public_disclosure"):
        if key not in boundaries:
            raise ValidationError(f"Project boundaries missing: {key}")

    target = Path(str(data["target_repo"])).expanduser().resolve()
    for protected in boundaries["protected_paths"]:
        protected_path = Path(str(protected)).expanduser().resolve()
        if target == protected_path or protected_path in target.parents:
            raise ValidationError(
                f"Target repository is inside protected path: {protected_path}"
            )


def validate_task(data: dict[str, Any]) -> None:
    _require(data, TASK_REQUIRED, "Task")
    if data["type"] not in TASK_TYPES:
        raise ValidationError(f"Unsupported task type: {data['type']}")
    if data["status"] not in TASK_STATES:
        raise ValidationError(f"Unsupported task state: {data['status']}")
    if data["type"] == "capability" and not data["capability_unlocked"]:
        raise ValidationError("Capability task must identify a capability_unlocked")
    if not isinstance(data["allowed_files"], list) or not data["allowed_files"]:
        raise ValidationError("Task allowed_files must be a non-empty list")
    if not isinstance(data["stop_conditions"], list) or not data["stop_conditions"]:
        raise ValidationError("Task stop_conditions must be a non-empty list")
