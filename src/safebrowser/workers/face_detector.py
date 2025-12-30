"""
Face Detector Worker
InsightFace asosidagi yuz aniqlash
"""
import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker
from PyQt6.QtGui import QImage


class FaceDetectorWorker(QThread):
    """
    InsightFace asosidagi yuz aniqlash worker
    - Kam CPU/GPU resurs ishlatadi
    - Real-time kamera stream uchun optimallashtirilgan
    """
    face_detected = pyqtSignal(object)

    def __init__(self, app=None, camera_index: int = 0):
        super().__init__()
        self._running = True
        self._lock = QMutex()

        self.app = app
        self.camera_index = camera_index

        # Performance settings
        self.frame_skip = 2
        self.frame_counter = 0
        self.last_face_box = None
        self.detection_size = (320, 320)

        # Camera settings
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480

    def set_app(self, app):
        """InsightFace app'ni o'rnatish"""
        self.app = app

    def is_running(self) -> bool:
        with QMutexLocker(self._lock):
            return self._running

    def stop(self):
        with QMutexLocker(self._lock):
            self._running = False
        self.wait()
        print("Face Detector Worker stopped")

    def _init_camera(self) -> bool:
        """Kamerani ishga tushirish"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                print(f"Camera {self.camera_index} ochilmadi")
                return False

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FPS, 30)

            print(f"Camera {self.camera_index} initialized")
            return True
        except Exception as e:
            print(f"Camera init error: {e}")
            return False

    def _detect_face_insightface(self, frame: np.ndarray):
        """InsightFace yordamida yuz aniqlash"""
        if self.app is None:
            return None, None

        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.app.get(rgb_frame)

            if not faces:
                return None, None

            # Eng katta yuzni tanlash
            best_face = max(
                faces,
                key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
            )

            bbox = best_face.bbox.astype(int)
            x1, y1, x2, y2 = bbox

            # Margin qo'shish
            h, w = frame.shape[:2]
            margin_x, margin_y = 25, 40
            x1 = max(0, x1 - margin_x)
            y1 = max(0, y1 - margin_y)
            x2 = min(w, x2 + margin_x)
            y2 = min(h, y2 + margin_y)

            cropped_face = frame[y1:y2, x1:x2].copy()
            return (x1, y1, x2, y2), cropped_face

        except Exception as e:
            print(f"Face detection error: {e}")
            return None, None

    def _draw_face_box(self, frame: np.ndarray, box: tuple):
        """Yuz atrofiga ramka chizish"""
        if box is None:
            return frame

        x1, y1, x2, y2 = box
        color = (0, 200, 100)
        thickness = 2
        corner_length = 20

        # Burchaklar
        cv2.line(frame, (x1, y1), (x1 + corner_length, y1), color, thickness)
        cv2.line(frame, (x1, y1), (x1, y1 + corner_length), color, thickness)
        cv2.line(frame, (x2, y1), (x2 - corner_length, y1), color, thickness)
        cv2.line(frame, (x2, y1), (x2, y1 + corner_length), color, thickness)
        cv2.line(frame, (x1, y2), (x1 + corner_length, y2), color, thickness)
        cv2.line(frame, (x1, y2), (x1, y2 - corner_length), color, thickness)
        cv2.line(frame, (x2, y2), (x2 - corner_length, y2), color, thickness)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_length), color, thickness)

        return frame

    def _frame_to_qimage(self, frame: np.ndarray) -> QImage:
        """OpenCV frame'ni QImage'ga o'tkazish"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        return QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

    def run(self):
        """Asosiy thread loop"""
        if not self._init_camera():
            print("Camera initialization failed")
            return

        print("Face Detector Worker started")

        while self.is_running():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.msleep(10)
                    continue

                self.frame_counter += 1
                cropped_face = None
                face_box = None

                # Frame skip
                if self.frame_counter % self.frame_skip == 0:
                    face_box, cropped_face = self._detect_face_insightface(frame)
                    if face_box:
                        self.last_face_box = face_box
                else:
                    face_box = self.last_face_box

                display_frame = self._draw_face_box(frame.copy(), face_box)
                qt_image = self._frame_to_qimage(display_frame)

                self.face_detected.emit({
                    "image": qt_image,
                    "crop_face": cropped_face,
                    "has_face": face_box is not None
                })

                self.msleep(33)

            except Exception as e:
                print(f"Frame processing error: {e}")
                self.msleep(50)

        if self.cap:
            self.cap.release()
        print("Face Detector Worker finished")
