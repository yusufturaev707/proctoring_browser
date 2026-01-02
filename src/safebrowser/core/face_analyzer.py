"""
Face Analyzer - InsightFace wrapper
Yuzni aniqlash va tanib olish
Cross-platform qo'llab-quvvatlash
"""
import numpy as np
from typing import Optional, Tuple, List
from insightface.app import FaceAnalysis


class FaceAnalyzer:
    """
    InsightFace FaceAnalysis wrapper class
    """

    def __init__(self, det_size: Tuple[int, int] = (640, 640), gpu_id: int = -1):
        self.det_size = det_size
        self.gpu_id = gpu_id
        self._app = None
        self._initialized = False

    def initialize(self) -> bool:
        """Modelni ishga tushirish (cross-platform)"""
        # Lazy import to avoid circular dependency
        from safebrowser.utils.system import get_models_dir

        # Cross-platform models directory
        models_path = str(get_models_dir())
        print(f"InsightFace models path: {models_path}")

        try:
            if self.gpu_id >= 0:
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            else:
                providers = ['CPUExecutionProvider']

            self._app = FaceAnalysis(
                providers=providers,
                root=models_path,
                allowed_modules=['detection', 'recognition']
            )
            self._app.prepare(ctx_id=self.gpu_id, det_size=self.det_size)

            self._initialized = True
            print(f"FaceAnalyzer initialized: det_size={self.det_size}, gpu_id={self.gpu_id}")
            return True

        except Exception as e:
            print(f"FaceAnalyzer init error: {e}")
            # Fallback - CPU only
            try:
                self._app = FaceAnalysis(
                    providers=['CPUExecutionProvider'],
                    root=models_path
                )
                self._app.prepare(ctx_id=-1, det_size=(320, 320))
                self._initialized = True
                return True
            except Exception as fallback_error:
                print(f"Fallback init error: {fallback_error}")
                return False

    @property
    def app(self):
        """InsightFace app instance"""
        return self._app

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    def detect_faces(self, image: np.ndarray) -> List:
        """Yuzlarni aniqlash"""
        if not self._initialized or self._app is None:
            return []

        try:
            return self._app.get(image)
        except Exception as e:
            print(f"Face detection error: {e}")
            return []

    def get_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Rasmdan embedding olish"""
        faces = self.detect_faces(image)
        if not faces:
            return None
        return faces[0].embedding

    def get_largest_face(self, image: np.ndarray) -> Optional[dict]:
        """Eng katta yuzni olish"""
        faces = self.detect_faces(image)
        if not faces:
            return None

        largest = max(
            faces,
            key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
        )

        return {
            "bbox": largest.bbox.astype(int).tolist(),
            "embedding": largest.embedding,
            "det_score": float(largest.det_score),
        }

    @staticmethod
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Ikki embedding o'rtasidagi o'xshashlik"""
        if embedding1 is None or embedding2 is None:
            return 0.0

        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(np.dot(embedding1, embedding2) / (norm1 * norm2))

    def compare_faces(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
        threshold: float = 0.4
    ) -> Tuple[bool, float]:
        """
        Ikki rasmdagi yuzlarni solishtirish

        Returns:
            (is_match, similarity_score)
        """
        emb1 = self.get_embedding(image1)
        emb2 = self.get_embedding(image2)

        if emb1 is None or emb2 is None:
            return False, 0.0

        similarity = self.cosine_similarity(emb1, emb2)
        is_match = similarity >= threshold

        return is_match, similarity

    @staticmethod
    def detect_best_device() -> int:
        """
        Eng yaxshi qurilmani aniqlash
        Returns: 0+ = GPU, -1 = CPU
        """
        try:
            import onnxruntime as ort
            providers = ort.get_available_providers()

            if 'CUDAExecutionProvider' in providers:
                return 0
            if 'DmlExecutionProvider' in providers:
                return 0
            if 'OpenVINOExecutionProvider' in providers:
                return 0

            return -1
        except Exception:
            return -1
