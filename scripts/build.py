#!/usr/bin/env python
"""
Build Script for SafeBrowser
PyPI ga yuklash uchun package yaratish

Usage:
    python scripts/build.py
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).parent.parent
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
EGG_INFO = ROOT_DIR / "src" / "safebrowser.egg-info"


def clean():
    """Eski build fayllarini tozalash"""
    print("Cleaning old builds...")

    for path in [DIST_DIR, BUILD_DIR, EGG_INFO]:
        if path.exists():
            shutil.rmtree(path)
            print(f"  Removed: {path}")

    # Remove __pycache__ directories
    for pycache in ROOT_DIR.rglob("__pycache__"):
        if ".venv" not in str(pycache):
            shutil.rmtree(pycache)

    print("Clean completed!")


def check_dependencies():
    """Build dependencies tekshirish"""
    print("Checking build dependencies...")

    required = ["build", "twine"]
    missing = []

    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        subprocess.run([
            sys.executable, "-m", "pip", "install", *missing
        ], check=True)

    print("Dependencies OK!")


def build():
    """Package yaratish"""
    print("Building package...")

    os.chdir(ROOT_DIR)

    # Build using python -m build
    result = subprocess.run([
        sys.executable, "-m", "build"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        sys.exit(1)

    print(result.stdout)
    print("Build completed!")

    # Show created files
    print("\nCreated files:")
    for f in DIST_DIR.iterdir():
        size = f.stat().st_size / 1024
        print(f"  {f.name} ({size:.1f} KB)")


def check_package():
    """Package'ni tekshirish"""
    print("\nChecking package with twine...")

    result = subprocess.run([
        sys.executable, "-m", "twine", "check", "dist/*"
    ], capture_output=True, text=True)

    print(result.stdout)

    if result.returncode != 0:
        print(f"Check failed: {result.stderr}")
        return False

    print("Package check passed!")
    return True


def main():
    """Asosiy funksiya"""
    print("=" * 50)
    print("SafeBrowser Build Script")
    print("=" * 50)

    clean()
    check_dependencies()
    build()

    if check_package():
        print("\n" + "=" * 50)
        print("Build successful!")
        print("=" * 50)
        print("\nNext steps:")
        print("  1. Test locally: pip install dist/*.whl")
        print("  2. Upload to TestPyPI: python scripts/upload.py --test")
        print("  3. Upload to PyPI: python scripts/upload.py")
    else:
        print("\nBuild completed with warnings.")


if __name__ == "__main__":
    main()
