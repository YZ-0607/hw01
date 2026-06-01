# 📝 Meeting Minutes Formatter Skill

## 📌 项目简介
这是一个结合了 Prompt Engineering 与 Python 编程的 AI 技能（Skill）。它能将零散、口语化的会议速记，自动转化为结构清晰、重点突出的标准 Markdown 会议纪要。

## 🛠️ 核心文件说明
- **SKILL.md**: 定义了 AI 的触发条件、思考逻辑和输出规范（Prompt 层）。
- **src/skill.py**: 实现了文本清洗、正则提取和格式化输出的具体业务逻辑（代码层）。

## 🚀 如何运行
1. 克隆本仓库：`git clone https://github.com/你的用户名/meeting-minutes-skill.git`
2. 运行测试脚本：
```bash
python src/skill.py