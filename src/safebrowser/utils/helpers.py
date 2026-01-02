"""
Helper Functions for Face Recognition
InsightFace asosidagi yordamchi funksiyalar
Cross-platform qo'llab-quvvatlash
"""
import cv2
import numpy as np
from PyQt6.QtGui import QImage
from insightface.app import FaceAnalysis

from src.safebrowser.utils.system import get_models_dir


def init_face_analyzer(det_size: tuple = (640, 640), gpu_id: int = -1):
    """
    InsightFace FaceAnalysis modelini ishga tushirish (cross-platform)

    Args:
        det_size: Detection size (kichikroq = tezroq, lekin kamroq aniqlik)
        gpu_id: -1 = CPU, 0+ = GPU

    Returns:
        FaceAnalysis app instance
    """
    # Cross-platform models directory
    models_path = str(get_models_dir())

    try:
        if gpu_id >= 0:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        else:
            providers = ['CPUExecutionProvider']

        app = FaceAnalysis(
            providers=providers,
            root=models_path,
            allowed_modules=['detection', 'recognition']
        )
        app.prepare(ctx_id=gpu_id, det_size=det_size)

        print(f"FaceAnalysis initialized: det_size={det_size}, gpu_id={gpu_id}")
        return app
    except Exception as e:
        print(f"FaceAnalysis init error: {e}")
        app = FaceAnalysis(
            providers=['CPUExecutionProvider'],
            root=models_path
        )
        app.prepare(ctx_id=-1, det_size=(320, 320))
        return app


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Ikki embedding o'rtasidagi cosine similarity hisoblash

    Args:
        embedding1: Birinchi yuz embeddingi
        embedding2: Ikkinchi yuz embeddingi

    Returns:
        Similarity score (0-1 oralig'ida)
    """
    if embedding1 is None or embedding2 is None:
        return 0.0

    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return np.dot(embedding1, embedding2) / (norm1 * norm2)


def ready_frame_for_gui(frame: np.ndarray) -> QImage:
    """
    OpenCV frame'ni PyQt6 QImage'ga o'tkazish

    Args:
        frame: BGR formatdagi OpenCV frame

    Returns:
        QImage formatdagi rasm
    """
    if frame is None:
        return QImage()

    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w

    return QImage(
        rgb_image.data,
        w, h,
        bytes_per_line,
        QImage.Format.Format_RGB888
    )


def resize_frame(frame: np.ndarray, max_width: int = 640, max_height: int = 480) -> np.ndarray:
    """
    Frame'ni maksimal o'lchamga moslashtirish
    """
    if frame is None:
        return None

    h, w = frame.shape[:2]

    if w <= max_width and h <= max_height:
        return frame

    scale = min(max_width / w, max_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)


def crop_face_with_margin(
    frame: np.ndarray,
    bbox: tuple,
    margin_x: int = 25,
    margin_y: int = 40
) -> np.ndarray:
    """
    Yuzni margin bilan kesib olish
    """
    if frame is None or bbox is None:
        return None

    h, w = frame.shape[:2]
    x1, y1, x2, y2 = bbox

    x1 = max(0, x1 - margin_x)
    y1 = max(0, y1 - margin_y)
    x2 = min(w, x2 + margin_x)
    y2 = min(h, y2 + margin_y)

    return frame[y1:y2, x1:x2].copy()


def draw_face_corners(
    frame: np.ndarray,
    bbox: tuple,
    color: tuple = (0, 200, 100),
    thickness: int = 2,
    corner_length: int = 20
) -> np.ndarray:
    """
    Yuz atrofiga zamonaviy burchak ramkalari chizish
    """
    if frame is None or bbox is None:
        return frame

    x1, y1, x2, y2 = bbox

    # Yuqori chap
    cv2.line(frame, (x1, y1), (x1 + corner_length, y1), color, thickness)
    cv2.line(frame, (x1, y1), (x1, y1 + corner_length), color, thickness)

    # Yuqori o'ng
    cv2.line(frame, (x2, y1), (x2 - corner_length, y1), color, thickness)
    cv2.line(frame, (x2, y1), (x2, y1 + corner_length), color, thickness)

    # Pastki chap
    cv2.line(frame, (x1, y2), (x1 + corner_length, y2), color, thickness)
    cv2.line(frame, (x1, y2), (x1, y2 - corner_length), color, thickness)

    # Pastki o'ng
    cv2.line(frame, (x2, y2), (x2 - corner_length, y2), color, thickness)
    cv2.line(frame, (x2, y2), (x2, y2 - corner_length), color, thickness)

    return frame


def get_largest_face(faces: list):
    """Eng katta yuzni tanlash"""
    if not faces:
        return None
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))


def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    """Embeddingni normalize qilish"""
    if embedding is None:
        return None

    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding

    return embedding / norm
