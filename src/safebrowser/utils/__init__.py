"""
Utils module - Utility functions and helpers
Cross-platform qo'llab-quvvatlash

Import faqat kerak bo'lganda qiling:
    from safebrowser.utils.system import is_windows, get_models_dir
    from safebrowser.utils.helpers import init_face_analyzer
    from safebrowser.utils.graphics import create_success_pixmap
"""

# Lazy imports to avoid circular dependency issues
# Users should import directly from submodules

__all__ = [
    # helpers module
    "init_face_analyzer",
    "cosine_similarity",
    "draw_face_corners",
    # graphics module
    "create_success_pixmap",
    "create_id_card_pixmap",
    "create_lock_icon",
    # system module
    "get_platform",
    "is_windows",
    "is_linux",
    "is_macos",
    "get_platform_name",
    "get_camera_backend",
    "open_camera",
    "get_app_data_dir",
    "get_config_dir",
    "get_models_dir",
    "get_recordings_dir",
    "get_disk_with_most_free_space",
    "get_system_info",
]


def __getattr__(name):
    """Lazy import for module attributes"""
    if name in ("init_face_analyzer", "cosine_similarity", "draw_face_corners"):
        from safebrowser.utils import helpers
        return getattr(helpers, name)

    elif name in ("create_success_pixmap", "create_id_card_pixmap", "create_lock_icon"):
        from safebrowser.utils import graphics
        return getattr(graphics, name)

    elif name in (
        "get_platform", "is_windows", "is_linux", "is_macos", "get_platform_name",
        "get_camera_backend", "open_camera", "get_app_data_dir", "get_config_dir",
        "get_models_dir", "get_recordings_dir", "get_disk_with_most_free_space",
        "get_system_info"
    ):
        from safebrowser.utils import system
        return getattr(system, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
