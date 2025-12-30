"""
System utilities - Tizim funksiyalari
"""
import psutil
from typing import Tuple, Optional


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
