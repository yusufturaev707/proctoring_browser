#!/usr/bin/env python
"""
SafeBrowser Runner
Dasturni ishga tushirish uchun asosiy fayl

Usage:
    python run.py

Or with the new structure:
    python -m safebrowser
"""
import sys
import os

# src papkasini path'ga qo'shish
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def main():
    """Asosiy funksiya"""
    from src.safebrowser.app import SafeBrowserApp
    app = SafeBrowserApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
