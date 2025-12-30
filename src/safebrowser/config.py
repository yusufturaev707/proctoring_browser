"""
Configuration Management
Dastur sozlamalari
"""
import os
import configparser
from pathlib import Path
from typing import Optional


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "config.ini"

# Default values
DEFAULTS = {
    "app": {
        "name": "SafeBrowser",
        "version": "2.0.0",
        "debug": "false",
    },
    "api": {
        "base_url": "http://localhost:8000/api/v1",
        "timeout": "15",
    },
    "face_recognition": {
        "detection_size": "640",
        "similarity_threshold": "40",
        "check_interval": "10",
    },
    "camera": {
        "width": "640",
        "height": "480",
        "fps": "30",
    },
    "recording": {
        "enabled": "true",
        "fps": "20",
        "format": "XVID",
    },
}


class Config:
    """Dastur sozlamalarini boshqarish"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Konfiguratsiyani yuklash"""
        self._config = configparser.ConfigParser()

        # Default qiymatlarni o'rnatish
        for section, options in DEFAULTS.items():
            self._config[section] = options

        # Fayl mavjud bo'lsa, o'qish
        if CONFIG_FILE.exists():
            self._config.read(CONFIG_FILE)

    def save(self):
        """Konfiguratsiyani saqlash"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            self._config.write(f)

    def get(self, section: str, key: str, fallback: str = None) -> Optional[str]:
        """Qiymat olish"""
        return self._config.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Integer qiymat olish"""
        return self._config.getint(section, key, fallback=fallback)

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Boolean qiymat olish"""
        return self._config.getboolean(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        """Qiymat o'rnatish"""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = str(value)

    # Shortcut properties
    @property
    def api_base_url(self) -> str:
        return self.get("api", "base_url")

    @property
    def api_timeout(self) -> int:
        return self.getint("api", "timeout", 15)

    @property
    def detection_size(self) -> int:
        return self.getint("face_recognition", "detection_size", 640)

    @property
    def similarity_threshold(self) -> int:
        return self.getint("face_recognition", "similarity_threshold", 40)

    @property
    def check_interval(self) -> int:
        return self.getint("face_recognition", "check_interval", 10)

    @property
    def camera_width(self) -> int:
        return self.getint("camera", "width", 640)

    @property
    def camera_height(self) -> int:
        return self.getint("camera", "height", 480)

    @property
    def camera_fps(self) -> int:
        return self.getint("camera", "fps", 30)

    @property
    def recording_enabled(self) -> bool:
        return self.getboolean("recording", "enabled", True)

    @property
    def recording_fps(self) -> int:
        return self.getint("recording", "fps", 20)


# Singleton instance
config = Config()
