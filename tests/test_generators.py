import os
import subprocess
import sys
from pathlib import Path

import pytest

from control_plane.rendering import (
    load_engineering_quality_requirements,
    load_project_task,
    load_project_task_evidence,
    render_prompt_markdown,
    render_review_packet_markdown,
)
from control_plane.validation import ValidationError


ROOT = Path(__file__).resolve().parents[1]


def test_render_prompt_from_example_fixture():
    project, task = load_project_task(
        ROOT / "projects/example_project/project.yaml",
        ROOT / "projects/example_project/tasks/EX-001.yaml",
    )

    content = render_prompt_markdown(project, task)

    assert "## Task" in content
    assert "- Task ID: EX-001" in content
    assert "- Target repository: /tmp/example-target-repo" in content
    assert "## Strict Boundaries" in content
    assert "- Network access: prohibited." in content
    assert "- Do not auto-push or auto-merge." in content
    assert "- Do not widen scope beyond the declared task." in content
    assert "## Engineering Quality Requirements" in content
    assert "KISS: choose the minimal design" in content
    assert "Complexity: every non-trivial implementation must state expected time and space complexity." in content
    assert "Deterministic validation: tests must be reproducible" in content
    assert "Evidence-based claims: include explicit claims and non-claims" in content
    assert "## Validation Commands" in content
    assert "python3 -m pytest -q" in content
    assert "## Final Handoff Requirements" in content


def test_render_review_packet_from_leet_fixture():
    project, task, evidence = load_project_task_evidence(
        ROOT / "projects/leetcode_rotated_search/project.yaml",
        ROOT / "projects/leetcode_rotated_search/tasks/LEET-001.yaml",
        ROOT / "projects/leetcode_rotated_search/evidence/LEET-001.yaml",
    )

    content = render_review_packet_markdown(project, task, evidence)

    assert "- Task ID: LEET-001" in content
    assert "- Control-plane project ID: leetcode_rotated_search" in content
    assert "## Implemented Files" in content
    assert "src/rotated_search/search.py" in content
    assert "## Algorithm / Complexity" in content
    assert "O(log n) time, O(1) extra space." in content
    assert "## Quality Review" in content
    assert "Minimal implementation: one focused search module" in content
    assert "O(log n) time and O(1) extra space" in content
    assert "Deterministic pytest coverage" in content
    assert "## Non-Claims" in content
    assert "- No external service integration claim." in content
    assert "## Boundary Review" in content
    assert "- No network/API usage." in content


def test_render_prompt_cli_returns_zero(tmp_path):
    output_path = tmp_path / "prompt.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "control_plane.cli",
            "render-prompt",
            "--project",
            str(ROOT / "projects/leetcode_rotated_search/project.yaml"),
            "--task",
            str(ROOT / "projects/leetcode_rotated_search/tasks/LEET-001.yaml"),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    content = output_path.read_text(encoding="utf-8")
    assert "- Target branch: agent/LEET-001-rotated-search" in content
    assert "## Engineering Quality Requirements" in content
    assert "/home/a/software-dev-control-plane" in content


def test_render_review_packet_cli_returns_zero(tmp_path):
    output_path = tmp_path / "review-packet.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "control_plane.cli",
            "render-review-packet",
            "--project",
            str(ROOT / "projects/leetcode_rotated_search/project.yaml"),
            "--task",
            str(ROOT / "projects/leetcode_rotated_search/tasks/LEET-001.yaml"),
            "--evidence",
            str(ROOT / "projects/leetcode_rotated_search/evidence/LEET-001.yaml"),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    content = output_path.read_text(encoding="utf-8")
    assert "## Quality Review" in content
    assert "## Claims Supported" in content
    assert "## Non-Claims" in content
    assert "## Final Status" in content


def test_engineering_quality_requirements_template_loads():
    data = load_engineering_quality_requirements(
        ROOT / "templates/requirements/engineering_quality.yaml"
    )

    assert data["principles"]
    assert data["required_prompt_sections"]


def test_render_prompt_fails_closed_when_engineering_quality_requirements_missing(monkeypatch):
    project, task = load_project_task(
        ROOT / "projects/example_project/project.yaml",
        ROOT / "projects/example_project/tasks/EX-001.yaml",
    )

    monkeypatch.setattr(
        "control_plane.rendering.ENGINEERING_QUALITY_PATH",
        ROOT / "templates/requirements/missing_engineering_quality.yaml",
    )

    with pytest.raises(ValidationError, match="File does not exist"):
        render_prompt_markdown(project, task)
