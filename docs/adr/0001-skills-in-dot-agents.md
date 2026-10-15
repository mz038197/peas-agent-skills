# 學生端技能卷軸放在專案的 `.agents/skills/`，core 仍讀 workspace

學生 Agent 的技能卷軸改放在專案根的 `.agents/skills/<name>/SKILL.md`，對齊各家 Agent 通用的資料夾慣例；套件不再附模板，`init` 只建立這個資料夾。PEAS Agent core 繼續讀 workspace 的 `skills/` 與 `builtin_skills/`，因為 workspace（Agent 自己的家）和專案根是不同概念。兩邊共用的是「常駐技能放正文、其餘只放技能摘要」這條規則，由同一支函式產生，不是讀取位置。

## Considered Options

- core 也讀專案的 `.agents/skills/`：會把讀取位置和 workspace／專案根的界線綁在一起，另案再議。
- core 的 workspace `skills/` 改名成 `.agents/skills/`：該慣例指的是專案內資料夾，放在 workspace 裡沒有意義。
- 同時讀舊的 `skills/`：等於又多一條路；改為請學生把 `skills/` 搬到 `.agents/skills/`。
- 讀使用者家目錄的 `~/.agents/skills/`：結果會隨電腦不同而變，學生難以理解。
