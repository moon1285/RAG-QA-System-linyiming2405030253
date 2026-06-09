import sys
import os

os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

from streamlit.web.cli import main
if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(main())