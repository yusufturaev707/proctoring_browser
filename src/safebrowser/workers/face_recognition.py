"""
Face Recognition Workers
Yuzni tanib olish va tekshirish workerlari
"""
import base64
import time
import queue
import gc
import numpy as np
import cv2
import requests
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker

from safebrowser.utils.helpers import cosine_similarity
from safebrowser.services.api_client import BASE_URL


class CPUOptimizedFaceIdWorker(QThread):
    """
    Nomzod yuzini tekshirish workeri
    - Base64 rasm bilan solishtirish
    - Rate limiting
    - Memory management
    """
    result_ready = pyqtSignal(object)

    def __init__(self, app=None):
        super().__init__()
        self._running = True
        self.app = app
        self._lock = QMutex()
        self._task_queue = queue.Queue(maxsize=1)
        self.processing = False
        self.last_process_time = 0
        self.min_interval = 500
        self.process_count = 0

    def is_running(self) -> bool:
        with QMutexLocker(self._lock):
            return self._running

    def stop(self):
        with QMutexLocker(self._lock):
            self._running = False

        try:
            while not self._task_queue.empty():
                self._task_queue.get_nowait()
        except queue.Empty:
            pass

        gc.collect()
        self.wait()

    def add_task(
        self,
        image_base64: str = None,
        cropped_face=None,
        score: int = 40
    ) -> bool:
        """Yangi task qo'shish"""
        current_time = time.time() * 1000

        if current_time - self.last_process_time < self.min_interval:
            return False

        if self.processing:
            return False

        task = {
            "image_base64": image_base64,
            "cropped_face": cropped_face,
            "score": score
        }

        try:
            if not self._task_queue.empty():
                try:
                    self._task_queue.get_nowait()
                except queue.Empty:
                    pass

            self._task_queue.put_nowait(task)

            if not self.isRunning():
                self.start()

            return True
        except queue.Full:
            return False

    def _decode_base64_image(self, image_base64: str):
        """Base64 rasmni decode qilish"""
        try:
            if not image_base64 or "," not in image_base64:
                return None, "Noto'g'ri format"

            image_data = image_base64.split(",")[1]
            img_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                return None, "Rasm decode bo'lmadi"

            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), None
        except Exception as e:
            return None, str(e)

    def _get_embedding(self, image) -> tuple:
        """Rasmdan embedding olish"""
        try:
            faces = self.app.get(image)
            if not faces:
                return None, "Yuz topilmadi"
            return faces[0].embedding, None
        except Exception as e:
            return None, str(e)

    def _process_task(self, task: dict):
        """Taskni bajarish"""
        self.processing = True
        self.process_count += 1

        try:
            image_base64 = task.get("image_base64")
            cropped_face = task.get("cropped_face")
            score = task.get("score", 40)

            ps_image, error = self._decode_base64_image(image_base64)
            if error:
                self.result_ready.emit({
                    "status": "error",
                    "is_verified": False,
                    "message": error
                })
                return

            ps_embedding, error = self._get_embedding(ps_image)
            if error:
                self.result_ready.emit({
                    "status": "error",
                    "is_verified": False,
                    "message": f"Pasport rasm: {error}"
                })
                return

            live_embedding, error = self._get_embedding(cropped_face)
            if error:
                self.result_ready.emit({
                    "status": "error",
                    "is_verified": False,
                    "message": f"Live yuz: {error}"
                })
                return

            similarity = cosine_similarity(ps_embedding, live_embedding)
            similarity_percent = round(float(similarity) * 100, 2)
            is_match = 0 < score <= similarity_percent

            self.result_ready.emit({
                "status": "success",
                "is_verified": is_match,
                "similarity": similarity_percent,
                "threshold": score,
                "ps_embedding": live_embedding.tolist() if is_match else None,
                "message": f"O'xshashlik: {similarity_percent}%"
            })

        except Exception as e:
            self.result_ready.emit({
                "status": "error",
                "is_verified": False,
                "message": f"Xatolik: {e}"
            })
        finally:
            self.processing = False
            self.last_process_time = time.time() * 1000

            if self.process_count % 10 == 0:
                gc.collect()

    def run(self):
        """Asosiy loop"""
        while self.is_running():
            try:
                try:
                    task = self._task_queue.get(timeout=2)
                except queue.Empty:
                    continue

                self._process_task(task)
                self.msleep(200)

            except Exception as e:
                print(f"CPUOptimizedFaceIdWorker error: {e}")
                self.msleep(500)


