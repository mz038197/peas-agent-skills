# PEAS Agent Skills

給 Agent 讀的做事流程。學生 Agent 與 PEAS Agent core 用同一套規則決定哪些技能全文進 system prompt、哪些只留一行摘要。

## Language

**技能卷軸**:
一份寫給 Agent 照著做的流程，以 `SKILL.md` 存放在專案裡。不是工具程式。
_Avoid_: skill 檔、工具、plugin

**常駐技能**:
標記為常駐的技能卷軸；正文一律放進 system prompt。
_Avoid_: Active Skill、always 技能

**技能摘要**:
非常駐技能卷軸在 system prompt 裡的一行：名稱、描述、路徑。模型要用時再讀全文。
_Avoid_: 索引、目錄、技能清單
