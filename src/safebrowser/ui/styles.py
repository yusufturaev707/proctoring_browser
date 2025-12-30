"""
Modern UI Styles for SafeBrowser
Zamonaviy dizayn - 2024 style
"""

# Asosiy ranglar
COLORS = {
    "primary": "#2563eb",      # Blue
    "primary_dark": "#1d4ed8",
    "primary_light": "#3b82f6",
    "success": "#10b981",      # Green
    "success_dark": "#059669",
    "danger": "#ef4444",       # Red
    "warning": "#f59e0b",      # Amber
    "dark": "#1e293b",         # Slate 800
    "dark_secondary": "#334155",
    "light": "#f8fafc",        # Slate 50
    "gray": "#64748b",         # Slate 500
    "gray_light": "#e2e8f0",   # Slate 200
    "white": "#ffffff",
    "shadow": "rgba(0, 0, 0, 0.1)",
}

# Global stylesheet
GLOBAL_STYLESHEET = """
/* Global Styles - Material Design Background */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #f5f7fa,
        stop:0.3 #f0f2f5,
        stop:0.7 #e8ecf1,
        stop:1 #e1e5eb);
}

/* Stacked Widget - Soft overlay */
QStackedWidget {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.7),
        stop:1 rgba(248, 250, 252, 0.5));
    border-radius: 20px;
}

QWidget {
    font-family: "Segoe UI", "Inter", -apple-system, sans-serif;
    font-size: 14px;
    color: #1e293b;
}

/* Labels */
QLabel {
    color: #1e293b;
}

/* Buttons - Primary */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3b82f6, stop:1 #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #60a5fa, stop:1 #3b82f6);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1d4ed8, stop:1 #1e40af);
}

QPushButton:disabled {
    background: #94a3b8;
    color: #e2e8f0;
}

/* Success Button */
QPushButton[class="success"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #34d399, stop:1 #10b981);
}

QPushButton[class="success"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #6ee7b7, stop:1 #34d399);
}

/* Input Fields */
QLineEdit {
    background-color: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 16px;
    color: #1e293b;
    selection-background-color: #3b82f6;
}

QLineEdit:focus {
    border-color: #3b82f6;
    background-color: #ffffff;
}

QLineEdit:hover {
    border-color: #94a3b8;
}

QLineEdit::placeholder {
    color: #94a3b8;
}

/* ComboBox - Material Design */
QComboBox {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 16px;
    color: #1e293b;
    min-width: 280px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: #94a3b8;
    background: #fafafa;
}

QComboBox:focus {
    border-color: #3b82f6;
    background: #ffffff;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 40px;
    border: none;
    border-radius: 0 12px 12px 0;
    background: transparent;
}

QComboBox::down-arrow {
    width: 14px;
    height: 14px;
}

QComboBox QAbstractItemView {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    selection-background-color: #3b82f6;
    selection-color: white;
    padding: 8px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 12px 18px;
    border-radius: 8px;
    min-height: 36px;
    margin: 2px 0;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f1f5f9;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #3b82f6;
    color: white;
}

/* Scroll Area */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: #f1f5f9;
    width: 10px;
    border-radius: 5px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #94a3b8;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #64748b;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* Message Box */
QMessageBox {
    background-color: white;
}

QMessageBox QLabel {
    color: #1e293b;
    font-size: 14px;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 20px;
}

/* Cards / Frames */
QFrame {
    background: white;
    border-radius: 12px;
}

/* Headings */
QLabel[class="heading"] {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
}

QLabel[class="subheading"] {
    font-size: 18px;
    font-weight: 500;
    color: #475569;
}

/* Camera Label */
QLabel[class="camera"] {
    background: #0f172a;
    border: 3px solid #3b82f6;
    border-radius: 16px;
}

/* Status Labels */
QLabel[class="status-success"] {
    color: #10b981;
    font-weight: 600;
}

QLabel[class="status-error"] {
    color: #ef4444;
    font-weight: 600;
}

QLabel[class="status-warning"] {
    color: #f59e0b;
    font-weight: 600;
}
"""

# Page-specific styles
PAGE_MAIN_STYLE = """
/* Page Main - Material Card Style */
QWidget#page_main {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.95),
        stop:1 rgba(248, 250, 252, 0.9));
    border-radius: 24px;
    margin: 20px;
}

QLabel#label_2 {
    color: #1a1a2e;
    font-size: 28px;
    font-weight: 700;
    line-height: 1.4;
}

QPushButton#btn_next_page {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4ade80, stop:1 #22c55e);
    font-size: 18px;
    padding: 16px 40px;
    min-width: 180px;
    border-radius: 12px;
}

QPushButton#btn_next_page:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #86efac, stop:1 #4ade80);
}

QPushButton#btn_next_page:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #16a34a, stop:1 #15803d);
}
"""

