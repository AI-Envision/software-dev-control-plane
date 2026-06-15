from __future__ import annotations

from pathlib import Path

from control_plane.skills import validate_skills


def test_employer_facing_docs_exist() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    required = [
        "README.md",
        "docs/EMPLOYER_OVERVIEW.md",
        "docs/HOW_TO_USE.md",
        "docs/QUALITY_WORKFLOW.md",
        "docs/AGENT_CONTROL_MODEL.md",
    ]
    for relative in required:
        assert (repo_root / relative).is_file(), relative


def test_employer_facing_docs_include_linkedin() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    docs = [repo_root / "README.md"] + sorted((repo_root / "docs").glob("*.md"))
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "linkedin.com/in/levkantorovich" in text, str(path)


def test_readme_explains_control_plane_purpose() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    text = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "AI-assisted software development" in text
    assert "quality gates" in text
    assert "human review" in text


def test_code_quality_skill_is_present() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = validate_skills(repo_root)
    names = {skill.name for skill in skills}
    assert "code-quality-comments" in names
