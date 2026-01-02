"""
Screen Recorder Worker
Ekranni yozib olish
Cross-platform qo'llab-quvvatlash
"""
import sys
import time
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import QThread

# Platform-specific screenshot
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("pyautogui mavjud emas - ekran yozish ishlamaydi")

# Linux uchun alternative
try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False


# Local platform detection to avoid circular imports
def _is_windows() -> bool:
    return sys.platform == 'win32'


def _is_linux() -> bool:
    return sys.platform.startswith('linux')


def _is_macos() -> bool:
    return sys.platform == 'darwin'


def _get_platform_name() -> str:
    if _is_windows():
        return "Windows"
    elif _is_macos():
        return "macOS"
    elif _is_linux():
        return "Linux"
    return sys.platform


def _get_recordings_dir() -> Path:
    """Yozuvlar papkasini qaytarish"""
    if _is_windows():
        videos = Path.home() / 'Videos' / 'SafeBrowser'
    elif _is_macos():
        videos = Path.home() / 'Movies' / 'SafeBrowser'
    else:
        videos = Path.home() / 'Videos' / 'SafeBrowser'

    videos.mkdir(parents=True, exist_ok=True)
    return videos


class ScreenRecorderWorker(QThread):
    """
    Ekranni yozib oluvchi worker (cross-platform)

    Qo'llab-quvvatlanadigan platformalar:
    - Windows: pyautogui yoki mss
    - Linux: mss (pyautogui X11 talab qiladi)
    - macOS: pyautogui yoki mss
    """

    def __init__(self, filename: str = None, fps: int = 20):
        super().__init__()

        # Auto-generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            recordings_dir = _get_recordings_dir()
            self.filename = str(recordings_dir / f"recording_{timestamp}.avi")
        else:
            self.filename = filename

        self.fps = fps
        self._recording = False
        self._use_mss = False

        # Platform-specific setup
        self._setup_capture_method()

    def _setup_capture_method(self):
        """Platformaga mos capture usulini tanlash"""
        if _is_linux():
            # Linux: mss afzal (X11/Wayland muammolari kamroq)
            if MSS_AVAILABLE:
                self._use_mss = True
                print("Linux: mss ishlatiladi")
            elif PYAUTOGUI_AVAILABLE:
                self._use_mss = False
                print("Linux: pyautogui ishlatiladi (X11 talab qilinadi)")
            else:
                print("Linux: Ekran yozish uchun mss yoki pyautogui kerak")

        elif _is_macos():
            # macOS: pyautogui yaxshi ishlaydi, lekin permissions kerak
            if PYAUTOGUI_AVAILABLE:
                self._use_mss = False
                print("macOS: pyautogui ishlatiladi (Screen Recording permission kerak)")
            elif MSS_AVAILABLE:
                self._use_mss = True
                print("macOS: mss ishlatiladi")

        else:
            # Windows: pyautogui yaxshi ishlaydi
            if PYAUTOGUI_AVAILABLE:
                self._use_mss = False
                print("Windows: pyautogui ishlatiladi")
            elif MSS_AVAILABLE:
                self._use_mss = True
                print("Windows: mss ishlatiladi")

    def _get_screen_size(self) -> tuple:
        """Ekran o'lchamini olish"""
        if self._use_mss and MSS_AVAILABLE:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                return (monitor['width'], monitor['height'])
        elif PYAUTOGUI_AVAILABLE:
            return pyautogui.size()
        else:
            return (1920, 1080)  # Default fallback

    def _capture_screen(self):
        """Ekranni suratga olish"""
        if self._use_mss and MSS_AVAILABLE:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                img = sct.grab(monitor)
                frame = np.array(img)
                # mss BGRA formatda qaytaradi
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                return frame
        elif PYAUTOGUI_AVAILABLE:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        else:
            return None

    def run(self):
        """Asosiy recording loop"""
        if not PYAUTOGUI_AVAILABLE and not MSS_AVAILABLE:
            print(f"Screen recording not available on {_get_platform_name()}")
            return

        print(f"Screen recording started: {self.filename}")
        print(f"Platform: {_get_platform_name()}, Method: {'mss' if self._use_mss else 'pyautogui'}")

        try:
            screen_size = self._get_screen_size()

            # Video codec selection (cross-platform)
            if _is_windows():
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
            elif _is_macos():
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            else:
                # Linux
                fourcc = cv2.VideoWriter_fourcc(*'XVID')

            out = cv2.VideoWriter(self.filename, fourcc, self.fps, screen_size)

            self._recording = True
            while self._recording:
                frame = self._capture_screen()
                if frame is not None:
                    # Resize if needed
                    h, w = frame.shape[:2]
                    if (w, h) != screen_size:
                        frame = cv2.resize(frame, screen_size)
                    out.write(frame)
                time.sleep(1 / self.fps)

            out.release()
            print(f"Screen recording stopped: {self.filename}")

        except Exception as e:
            print(f"Screen recording error: {e}")

    def stop(self):
        self._recording = False
        self.wait()
