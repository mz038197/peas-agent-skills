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
```

`init` 建立 `.agents/skills/`；資料夾已存在就不動。套件不附技能模板，技能卷軸自己寫：

```
.agents/skills/debug-helper/SKILL.md
```

```markdown
---
description: 程式行為跟預期不一樣，需要找出並修掉一個 bug 時
---
# Skill：除錯

1. 先重現問題。
2. 一次只改一個假設。
```

寫好之後可以檢查：

```bash
uv run peas-agent-skills list
uv run peas-agent-skills show debug-helper
```

frontmatter 兩個欄位：

- `description`：一行，告訴 Agent 什麼時候該讀這份技能。沒寫就只顯示資料夾名稱。
- `always: true`：常駐技能，正文每次都放進 system prompt。沒寫就只放一行技能摘要（名稱、描述、路徑），Agent 要用時再用 `read_file` 讀全文。

```python
from peas_agent_skills import load_all_skills

skills_text = load_all_skills()
```

`load_all_skills()` 讀取目前工作目錄下的 `.agents/skills/`。也可傳入專案根：`load_all_skills(project_root)`。不讀舊的 `skills/`，也不讀家目錄的 `~/.agents/skills/`；舊專案請把 `skills/` 搬到 `.agents/skills/`。

另外還有 `load_skill(name)` 與 `list_skills()`。

## peas-agent-core

完整 Agent 用同一個套件裡的 `SkillsLoader`：workspace 的 `skills/` 覆蓋 `builtin_skills/`。常駐技能與技能摘要的組法由 `build_skills_prompt(entries)` 產生，與 `load_all_skills()` 相同。讀取位置為何不同見 `docs/adr/0001-skills-in-dot-agents.md`。
