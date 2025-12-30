"""
Exit Dialog
Dasturdan chiqish uchun parol dialog
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from safebrowser.utils.graphics import create_lock_icon


class ExitDialog(QDialog):
    """
    Dasturdan chiqish uchun zamonaviy parol dialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Chiqish")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(440, 380)

        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 3px solid #3b82f6;
                border-radius: 24px;
            }
        """)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(12)

        # Icon container
        icon_container = QLabel()
        icon_container.setFixedSize(90, 90)
        icon_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_container.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fffbeb, stop:0.5 #fef3c7, stop:1 #fde68a);
                border-radius: 45px;
                border: 4px solid #d97706;
            }
        """)

        lock_pixmap = create_lock_icon(60, 60)
        icon_container.setPixmap(lock_pixmap)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(217, 119, 6, 80))
        shadow.setOffset(0, 4)
        icon_container.setGraphicsEffect(shadow)

        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        icon_layout.addWidget(icon_container)
        icon_layout.addStretch()
        layout.addLayout(icon_layout)

        layout.addSpacing(10)

        # Title
        title_label = QLabel("Dasturdan chiqish")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 800;
                color: #1e293b;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                padding: 5px;
            }
        """)

        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(1)
        title_shadow.setColor(QColor(0, 0, 0, 30))
        title_shadow.setOffset(1, 1)
        title_label.setGraphicsEffect(title_shadow)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Davom etish uchun admin parolini kiriting")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 500;
                color: #475569;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                padding: 8px;
            }
        """)
        layout.addWidget(subtitle_label)

        layout.addSpacing(8)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("● ● ● ● ● ● ● ●")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(55)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 3px solid #cbd5e1;
                border-radius: 14px;
                padding: 12px 20px;
                font-size: 18px;
                font-weight: 600;
                color: #0f172a;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                background-color: #ffffff;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        self.password_input.returnPressed.connect(self.accept)
        layout.addWidget(self.password_input)

        layout.addSpacing(15)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        btn_cancel = QPushButton("Bekor qilish")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setMinimumHeight(50)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #334155;
                border: 3px solid #cbd5e1;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 130px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_confirm = QPushButton("Chiqish")
        btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_confirm.setMinimumHeight(50)
        btn_confirm.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial, sans-serif;
                min-width: 130px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
            QPushButton:pressed {
                background-color: #991b1b;
            }
        """)
        btn_confirm.clicked.connect(self.accept)
        btn_layout.addWidget(btn_confirm)

        layout.addLayout(btn_layout)

    def get_password(self) -> str:
        """Kiritilgan parolni olish"""
        return self.password_input.text()

    def showEvent(self, event):
        """Dialog ko'rsatilganda"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        self.password_input.setFocus()
        super().showEvent(event)