PAGE_FACE_STYLE = """
/* Face ID Pages - Material Card */
QWidget#page_home, QWidget#page_face {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.95),
        stop:1 rgba(248, 250, 252, 0.9));
    border-radius: 24px;
    margin: 15px;
}

QLabel#label_org, QLabel#label_face_check {
    color: #1a1a2e;
    font-size: 26px;
    font-weight: 700;
    padding: 10px;
}

/* Camera Frame - Modern Dark Style */
QLabel#label_face {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e293b, stop:1 #0f172a);
    border: 3px solid #3b82f6;
    border-radius: 20px;
    min-width: 480px;
    max-width: 480px;
    min-height: 360px;
    max-height: 360px;
}

QLabel#label_video_box {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e293b, stop:1 #0f172a);
    border: 3px solid #3b82f6;
    border-radius: 20px;
    min-width: 520px;
    max-width: 520px;
    min-height: 390px;
    max-height: 390px;
}

QLabel#label_response {
    font-size: 18px;
    font-weight: 600;
    padding: 12px 20px;
    color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
    border-radius: 10px;
}

QLabel#label_result_face_candidate {
    font-size: 18px;
    font-weight: 600;
    padding: 12px 20px;
    color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
    border-radius: 10px;
}
"""

PAGE_PINFL_STYLE = """
/* PINFL Page - Material Card */
QWidget#page_pinfl {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.95),
        stop:1 rgba(248, 250, 252, 0.9));
    border-radius: 24px;
    margin: 15px;
}

QLabel#label {
    color: #1a1a2e;
    font-size: 26px;
    font-weight: 600;
    padding: 15px;
}

QLineEdit#input_pinfl {
    font-size: 26px;
    padding: 18px 24px;
    min-width: 380px;
    text-align: center;
    letter-spacing: 3px;
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    color: #1a1a2e;
}

QLineEdit#input_pinfl:focus {
    border: 2px solid #3b82f6;
    background: #ffffff;
}

QPushButton#btn_check_im {
    font-size: 18px;
    padding: 16px 48px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3b82f6, stop:1 #2563eb);
    border-radius: 12px;
    min-width: 180px;
}

QPushButton#btn_check_im:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #60a5fa, stop:1 #3b82f6);
}
"""

PAGE_NOTE_STYLE = """
/* Note Page - Material Card */
QWidget#page_note {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.95),
        stop:1 rgba(248, 250, 252, 0.9));
    border-radius: 24px;
    margin: 15px;
}

QLabel#label_not_title {
    color: #dc2626;
    font-size: 28px;
    font-weight: 700;
    padding: 15px;
    background: rgba(220, 38, 38, 0.08);
    border-radius: 12px;
}

QLabel#label_warning_text {
    background: #ffffff;
    padding: 24px;
    border-radius: 16px;
    font-size: 15px;
    line-height: 1.7;
    color: #334155;
    border: 1px solid #e2e8f0;
}

QPushButton#btn_start_test {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4ade80, stop:1 #22c55e);
    font-size: 20px;
    padding: 18px 56px;
    min-width: 220px;
    border-radius: 14px;
}

QPushButton#btn_start_test:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #86efac, stop:1 #4ade80);
}
"""

PAGE_NO_INTERNET_STYLE = """
/* No Internet Page */
QWidget#page_no_internet {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.95),
        stop:1 rgba(254, 242, 242, 0.9));
    border-radius: 24px;
    margin: 15px;
}

QLabel#label_8 {
    color: #dc2626;
    font-size: 32px;
    font-weight: 700;
    padding: 20px;
    background: rgba(220, 38, 38, 0.1);
    border-radius: 16px;
}
"""

# Modal styles
MODAL_STYLE = """
QDialog {
    background: white;
    border-radius: 16px;
}

QDialog QLabel {
    font-size: 16px;
    color: #1e293b;
}

QDialog QPushButton {
    min-width: 100px;
}
"""


def get_full_stylesheet():
    """Barcha stylesheetlarni birlashtirish"""
    return (
        GLOBAL_STYLESHEET +
        PAGE_MAIN_STYLE +
        PAGE_FACE_STYLE +
        PAGE_PINFL_STYLE +
        PAGE_NOTE_STYLE +
        PAGE_NO_INTERNET_STYLE
    )
