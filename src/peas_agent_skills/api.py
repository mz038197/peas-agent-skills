"""Read a project's skills/ folder for a system prompt."""

from __future__ import annotations

from pathlib import Path

from peas_agent_skills.loader import split_frontmatter

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def skills_root(root: Path | None = None) -> Path:
    base = Path.cwd() if root is None else Path(root)
    return base / "skills"


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
    chunks: list[str] = []
    for name in list_skill_names(root):
        text = load_skill(name, root)
        if text is None:
            continue
        _, body = split_frontmatter(text)
        content = (body or text).strip()
        if not content:
            continue
        chunks.append(f"## {name}\n\n{content}")
    return "\n\n".join(chunks)
