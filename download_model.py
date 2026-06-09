import requests
import json

def download_model(model_name):
    print(f"正在下载模型: {model_name}")
    print("这可能需要一些时间，请耐心等待...")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/pull',
            json={'name': model_name},
            stream=True
        )
        
        if response.status_code != 200:
            print(f"下载失败，状态码: {response.status_code}")
            return False
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    status = data.get('status', '')
                    digest = data.get('digest', '')
                    total = data.get('total', 0)
                    completed = data.get('completed', 0)
                    
                    if status:
                        print(f"\r状态: {status}", end='')
                        if total > 0:
                            progress = (completed / total) * 100
                            print(f" | 进度: {progress:.1f}%", end='')
                        else:
                            print(f" | {digest}", end='')
                except:
                    pass
        
        print("\n✅ 模型下载完成！")
        return True
    
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        return False

if __name__ == "__main__":
    download_model("qwen2:7b")