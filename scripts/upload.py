#!/usr/bin/env python
"""
Upload Script for SafeBrowser
PyPI ga package yuklash

Usage:
    python scripts/upload.py          # Upload to PyPI
    python scripts/upload.py --test   # Upload to TestPyPI
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).parent.parent
DIST_DIR = ROOT_DIR / "dist"

# PyPI URLs
PYPI_URL = "https://upload.pypi.org/legacy/"
TEST_PYPI_URL = "https://test.pypi.org/legacy/"


def check_dist():
    """dist/ papkasini tekshirish"""
    if not DIST_DIR.exists():
        print("Error: dist/ directory not found!")
        print("Run 'python scripts/build.py' first.")
        sys.exit(1)

    files = list(DIST_DIR.glob("*"))
    if not files:
        print("Error: No distribution files found!")
        print("Run 'python scripts/build.py' first.")
        sys.exit(1)

    print("Found distribution files:")
    for f in files:
        print(f"  {f.name}")

    return files


def upload(test: bool = False):
    """PyPI ga yuklash"""
    files = check_dist()

    if test:
        print("\n" + "=" * 50)
        print("Uploading to TestPyPI...")
        print("=" * 50)
        repository_url = TEST_PYPI_URL
        repo_name = "testpypi"
    else:
        print("\n" + "=" * 50)
        print("Uploading to PyPI...")
        print("=" * 50)
        repository_url = PYPI_URL
        repo_name = "pypi"

    # Confirm upload
    if not test:
        response = input("\nAre you sure you want to upload to PyPI? (y/N): ")
        if response.lower() != 'y':
            print("Upload cancelled.")
            sys.exit(0)

    # Upload using twine
    cmd = [
        sys.executable, "-m", "twine", "upload",
        "--repository-url", repository_url,
        "dist/*"
    ]

    print(f"\nRunning: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print(f"\nUpload failed!")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Upload successful!")
    print("=" * 50)

    if test:
        print("\nTest installation:")
        print("  pip install --index-url https://test.pypi.org/simple/ safebrowser")
    else:
        print("\nInstallation:")
        print("  pip install safebrowser")


def setup_pypirc():
    """~/.pypirc faylini tekshirish va sozlash"""
    pypirc_path = Path.home() / ".pypirc"

    if pypirc_path.exists():
        print(f"Found existing .pypirc at {pypirc_path}")
        return

    print("\n" + "=" * 50)
    print("PyPI Configuration Setup")
    print("=" * 50)
    print("\nYou need to configure PyPI credentials.")
    print("You can either:")
    print("  1. Create API token at https://pypi.org/manage/account/token/")
    print("  2. Use username/password (not recommended)")

    create = input("\nWould you like to create .pypirc now? (y/N): ")
    if create.lower() != 'y':
        print("\nYou can create it manually at ~/.pypirc")
        return

    print("\nEnter your PyPI API token (starts with 'pypi-'):")
    token = input("Token: ").strip()

    if not token.startswith("pypi-"):
        print("Warning: Token should start with 'pypi-'")

    pypirc_content = f"""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = {token}

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = {token}
"""

    with open(pypirc_path, 'w') as f:
        f.write(pypirc_content)

    # Set permissions (Unix only)
    try:
        os.chmod(pypirc_path, 0o600)
    except:
        pass

    print(f"\nCreated {pypirc_path}")
    print("You can now upload packages to PyPI!")


def main():
    parser = argparse.ArgumentParser(description="Upload SafeBrowser to PyPI")
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Upload to TestPyPI instead of PyPI"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup PyPI credentials (~/.pypirc)"
    )

    args = parser.parse_args()

    if args.setup:
        setup_pypirc()
        return

    upload(test=args.test)


if __name__ == "__main__":
    main()
