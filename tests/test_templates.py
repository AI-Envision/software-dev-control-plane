import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from control_plane.templates import init_target, load_template
from control_plane.validation import ValidationError, load_yaml, validate_project, validate_task


ROOT = Path(__file__).resolve().parents[1]


def test_python_package_template_loads():
    data = load_template("python_package")
    assert data["language"] == "python"
    assert "src/{{package_name}}/main.py" in data["files"]


def test_cpp_cli_template_loads():
    data = load_template("cpp_cli")
    assert data["language"] == "cpp"
    assert "CMakeLists.txt" in data["files"]


def test_missing_template_fails_clearly():
    with pytest.raises(ValidationError, match="File does not exist"):
        load_template("missing_template")


def test_malformed_template_fails_clearly(tmp_path):
    broken_root = tmp_path / "project_types"
    broken_dir = broken_root / "broken"
    broken_dir.mkdir(parents=True)
    (broken_dir / "template.yaml").write_text("id: broken\nlanguage: python\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="missing required fields"):
        load_template("broken", broken_root)


def test_init_target_creates_expected_python_files_and_yaml(tmp_path):
    target_repo = tmp_path / "python-target"
    project_yaml = tmp_path / "python-project.yaml"
    task_yaml = tmp_path / "python-task.yaml"

    summary = init_target(
        template_id="python_package",
        project_id="demo-python.project",
        project_name="demo-python-project",
        target_repo=target_repo,
        output_project_yaml=project_yaml,
        output_task_yaml=task_yaml,
    )

    expected_files = {
        ".gitignore",
        "README.md",
        "CONTROL_PLANE.md",
        "pyproject.toml",
        "src/demo_python_project/__init__.py",
        "src/demo_python_project/main.py",
        "tests/test_smoke.py",
    }
    assert set(summary["files_written"]) == expected_files
    assert summary["template_id"] == "python_package"
    assert (target_repo / "README.md").read_text(encoding="utf-8").count("Engineering Quality Requirements") == 1
    assert "KISS / minimal design" in (target_repo / "CONTROL_PLANE.md").read_text(encoding="utf-8")
    assert "*.py[cod]" in (target_repo / ".gitignore").read_text(encoding="utf-8")
    assert "demo-python-project: minimal deterministic python scaffold" in (
        target_repo / "src/demo_python_project/main.py"
    ).read_text(encoding="utf-8")

    project_data = load_yaml(project_yaml)
    task_data = load_yaml(task_yaml)
    validate_project(project_data)
    validate_task(task_data)
    assert project_data["languages"] == ["python"]
    assert task_data["allowed_files"] == [
        ".gitignore",
        "README.md",
        "CONTROL_PLANE.md",
        "pyproject.toml",
        "src/**",
        "tests/**",
    ]
    assert any("evidence-based" in item for item in task_data["required_outputs"])


def test_init_target_creates_expected_cpp_files_and_yaml(tmp_path):
    target_repo = tmp_path / "cpp-target"
    project_yaml = tmp_path / "cpp-project.yaml"
    task_yaml = tmp_path / "cpp-task.yaml"

    summary = init_target(
        template_id="cpp_cli",
        project_id="demo_cpp_project",
        project_name="demo-cpp-project",
        target_repo=target_repo,
        output_project_yaml=project_yaml,
        output_task_yaml=task_yaml,
    )

    expected_files = {
        ".gitignore",
        "README.md",
        "CONTROL_PLANE.md",
        "CMakeLists.txt",
        "src/main.cpp",
        "tests/test_smoke.cpp",
    }
    assert set(summary["files_written"]) == expected_files
    cmake_text = (target_repo / "CMakeLists.txt").read_text(encoding="utf-8")
    assert "set(CMAKE_CXX_STANDARD 17)" in cmake_text
    assert "include(CTest)" in cmake_text
    assert "add_test(NAME demo_cpp_project_smoke COMMAND demo_cpp_project_smoke)" in cmake_text
    test_text = (target_repo / "tests/test_smoke.cpp").read_text(encoding="utf-8")
    assert "#include <cassert>" in test_text
    assert "assert(" in test_text
    assert "Engineering Quality Requirements" in (target_repo / "README.md").read_text(encoding="utf-8")
    assert "compile_commands.json" in (target_repo / ".gitignore").read_text(encoding="utf-8")

    project_data = load_yaml(project_yaml)
    task_data = load_yaml(task_yaml)
    validate_project(project_data)
    validate_task(task_data)
    assert project_data["languages"] == ["cpp"]
    assert task_data["allowed_files"] == [
        ".gitignore",
        "README.md",
        "CONTROL_PLANE.md",
        "CMakeLists.txt",
        "src/**",
        "include/**",
        "tests/**",
    ]
    assert any("deterministic" in item.lower() for item in task_data["reality_check"])


def test_init_target_refuses_to_overwrite_non_empty_directory_without_force(tmp_path):
    target_repo = tmp_path / "target"
    target_repo.mkdir()
    (target_repo / "existing.txt").write_text("keep", encoding="utf-8")

    with pytest.raises(ValidationError, match="not empty"):
        init_target(
            template_id="python_package",
            project_id="demo_python_project",
            project_name="demo-python-project",
            target_repo=target_repo,
        )


def test_init_target_force_overwrites_non_empty_directory(tmp_path):
    target_repo = tmp_path / "target"
    target_repo.mkdir()
    (target_repo / "existing.txt").write_text("old", encoding="utf-8")

    init_target(
        template_id="python_package",
        project_id="demo_python_project",
        project_name="demo-python-project",
        target_repo=target_repo,
        force=True,
    )

    assert not (target_repo / "existing.txt").exists()
    assert (target_repo / "README.md").is_file()


def test_cli_init_target_returns_zero_for_python_example(tmp_path):
    target_repo = tmp_path / "python-cli-target"
    project_yaml = tmp_path / "python-cli-project.yaml"
    task_yaml = tmp_path / "python-cli-task.yaml"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "control_plane.cli",
            "init-target",
            "--template",
            "python_package",
            "--project-id",
            "demo_python_project",
            "--name",
            "demo-python-project",
            "--package-name",
            "demo_python_project",
            "--target-repo",
            str(target_repo),
            "--output-project-yaml",
            str(project_yaml),
            "--output-task-yaml",
            str(task_yaml),
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["template_id"] == "python_package"
    assert data["target_repo"] == str(target_repo)
    assert "README.md" in data["files_written"]


def test_cli_init_target_returns_zero_for_cpp_example(tmp_path):
    target_repo = tmp_path / "cpp-cli-target"
    project_yaml = tmp_path / "cpp-cli-project.yaml"
    task_yaml = tmp_path / "cpp-cli-task.yaml"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "control_plane.cli",
            "init-target",
            "--template",
            "cpp_cli",
            "--project-id",
            "demo_cpp_project",
            "--name",
            "demo-cpp-project",
            "--package-name",
            "demo_cpp_project",
            "--target-repo",
            str(target_repo),
            "--output-project-yaml",
            str(project_yaml),
            "--output-task-yaml",
            str(task_yaml),
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["template_id"] == "cpp_cli"
    assert data["target_repo"] == str(target_repo)
    assert "CMakeLists.txt" in data["files_written"]
