from pathlib import Path

from peas_agent_skills import SkillsLoader, list_skills, load_all_skills, load_skill
from peas_agent_skills.cli import main


def test_cli_init_creates_skills_folder(tmp_path: Path, capsys) -> None:
    assert main(["--cwd", str(tmp_path), "init"]) == 0
    out = capsys.readouterr().out
    assert "✅ Created .agents/skills/" in out
    assert "description" in out
    assert "always" in out
    assert (tmp_path / ".agents" / "skills").is_dir()
    assert list_skills(tmp_path) == []


def test_cli_init_leaves_existing_folder_alone(tmp_path: Path, capsys) -> None:
    _write_skill(tmp_path, "debug-helper", "student edit\n")
    (tmp_path / "skills").mkdir()
    assert main(["--cwd", str(tmp_path), "init"]) == 0
    out = capsys.readouterr().out
    assert "⚠️ .agents/skills/ already exists" in out
    assert "move its skills into .agents/skills/" in out
    skill = tmp_path / ".agents" / "skills" / "debug-helper" / "SKILL.md"
    assert skill.read_text(encoding="utf-8") == "student edit\n"
    assert list_skills(tmp_path) == ["debug-helper"]


def _write_skill(root: Path, name: str, text: str) -> None:
    folder = root / ".agents" / "skills" / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(text, encoding="utf-8")


def test_load_all_skills_lists_other_skills_as_summary(tmp_path: Path) -> None:
    _write_skill(
        tmp_path,
        "debug-helper",
        "---\ndescription: 需要找出並修掉一個 bug 時\n---\n一次只改一個假設。\n",
    )
    text = load_all_skills(tmp_path)
    assert (
        "- **debug-helper** — 需要找出並修掉一個 bug 時 "
        "`.agents/skills/debug-helper/SKILL.md`"
    ) in text
    assert "read_file" in text
    assert "一次只改一個假設" not in text
    assert load_skill("missing", tmp_path) is None


def test_load_all_skills_puts_always_on_skill_body(tmp_path: Path) -> None:
    _write_skill(
        tmp_path,
        "house-rules",
        "---\nalways: true\ndescription: 每次都要遵守\n---\n回答前先確認需求。\n",
    )
    text = load_all_skills(tmp_path)
    assert "### Skill: house-rules\n\n回答前先確認需求。" in text
    assert "always: true" not in text
    assert "`.agents/skills/house-rules/SKILL.md`" not in text


def test_workspace_skill_overrides_builtin(tmp_path: Path) -> None:
    builtin = tmp_path / "builtin_skills" / "always-on"
    builtin.mkdir(parents=True)
    (builtin / "SKILL.md").write_text(
        "---\nalways: true\ndescription: builtin\n---\nwoof\n",
        encoding="utf-8",
    )
    custom = tmp_path / "skills" / "always-on"
    custom.mkdir(parents=True)
    (custom / "SKILL.md").write_text(
        "---\nalways: true\ndescription: custom\n---\nstudent\n",
        encoding="utf-8",
    )

    entries = {e.name: e for e in SkillsLoader(tmp_path).list_skills()}
    assert entries["always-on"].source == "workspace"
    assert entries["always-on"].description == "custom"
    assert "student" in entries["always-on"].body
