from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox, QCheckBox,
    QApplication,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QBrush, QIcon

from core.data import QUALITY_NAMES
from core.calculator import total_chance, distribute, calculate_with_recycling

import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

QUALITY_ICONS = {
    1: os.path.join(ASSETS_DIR, "Quality_normal.png"),
    2: os.path.join(ASSETS_DIR, "Quality_uncommon.png"),
    3: os.path.join(ASSETS_DIR, "Quality_rare.png"),
    4: os.path.join(ASSETS_DIR, "Quality_epic.png"),
    5: os.path.join(ASSETS_DIR, "Quality_legendary.png"),
}

MODULE_ICONS = {
    1: os.path.join(ASSETS_DIR, "Quality_module.png"),
    2: os.path.join(ASSETS_DIR, "Quality_module_2.png"),
    3: os.path.join(ASSETS_DIR, "Quality_module_3.png"),
}

ARROW_UP = os.path.join(ASSETS_DIR, "chevron-arrow-up_14.png").replace("\\", "/")
ARROW_DOWN = os.path.join(ASSETS_DIR, "chevron-arrow-down_14.png").replace("\\", "/")

COLOR_BG = "#1a1a1a"
COLOR_BG_LIGHT = "#252525"
COLOR_PANEL = "#2b2b2b"
COLOR_PANEL_HEADER = "#3a3a3a"
COLOR_YELLOW = "#ffcc00"
COLOR_ACCENT = "#d97b14"
COLOR_ACCENT_LIGHT = "#f09030"
COLOR_ACCENT_DARK = "#8a4a00"
COLOR_GREEN = "#4a8c1c"
COLOR_TEXT = "#e0e0e0"
COLOR_TEXT_SECONDARY = "#a0a0a0"
COLOR_BEVEL_LIGHT = "#5a5a5a"
COLOR_BEVEL_DARK = "#0a0a0a"
COLOR_ROW_ALT = "#333333"

LABEL_SECONDARY = (
    f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; background: transparent;"
)
LABEL_INFO = (
    f"color: {COLOR_ACCENT}; font-size: 16px; font-weight: bold; background: transparent;"
)
LABEL_GREEN = (
    f"color: {COLOR_GREEN}; font-size: 16px; font-weight: bold; background: transparent;"
)

quality_icon_size = QSize(28, 28)

