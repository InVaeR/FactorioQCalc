from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from core.data import QUALITY_NAMES, MAX_MODULE_SLOTS
from core.calculator import total_chance_from_modules
from ui.widgets.module_slot import ModuleSlot
from ui.assets import QUALITY_ICONS, MODULE_ICONS, quality_icon_size
from ui.style import LABEL_SECONDARY


class ModuleRow(QWidget):
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_index = -1

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)

        slots_row = QHBoxLayout()
        slots_row.setSpacing(6)
        self._slots: list[ModuleSlot] = []
        for i in range(MAX_MODULE_SLOTS):
            slot = ModuleSlot(i)
            slot.clicked.connect(self._on_slot_clicked)
            slot.right_clicked.connect(self._on_slot_right_clicked)
            self._slots.append(slot)
            slots_row.addWidget(slot)
        slots_row.addStretch()

        self._sum_label = QLabel("Σ шанс: 0.00%")
        self._sum_label.setStyleSheet(LABEL_SECONDARY)
        slots_row.addWidget(self._sum_label)

        self._layout.addLayout(slots_row)

        self._editor_widget = QWidget()
        self._editor_layout = QHBoxLayout(self._editor_widget)
        self._editor_layout.setContentsMargins(0, 0, 0, 0)
        self._editor_layout.setSpacing(4)

        self._tier_combo = QComboBox()
        self._tier_combo.setIconSize(quality_icon_size)
        for t in [1, 2, 3]:
            icon_path = MODULE_ICONS[t]
            self._tier_combo.addItem(QIcon(icon_path), f"Quality {t}", t)
        self._tier_combo.setCurrentIndex(2)

        self._quality_combo = QComboBox()
        self._quality_combo.setIconSize(quality_icon_size)
        for i in range(1, 6):
            icon_path = QUALITY_ICONS[i]
            self._quality_combo.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)

        self._tier_label = QLabel("Модуль:")
        self._tier_label.setStyleSheet(LABEL_SECONDARY)
        self._quality_label = QLabel("Качество:")
        self._quality_label.setStyleSheet(LABEL_SECONDARY)
        self._editor_layout.addWidget(self._tier_label)
        self._editor_layout.addWidget(self._tier_combo)
        self._editor_layout.addWidget(self._quality_label)
        self._editor_layout.addWidget(self._quality_combo)
        self._editor_layout.addStretch()

        self._layout.addWidget(self._editor_widget)

        for slot in self._slots:
            slot.set_module(3, 1)
        self._update_sum()

    def reset_defaults(self):
        self._deselect_current()
        for slot in self._slots:
            slot.set_module(3, 1)
        self._update_sum()

    def get_modules(self) -> list[tuple[int, int] | None]:
        result = []
        for slot in self._slots:
            if slot.is_empty():
                result.append(None)
            else:
                result.append((slot.tier, slot.quality))
        return result

    def _on_slot_clicked(self, index: int):
        tier = self._tier_combo.currentData()
        quality = self._quality_combo.currentData()

        slot = self._slots[index]
        if not slot.is_empty() and slot.tier == tier and slot.quality == quality:
            return

        slot.set_module(tier, quality)
        self._update_sum()
        self._set_selected(index)

    def _on_slot_right_clicked(self, index: int):
        self._slots[index].clear()
        if self._selected_index == index:
            self._deselect_current()
        self._update_sum()

    def _deselect_current(self):
        if 0 <= self._selected_index < len(self._slots):
            self._slots[self._selected_index].set_selected(False)
        self._selected_index = -1

    def _set_selected(self, index: int):
        self._deselect_current()
        self._selected_index = index
        if 0 <= index < len(self._slots):
            self._slots[index].set_selected(True)

    def _update_sum(self):
        modules = self.get_modules()
        chance = total_chance_from_modules(modules)
        self._sum_label.setText(f"Σ шанс: {chance * 100:.2f}%")
        self.changed.emit()
