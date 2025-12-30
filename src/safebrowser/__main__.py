"""
SafeBrowser Entry Point
python -m safebrowser
"""
import sys


def main():
    """Entry point"""
    from safebrowser.app import SafeBrowserApp
    app = SafeBrowserApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
