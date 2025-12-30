"""
Internet Connection Checker Worker
Internet ulanishini tekshirish
"""
import socket
from PyQt6.QtCore import QThread, pyqtSignal


class InternetCheckWorker(QThread):
    """Internet ulanishini tekshiruvchi worker"""
    status_changed = pyqtSignal(bool)

    def __init__(self, interval: int = 10):
        super().__init__()
        self.interval = interval
        self._running = True
        self.last_status = None

    def stop(self):
        self._running = False
        self.wait()

    @staticmethod
    def check_connection() -> bool:
        """Internet ulanishini tekshirish"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def run(self):
        while self._running:
            status = self.check_connection()
            if status != self.last_status:
                self.last_status = status
                self.status_changed.emit(status)
            self.msleep(self.interval * 1000)
