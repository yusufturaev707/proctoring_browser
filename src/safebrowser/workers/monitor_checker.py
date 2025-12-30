"""
Monitor Checker Worker
Qo'shimcha monitorlarni aniqlash (cheating prevention)
"""
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QGuiApplication


class MonitorWorker(QThread):
    """Qo'shimcha monitorlarni aniqlovchi worker"""
    result = pyqtSignal(bool)

    def __init__(self, interval: int = 5):
        super().__init__()
        self.interval = interval
        self._running = True
        self.last_status = None

    @staticmethod
    def check_cheating_monitor() -> bool:
        """Qo'shimcha monitor borligini tekshirish"""
        try:
            screens = QGuiApplication.screens()
            return len(screens) > 1
        except Exception as e:
            print(f"Monitor check error: {e}")
            return False

    def run(self):
        while self._running:
            status = self.check_cheating_monitor()
            if status != self.last_status:
                self.last_status = status
                self.result.emit(status)
            self.msleep(self.interval * 1000)

    def stop(self):
        self._running = False
        self.wait()
