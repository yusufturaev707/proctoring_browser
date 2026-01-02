"""
Main Window - Asosiy oyna
Bu fayl legacy main.py dan re-export qiladi va yangi strukturaga bridge vazifasini bajaradi
"""
import sys
import os

# Legacy main.py ni import qilish uchun path qo'shish
# Bu vaqtinchalik yechim - keyinchalik to'liq migratsiya qilinadi
_legacy_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if _legacy_path not in sys.path:
    sys.path.insert(0, _legacy_path)

# Yangi strukturadan import
from safebrowser.ui.styles import get_full_stylesheet, COLORS
from safebrowser.ui.dialogs import InfoModal, ExitDialog
from safebrowser.ui.generated_ui import Ui_MainWindow
from safebrowser.workers import (
    CameraCheckerWorker,
    FaceDetectorWorker,
    CPUOptimizedFaceIdWorker,
    FaceIdStaffWorker,
    Camera1Worker,
    InternetCheckWorker,
    MonitorWorker,
    ScreenRecorderWorker,
    AppLoaderWorker,
    TestLoaderWorker,
)
from safebrowser.utils.graphics import (
    create_success_pixmap,
    create_id_card_pixmap,
    create_lock_icon,
)
from safebrowser.utils.system import get_disk_with_most_free_space
from safebrowser.services.api_client import APIClient, BASE_URL
from safebrowser.core.face_analyzer import FaceAnalyzer
from safebrowser.utils.system import is_windows, is_linux, is_macos, get_platform_name

# PyQt6 imports
import configparser
import requests
import cv2

# Platform-specific keyboard blocking
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("keyboard moduli mavjud emas - tugmalarni bloklash ishlamaydi")

