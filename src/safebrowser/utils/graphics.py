"""
Graphics utilities - QPainter bilan rasm yaratish
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QFont, QPen, QBrush,
    QLinearGradient, QRadialGradient
)


def create_success_pixmap(width: int = 520, height: int = 390) -> QPixmap:
    """
    Yuz tasdiqlanganda ko'rsatiladigan success effekti
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Background gradient - yashil
    gradient = QLinearGradient(0, 0, 0, height)
    gradient.setColorAt(0, QColor(16, 185, 129, 230))
    gradient.setColorAt(1, QColor(5, 150, 105, 230))
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, width, height, 20, 20)

    # Checkmark doira
    cx, cy = width // 2, height // 2 - 30
    radius = 70

    # Oq doira
    painter.setBrush(QBrush(QColor(255, 255, 255, 40)))
    painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

    # Checkmark
    pen = QPen(QColor(255, 255, 255))
    pen.setWidth(8)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)

    # Checkmark chiziqlari
    painter.drawLine(cx - 30, cy, cx - 5, cy + 25)
    painter.drawLine(cx - 5, cy + 25, cx + 35, cy - 20)

    # "TASDIQLANDI" text
    painter.setPen(QColor(255, 255, 255))
    font = QFont("Segoe UI", 28, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(0, cy + radius + 30, width, 50,
                     Qt.AlignmentFlag.AlignCenter, "TASDIQLANDI")

    # Subtitle
    font.setPointSize(14)
    font.setWeight(QFont.Weight.Normal)
    painter.setFont(font)
    painter.setPen(QColor(255, 255, 255, 200))
    painter.drawText(0, cy + radius + 75, width, 30,
                     Qt.AlignmentFlag.AlignCenter, "Yuz muvaffaqiyatli aniqlandi")

    painter.end()
    return pixmap


def create_id_card_pixmap(width: int = 320, height: int = 200) -> QPixmap:
    """
    JSHSHIR sahifasi uchun ID karta dizayni
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Karta background - gradient
    gradient = QLinearGradient(0, 0, width, height)
    gradient.setColorAt(0, QColor(59, 130, 246))
    gradient.setColorAt(0.5, QColor(37, 99, 235))
    gradient.setColorAt(1, QColor(29, 78, 216))
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, width, height, 16, 16)

    # Chip (oltin rang)
    chip_x, chip_y = 25, 50
    chip_w, chip_h = 50, 40
    chip_gradient = QLinearGradient(chip_x, chip_y, chip_x + chip_w, chip_y + chip_h)
    chip_gradient.setColorAt(0, QColor(251, 191, 36))
    chip_gradient.setColorAt(0.5, QColor(245, 158, 11))
    chip_gradient.setColorAt(1, QColor(217, 119, 6))
    painter.setBrush(QBrush(chip_gradient))
    painter.drawRoundedRect(chip_x, chip_y, chip_w, chip_h, 6, 6)

    # Chip chiziqlari
    painter.setPen(QPen(QColor(180, 120, 20), 1))
    painter.drawLine(chip_x + 15, chip_y + 5, chip_x + 15, chip_y + chip_h - 5)
    painter.drawLine(chip_x + 35, chip_y + 5, chip_x + 35, chip_y + chip_h - 5)
    painter.drawLine(chip_x + 5, chip_y + 20, chip_x + chip_w - 5, chip_y + 20)

    # User icon placeholder
    icon_x = width - 90
    icon_y = 35
    icon_size = 65
    painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(icon_x, icon_y, icon_size, icon_size, 8, 8)

    # User silhouette
    painter.setBrush(QBrush(QColor(255, 255, 255, 80)))
    head_r = 12
    painter.drawEllipse(icon_x + icon_size // 2 - head_r, icon_y + 12, head_r * 2, head_r * 2)
    painter.drawEllipse(icon_x + 12, icon_y + 38, icon_size - 24, 22)

    # "ID CARD" text
    painter.setPen(QColor(255, 255, 255, 180))
    font = QFont("Segoe UI", 10, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(25, 25, "ID CARD")

    # JSHSHIR placeholder
    painter.setPen(QColor(255, 255, 255))
    font.setPointSize(16)
    font.setWeight(QFont.Weight.Bold)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
    painter.setFont(font)
    painter.drawText(25, height - 55, "JSHSHIR")

    # Number placeholder
    font.setPointSize(20)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
    painter.setFont(font)
    painter.drawText(25, height - 25, "_ _ _ _ _ _ _ _ _ _ _ _ _ _")

    painter.end()
    return pixmap


def create_lock_icon(width: int = 70, height: int = 70) -> QPixmap:
    """
    Qulf ikonkasi chizish - katta va aniq
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Markazlash uchun offset
    cx = width // 2
    cy = height // 2 + 5

    # Qulf tanasi - kattaroq
    body_w = 40
    body_h = 32
    body_x = cx - body_w // 2
    body_y = cy - 5

    # Gradient rangli qulf tanasi
    body_gradient = QLinearGradient(body_x, body_y, body_x, body_y + body_h)
    body_gradient.setColorAt(0, QColor(217, 119, 6))
    body_gradient.setColorAt(1, QColor(180, 83, 9))

    painter.setBrush(QBrush(body_gradient))
    painter.setPen(QPen(QColor(120, 53, 15), 2))
    painter.drawRoundedRect(body_x, body_y, body_w, body_h, 8, 8)

    # Qulf halqasi - qalinroq
    pen = QPen(QColor(217, 119, 6))
    pen.setWidth(8)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    arc_w = 26
    arc_h = 32
    arc_x = cx - arc_w // 2
    arc_y = cy - 30
    painter.drawArc(arc_x, arc_y, arc_w, arc_h, 0, 180 * 16)

    # Kalit teshigi
    painter.setBrush(QBrush(QColor(68, 51, 17)))
    painter.setPen(Qt.PenStyle.NoPen)
    hole_r = 6
    painter.drawEllipse(cx - hole_r, body_y + 8, hole_r * 2, hole_r * 2)
    painter.drawRect(cx - 3, body_y + 16, 6, 10)

    painter.end()
    return pixmap
