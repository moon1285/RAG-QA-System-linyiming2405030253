class FakeLLM:
    def __init__(self):
        self.model_name = "fake-model"
    
    def generate(self, messages):
        user_content = ""
        for msg in messages:
            if msg["role"] == "user":
                user_content = msg["content"]
        
        if "你好" in user_content or "hello" in user_content.lower():
            return "你好！我是一个离线的AI助手，很高兴为你服务。我可以回答各种问题，包括自然语言处理、机器学习等相关话题。"
        elif "能做什么" in user_content or "能力" in user_content:
            return "我可以回答问题、提供信息、帮助解决问题等。由于我是离线模型，我的知识基于内置的知识库。"
        elif "自然语言处理" in user_content or "NLP" in user_content:
            return "自然语言处理（NLP）是人工智能的一个分支，致力于使计算机能够理解、解释和生成人类语言。它涉及语音识别、文本分析、机器翻译等技术。"
        elif "Transformer" in user_content or "transformer" in user_content.lower():
            return "Transformer是一种基于自注意力机制的深度学习架构，由Google在2017年提出。它包括编码器和解码器两部分，使用多头注意力机制来处理序列数据。"
        else:
            return f"这是一个离线AI的模拟回答。你的问题是：{user_content}"

def test_true_api():
    print("使用离线 FakeLLM 进行测试...")
    
    llm = FakeLLM()
    
    messages = [
        {"role": "system", "content": "你是一个友好的助手。"},
        {"role": "user", "content": "你好，请问你能做什么？"}
    ]
    
    try:
        response = llm.generate(messages)
        
        print("✓ 离线 LLM 测试成功！")
        print("模型响应：")
        print(response)
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_true_api()