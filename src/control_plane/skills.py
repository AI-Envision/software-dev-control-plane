from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path


class SkillValidationError(ValueError):
    pass


def _parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SkillValidationError(f"{path}: missing front matter")
    try:
        _before, fm, _body = text.split("---", 2)
    except ValueError as exc:
        raise SkillValidationError(f"{path}: invalid front matter") from exc

    data: dict[str, str] = {}
    for raw in fm.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise SkillValidationError(f"{path}: invalid metadata line: {raw!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def discover_skills(root: str | Path) -> list[Skill]:
    repo_root = Path(root).resolve()
    skills_root = repo_root / "skills"
    if not skills_root.exists():
        return []

    skills: list[Skill] = []
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        meta = _parse_front_matter(skill_md)
        name = meta.get("name", "")
        description = meta.get("description", "")

        if not name:
            raise SkillValidationError(f"{skill_md}: missing name")
        if not description:
            raise SkillValidationError(f"{skill_md}: missing description")
        if len(description) > 1024:
            raise SkillValidationError(f"{skill_md}: description too long")
        if name != skill_md.parent.name:
            raise SkillValidationError(f"{skill_md}: name must match directory")

        skills.append(Skill(name=name, description=description, path=skill_md))
    return skills


def validate_skills(root: str | Path) -> list[Skill]:
    skills = discover_skills(root)
    if not skills:
        raise SkillValidationError(f"{Path(root).resolve()}: no skills found")
    return skills


def format_skill_index(skills: Iterable[Skill]) -> str:
    return "\n".join(f"{s.name}: {s.description}" for s in skills)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and list control-plane skills.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)

    try:
        skills = validate_skills(args.root)
    except SkillValidationError as exc:
        print(f"skills_invalid: {exc}")
        return 1

    print(f"skills_valid: {len(skills)}")
    print(format_skill_index(skills))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
