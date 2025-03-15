import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Now import from src package
from src import test

if __name__ == "__main__":
    test.app.run(host="::0", port=5201, debug=True)