from PyQt6.QtCore import Qt, QUrl, QRegularExpression, pyqtSlot
from PyQt6.QtGui import (
    QPixmap, QRegularExpressionValidator, QImage, QPainter,
    QColor, QFont, QPen, QBrush, QLinearGradient
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QLabel, QDialog,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QGraphicsDropShadowEffect,
)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    SafeBrowser asosiy oynasi
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Apply modern stylesheet
        self.setStyleSheet(get_full_stylesheet())

        # Material Design background
        self.stack.setStyleSheet("""
            QStackedWidget#stack {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f4f8,
                    stop:0.3 #d1e8f0,
                    stop:0.6 #c9dde8,
                    stop:1 #b8d4e3);
            }
        """)

        # Initialize
        self._init_keys()
        self._init_validators()
        self._init_variables()
        self._init_workers()
        self._init_ui_components()
        self._connect_signals()

        # Show window after all initialization is complete
        self.showFullScreen()

    def _init_keys(self):
        """
        Klaviatura tugmalarini bloklash (cross-platform)

        Windows: keyboard kutubxonasi yaxshi ishlaydi
        Linux: root/sudo talab qiladi
        macOS: Accessibility permissions talab qiladi
        """
        if not KEYBOARD_AVAILABLE:
            print(f"Keyboard blocking not available on {get_platform_name()}")
            return

        try:
            if is_windows():
                # Windows: to'liq bloklash
                keys_to_block = ['alt', 'tab', 'win', 'f4', 'caps lock', 'print screen']
                for key in keys_to_block:
                    try:
                        keyboard.block_key(key)
                    except Exception as e:
                        print(f"Cannot block {key}: {e}")
                print("Windows klaviatura tugmalari bloklandi")

            elif is_linux():
                # Linux: faqat root da ishlaydi
                import os
                is_root = False
                try:
                    is_root = os.geteuid() == 0
                except AttributeError:
                    # geteuid Windows da mavjud emas
                    is_root = False

                if is_root:
                    keys_to_block = ['alt', 'tab', 'print_screen']
                    for key in keys_to_block:
                        try:
                            keyboard.block_key(key)
                        except Exception:
                            pass
                    print("Linux klaviatura tugmalari bloklandi (root)")
                else:
                    print("Linux: Tugmalarni bloklash uchun root kerak")

            elif is_macos():
                # macOS: keyboard library cheklangan ishlaydi
                # Accessibility permissions kerak
                print("macOS: Tugmalarni bloklash qo'llab-quvvatlanmaydi")
                # macOS da boshqa yechim - PyObjC ishlatish mumkin
                # lekin bu qo'shimcha dependency talab qiladi

            else:
                print(f"Platform {get_platform_name()}: Tugmalarni bloklash qo'llab-quvvatlanmaydi")

        except Exception as e:
            print(f"Block keys error: {e}")

    def _init_validators(self):
        """Input validatorlarini o'rnatish"""
        regex = QRegularExpression(r'^[3-6][0-9]{13}$')
        validator = QRegularExpressionValidator(regex)
        self.input_pinfl.setValidator(validator)

    def _init_variables(self):
        """O'zgaruvchilarni boshlash"""
        self.msg_box = None
        self.quit = False
        self.webview = None
        self.modal = InfoModal(self)

        self.stack.setCurrentIndex(0)
        self.current_index_page = 0

        # User data
        self.im = None
        self.image_base64 = None
        self.cropped_face = None
        self.score = 0
        self.ps_embedding = None
        self.test_name = None
        self.is_verified = False
        self.chosen_test_key = None
        self.warning_text = None
        self.app = None
        self.face_analyzer = None
        self.state = None

        # Settings
        self.is_detect_monitor = None
        self.is_check_face_staff = None
        self.is_detect_camera = None
        self.is_check_face_candidate = None
        self.is_screen_record = None
        self.is_face_identification = None
        self.timer_face_id = None

        # Admin password
        self.admin_password = self._load_admin_password()

    def _init_workers(self):
        """Worker'larni boshlash"""
        self.checker_internet_worker = InternetCheckWorker(interval=5)
        self.checker_internet_worker.status_changed.connect(self._on_internet_status)
        self.checker_internet_worker.start()

        self.checker_monitor_worker = MonitorWorker(interval=1)
        self.checker_camera_worker = CameraCheckerWorker(interval=3)

        self.face_detector_worker = None
        self.face_identification_worker = None
        self.face_staff_worker = None
        self.screen_recorder_worker = None
        self.load_app_worker = None
        self.test_loader_worker = None

        # InsightFace modelini yuklash
        self._init_face_analyzer()

    def _init_face_analyzer(self):
        """InsightFace modelini yuklash"""
        try:
            print("InsightFace modeli yuklanmoqda...")
            self.face_analyzer = FaceAnalyzer(det_size=(320, 320), gpu_id=-1)

            if self.face_analyzer.initialize():
                self.app = self.face_analyzer.app
                print("InsightFace modeli muvaffaqiyatli yuklandi!")
            else:
                self.app = None
                print("InsightFace modelini yuklashda xatolik!")
        except Exception as e:
            print(f"FaceAnalyzer init error: {e}")
            self.app = None
            self.face_analyzer = None

    def _init_ui_components(self):
        """UI komponentlarini sozlash"""
        self.camera1_widget = None

        self.camera_face_label = QLabel()
        self.camera_face_label.setFixedSize(240, 180)
        self.camera_face_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_face_label.setStyleSheet("""
            QLabel {
                border: 2px solid #22c55e;
                border-radius: 14px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.95),
                    stop:1 rgba(15, 23, 42, 0.95));
            }
        """)

        # ID card design
        self._setup_id_card()

        # Load tests
        self._load_tests()

    def _connect_signals(self):
        """Signal-slot ulanishlar"""
        self.btn_check_im.clicked.connect(self._on_check_pinfl)
        self.btn_candidate_next.clicked.connect(self._on_candidate_continue)
        self.btn_candidate_next.hide()
        self.btn_next_page.clicked.connect(self._on_staff_face_page)
        self.btn_start_test.clicked.connect(self._on_start_test)

    def _load_admin_password(self) -> str:
        """Admin parolini yuklash"""
        try:
            config = configparser.ConfigParser()
            # Try new config location first
            config_paths = [
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', 'config.ini'),
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.ini'),
            ]

            for config_path in config_paths:
                if os.path.exists(config_path):
                    config.read(config_path)
                    return config.get('AUTH', 'admin_password', fallback="")

            return ""
        except Exception as e:
            print(f"Config error: {e}")
            return ""

    def _setup_id_card(self):
        """ID karta dizaynini sozlash"""
        try:
            id_card = create_id_card_pixmap(340, 220)
            self.label_4.setPixmap(id_card)
            self.label_4.setScaledContents(False)
            self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_4.setStyleSheet("background: transparent; border: none;")
        except Exception as e:
            print(f"ID card setup error: {e}")

    def _load_tests(self):
        """Testlarni yuklash"""
        try:
            self.test_loader_worker = TestLoaderWorker()
            self.test_loader_worker.result.connect(self._on_tests_loaded)
            self.test_loader_worker.start()
        except Exception as e:
            print(f"Test loader error: {e}")

    @pyqtSlot(object)
    def _on_tests_loaded(self, data: dict):
        """Testlar yuklanganda"""
        try:
            if data.get("status"):
                tests = data.get("result", [])
                self.combo_choose_test.clear()
                self.combo_choose_test.addItem("Testni tanlang...", None)
                for test in tests:
                    test_name = test.get("name", "Nomsiz test")
                    test_key = test.get("key") or test.get("id")
                    # Test ma'lumotlarini userData sifatida saqlash
                    self.combo_choose_test.addItem(test_name, test)
                print(f"Testlar yuklandi: {len(tests)} ta")
            else:
                message = data.get("message", "Testlarni yuklashda xatolik")
                print(f"Test yuklash xatosi: {message}")
                self.label_tests.setText(message)
        except Exception as e:
            print(f"Tests loaded handler error: {e}")

    def show_message(self, title: str, message: str, code: int = 2):
        """Xabar ko'rsatish"""
        try:
            self.msg_box = QMessageBox(self)
            icons = {
                0: QMessageBox.Icon.Critical,
                1: QMessageBox.Icon.Warning,
                2: QMessageBox.Icon.Information,
                3: QMessageBox.Icon.Question,
            }
            self.msg_box.setIcon(icons.get(code, QMessageBox.Icon.Information))
            self.msg_box.setWindowTitle(title)
            self.msg_box.setText(message)
            self.msg_box.setModal(True)
            self.msg_box.raise_()
            self.msg_box.activateWindow()
            self.msg_box.exec()
        except Exception as e:
            print(f"Message error: {e}")

    def request_exit_password(self) -> bool:
        """Chiqish parolini so'rash"""
        dialog = ExitDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.get_password() == self.admin_password:
                self.quit = True
                return True
            else:
                self.show_message("Xatolik", "Parol noto'g'ri!", 0)
        return False

    def stop_all_workers(self):
        """Barcha worker'larni to'xtatish"""
        workers = [
            self.checker_internet_worker,
            self.checker_monitor_worker,
            self.checker_camera_worker,
            self.face_identification_worker,
            self.face_detector_worker,
            self.screen_recorder_worker,
            self.load_app_worker,
            self.test_loader_worker,
        ]

        for worker in workers:
            if worker:
                try:
                    if hasattr(worker, 'isRunning') and worker.isRunning():
                        worker.stop()
                        worker.wait(1000)
                except Exception as e:
                    print(f"Worker stop error: {e}")

    # Event handlers
    def keyPressEvent(self, event):
        """Tugma bosilganda"""
        try:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                if event.key() == Qt.Key.Key_Q:
                    if self.request_exit_password():
                        self.stop_all_workers()
                        self.close()
        except Exception as e:
            print(f"KeyPress error: {e}")

    def closeEvent(self, event):
        """Oyna yopilganda"""
        if self.quit:
            event.accept()
        else:
            event.ignore()

    # Slot handlers
    @pyqtSlot(bool)
    def _on_internet_status(self, is_online: bool):
        """Internet holati o'zgarganda"""
        try:
            if is_online:
                self.stack.setCurrentIndex(self.current_index_page)
            else:
                self.current_index_page = self.stack.currentIndex()
                self._next_page_by_name('page_no_internet')
        except Exception as e:
            print(f"Internet checker error: {e}")

    def _next_page_by_name(self, page_name: str):
        """Sahifaga o'tish"""
        for i in range(self.stack.count()):
            if self.stack.widget(i).objectName() == page_name:
                self.stack.setCurrentIndex(i)
                break

    # Button click handlers (placeholders - to be implemented)
    def _on_check_pinfl(self):
        """PINFL tekshirish"""
        pass

    def _on_candidate_continue(self):
        """Nomzod davom etish"""
        pass

    def _on_staff_face_page(self):
        """Xodim yuz sahifasiga o'tish - test tanlangandan keyin"""
        try:
            # Tanlangan testni olish
            current_index = self.combo_choose_test.currentIndex()
            test_data = self.combo_choose_test.currentData()

            # Test tanlanganligini tekshirish
            if current_index == 0 or test_data is None:
                self.show_message("Ogohlantirish", "Iltimos, testni tanlang!", 1)
                return

            # Test ma'lumotlarini saqlash
            self.chosen_test_key = test_data.get("key") or test_data.get("id")
            self.test_name = test_data.get("name")

            # Serverdan kelgan sozlamalarni setting_mode dan olish
            setting_mode = test_data.get("setting_mode", {})
            self.is_check_face_staff = setting_mode.get("is_check_face_staff", False)
            self.is_check_face_candidate = setting_mode.get("is_check_face_candidate", False)
            self.is_detect_monitor = setting_mode.get("is_detect_monitor", False)
            self.is_detect_camera = setting_mode.get("is_detect_camera", False)
            self.is_screen_record = setting_mode.get("is_screen_record", False)
            self.is_face_identification = setting_mode.get("is_face_identification", False)
            self.warning_text = test_data.get("warning_text")

            print(f"Tanlangan test: {self.test_name}, key: {self.chosen_test_key}")
            print(f"Staff face check: {self.is_check_face_staff}")

            # Agar xodim yuz tekshiruvi yoqilgan bo'lsa - page_home ga o'tish
            if self.is_check_face_staff:
                self._next_page_by_name('page_home')
                self._start_staff_face_recognition()
            else:
                # Aks holda to'g'ridan-to'g'ri PINFL sahifasiga o'tish
                self._next_page_by_name('page_pinfl')

        except Exception as e:
            print(f"Staff face page error: {e}")
            self.show_message("Xatolik", f"Xatolik yuz berdi: {e}", 0)

    def _start_staff_face_recognition(self):
        """Xodim yuz tekshiruvini boshlash"""
        try:
            if self.app is None:
                self.show_message("Xatolik", "Yuz aniqlash modeli yuklanmagan!", 0)
                return

            # Oldingi worker'larni to'xtatish
            if self.face_detector_worker and self.face_detector_worker.isRunning():
                self.face_detector_worker.stop()

            if self.face_staff_worker and self.face_staff_worker.isRunning():
                self.face_staff_worker.stop()

            # Face Detector Worker'ni boshlash
            self.face_detector_worker = FaceDetectorWorker(app=self.app, camera_index=0)
            self.face_detector_worker.face_detected.connect(self._on_staff_face_detected)
            self.face_detector_worker.start()

            # Staff Face ID Worker'ni boshlash
            self.face_staff_worker = FaceIdStaffWorker(app=self.app)
            self.face_staff_worker.result_ready.connect(self._on_staff_face_result)
            self.face_staff_worker.start()

            print("Staff face recognition boshlandi...")

        except Exception as e:
            print(f"Start staff face recognition error: {e}")
            self.show_message("Xatolik", f"Yuz tekshiruvini boshlashda xatolik: {e}", 0)

    @pyqtSlot(object)
    def _on_staff_face_detected(self, data: dict):
        """Xodim yuzi aniqlanganda"""
        try:
            qt_image = data.get("image")
            cropped_face = data.get("crop_face")
            has_face = data.get("has_face", False)

            # Kamera tasvirini ko'rsatish (label_face page_home da)
            if qt_image and not qt_image.isNull():
                pixmap = QPixmap.fromImage(qt_image)
                scaled = pixmap.scaled(
                    self.label_face.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label_face.setPixmap(scaled)

            # Yuz aniqlansa, staff worker'ga yuborish
            if has_face and cropped_face is not None and self.face_staff_worker:
                # RGB formatga o'tkazish
                if len(cropped_face.shape) == 3:
                    rgb_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
                else:
                    rgb_face = cropped_face

                self.face_staff_worker.set_face(cropped_face=rgb_face)

        except Exception as e:
            print(f"Staff face detected handler error: {e}")

    @pyqtSlot(object)
    def _on_staff_face_result(self, data: dict):
        """Xodim yuz tekshiruvi natijasi"""
        try:
            is_verified = data.get("is_verified", False)
            message = data.get("message", "")

            if is_verified:
                # Muvaffaqiyatli - natijani ko'rsatish
                self.label_response.setText("✓ Xodim tasdiqlandi!")
                self.label_response.setStyleSheet(
                    "color: #22c55e; font-size: 18px; font-weight: bold;"
                )

                # Face detection'ni to'xtatish
                if self.face_detector_worker and self.face_detector_worker.isRunning():
                    self.face_detector_worker.stop()

                if self.face_staff_worker and self.face_staff_worker.isRunning():
                    self.face_staff_worker.stop()

                # PINFL sahifasiga o'tish
                self._next_page_by_name('page_pinfl')
                print(f"Xodim tasdiqlandi: {message}")

            else:
                # Xatolik - tekshiruv davom etadi
                self.label_response.setText(f"Tekshirilmoqda... {message}")
                self.label_response.setStyleSheet(
                    "color: #f59e0b; font-size: 14px;"
                )

        except Exception as e:
            print(f"Staff face result handler error: {e}")

    def _on_start_test(self):
        """Testni boshlash"""
        pass
