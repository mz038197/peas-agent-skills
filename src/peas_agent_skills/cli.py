"""peas-agent-skills init | list | show"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from peas_agent_skills.api import TEMPLATES_DIR, list_skill_names, load_skill, skills_root


def init_skills(root: Path) -> tuple[list[str], list[str]]:
    """Copy bundled templates into skills/. Existing SKILL.md files are left alone."""
    created: list[str] = []
    skipped: list[str] = []
    destination = skills_root(root)
    destination.mkdir(parents=True, exist_ok=True)

    if not TEMPLATES_DIR.is_dir():
        return created, skipped

    for source_dir in sorted(TEMPLATES_DIR.iterdir(), key=lambda p: p.name):
        skill_file = source_dir / "SKILL.md"
        if not source_dir.is_dir() or not skill_file.is_file():
            continue
        target = destination / source_dir.name / "SKILL.md"
        rel = target.relative_to(root).as_posix()
        if target.is_file():
            skipped.append(rel)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_file, target)
        created.append(rel)
    return created, skipped


def _cmd_init(root: Path) -> int:
    created, skipped = init_skills(root)
    print("Skill Scrolls unlocked!")
    print()
    for rel in created:
        print(f"✅ Created {rel}")
    for rel in skipped:
        print(f"⚠️ Skipped {rel} because it already exists")
    if not created and not skipped:
        print("No skill templates found in the package.")
        return 1
    print()
    print("Your Agent can now read these skills with load_all_skills().")
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

    sub.add_parser("init", help="Create missing skills/*/SKILL.md from templates")
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
