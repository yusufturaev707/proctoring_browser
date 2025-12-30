"""
Info Modal Dialog
Zamonaviy ogohlantirish oynasi
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class InfoModal(QDialog):
    """
    Zamonaviy modal oyna - ogohlantirish va xabarlar uchun
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(450, 250)

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8fafc);
                border: 2px solid #e2e8f0;
                border-radius: 20px;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: 700;
                color: #0f172a;
                padding: 10px;
            }
            QLabel#message {
                font-size: 16px;
                color: #475569;
                padding: 15px;
                line-height: 1.5;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 40px;
                font-size: 16px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1d4ed8, stop:1 #1e40af);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        # Title label
        self.title_label = QLabel(self)
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))

        # Message label
        self.message_label = QLabel(self)
        self.message_label.setObjectName("message")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(QFont("Segoe UI", 14))

        # OK button
        self.ok_button = QPushButton("Tushunarli")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addStretch()
        layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def update_data(self, title: str, message: str):
        """Modal ma'lumotlarini yangilash"""
        self.title_label.setText(title)
        self.message_label.setText(message)

        if "WARNING" in title.upper() or "OGOHLANTIRISH" in title.upper():
            self.title_label.setStyleSheet("color: #f59e0b;")
        elif "ERROR" in title.upper() or "XATO" in title.upper():
            self.title_label.setStyleSheet("color: #ef4444;")
        else:
            self.title_label.setStyleSheet("color: #0f172a;")

    def showEvent(self, event):
        """Modalni markazga joylash"""
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            self.move(x, y)
        super().showEvent(event)
