def simple_chatbot(user_input):
    # 本地规则对话，无需调用API
    if "将军饮马" in user_input:
        return "将军饮马问题是经典的最短路径问题：在直线l上找一点P，使PA+PB最短。解法是作A关于l的对称点A'，连接A'B交l于P，P即为所求。"
    elif "你好" in user_input:
        return "你好呀！我是你的简易聊天机器人。"
    elif "名字" in user_input:
        return "我是本地简易Python Chatbot，不需要调用API就能运行。"
    else:
        return f"我收到你的问题：{user_input}，这是本地模拟回复~"

if __name__ == "__main__":
    print("本地简易Chatbot（输入exit退出）")
    while True:
        question = input("请输入问题：")
        if question.lower() == "exit":
            print("再见！")
            break
        reply = simple_chatbot(question)
        print("AI回答：", reply, "\n")