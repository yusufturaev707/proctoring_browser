"""
Screen Recorder Worker
Ekranni yozib olish
"""
import time
import cv2
import numpy as np
import pyautogui
from PyQt6.QtCore import QThread


class ScreenRecorderWorker(QThread):
    """Ekranni yozib oluvchi worker"""

    def __init__(self, filename: str = 'recording.avi', fps: int = 20):
        super().__init__()
        self.filename = filename
        self.fps = fps
        self._recording = False

    def run(self):
        print(f"Screen recording started: {self.filename}")
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.filename, fourcc, self.fps, screen_size)

        self._recording = True
        while self._recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            time.sleep(1 / self.fps)

        out.release()
        print("Screen recording stopped")

    def stop(self):
        self._recording = False
        self.wait()
