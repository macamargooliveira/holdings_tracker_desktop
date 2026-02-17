import shutil
import subprocess
import sys

from pathlib import Path

def remove_dir(path: Path):
    if path.exists() and path.is_dir():
        print(f"Removing {path}...")
        shutil.rmtree(path)

def main():
    project_root = Path(__file__).resolve().parent.parent

    build_dir = project_root / "build"
    dist_dir = project_root / "dist"

    # Remove build artifacts
    remove_dir(build_dir)
    remove_dir(dist_dir)

    print("Running PyInstaller...")
    result = subprocess.run(
        ["poetry", "run", "pyinstaller", "HoldingsTracker.spec"],
        cwd=project_root,
    )

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
