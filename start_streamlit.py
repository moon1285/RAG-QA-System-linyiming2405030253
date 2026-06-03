import subprocess
import os

os.environ['STREAMLIT_FIRST_RUN'] = 'false'
subprocess.run(['py', '-m', 'streamlit', 'run', 'app.py', '--browser.gatherUsageStats=false'])