"""peas-agent-skills init | list | show"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from peas_agent_skills.api import list_skill_names, load_skill, skills_root

SKILL_FORMAT_HINT = """\
Add a skill as .agents/skills/<name>/SKILL.md, for example:

---
description: When the Agent should use this skill
---
# Steps the Agent should follow

description: one line telling the Agent when to read this skill.
always: true puts the whole skill into the system prompt every time;
otherwise the Agent only sees name, description and path, and reads the file when needed.

Your Agent reads these skills with load_all_skills().
An old skills/ folder is no longer read: move its skills into .agents/skills/."""


def _cmd_init(root: Path) -> int:
    folder = skills_root(root)
    if folder.is_dir():
        print("⚠️ .agents/skills/ already exists")
        if (root / "skills").is_dir():
            print("An old skills/ folder is no longer read: move its skills into .agents/skills/.")
        return 0
    folder.mkdir(parents=True)
    print("✅ Created .agents/skills/")
    print()
    print(SKILL_FORMAT_HINT)
    return 0


def _cmd_list(root: Path) -> int:
    names = list_skill_names(root)
    if not names:
        print("No skills yet. Run: peas-agent-skills init")
        return 0
    for name in names:
        print(name)
    return 0


def _cmd_show(root: Path, name: str) -> int:
    text = load_skill(name, root)
    if text is None:
        print(f"Skill not found: {name}", file=sys.stderr)
        return 1
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Skill scrolls for a student Agent project")
    parser.add_argument("--cwd", default="", help="Project root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create .agents/skills/ if it is missing")
    sub.add_parser("list", help="List skill folder names")
    show = sub.add_parser("show", help="Print one SKILL.md")
    show.add_argument("name")

    args = parser.parse_args(argv)
    root = Path(args.cwd).resolve() if args.cwd else Path.cwd()

    if args.command == "init":
        return _cmd_init(root)
    if args.command == "list":
        return _cmd_list(root)
    return _cmd_show(root, args.name)


if __name__ == "__main__":
    raise SystemExit(main())