class FaceIdStaffWorker(QThread):
    """
    Xodim yuzini server orqali tekshirish workeri
    """
    result_ready = pyqtSignal(object)

    def __init__(self, app=None):
        super().__init__()
        self._running = True
        self.app = app
        self._lock = QMutex()
        self.cropped_face = None

    def is_running(self) -> bool:
        with QMutexLocker(self._lock):
            return self._running

    def stop(self):
        with QMutexLocker(self._lock):
            self._running = False
        self.wait()

    def set_face(self, cropped_face=None, **kwargs):
        """Yangi yuz o'rnatish"""
        with QMutexLocker(self._lock):
            self.cropped_face = cropped_face

    def _get_face(self):
        """Thread-safe face olish"""
        with QMutexLocker(self._lock):
            face = self.cropped_face
            self.cropped_face = None
            return face

    def _verify_staff(self, face):
        """Xodimni server orqali tekshirish"""
        try:
            if face is None:
                return {"is_verified": False, "message": "Yuz topilmadi"}

            if self.app is None:
                return {"is_verified": False, "message": "Model yuklanmadi"}

            faces = self.app.get(face)
            if not faces:
                return {"is_verified": False, "message": "Yuz aniqlanmadi"}

            embedding = faces[0].embedding.tolist()

            response = requests.post(
                f"{BASE_URL}/users/face_identification/",
                json={"embedding": str(embedding)},
                timeout=10
            )

            data = response.json()

            return {
                "is_verified": data.get("verified", False),
                "message": data.get("message", "")
            }

        except requests.exceptions.Timeout:
            return {"is_verified": False, "message": "Server javob bermadi"}
        except requests.exceptions.RequestException as e:
            return {"is_verified": False, "message": f"Server xatolik: {e}"}
        except Exception as e:
            return {"is_verified": False, "message": f"Xatolik: {e}"}

    def run(self):
        """Asosiy loop"""
        while self.is_running():
            face = self._get_face()
            if face is not None:
                result = self._verify_staff(face)
                self.result_ready.emit(result)
            self.msleep(100)


class Camera1Worker(QThread):
    """
    Test vaqtida yuzni real-time tekshirish workeri
    """
    result_ready = pyqtSignal(object)

    def __init__(self, app=None):
        super().__init__()
        self._lock = QMutex()
        self.app = app
        self._running = False
        self.ps_embedding = None
        self.cropped_face = None
        self.score = 40
        self.check_timer = 10
        self.last_check_time = 0

    def is_running(self) -> bool:
        with QMutexLocker(self._lock):
            return self._running

    def stop(self):
        with QMutexLocker(self._lock):
            self._running = False
        self.wait()

    def set_face(
        self,
        ps_embedding=None,
        cropped_face=None,
        score: int = 40,
        check_timer: int = 10
    ):
        """Yangi yuz ma'lumotlarini o'rnatish"""
        with QMutexLocker(self._lock):
            if ps_embedding is not None:
                self.ps_embedding = ps_embedding
            if cropped_face is not None:
                self.cropped_face = cropped_face
            self.score = score
            self.check_timer = check_timer

            if not self._running:
                self._running = True
                self.last_check_time = 0
                if not self.isRunning():
                    self.start()

    def _get_data(self):
        """Thread-safe data olish"""
        with QMutexLocker(self._lock):
            embedding = self.ps_embedding
            face = self.cropped_face
            self.ps_embedding = None
            self.cropped_face = None
            return embedding, face

    def _verify_face(self, ps_embedding, live_face) -> dict:
        """Yuzni tekshirish"""
        try:
            if self.app is None:
                return {"is_verified": False, "message": "App not initialized"}

            faces = self.app.get(live_face)
            if not faces:
                return {"is_verified": False, "message": "Yuz topilmadi"}

            live_embedding = faces[0].embedding

            similarity = cosine_similarity(live_embedding, ps_embedding)
            similarity_percent = round(float(similarity) * 100)

            is_match = 0 < self.score <= similarity_percent

            return {
                "is_verified": is_match,
                "similarity": similarity_percent,
                "message": "Tasdiqlandi" if is_match else "Tasdiqlanmadi"
            }

        except Exception as e:
            return {"is_verified": False, "message": f"Xatolik: {e}"}

    def run(self):
        """Asosiy loop"""
        while self.is_running():
            try:
                current_time = time.time()

                if current_time - self.last_check_time >= self.check_timer:
                    self.last_check_time = current_time

                    ps_embedding, cropped_face = self._get_data()

                    if ps_embedding is None or cropped_face is None:
                        self.result_ready.emit({
                            "is_verified": False,
                            "message": "Ma'lumot yo'q"
                        })
                    else:
                        result = self._verify_face(ps_embedding, cropped_face)
                        self.result_ready.emit(result)

                self.msleep(100)

            except Exception as e:
                print(f"Camera1Worker error: {e}")
                self.msleep(500)
