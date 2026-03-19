import sys
from pathlib import Path

# Add src to python path to allow absolute imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from ui.windows.main_window import main

if __name__ == "__main__":
    main()
