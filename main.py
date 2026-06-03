import sys
import os

user_site = os.path.expanduser("~\\AppData\\Roaming\\Python\\Python314\\site-packages")
sys.path.insert(0, user_site)

import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py", "--server.port", "8501"]
    sys.exit(stcli.main())