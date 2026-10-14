# Handoff：`load_all_skills()` 與 core 同一套規則

日期：2026-10-14  
專案：`C:\Users\mz038\Desktop\peas-agent\peas-agent-skills`  
上一輪只確認需求，沒有改程式。

## 下一輪要做的事

讓 `load_all_skills()` 跟 `peas-agent-core` 的 `build_system_prompt` 用同一套技能進 prompt 的規則。不要再留「學生版一律塞正文、core 版看 `always`」兩條路。

規則：

- `always: true`：正文整段放進回傳字串。frontmatter 本身不進這段。
- 沒有 `always: true`：只留 frontmatter 的名稱、`description`、路徑。正文不放進去。模型要用時再讀那份 `SKILL.md`。

使用者原話：不應該存在兩條路，`load_all_skills()` 就應該一樣。

## 現況

`load_all_skills()` 在 `src/peas_agent_skills/api.py`。它掃 `skills/` 每一份 `SKILL.md`，丟掉 frontmatter，把正文接成一段字串，不看 `always`。

core 的規則在 `C:\Users\mz038\Desktop\peas-agent\peas-agent-core\src\peas_agent\core.py` 的 `build_system_prompt`（約 1324–1339 行）：`always` 技能進 `# Active Skills`，其餘走 `build_skills_summary`。摘要格式在 `src/peas_agent_skills/loader.py` 的 `build_skills_summary`：`- **{name}** — {description} `{path}``。`list_skills()` 仍整份讀檔才能拆 frontmatter；沒標 `always` 的 body 留在 `SkillEntry.body`，不進 prompt。

實際呼叫端是 `C:\Users\mz038\Desktop\peas-agent\agentic_ai_vans\main.py` 的 `build_system_prompt`。它同時呼叫 `load_all_skills()` 和 `get_builtin_tools()`。後者預設含 `read_file`（`C:\Users\mz038\Desktop\peas-agent\peas-agent-tools\src\peas_agent_tools\registry.py`）。該檔有寫死的 API key，不要抄進文件、commit 或對話。

兩條路的由來見 `C:\Users\mz038\Desktop\peas-agent\agent-dungeon-skill-scroll-plan.md` 第 9、10 節，以及 commit `d10c4f2`（`feat(skills): add skill scroll loader and init CLI`）。第一版刻意不讓學生碰 `always` frontmatter，所以 `load_all_skills()` 直接貼正文。使用者已否決這個分叉。

## 實作時會碰到的點

- `tests/test_skills.py` 的 `test_load_all_skills_reads_project_skills` 斷言回傳含正文「一次只推進一個明確目標」。模板沒有 `always: true`，改完這行會失敗，測試要改成對應新規則。
- 五份模板在 `src/peas_agent_skills/templates/`，都是純 Markdown，沒有 YAML frontmatter，也沒有 `always`。改完之後它們只會進摘要；`description` 缺省時 `SkillsLoader` 用資料夾名。要不要補 frontmatter，上一輪沒有決定。
- `load_all_skills()` 只讀專案 `skills/`。`SkillsLoader` 還會合併 `builtin_skills/`，workspace 同名覆蓋 builtin。上一輪要求的是進 prompt 的規則相同，沒有要求這支函式改去掃 builtin。
- README、`cli.py` 的 init 提示、計畫文件都還寫「把 `load_all_skills()` 的全文放進 system prompt」。改行為時一併改會被學生看到的說明。計畫文件在專案外，沒有被要求改。
- `load_skill(name)` 仍回傳整份 `SKILL.md`。上一輪沒有要求改它。

## Suggested skills

- `C:\Users\mz038\.agents\skills\tdd\SKILL.md`：先改 `tests/test_skills.py`，讓沒有 `always` 的技能只出現摘要、`always: true` 才出現正文，再改 `load_all_skills()`。
- `C:\Users\mz038\.cursor\plugins\cache\cursor-public\superpowers\d884ae04edebef577e82ff7c4e143debd0bbec99\skills\verification-before-completion\SKILL.md`：改完跑既有測試再收尾。
