from __future__ import annotations

from pathlib import Path

from control_plane.skills import validate_skills


def test_governance_skills_are_present() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = validate_skills(repo_root)
    names = {skill.name for skill in skills}

    assert "kiss-engineering" in names
    assert "algorithmic-efficiency" in names


def test_governance_document_exists_and_names_core_rules() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    doc = repo_root / "governance" / "KISS_AND_ALGORITHMIC_EFFICIENCY.md"

    text = doc.read_text(encoding="utf-8")

    assert "KISS Engineering" in text
    assert "Algorithmic Efficiency" in text
    assert "simple enough to review" in text
    assert "efficient enough for expected scale" in text


def test_governance_skill_descriptions_are_routing_triggers() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    skills = validate_skills(repo_root)
    by_name = {skill.name: skill for skill in skills}

    assert by_name["kiss-engineering"].description.startswith("Load when")
    assert by_name["algorithmic-efficiency"].description.startswith("Load when")
