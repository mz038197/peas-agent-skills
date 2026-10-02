# peas-agent-skills

給 Agent 讀的技能卷軸。`SKILL.md` 是做事流程，不是工具程式。

## 安裝

本機開發（與 `peas-agent-core`、`agentic_ai_vans` 同一層）：

```bash
uv add --editable ../peas-agent-skills
```

發布到 GitHub 之後：

```bash
uv add git+https://github.com/mz038197/peas-agent-skills.git
```

## 學生專案

在專案根目錄執行：

```bash
uv run peas-agent-skills init
uv run peas-agent-skills list
uv run peas-agent-skills show ai-coding-helper
```

`init` 只補缺少的 `skills/<name>/SKILL.md`，已存在的檔案不覆蓋。

```python
from peas_agent_skills import load_all_skills

skills_text = load_all_skills()
```

`load_all_skills()` 讀取目前工作目錄下的 `skills/`。也可傳入專案根：`load_all_skills(project_root)`。

另外還有 `load_skill(name)` 與 `list_skills()`。

## peas-agent-core

完整 Agent 用同一個套件裡的 `SkillsLoader`：workspace 的 `skills/` 覆蓋 `builtin_skills/`，並讀 frontmatter 的 `description` 與 `always`。