STYLESHEET = f"""
QMainWindow {{
    background-color: #1a1a1a;
}}
QWidget {{
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}}
QLabel {{
    color: #e0e0e0;
    background: transparent;
}}

QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-size: 14px;
    font-weight: bold;
    padding: 4px 8px;
    border: 2px solid #0a0a0a;
    border-top: 2px solid #3a3a3a;
    border-left: 2px solid #3a3a3a;
    min-height: 24px;
}}
QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {{
    background-color: #252525;
}}
QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 2px solid #d97b14;
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    background-color: #3a3a3a;
    border: 1px solid #0a0a0a;
    border-top: 1px solid #5a5a5a;
    border-left: 1px solid #5a5a5a;
    width: 20px;
    margin: 2px;
    subcontrol-position: top right;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background-color: #505050;
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid #0a0a0a;
    border-left: 1px solid #0a0a0a;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url("{ARROW_UP}");
    width: 14px;
    height: 14px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background-color: #3a3a3a;
    border: 1px solid #0a0a0a;
    border-top: 1px solid #5a5a5a;
    border-left: 1px solid #5a5a5a;
    width: 20px;
    margin: 2px;
    subcontrol-position: bottom right;
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: #505050;
}}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid #0a0a0a;
    border-left: 1px solid #0a0a0a;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url("{ARROW_DOWN}");
    width: 14px;
    height: 14px;
}}

QComboBox {{
    padding: 4px 28px 4px 8px;
}}
QComboBox::drop-down {{
    background-color: #3a3a3a;
    border: 1px solid #0a0a0a;
    border-top: 1px solid #5a5a5a;
    border-left: 1px solid #5a5a5a;
    width: 24px;
    margin: 2px;
    subcontrol-origin: padding;
}}
QComboBox::drop-down:hover {{
    background-color: #505050;
}}
QComboBox::drop-down:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid #0a0a0a;
    border-left: 1px solid #0a0a0a;
}}
QComboBox::down-arrow {{
    image: url("{ARROW_DOWN}");
    width: 14px;
    height: 14px;
}}
QComboBox QAbstractItemView {{
    background-color: #1a1a1a;
    color: #e0e0e0;
    border: 2px solid #0a0a0a;
    selection-background-color: #d97b14;
    selection-color: #000000;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    min-height: 30px;
    padding: 4px 8px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: #d97b14;
    color: #000000;
}}

QPushButton {{
    background-color: #d97b14;
    color: #1a1a1a;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px 20px;
    border-top: 2px solid #f09030;
    border-left: 2px solid #f09030;
    border-bottom: 2px solid #8a4a00;
    border-right: 2px solid #8a4a00;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: #f09030;
    border-top: 2px solid #f9b060;
    border-left: 2px solid #f9b060;
}}
QPushButton:pressed {{
    background-color: #8a4a00;
    border-top: 2px solid #6a3000;
    border-left: 2px solid #6a3000;
    border-bottom: 2px solid #f09030;
    border-right: 2px solid #f09030;
    padding: 12px 20px 8px 20px;
}}

QTableWidget {{
    background-color: #1a1a1a;
    color: #e0e0e0;
    border: 2px solid #0a0a0a;
    border-top: 2px solid #3a3a3a;
    border-left: 2px solid #3a3a3a;
    gridline-color: #0a0a0a;
    font-size: 13px;
}}
QTableWidget::item {{
    padding: 6px 10px;
    border-bottom: 1px solid #0a0a0a;
}}
QHeaderView::section {{
    background-color: #3a3a3a;
    color: #ffcc00;
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 6px 10px;
    border-bottom: 2px solid #0a0a0a;
    border-right: 1px solid #0a0a0a;
}}

QScrollBar:vertical {{
    background-color: #1a1a1a;
    width: 16px;
    border: 1px solid #0a0a0a;
}}
QScrollBar::handle:vertical {{
    background-color: #3a3a3a;
    border: 1px solid #0a0a0a;
    border-top: 1px solid #5a5a5a;
    border-left: 1px solid #5a5a5a;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: #4a4a4a;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""


class FactorioPanel(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("factorioPanel")
        self.setStyleSheet("""
            #factorioPanel {
                background-color: #2b2b2b;
                border-top: 3px solid #5a5a5a;
                border-left: 3px solid #5a5a5a;
                border-bottom: 3px solid #0a0a0a;
                border-right: 3px solid #0a0a0a;
            }
        """)
        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)

        self.header = QLabel(title)
        self.header.setObjectName("panelHeader")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("""
            QLabel {
                color: #ffcc00;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
                background: #3a3a3a;
                padding: 6px 10px;
                border-bottom: 2px solid #0a0a0a;
            }
        """)
        self._root_layout.addWidget(self.header)

        self.content = QWidget()
        self.content.setObjectName("panelContent")
        self.content.setStyleSheet("background-color: #2b2b2b;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(14, 12, 14, 12)
        self.content_layout.setSpacing(8)
        self._root_layout.addWidget(self.content)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factorio Quality Calculator")
        self.setMinimumSize(760, 620)
        self.resize(800, 680)
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(10)

        self._build_title(main_layout)
        self._build_input_panel(main_layout)
        self._build_calculate_button(main_layout)
        self._build_result_panel(main_layout)

    def _build_title(self, parent: QVBoxLayout):
        title = QLabel("Калькулятор качества Factorio")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #ffcc00;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 2px;
                background: #2b2b2b;
                padding: 12px 0px;
                border-top: 3px solid #5a5a5a;
                border-left: 3px solid #5a5a5a;
                border-right: 3px solid #0a0a0a;
                border-bottom: 3px solid #0a0a0a;
            }
        """)
        parent.addWidget(title)

    def _make_param_row(self, label_text: str, widget, parent: QVBoxLayout):
        row = QHBoxLayout()
        row.setSpacing(8)
        label = QLabel(label_text)
        label.setFixedWidth(150)
        label.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY}; font-size: 13px; background: transparent;")
        row.addWidget(label)
        row.addWidget(widget, 1)
        parent.addLayout(row)

    def _build_input_panel(self, parent: QVBoxLayout):
        panel = FactorioPanel("ПАРАМЕТРЫ УСТАНОВКИ")
        panel.content_layout.setSpacing(6)

        self.module_count = QSpinBox()
        self.module_count.setRange(0, 10)
        self.module_count.setValue(4)
        self.module_count.setToolTip("Количество установленных модулей качества (0–10)")

        self.module_tier = QComboBox()
        self.module_tier.setIconSize(quality_icon_size)
        for t in [1, 2, 3]:
            icon_path = MODULE_ICONS[t]
            self.module_tier.addItem(QIcon(icon_path), f"Quality {t}", t)
        self.module_tier.setCurrentIndex(2)

        self.module_quality = QComboBox()
        self.module_quality.setIconSize(quality_icon_size)
        for i in range(1, 6):
            icon_path = QUALITY_ICONS[i]
            self.module_quality.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)

        self.production_rate = QDoubleSpinBox()
        self.production_rate.setRange(0.0, 1_000_000.0)
        self.production_rate.setValue(60.0)
        self.production_rate.setDecimals(2)
        self.production_rate.setToolTip("Объём производства")

        self.rate_unit = QComboBox()
        self.rate_unit.addItem("шт/с", "s")
        self.rate_unit.addItem("шт/мин", "min")
        self.rate_unit.addItem("шт/ч", "h")
        self.rate_unit.setCurrentIndex(1)
        self.rate_unit.currentIndexChanged.connect(self._update_table_header)

        rate_widget = QWidget()
        rate_layout = QHBoxLayout(rate_widget)
        rate_layout.setContentsMargins(0, 0, 0, 0)
        rate_layout.setSpacing(4)
        rate_layout.addWidget(self.production_rate, 1)
        rate_layout.addWidget(self.rate_unit)

        self.start_quality = QComboBox()
        self.start_quality.setIconSize(quality_icon_size)
        for i in range(1, 5):
            icon_path = QUALITY_ICONS[i]
            self.start_quality.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)

        self.max_quality = QComboBox()
        self.max_quality.setIconSize(quality_icon_size)
        for i in range(1, 6):
            icon_path = QUALITY_ICONS[i]
            self.max_quality.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)
        self.max_quality.setCurrentIndex(4)

        left_col = QVBoxLayout()
        left_col.setSpacing(6)
        self._make_param_row("Кол-во модулей:", self.module_count, left_col)
        self._make_param_row("Уровень модуля:", self.module_tier, left_col)
        self._make_param_row("Качество модуля:", self.module_quality, left_col)

        right_col = QVBoxLayout()
        right_col.setSpacing(6)
        self._make_param_row("Выработка:", rate_widget, right_col)
        self._make_param_row("Нач. качество входа:", self.start_quality, right_col)
        self._make_param_row("Макс. открытое качество:", self.max_quality, right_col)

        cols = QHBoxLayout()
        cols.setSpacing(24)
        cols.addLayout(left_col)
        cols.addLayout(right_col)
        panel.addLayout(cols)

        # Recycling section
        self.recycle_check = QCheckBox("Рециклинг")
        self.recycle_check.setToolTip("Включить расчёт с циклом переработки")
        self.recycle_check.setStyleSheet("""
            QCheckBox {
                color: #ffcc00;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 1px;
                background: transparent;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background-color: #1a1a1a;
                border: 2px solid #0a0a0a;
                border-top: 2px solid #3a3a3a;
                border-left: 2px solid #3a3a3a;
            }
            QCheckBox::indicator:checked {
                background-color: #d97b14;
                border: 2px solid #f09030;
            }
            QCheckBox::indicator:hover {
                background-color: #333333;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #f09030;
            }
        """)
        self.recycle_check.stateChanged.connect(self._toggle_recycling_fields)

        self.recycle_threshold = QComboBox()
        self.recycle_threshold.setIconSize(quality_icon_size)
        for i in range(1, 5):
            icon_path = QUALITY_ICONS[i]
            self.recycle_threshold.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)
        self.recycle_threshold.setToolTip("Всё, что на этом уровне и ниже, уходит в рециклер")

        self.rec_module_count = QSpinBox()
        self.rec_module_count.setRange(0, 10)
        self.rec_module_count.setValue(4)
        self.rec_module_count.setToolTip("Количество модулей качества в рециклере (0–10)")

        self.rec_module_tier = QComboBox()
        self.rec_module_tier.setIconSize(quality_icon_size)
        for t in [1, 2, 3]:
            icon_path = MODULE_ICONS[t]
            self.rec_module_tier.addItem(QIcon(icon_path), f"Quality {t}", t)
        self.rec_module_tier.setCurrentIndex(2)

        self.rec_module_quality = QComboBox()
        self.rec_module_quality.setIconSize(quality_icon_size)
        for i in range(1, 6):
            icon_path = QUALITY_ICONS[i]
            self.rec_module_quality.addItem(QIcon(icon_path), f"{QUALITY_NAMES[i]}", i)

        self._recycling_widgets = [
            self.recycle_threshold, self.rec_module_count,
            self.rec_module_tier, self.rec_module_quality,
        ]

        rec_header = QHBoxLayout()
        rec_header.setSpacing(8)
        rec_header.addWidget(self.recycle_check)
        rec_header.addStretch()
        panel.addLayout(rec_header)

        rec_grid = QHBoxLayout()
        rec_grid.setSpacing(24)

        rec_left = QVBoxLayout()
        rec_left.setSpacing(6)
        self._make_param_row("Порог рециклинга:", self.recycle_threshold, rec_left)
        self._make_param_row("Кол-во модулей рец.:", self.rec_module_count, rec_left)

        rec_right = QVBoxLayout()
        rec_right.setSpacing(6)
        self._make_param_row("Уровень модуля рец.:", self.rec_module_tier, rec_right)
        self._make_param_row("Качество модуля рец.:", self.rec_module_quality, rec_right)

        rec_grid.addLayout(rec_left)
        rec_grid.addLayout(rec_right)
        panel.addLayout(rec_grid)

        self._toggle_recycling_fields(False)

        parent.addWidget(panel)

    def _toggle_recycling_fields(self, enabled=None):
        if enabled is None:
            enabled = self.recycle_check.isChecked()
        else:
            enabled = bool(enabled)
        for w in self._recycling_widgets:
            w.setVisible(enabled)

    def _build_calculate_button(self, parent: QVBoxLayout):
        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calc_button.setMinimumHeight(44)
        self.calc_button.clicked.connect(self._on_calculate)
        parent.addWidget(self.calc_button)

    def _build_result_panel(self, parent: QVBoxLayout):
        panel = FactorioPanel("РЕЗУЛЬТАТЫ")
        panel.content_layout.setSpacing(8)

        info_row = QHBoxLayout()
        info_row.setSpacing(32)

        self.total_chance_label = QLabel("Суммарный шанс качества: —")
        self.total_chance_label.setObjectName("infoLabel")
        self.total_chance_label.setStyleSheet(LABEL_INFO)
        info_row.addWidget(self.total_chance_label)

        self.max_quality_label = QLabel("Макс. открытое качество: —")
        self.max_quality_label.setObjectName("infoLabel")
        self.max_quality_label.setStyleSheet(LABEL_INFO)
        info_row.addWidget(self.max_quality_label)

        self.recycle_info_label = QLabel("")
        self.recycle_info_label.setObjectName("greenLabel")
        self.recycle_info_label.setStyleSheet(LABEL_GREEN)
        info_row.addWidget(self.recycle_info_label)

        info_row.addStretch()
        panel.addLayout(info_row)

        self.table = QTableWidget(0, 3)
        self._update_table_header()
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #333333;
            }
        """)
        panel.addWidget(self.table)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.export_btn = QPushButton("Копировать таблицу")
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setMinimumHeight(32)
        self.export_btn.clicked.connect(self._on_export)
        btn_row.addWidget(self.export_btn)

        btn_row.addStretch()
        panel.addLayout(btn_row)

        parent.addWidget(panel)

    def _update_table_header(self):
        unit_text = self.rate_unit.currentText()
        self.table.setHorizontalHeaderLabels(["Качество", "Доля, %", unit_text])

    def _on_export(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        if rows == 0:
            return

        lines = []
        headers = []
        for c in range(cols):
            item = self.table.horizontalHeaderItem(c)
            headers.append(item.text() if item else "")
        lines.append("\t".join(headers))

        for r in range(rows):
            row_data = []
            for c in range(cols):
                item = self.table.item(r, c)
                row_data.append(item.text() if item else "")
            lines.append("\t".join(row_data))

        text = "\n".join(lines)
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def _get_rate_multiplier(self) -> float:
        unit = self.rate_unit.currentData()
        if unit == "s":
            return 60.0
        if unit == "h":
            return 1.0 / 60.0
        return 1.0

    def _on_calculate(self):
        count = self.module_count.value()
        tier = self.module_tier.currentData()
        quality = self.module_quality.currentData()
        rate_input = self.production_rate.value()
        start = self.start_quality.currentData()
        max_unlocked = self.max_quality.currentData()

        if start > max_unlocked:
            self._show_warning("Начальное качество не может превышать максимально открытое.")
            return

        rate = rate_input * self._get_rate_multiplier()
        display_mult = 1.0 / self._get_rate_multiplier()
        self._update_table_header()
        self._toggle_recycling_fields(self.recycle_check.isChecked())

        using_recycling = self.recycle_check.isChecked()
        if using_recycling:
            rec_threshold = self.recycle_threshold.currentData()
            if rec_threshold > max_unlocked:
                self._show_warning("Порог рециклинга не может превышать максимально открытое качество.")
                return
            if rec_threshold == max_unlocked:
                self._show_warning("Порог рециклинга равен максимальному качеству — весь выход уйдёт в рециклер.")
                return

            Q_prod = total_chance(count, tier, quality)
            Q_rec = total_chance(
                self.rec_module_count.value(),
                self.rec_module_tier.currentData(),
                self.rec_module_quality.currentData(),
            )

            result_items = calculate_with_recycling(
                base_input=rate, start_level=start,
                Q_prod=Q_prod, Q_rec=Q_rec,
                recycle_threshold=rec_threshold,
                max_unlocked_level=max_unlocked,
            )

            total_out = sum(result_items.values())
            ratio = total_out / rate if rate > 0 else 1.0
            self._render_summary(Q_prod, max_unlocked, f"Коэфф. рециклинга: {ratio:.4f}  |  Шанс рец.: {Q_rec * 100:.2f}%")
        else:
            chance = total_chance(count, tier, quality)

            result_items = dict(distribute(start, chance, rate, max_unlocked))
            result_items = {lvl: items for lvl, (_, items) in result_items.items()}

            self._render_summary(chance, max_unlocked, "")

        self._render_table(result_items, start, max_unlocked, display_mult, rate)

    def _render_summary(self, chance: float, max_unlocked: int, recycle_text: str):
        self.total_chance_label.setText(
            f"Суммарный шанс качества: {chance * 100:.2f}%"
        )
        self.max_quality_label.setText(
            f"Макс. открытое качество: {QUALITY_NAMES[max_unlocked]}"
        )
        self.recycle_info_label.setText(recycle_text)

    def _render_table(self, result_items: dict[int, float], start: int, max_unlocked: int, display_mult: float, input_rate: float = 0.0):
        self.table.setRowCount(0)
        total_rate = 0.0
        total_share = 0.0
        input_display = input_rate * display_mult

        for level in range(start, max_unlocked + 1):
            items = result_items.get(level, 0.0)
            items_display = items * display_mult
            total_rate += items
            share_pct = (items / input_rate * 100) if input_rate > 0 else 0.0
            total_share += share_pct

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(QIcon(QUALITY_ICONS[level]), QUALITY_NAMES[level]))
            self.table.setItem(row, 1, QTableWidgetItem(f"{share_pct:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{items_display:.2f}"))

        loss = input_rate - total_rate
        loss_display = loss * display_mult
        loss_pct = loss / input_rate * 100 if input_rate > 0 else 0.0

        if loss > 1e-9:
            row = self.table.rowCount()
            self.table.insertRow(row)
            red = QColor("#cc3333")
            bg_dark = QBrush(QColor(COLOR_BG))
            loss_font = QFont()
            loss_font.setBold(True)
            for col, text in [(0, "ПОТЕРИ (75% рециклинга)"), (1, f"{loss_pct:.2f}"), (2, f"{loss_display:.2f}")]:
                item = QTableWidgetItem(text)
                item.setForeground(red)
                item.setFont(loss_font)
                item.setBackground(bg_dark)
                self.table.setItem(row, col, item)

        row = self.table.rowCount()
        self.table.insertRow(row)

        gold = QColor(COLOR_YELLOW)
        bg = QBrush(QColor(COLOR_BG))
        bold_font = QFont()
        bold_font.setBold(True)

        def _make_total_item(text: str) -> QTableWidgetItem:
            item = QTableWidgetItem(text)
            item.setForeground(gold)
            item.setFont(bold_font)
            item.setBackground(bg)
            return item

        total_display = total_rate * display_mult
        self.table.setItem(row, 0, _make_total_item("ИТОГО"))
        self.table.setItem(row, 1, _make_total_item(f"{total_share:.2f}"))
        self.table.setItem(row, 2, _make_total_item(f"{total_display:.2f}"))

        if loss > 1e-9:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, _make_total_item("ВСЕГО НА ВХОДЕ"))
            self.table.setItem(row, 1, _make_total_item("100.00"))
            self.table.setItem(row, 2, _make_total_item(f"{input_display:.2f}"))

    def _show_warning(self, message: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка валидации")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            QPushButton {
                background-color: #d97b14;
                color: #1a1a1a;
                font-weight: bold;
                padding: 6px 20px;
                border-top: 2px solid #f09030;
                border-left: 2px solid #f09030;
                border-bottom: 2px solid #8a4a00;
                border-right: 2px solid #8a4a00;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #f09030;
            }
        """)
        msg.exec()
