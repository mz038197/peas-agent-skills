"""Read a project's .agents/skills/ folder for a system prompt."""

from __future__ import annotations

from pathlib import Path

from peas_agent_skills.loader import SkillsLoader, build_skills_prompt


def skills_root(root: Path | None = None) -> Path:
    base = Path.cwd() if root is None else Path(root)
    return base / ".agents" / "skills"


def list_skill_names(root: Path | None = None) -> list[str]:
    folder = skills_root(root)
    if not folder.is_dir():
        return []
    names: list[str] = []
    for skill_dir in sorted(folder.iterdir(), key=lambda p: p.name):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
            names.append(skill_dir.name)
    return names


def list_skills(root: Path | None = None) -> list[str]:
    return list_skill_names(root)


def load_skill(name: str, root: Path | None = None) -> str | None:
    path = skills_root(root) / name / "SKILL.md"
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def load_all_skills(root: Path | None = None) -> str:
    base = Path.cwd() if root is None else Path(root)
    loader = SkillsLoader(base, skills_dir=skills_root(base), include_builtin=False)
    return build_skills_prompt(loader.list_skills())
