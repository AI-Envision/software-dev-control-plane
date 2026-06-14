import json
from pathlib import Path

from control_plane.manifest import write_manifest
from control_plane.validation import load_yaml


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_is_dry_run_and_nonexecuting(tmp_path):
    project_path = ROOT / "projects/example_project/project.yaml"
    task_path = ROOT / "projects/example_project/tasks/EX-001.yaml"
    manifest_path = write_manifest(
        tmp_path,
        project=load_yaml(project_path),
        task=load_yaml(task_path),
        project_path=project_path,
        task_path=task_path,
    )
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["dry_run"] is True
    assert data["execution_performed"] is False
    assert data["task_id"] == "EX-001"
