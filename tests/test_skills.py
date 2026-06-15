from __future__ import annotations

from pathlib import Path

from control_plane.skills import discover_skills, format_skill_index, validate_skills


def test_skills_are_discoverable() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = validate_skills(repo_root)
    names = {skill.name for skill in skills}

    assert "repository-safety" in names
    assert "task-execution" in names
    assert "quality-gates" in names
    assert "agent-handoff" in names
    assert "context-management" in names


def test_skill_descriptions_are_short_routing_triggers() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = discover_skills(repo_root)

    assert skills
    for skill in skills:
        assert len(skill.description) <= 1024
        assert "Load when" in skill.description


def test_skill_index_contains_names_and_descriptions() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = validate_skills(repo_root)
    index = format_skill_index(skills)

    assert "repository-safety:" in index
    assert "quality-gates:" in index
    assert "Load when" in index
