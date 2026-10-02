from pathlib import Path

from peas_agent_skills import SkillsLoader, list_skills, load_all_skills, load_skill
from peas_agent_skills.cli import init_skills, main


def test_cli_init_reports_created_and_skipped(tmp_path: Path, capsys) -> None:
    assert main(["--cwd", str(tmp_path), "init"]) == 0
    out = capsys.readouterr().out
    assert "Skill Scrolls unlocked!" in out
    assert "✅ Created skills/ai-coding-helper/SKILL.md" in out
    assert "load_all_skills()" in out

    skill = tmp_path / "skills" / "debug-helper" / "SKILL.md"
    skill.write_text("student edit\n", encoding="utf-8")
    assert main(["--cwd", str(tmp_path), "init"]) == 0
    skipped = capsys.readouterr().out
    assert "⚠️ Skipped skills/debug-helper/SKILL.md because it already exists" in skipped
    assert skill.read_text(encoding="utf-8") == "student edit\n"
    assert "ai-coding-helper" in list_skills(tmp_path)


def test_init_does_not_overwrite(tmp_path: Path) -> None:
    created, skipped = init_skills(tmp_path)
    assert "skills/ai-coding-helper/SKILL.md" in created
    assert skipped == []

    target = tmp_path / "skills" / "debug-helper" / "SKILL.md"
    target.write_text("student edit\n", encoding="utf-8")
    created_again, skipped_again = init_skills(tmp_path)
    assert created_again == []
    assert "skills/debug-helper/SKILL.md" in skipped_again
    assert target.read_text(encoding="utf-8") == "student edit\n"


def test_load_all_skills_reads_project_skills(tmp_path: Path) -> None:
    init_skills(tmp_path)
    text = load_all_skills(tmp_path)
    assert "## ai-coding-helper" in text
    assert "一次只推進一個明確目標" in text
    assert load_skill("missing", tmp_path) is None


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
