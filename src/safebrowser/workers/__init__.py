"""
Workers module - Background threads and workers
"""

from safebrowser.workers.camera_checker import CameraCheckerWorker
from safebrowser.workers.face_detector import FaceDetectorWorker
from safebrowser.workers.face_recognition import (
    CPUOptimizedFaceIdWorker,
    FaceIdStaffWorker,
    Camera1Worker
)
from safebrowser.workers.internet_checker import InternetCheckWorker
from safebrowser.workers.monitor_checker import MonitorWorker
from safebrowser.workers.screen_recorder import ScreenRecorderWorker
from safebrowser.workers.loader import AppLoaderWorker, TestLoaderWorker

__all__ = [
    "CameraCheckerWorker",
    "FaceDetectorWorker",
    "CPUOptimizedFaceIdWorker",
    "FaceIdStaffWorker",
    "Camera1Worker",
    "InternetCheckWorker",
    "MonitorWorker",
    "ScreenRecorderWorker",
    "AppLoaderWorker",
    "TestLoaderWorker",
]
