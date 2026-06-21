from __future__ import annotations

import argparse
import json
from pathlib import Path

from .manifest import write_manifest
from .rendering import (
    load_project_task,
    load_project_task_evidence,
    render_prompt_markdown,
    render_review_packet_markdown,
)
from .templates import init_target
from .validation import (
    ValidationError,
    load_yaml,
    validate_project,
    validate_task,
    validate_task_project_match,
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

    render_prompt = sub.add_parser("render-prompt")
    render_prompt.add_argument("--project", required=True, type=Path)
    render_prompt.add_argument("--task", required=True, type=Path)
    render_prompt.add_argument("--output", required=True, type=Path)

    render_review = sub.add_parser("render-review-packet")
    render_review.add_argument("--project", required=True, type=Path)
    render_review.add_argument("--task", required=True, type=Path)
    render_review.add_argument("--evidence", required=True, type=Path)
    render_review.add_argument("--output", required=True, type=Path)

    init = sub.add_parser("init-target")
    init.add_argument("--template", required=True)
    init.add_argument("--project-id", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--target-repo", required=True, type=Path)
    init.add_argument("--package-name")
    init.add_argument("--output-project-yaml", type=Path)
    init.add_argument("--output-task-yaml", type=Path)
    init.add_argument("--force", action="store_true")

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
            validate_task_project_match(project, task)
            path = write_manifest(
                args.runs_root,
                project=project,
                task=task,
                project_path=args.project,
                task_path=args.task,
            )
            print(json.dumps({"dry_run": True, "manifest": str(path)}, indent=2))
            return 0

        if args.command == "render-prompt":
            project, task = load_project_task(args.project, args.task)
            content = render_prompt_markdown(project, task)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
            print(json.dumps({"rendered": "prompt", "output": str(args.output)}, indent=2))
            return 0

        if args.command == "render-review-packet":
            project, task, evidence = load_project_task_evidence(
                args.project,
                args.task,
                args.evidence,
            )
            content = render_review_packet_markdown(project, task, evidence)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
            print(
                json.dumps(
                    {"rendered": "review_packet", "output": str(args.output)},
                    indent=2,
                )
            )
            return 0

        if args.command == "init-target":
            summary = init_target(
                template_id=args.template,
                project_id=args.project_id,
                project_name=args.name,
                target_repo=args.target_repo,
                package_name=args.package_name,
                output_project_yaml=args.output_project_yaml,
                output_task_yaml=args.output_task_yaml,
                force=args.force,
            )
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0

    except ValidationError as exc:
        print(f"ERROR: {exc}")
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
