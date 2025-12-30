"""
Camera Checker Worker
Kamera holatini tekshirish
"""
import cv2
import time
import socket
from urllib.parse import urlparse
from PyQt6.QtCore import QThread, pyqtSignal


class CameraCheckerWorker(QThread):
    """Kamera mavjudligini tekshiruvchi worker"""
    status_signal = pyqtSignal(dict)

    def __init__(
        self,
        interval: int = 5,
        ip_camera_url: str = "rtsp://admin:D12345678n@192.168.1.25:554/Streaming/Channels/101"
    ):
        super().__init__()
        self.interval = interval
        self.running = True
        self.ip_camera_url = ip_camera_url

    def is_ip_camera_online(self) -> bool:
        """IP kamerani tekshirish"""
        try:
            parsed = urlparse(self.ip_camera_url)
            ip = parsed.hostname
            port = parsed.port or 554
            with socket.create_connection((ip, port), timeout=2):
                return True
        except Exception:
            return False

    def run(self):
        while self.running:
            # Local kamerani tekshirish
            cap = cv2.VideoCapture(0)
            local_camera = cap.isOpened()
            cap.release()

            data = {
                'local_camera': local_camera,
                'ip_camera': self.is_ip_camera_online()
            }

            self.status_signal.emit(data)
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.wait()
