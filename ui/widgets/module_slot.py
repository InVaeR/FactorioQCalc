from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPixmap, QColor, QPen

from ui.assets import QUALITY_ICONS, MODULE_ICONS
from ui.style import COLOR_BG, COLOR_ACCENT, COLOR_BEVEL_DARK, COLOR_BEVEL_LIGHT

SLOT_SIZE = 56
BADGE_SIZE = 20


class ModuleSlot(QFrame):
    clicked = Signal(int)
    right_clicked = Signal(int)

    def __init__(self, index: int, parent=None):
        super().__init__(parent)
        self._index = index
        self.tier: int | None = None
        self.quality: int | None = None
        self._selected = False
        self.setFixedSize(SLOT_SIZE, SLOT_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("ЛКМ — установить модуль, ПКМ — очистить")

    def set_module(self, tier: int, quality: int):
        self.tier = tier
        self.quality = quality
        self.update()

    def clear(self):
        self.tier = None
        self.quality = None
        self.update()

    def is_empty(self) -> bool:
        return self.tier is None or self.quality is None

    def set_selected(self, selected: bool):
        self._selected = selected
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked.emit(self._index)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._index)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect()

        if self._selected:
            bevel_light = QColor(COLOR_ACCENT)
            bevel_dark = QColor(COLOR_ACCENT)
        else:
            bevel_light = QColor(COLOR_BEVEL_DARK)
            bevel_dark = QColor(COLOR_BEVEL_LIGHT)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(COLOR_BG))
        painter.drawRect(r)

        painter.setPen(QPen(bevel_light, 2))
        painter.drawLine(r.topLeft(), r.topRight())
        painter.drawLine(r.topLeft(), r.bottomLeft())

        painter.setPen(QPen(bevel_dark, 2))
        painter.drawLine(r.topRight(), r.bottomRight())
        painter.drawLine(r.bottomLeft(), r.bottomRight())

        if not self.is_empty() and self.tier is not None:
            mod_path = MODULE_ICONS.get(self.tier)
            if mod_path:
                mod_pix = QPixmap(mod_path)
                if not mod_pix.isNull():
                    scaled = mod_pix.scaled(SLOT_SIZE - 8, SLOT_SIZE - 8,
                                            Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                    x = (r.width() - scaled.width()) // 2
                    y = (r.height() - scaled.height()) // 2
                    painter.drawPixmap(x, y, scaled)

            if self.quality is not None:
                qual_path = QUALITY_ICONS.get(self.quality)
                if qual_path:
                    qual_pix = QPixmap(qual_path)
                    if not qual_pix.isNull():
                        badge = qual_pix.scaled(BADGE_SIZE, BADGE_SIZE,
                                                Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
                        bx = r.width() - BADGE_SIZE
                        by = r.height() - BADGE_SIZE
                        painter.drawPixmap(bx, by, badge)
