"""Load SKILL.md directories. Workspace skills override builtin skills of the same name."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SkillEntry:
    name: str
    path: str
    source: str
    description: str
    always: bool
    body: str


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    end: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()

    body = "\n".join(lines[end + 1 :]).strip()
    return meta, body


class SkillsLoader:
    def __init__(
        self,
        workspace: Path,
        *,
        builtin_dir: Path | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.workspace_skills = self.workspace / "skills"
        self.builtin_skills = (
            builtin_dir.resolve() if builtin_dir else self.workspace / "builtin_skills"
        )

    def _skill_path_for_read(self, skill_file: Path) -> str:
        resolved = skill_file.resolve()
        try:
            return resolved.relative_to(self.workspace).as_posix()
        except ValueError:
            if self.builtin_skills is not None:
                return resolved.relative_to(self.builtin_skills.parent).as_posix()
            return resolved.as_posix()

    def _entries_from_dir(
        self, root: Path, source: str, skip: set[str]
    ) -> list[SkillEntry]:
        if not root.exists():
            return []

        entries: list[SkillEntry] = []
        for skill_dir in sorted(root.iterdir(), key=lambda p: p.name):
            skill_file = skill_dir / "SKILL.md"
            if not skill_dir.is_dir() or not skill_file.is_file():
                continue
            if skill_dir.name in skip:
                continue

            text = skill_file.read_text(encoding="utf-8")
            meta, body = split_frontmatter(text)
            name = skill_dir.name
            description = meta.get("description") or name
            always = meta.get("always", "false").lower() == "true"
            rel_path = self._skill_path_for_read(skill_file)
            entries.append(
                SkillEntry(name, rel_path, source, description, always, body)
            )
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(
            self.workspace_skills, "workspace", set()
        )
        if self.builtin_skills is None:
            return workspace_entries

        workspace_names = {entry.name for entry in workspace_entries}
        builtin_entries = self._entries_from_dir(
            self.builtin_skills, "builtin", workspace_names
        )
        return workspace_entries + builtin_entries

    def load_skill(self, name: str) -> str | None:
        roots = [self.workspace_skills]
        if self.builtin_skills is not None:
            roots.append(self.builtin_skills)
        for root in roots:
            path = root / name / "SKILL.md"
            if path.is_file():
                return path.read_text(encoding="utf-8")
        return None


def build_skills_summary(entries: list[SkillEntry]) -> str:
    summarized = [e for e in entries if not e.always]
    if not summarized:
        return ""
    lines = [f"- **{e.name}** — {e.description} `{e.path}`" for e in summarized]
    return "\n".join(lines)
