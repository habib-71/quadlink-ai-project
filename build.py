"""Build a standalone QuadLink desktop application with PyInstaller."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parent
separator = ";" if sys.platform.startswith("win") else ":"

subprocess.run([
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
    "--name", "QuadLink", "--add-data", f"{ROOT / 'assets'}{separator}assets",
    str(ROOT / "src" / "main.py"),
], cwd=ROOT, check=True)
