import os
import requests
from dotenv import load_dotenv
from knowledge_base import KnowledgeBase

load_dotenv()

class FakeLLM:
    def __init__(self):
        self.model_name = "fake-model"
    
    def generate(self, messages, max_tokens=1024, temperature=0.7):
        user_content = ""
        context = ""
        
        for msg in messages:
            if msg["role"] == "user":
                user_content = msg["content"]
        
        lines = user_content.split('\n')
        in_context = False
        context_lines = []
        
        for line in lines:
            if line.startswith("参考文档:"):
                in_context = True
                continue
            if line.startswith("问题:"):
                in_context = False
                continue
            if in_context:
                context_lines.append(line)
        
        context = '\n'.join(context_lines).strip()
        
        if not context:
            return "文档中未找到相关答案"
        
        question_start = user_content.find("问题:")
        question = user_content[question_start+3:].strip() if question_start != -1 else ""
        
        nlp_keywords = ["自然语言处理", "NLP", "Transformer", "transformer", 
                        "情感分析", "机器翻译", "问答", "文本分类", 
                        "语音识别", "深度学习", "人工智能"]
        
        question_lower = question.lower()
        has_nlp_keyword = any(keyword.lower() in question_lower for keyword in nlp_keywords)
        
        if not has_nlp_keyword:
            return "文档中未找到相关答案"
        
        if "Transformer" in question or "transformer" in question.lower():
            return f"根据参考文档，Transformer架构是一种重要的深度学习模型。文档中提到：{context[:100]}..."
        elif "自然语言处理" in question or "NLP" in question:
            return f"自然语言处理（NLP）是人工智能的重要分支。参考文档内容：{context[:100]}..."
        elif "情感分析" in question:
            return f"情感分析是NLP的一个应用领域。文档相关内容：{context[:100]}..."
        elif "机器翻译" in question:
            return f"机器翻译是NLP的重要应用。文档相关内容：{context[:100]}..."
        elif "问答" in question:
            return f"问答系统是NLP研究的重要方向。文档相关内容：{context[:100]}..."
        else:
            return f"根据知识库内容，关于您的问题，文档中提到：{context[:150]}..."

class OllamaLLM:
    def __init__(self, model_name="qwen2:0.5b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434/api"
    
    def is_available(self):
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                model_names = [m["name"] for m in data.get("models", [])]
                return any(self.model_name in name for name in model_names)
            return False
        except:
            return False
    
    def generate(self, messages, max_tokens=1024, temperature=0.7):
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            response = requests.post(f"{self.base_url}/chat", json=payload, timeout=120)
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            else:
                return f"API调用失败: {response.status_code}"
        except Exception as e:
            return f"调用Ollama时发生错误: {str(e)}"

class RAGQA:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.kb.load_vector_store()
        
        self.ollama_llm = OllamaLLM()
        if self.ollama_llm.is_available():
            self.llm = self.ollama_llm
            print(f"✅ 使用Ollama模型: {self.llm.model_name}")
        else:
            self.llm = FakeLLM()
            print("⚠️ Ollama不可用，使用FakeLLM进行测试")
        
    def answer(self, question, chat_history=None):
        docs = self.kb.search(question, k=3)
        
        context = "\n\n".join([doc["page_content"] for doc in docs])
        
        messages = []
        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        if context.strip():
            system_prompt = """
你是一个基于知识库的问答助手。请根据提供的参考文档回答用户的问题。

重要规则：
1. 优先使用参考文档中的信息进行回答
2. 如果文档中有相关信息，请基于文档内容回答
3. 回答要简洁明了，直接针对问题
4. 如果有多个相关文档，可以综合多个文档的信息进行回答
"""
            
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            
            messages.append({
                "role": "user",
                "content": f"参考文档:\n{context}\n\n问题: {question}"
            })
        else:
            system_prompt = """
你是一个智能助手。请直接回答用户的问题。
"""
            
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            
            messages.append({
                "role": "user",
                "content": question
            })
        
        answer = self.llm.generate(messages)
        
        return answer

def main():
    rag = RAGQA()
    
    test_questions = [
        "什么是自然语言处理？",
        "Transformer架构由哪几部分组成？",
        "情感分析有哪些应用场景？",
        "机器翻译经历了哪些发展阶段？",
        "什么是问答系统？",
        "人工智能的发展历史是什么？",
        "北京的天气怎么样？"
    ]
    
    print("=== RAG问答测试 ===")
    for i, question in enumerate(test_questions):
        print(f"\n问题 {i+1}: {question}")
        answer = rag.answer(question)
        print(f"回答: {answer}")
        print("-" * 80)

if __name__ == "__main__":
    main()