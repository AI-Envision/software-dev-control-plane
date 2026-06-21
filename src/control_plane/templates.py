from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

from .validation import ValidationError, load_yaml, validate_project, validate_task

ROOT = Path(__file__).resolve().parents[2]
PROJECT_TEMPLATES_ROOT = ROOT / "templates" / "project_types"
ENGINEERING_QUALITY_REFERENCE = "templates/requirements/engineering_quality.yaml"
PROTECTED_PATHS = [
    "/home/a/software-dev-control-plane",
    "/home/a/ai-dev-platform",
    "/home/a/arb-rebuild-workspace",
    "/home/a/crypto-arb-bot",
]
TEMPLATE_REQUIRED = {
    "id",
    "language",
    "description",
    "default_validation",
    "default_allowed_files",
    "generated_ignore",
    "files",
}
PLACEHOLDER_PATTERN = re.compile(r"{{\s*([a-z_]+)\s*}}")


def load_template(
    template_id: str,
    templates_root: Path = PROJECT_TEMPLATES_ROOT,
) -> dict[str, Any]:
    template_dir = templates_root / template_id
    data = load_yaml(template_dir / "template.yaml")
    validate_template(data)
    if data["id"] != template_id:
        raise ValidationError(
            f"Template id mismatch: expected {template_id}, found {data['id']}"
        )
    files_root = template_dir / "files"
    if not files_root.is_dir():
        raise ValidationError(f"Template files directory does not exist: {files_root}")
    for relative_path in data["files"]:
        if not (files_root / relative_path).is_file():
            raise ValidationError(
                f"Template file is missing: {files_root / relative_path}"
            )
    return {**data, "_template_dir": template_dir, "_files_root": files_root}


def validate_template(data: dict[str, Any]) -> None:
    missing = sorted(TEMPLATE_REQUIRED - set(data))
    if missing:
        raise ValidationError(
            f"Template is missing required fields: {', '.join(missing)}"
        )
    for key in ("id", "language", "description"):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValidationError(f"Template field must be a non-empty string: {key}")
    for key in ("default_validation", "default_allowed_files", "generated_ignore", "files"):
        value = data[key]
        if not isinstance(value, list) or not value or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            raise ValidationError(
                f"Template field must be a non-empty list of strings: {key}"
            )


def derive_package_name(project_id: str) -> str:
    candidate = re.sub(r"[^0-9A-Za-z]+", "_", project_id).strip("_")
    if not candidate:
        raise ValidationError("Unable to derive package_name from project_id")
    if candidate[0].isdigit():
        candidate = f"pkg_{candidate}"
    return candidate.lower()


