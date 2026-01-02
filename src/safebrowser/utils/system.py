"""
System utilities - Tizim funksiyalari
Cross-platform qo'llab-quvvatlash
"""
import sys
import platform
import psutil
from pathlib import Path
from typing import Tuple, Optional


# ============================================
# Platform Detection
# ============================================

def get_platform() -> str:
    """
    Operatsion tizimni aniqlash
    Returns: 'windows', 'linux', 'darwin' (macOS)
    """
    return sys.platform


def is_windows() -> bool:
    """Windows tekshirish"""
    return sys.platform == 'win32'


def is_linux() -> bool:
    """Linux tekshirish"""
    return sys.platform.startswith('linux')


def is_macos() -> bool:
    """macOS tekshirish"""
    return sys.platform == 'darwin'


def get_platform_name() -> str:
    """Odam o'qiy oladigan platform nomi"""
    if is_windows():
        return "Windows"
    elif is_macos():
        return "macOS"
    elif is_linux():
        return "Linux"
    else:
        return platform.system()


# ============================================
# Camera Backend Selection
# ============================================

def get_camera_backend() -> int:
    """
    Platformaga mos kamera backend'ini qaytarish

    Returns:
        OpenCV VideoCapture backend constant
    """
    import cv2

    if is_windows():
        # Windows: DirectShow (DSHOW) eng yaxshi ishlaydi
        return cv2.CAP_DSHOW
    elif is_linux():
        # Linux: Video4Linux2 (V4L2)
        return cv2.CAP_V4L2
    elif is_macos():
        # macOS: AVFoundation
        return cv2.CAP_AVFOUNDATION
    else:
        # Boshqa platformalar: default backend
        return cv2.CAP_ANY


def open_camera(camera_index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
    """
    Cross-platform kamera ochish

    Args:
        camera_index: Kamera indeksi (default: 0)
        width: Frame kengligi
        height: Frame balandligi
        fps: Frames per second

    Returns:
        cv2.VideoCapture instance yoki None
    """
    import cv2

    backend = get_camera_backend()

    try:
        cap = cv2.VideoCapture(camera_index, backend)

        if not cap.isOpened():
            # Fallback: default backend bilan urinish
            print(f"Backend {backend} bilan ochilmadi, default bilan urinilmoqda...")
            cap = cv2.VideoCapture(camera_index)

        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, fps)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return cap
        else:
            print(f"Kamera {camera_index} ochilmadi")
            return None

    except Exception as e:
        print(f"Kamera ochishda xatolik: {e}")
        return None


# ============================================
# Path Utilities
# ============================================

def get_app_data_dir() -> Path:
    """
    Platformaga mos application data papkasini qaytarish
    """
    if is_windows():
        # Windows: %APPDATA%
        import os
        app_data = os.environ.get('APPDATA', '')
        if app_data:
            return Path(app_data) / 'SafeBrowser'
        return Path.home() / 'AppData' / 'Roaming' / 'SafeBrowser'
    elif is_macos():
        # macOS: ~/Library/Application Support
        return Path.home() / 'Library' / 'Application Support' / 'SafeBrowser'
    else:
        # Linux: ~/.local/share
        return Path.home() / '.local' / 'share' / 'safebrowser'


def get_config_dir() -> Path:
    """
    Platformaga mos config papkasini qaytarish
    """
    if is_windows():
        return get_app_data_dir() / 'config'
    elif is_macos():
        return Path.home() / 'Library' / 'Preferences' / 'SafeBrowser'
    else:
        # Linux: ~/.config
        return Path.home() / '.config' / 'safebrowser'


def get_models_dir() -> Path:
    """
    InsightFace modellar papkasini qaytarish
    """
    # Loyiha papkasida modellar
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    models_dir = project_root / 'insightface_models'

    # Agar mavjud bo'lsa
    if models_dir.exists():
        return models_dir

    # Aks holda app data papkasida
    app_models = get_app_data_dir() / 'models' / 'insightface'
    app_models.mkdir(parents=True, exist_ok=True)
    return app_models


def get_recordings_dir() -> Path:
    """
    Yozuvlar papkasini qaytarish
    """
    if is_windows():
        # Windows: Videos papkasi
        videos = Path.home() / 'Videos' / 'SafeBrowser'
    elif is_macos():
        # macOS: Movies papkasi
        videos = Path.home() / 'Movies' / 'SafeBrowser'
    else:
        # Linux: Videos papkasi
        videos = Path.home() / 'Videos' / 'SafeBrowser'

    videos.mkdir(parents=True, exist_ok=True)
    return videos


# ============================================
# Disk Utilities
# ============================================

def get_disk_with_most_free_space() -> Tuple[Optional[str], int]:
    """
    Eng ko'p bo'sh joy bo'lgan diskni aniqlash

    Returns:
        Tuple[path, free_bytes]
    """
    max_free = 0
    best_path = None

    partitions = psutil.disk_partitions()
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            if usage.free > max_free:
                max_free = usage.free
                best_path = part.mountpoint
        except PermissionError:
            continue

    return best_path, max_free


def get_system_info() -> dict:
    """Tizim haqida ma'lumot"""
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "memory_percent": psutil.virtual_memory().percent,
    }
