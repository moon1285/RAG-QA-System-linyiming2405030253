import requests
import json

def test_ollama_connection():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("✅ Ollama服务已连接")
            data = response.json()
            if data.get("models"):
                print("可用模型:")
                for model in data["models"]:
                    print(f"  - {model['name']}")
            else:
                print("提示: 暂无模型，请运行 `ollama pull qwen2:7b` 下载模型")
            return True
        else:
            print("❌ Ollama服务连接失败")
            print(f"状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("请确保Ollama已安装并运行: https://ollama.com/download")
        return False

def test_ollama_generate():
    try:
        payload = {
            "model": "qwen2:7b",
            "prompt": "你好，介绍一下你自己",
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Ollama生成测试成功")
            print(f"响应: {data.get('response', '')[:200]}...")
            return True
        else:
            print("❌ Ollama生成失败")
            print(f"状态码: {response.status_code}")
            print(f"错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Ollama API测试 ===")
    print("\n1. 测试连接...")
    connected = test_ollama_connection()
    
    if connected:
        print("\n2. 测试生成...")
        test_ollama_generate()
    
    print("\n提示: 如果Ollama未安装，请从 https://ollama.com/download 下载安装")
    print("下载模型命令: ollama pull qwen2:7b")