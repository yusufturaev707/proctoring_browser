"""
Utils module - Utility functions and helpers
Cross-platform qo'llab-quvvatlash
"""

from safebrowser.utils.helpers import (
    init_face_analyzer,
    cosine_similarity,
    draw_face_corners,
)
from safebrowser.utils.graphics import (
    create_success_pixmap,
    create_id_card_pixmap,
    create_lock_icon,
)
from safebrowser.utils.system import (
    # Platform detection
    get_platform,
    is_windows,
    is_linux,
    is_macos,
    get_platform_name,
    # Camera utilities
    get_camera_backend,
    open_camera,
    # Path utilities
    get_app_data_dir,
    get_config_dir,
    get_models_dir,
    get_recordings_dir,
    # Disk utilities
    get_disk_with_most_free_space,
    get_system_info,
)

__all__ = [
    # Face recognition
    "init_face_analyzer",
    "cosine_similarity",
    "draw_face_corners",
    # Graphics
    "create_success_pixmap",
    "create_id_card_pixmap",
    "create_lock_icon",
    # Platform detection
    "get_platform",
    "is_windows",
    "is_linux",
    "is_macos",
    "get_platform_name",
    # Camera utilities
    "get_camera_backend",
    "open_camera",
    # Path utilities
    "get_app_data_dir",
    "get_config_dir",
    "get_models_dir",
    "get_recordings_dir",
    # Disk utilities
    "get_disk_with_most_free_space",
    "get_system_info",
]