def validate_package_name(package_name: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", package_name):
        raise ValidationError(
            "package_name must match [A-Za-z_][A-Za-z0-9_]*"
        )
    return package_name


def render_placeholder_text(text: str, values: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise ValidationError(f"Unknown template placeholder: {key}")
        return values[key]

    return PLACEHOLDER_PATTERN.sub(replace, text)


def _ensure_relative_template_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        raise ValidationError(f"Template path must stay relative: {path_text}")
    return path


def _resolve_within_root(root: Path, relative_path: str) -> Path:
    relative = _ensure_relative_template_path(relative_path)
    destination = (root / relative).resolve()
    root_resolved = root.resolve()
    if destination != root_resolved and root_resolved not in destination.parents:
        raise ValidationError(f"Refusing to write outside target_repo: {destination}")
    return destination


def _validate_target_repo_boundary(target_repo: Path) -> None:
    target = target_repo.expanduser().resolve()
    for protected in PROTECTED_PATHS:
        protected_path = Path(protected).expanduser().resolve()
        if target == protected_path or protected_path in target.parents:
            raise ValidationError(
                f"Target repository is inside protected path: {protected_path}"
            )


def render_template_files(
    template: dict[str, Any],
    target_repo: Path,
    values: dict[str, str],
) -> list[str]:
    files_root = Path(template["_files_root"])
    written: list[str] = []
    for template_relative in template["files"]:
        source_path = files_root / _ensure_relative_template_path(template_relative)
        destination_relative = render_placeholder_text(template_relative, values)
        destination_path = _resolve_within_root(target_repo, destination_relative)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        content = source_path.read_text(encoding="utf-8")
        destination_path.write_text(
            render_placeholder_text(content, values),
            encoding="utf-8",
        )
        written.append(destination_relative)
    return sorted(written)


def render_project_yaml(
    *,
    template: dict[str, Any],
    project_id: str,
    target_repo: Path,
) -> str:
    data = {
        "project_id": project_id,
        "target_repo": str(target_repo),
        "default_branch": "main",
        "languages": [template["language"]],
        "test_commands": list(template["default_validation"]),
        "boundaries": {
            "protected_paths": list(PROTECTED_PATHS),
            "allow_network": False,
            "allow_secrets": False,
            "public_disclosure": "synthetic_or_explicitly_approved_only",
        },
    }
    validate_project(data)
    return yaml.safe_dump(data, sort_keys=False)


def render_task_yaml(
    *,
    template: dict[str, Any],
    project_id: str,
    project_name: str,
) -> str:
    data = {
        "id": f"{project_id.upper()}-001",
        "title": f"initialize_{project_id}_scaffold",
        "project": project_id,
        "type": "capability",
        "status": "ready",
        "strategic_goal": (
            f"Initialize a minimal, bounded {template['language']} target scaffold for "
            f"{project_name}."
        ),
        "current_factual_state": [
            "The target repository scaffold is generated from a named project template.",
            (
                "Engineering quality requirements are inherited from the control plane "
                f"reference template at {ENGINEERING_QUALITY_REFERENCE}."
            ),
            "No implementation beyond the generated scaffold is claimed.",
        ],
        "capability_unlocked": [
            "A reviewer can inspect a bounded starter repository with deterministic validation commands.",
            "The generated repository documents engineering quality requirements and disclosure boundaries.",
            "Future work can extend the scaffold without changing protected repositories.",
        ],
        "non_goals": [
            "No external API calls.",
            "No credentials.",
            "No production-readiness claim.",
            "No changes to protected repositories.",
            "No auto-push or auto-merge.",
            "No claim beyond evidence gathered from deterministic local validation.",
        ],
        "allowed_files": list(template["default_allowed_files"]),
        "required_outputs": [
            "A minimal scaffold that follows KISS / minimal design.",
            "Non-trivial code notes expected time and space complexity.",
            "Deterministic validation commands and outcomes.",
            "Security and disclosure boundaries remain explicit and enforced.",
            "Claims and non-claims remain evidence-based.",
        ],
        "stop_conditions": [
            "Work requires credentials or network access.",
            "Work touches repositories outside declared target repo.",
            "Scope expands beyond the declared task.",
            "Tests cannot support the completion claim.",
        ],
        "reality_check": [
            f"Does the {template['language']} scaffold stay minimal and reviewable?",
            "Are non-trivial code paths documented with time and space complexity?",
            "Is validation deterministic and reproducible without network access?",
            "Are security, disclosure, claims, and non-claims evidence-based and explicit?",
        ],
    }
    validate_task(data)
    return yaml.safe_dump(data, sort_keys=False)


def init_target(
    *,
    template_id: str,
    project_id: str,
    project_name: str,
    target_repo: Path,
    package_name: str | None = None,
    output_project_yaml: Path | None = None,
    output_task_yaml: Path | None = None,
    force: bool = False,
    templates_root: Path = PROJECT_TEMPLATES_ROOT,
) -> dict[str, Any]:
    template = load_template(template_id, templates_root)
    target_repo = target_repo.expanduser()
    _validate_target_repo_boundary(target_repo)
    package_name_value = validate_package_name(
        package_name or derive_package_name(project_id)
    )

    if target_repo.exists():
        if not target_repo.is_dir():
            raise ValidationError(f"Target repository path is not a directory: {target_repo}")
        has_entries = any(target_repo.iterdir())
        if has_entries and not force:
            raise ValidationError(
                f"Target repository is not empty; use --force to overwrite: {target_repo}"
            )
        if has_entries and force:
            shutil.rmtree(target_repo)
    target_repo.mkdir(parents=True, exist_ok=True)

    values = {
        "project_id": project_id,
        "project_name": project_name,
        "package_name": package_name_value,
        "target_repo": str(target_repo),
        "language": str(template["language"]),
    }
    files_written = render_template_files(template, target_repo, values)

    summary: dict[str, Any] = {
        "template_id": template["id"],
        "project_id": project_id,
        "target_repo": str(target_repo),
        "files_written": files_written,
    }

    if output_project_yaml is not None:
        output_project_yaml.parent.mkdir(parents=True, exist_ok=True)
        output_project_yaml.write_text(
            render_project_yaml(
                template=template,
                project_id=project_id,
                target_repo=target_repo.resolve(),
            ),
            encoding="utf-8",
        )
        summary["output_project_yaml"] = str(output_project_yaml)

    if output_task_yaml is not None:
        output_task_yaml.parent.mkdir(parents=True, exist_ok=True)
        output_task_yaml.write_text(
            render_task_yaml(
                template=template,
                project_id=project_id,
                project_name=project_name,
            ),
            encoding="utf-8",
        )
        summary["output_task_yaml"] = str(output_task_yaml)

    return json.loads(json.dumps(summary, sort_keys=True))
