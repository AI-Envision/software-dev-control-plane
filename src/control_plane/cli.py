from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import write_manifest
from .validation import (
    ValidationError,
    load_yaml,
    validate_project,
    validate_task,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdcp",
        description="Software Development Control Plane",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    project = sub.add_parser("validate-project")
    project.add_argument("path", type=Path)

    task = sub.add_parser("validate-task")
    task.add_argument("path", type=Path)

    prepare = sub.add_parser("prepare-run")
    prepare.add_argument("--project", required=True, type=Path)
    prepare.add_argument("--task", required=True, type=Path)
    prepare.add_argument("--runs-root", type=Path, default=Path("shared/runs"))

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate-project":
            data = load_yaml(args.path)
            validate_project(data)
            print(f"project_valid: {data['project_id']}")
            return 0

        if args.command == "validate-task":
            data = load_yaml(args.path)
            validate_task(data)
            print(f"task_valid: {data['id']}")
            return 0

        if args.command == "prepare-run":
            project = load_yaml(args.project)
            task = load_yaml(args.task)
            validate_project(project)
            validate_task(task)
            if task["project"] != project["project_id"]:
                raise ValidationError(
                    f"Task project {task['project']} does not match "
                    f"project profile {project['project_id']}"
                )
            path = write_manifest(
                args.runs_root,
                project=project,
                task=task,
                project_path=args.project,
                task_path=args.task,
            )
            print(json.dumps({"dry_run": True, "manifest": str(path)}, indent=2))
            return 0

    except ValidationError as exc:
        print(f"ERROR: {exc}")
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
