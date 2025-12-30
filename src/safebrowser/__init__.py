"""
SafeBrowser - Online Test Proctoring System
Face ID asosida online test proctoring tizimi
"""

__version__ = "2.0.0"
__author__ = "SafeBrowser Team"
__all__ = ["SafeBrowserApp", "__version__", "__author__"]


def __getattr__(name):
    """Lazy import for heavy modules"""
    if name == "SafeBrowserApp":
        from safebrowser.app import SafeBrowserApp
        return SafeBrowserApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
