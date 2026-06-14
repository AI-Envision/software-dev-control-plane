from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_manifest(
    output_dir: Path,
    *,
    project: dict[str, Any],
    task: dict[str, Any],
    project_path: Path,
    task_path: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_dir / f"{task['id']}_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=False)

    manifest = {
        "schema_version": 1,
        "prepared_at_utc": timestamp,
        "project_id": project["project_id"],
        "task_id": task["id"],
        "task_status": task["status"],
        "target_repo": project["target_repo"],
        "target_branch": task.get("target_branch"),
        "project_file": str(project_path),
        "task_file": str(task_path),
        "allow_network": project["boundaries"]["allow_network"],
        "allow_secrets": project["boundaries"]["allow_secrets"],
        "dry_run": True,
        "execution_performed": False,
    }
    path = run_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path
