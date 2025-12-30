"""
Draggable Label Widget
Suring mumkin bo'lgan label
"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QPoint


class DraggableLabel(QLabel):
    """Surish mumkin bo'lgan QLabel"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setFixedSize(320, 240)
        self.dragging = False
        self.drag_start_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
