"""
App and Test Loader Workers
Model va testlarni yuklash
"""
import requests
from PyQt6.QtCore import QThread, pyqtSignal

from src.safebrowser.utils.helpers import init_face_analyzer
from src.safebrowser.services.api_client import BASE_URL


class AppLoaderWorker(QThread):
    """
    InsightFace modelni background'da yuklash
    """
    app = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.loaded_app = None

    def run(self):
        try:
            gpu_id = self._detect_best_device()

            self.loaded_app = init_face_analyzer(
                det_size=(640, 640),
                gpu_id=gpu_id
            )
            self.app.emit({"app": self.loaded_app, "status": True})
        except Exception as e:
            print(f"AppLoaderWorker error: {e}")
            self.app.emit({"app": None, "status": False, "error": str(e)})

    def _detect_best_device(self) -> int:
        """
        Eng yaxshi qurilmani aniqlash
        Returns: 0+ = GPU, -1 = CPU
        """
        try:
            import onnxruntime as ort
            providers = ort.get_available_providers()
            print(f"Mavjud providerlar: {providers}")

            # NVIDIA GPU (CUDA)
            if 'CUDAExecutionProvider' in providers:
                print("GPU (NVIDIA CUDA) topildi - GPU ishlatiladi")
                return 0

            # AMD GPU (DirectML - Windows)
            if 'DmlExecutionProvider' in providers:
                print("GPU (DirectML) topildi - GPU ishlatiladi")
                return 0

            # Intel GPU (OpenVINO)
            if 'OpenVINOExecutionProvider' in providers:
                print("GPU (OpenVINO) topildi - GPU ishlatiladi")
                return 0

            print("GPU topilmadi - CPU ishlatiladi")
            return -1

        except Exception as e:
            print(f"Device detection xatosi: {e} - CPU ishlatiladi")
            return -1


class TestLoaderWorker(QThread):
    """
    Server'dan testlar ro'yxatini yuklash
    """
    result = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            res = requests.get(f"{BASE_URL}/load-tests/", timeout=15)

            if res.status_code in [400, 404, 500, 502]:
                self.result.emit({
                    "status": False,
                    "result": [],
                    "message": "Server bilan bog'lanishda muammo!"
                })
                return

            res_data = res.json()

            if res_data.get('status') == 'success':
                tests = res_data.get('data', [])
                self.result.emit({
                    "status": True,
                    "result": tests,
                    "message": "Muvaffaqiyatli yuklandi"
                })
            else:
                self.result.emit({
                    "status": False,
                    "result": [],
                    "message": res_data.get('message', 'Xatolik')
                })

        except requests.exceptions.Timeout:
            self.result.emit({
                "status": False,
                "result": [],
                "message": "Server javob bermadi (timeout)"
            })
        except requests.exceptions.RequestException as e:
            self.result.emit({
                "status": False,
                "result": [],
                "message": f"Ulanish xatoligi: {e}"
            })
        except Exception as e:
            self.result.emit({
                "status": False,
                "result": [],
                "message": f"Xatolik: {e}"
            })
