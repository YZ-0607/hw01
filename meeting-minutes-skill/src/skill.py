import re
import json
from datetime import datetime

class MeetingMinutesSkill:
    """
    会议纪要结构化整理 Skill 的 Python 执行逻辑
    """
    def __init__(self):
        self.name = "meeting-minutes-formatter"
    
    def execute(self, raw_text: str) -> str:
        """
        接收原始会议记录文本，返回格式化后的 Markdown 字符串
        """
        # 1. 提取基本信息 (使用简单的正则匹配作为演示)
        time_match = re.search(r'(今天|明天|\d{1,2}点|\d{1,2}:\d{2})', raw_text)
        meeting_time = time_match.group(0) if time_match else "[待补充]"
        
        # 简单的人名提取逻辑（假设中文名为2-3个字）
        people_match = re.findall(r'[\u4e00-\u9fa5]{2,3}(?=说|觉得|负责|在)', raw_text)
        attendees = "、".join(list(set(people_match))) if people_match else "[待补充]"
        
        # 2. 提取会议主题 (简单取前10个字作为主题)
        topic = raw_text.split('。')[0][:15] + "..."
        
        # 3. 提取待办事项 (寻找包含"负责"、"去"等关键词的句子)
        action_items = []
        sentences = re.split(r'[。；;]', raw_text)
        for sentence in sentences:
            if "负责" in sentence or "去" in sentence or "下周" in sentence:
                # 简单的负责人提取
                owner_match = re.search(r'([\u4e00-\u9fa5]{2,3})', sentence)
                owner = owner_match.group(0) if owner_match else "待定"
                action_items.append({
                    "task": sentence.strip(),
                    "owner": owner,
                    "deadline": "待定"
                })

        # 4. 生成 Markdown 格式输出
        markdown_output = self._generate_markdown(topic, meeting_time, attendees, action_items)
        return markdown_output

    def _generate_markdown(self, topic, time, attendees, actions):
        """生成最终的 Markdown 字符串"""
        md = f"""### 📅 {topic}
- **时间**：{time}
- **参会人**：{attendees}

#### 核心议题与讨论
- (此处由大模型根据原始文本进行语义总结...)

#### 📝 待办事项 (Action Items)
| 任务描述 | 负责人 | 截止时间 |
| :--- | :--- | :--- |
"""
        for action in actions:
            md += f"| {action['task']} | {action['owner']} | {action['deadline']} |\n"
        
        return md

# --- 测试代码 ---
if __name__ == "__main__":
    # 实例化 Skill
    skill = MeetingMinutesSkill()
    
    # 模拟输入数据
    mock_input = "今天下午3点开了个产品评审会，老张、小李和我都在。老张觉得蓝色背景太丑，建议换成白色。最后决定下周一再对一下UI细节。老张负责去催设计图。"
    
    # 执行并打印结果
    print("--- 原始输入 ---")
    print(mock_input)
    print("\n--- Python Skill 处理后的输出 ---")
    result = skill.execute(mock_input)
    print(result)