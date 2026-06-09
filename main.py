import sys
import os
import subprocess

os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'app.py')
    
    if not os.path.exists(app_path):
        print(f"错误：未找到 app.py 文件在 {script_dir}")
        input("按回车键退出...")
        return
    
    os.chdir(script_dir)
    
    import streamlit.web.cli as st_cli
    sys.argv = ["streamlit", "run", "app.py", "--server.port", "8501"]
    
    try:
        st_cli.main()
    except Exception as e:
        print(f"启动应用时发生错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()