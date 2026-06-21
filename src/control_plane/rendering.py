from __future__ import annotations

from pathlib import Path
from typing import Any

from .validation import (
    ValidationError,
    load_yaml,
    validate_engineering_quality_requirements,
    validate_evidence,
    validate_project,
    validate_task,
    validate_task_project_match,
)

ENGINEERING_QUALITY_PATH = (
    Path(__file__).resolve().parents[2]
    / "templates"
    / "requirements"
    / "engineering_quality.yaml"
)


def _section(title: str, lines: list[str]) -> str:
    return "\n".join([f"## {title}", *lines]).rstrip()


def _bullet_list(items: list[Any]) -> list[str]:
    return [f"- {item}" for item in items]


def _optional_line(label: str, value: Any) -> list[str]:
    if value in (None, ""):
        return []
    return [f"- {label}: {value}"]


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def load_engineering_quality_requirements(path: Path | None = None) -> dict[str, Any]:
    quality_path = path or ENGINEERING_QUALITY_PATH
    data = load_yaml(quality_path)
    validate_engineering_quality_requirements(data)
    return data


def load_project_task(project_path: Path, task_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    project = load_yaml(project_path)
    task = load_yaml(task_path)
    validate_project(project)
    validate_task(task)
    validate_task_project_match(project, task)
    return project, task


def load_project_task_evidence(
    project_path: Path,
    task_path: Path,
    evidence_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    project, task = load_project_task(project_path, task_path)
    evidence = load_yaml(evidence_path)
    validate_evidence(evidence)
    if evidence["target_repo"] != project["target_repo"]:
        raise ValidationError(
            "Evidence target_repo does not match project target_repo"
        )
    return project, task, evidence


def render_prompt_markdown(project: dict[str, Any], task: dict[str, Any]) -> str:
    boundaries = project["boundaries"]
    quality = load_engineering_quality_requirements()
    sections = [
        _section(
            "Task",
            [
                f"- Task ID: {task['id']}",
                f"- Title: {task['title']}",
                f"- Control-plane project: {project['project_id']}",
                f"- Target repository: {project['target_repo']}",
                *_optional_line("Target branch", task.get("target_branch")),
            ],
        ),
        _section(
            "Strict Boundaries",
            [
                "- Scope must remain inside the declared target repository and allowed files.",
                "- Do not auto-push or auto-merge.",
                "- Do not widen scope beyond the declared task.",
                f"- Network access: {'allowed' if boundaries['allow_network'] else 'prohibited'}.",
                f"- Secrets/credentials: {'allowed' if boundaries['allow_secrets'] else 'prohibited'}.",
                f"- Public disclosure rule: {boundaries['public_disclosure']}",
                "Protected paths:",
                *_bullet_list(boundaries["protected_paths"]),
            ],
        ),
        _section("Allowed Files", _bullet_list(task["allowed_files"])),
        _section(
            "Engineering Quality Requirements",
            _bullet_list(quality["required_prompt_sections"]),
        ),
        _section("Strategic Goal", [str(task["strategic_goal"])]),
        _section("Current Factual State", _bullet_list(task["current_factual_state"])),
        _section("Required Outputs", _bullet_list(task["required_outputs"])),
        _section("Stop Conditions", _bullet_list(task["stop_conditions"])),
        _section("Reality-Check Questions", _bullet_list(task["reality_check"])),
        _section("Validation Commands", _bullet_list(project["test_commands"])),
        _section(
            "Final Handoff Requirements",
            [
                "- Report files changed.",
                "- Report commands run.",
                "- Report validation and test results.",
                "- Report explicit limitations and non-claims.",
                "- Report git status --short.",
            ],
        ),
    ]
    return "\n\n".join(sections) + "\n"


def render_review_packet_markdown(
    project: dict[str, Any],
    task: dict[str, Any],
    evidence: dict[str, Any],
) -> str:
    summary_lines = [
        f"- Task ID: {task['id']}",
        f"- Title: {task['title']}",
        f"- Target repo: {evidence['target_repo']}",
        f"- Control-plane project ID: {project['project_id']}",
    ]
    if task.get("target_branch"):
        summary_lines.append(f"- Target branch: {task['target_branch']}")

    algo_lines: list[str] = []
    if evidence.get("algorithm"):
        algo_lines.append(f"- Algorithm: {evidence['algorithm']}")
    if evidence.get("complexity"):
        algo_lines.append(f"- Complexity: {evidence['complexity']}")

    quality_lines: list[str] = []
    review_labels = {
        "quality_review": "Quality review",
        "complexity_review": "Complexity review",
        "design_review": "Design review",
        "test_review": "Test review",
    }
    for field, label in review_labels.items():
        for item in _string_list(evidence.get(field)):
            quality_lines.append(f"- {label}: {item}")

    sections = [
        _section("Task", summary_lines),
        _section("Commits", _bullet_list(evidence["commits"])),
        _section("Validation Results", _bullet_list(evidence["validation"])),
        _section("Implemented Files", _bullet_list(evidence["implemented_files"])),
        _section("Algorithm / Complexity", algo_lines or ["- Not provided."]),
        _section("Quality Review", quality_lines or ["- Not provided."]),
        _section("Claims Supported", _bullet_list(evidence["claims_supported"])),
        _section("Non-Claims", _bullet_list(evidence["non_claims"])),
        _section("Boundary Review", _bullet_list(evidence["boundary_review"])),
        _section("Final Status", [evidence["final_status"]]),
    ]
    return "\n\n".join(sections) + "\n"
