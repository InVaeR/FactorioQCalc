from dataclasses import dataclass

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDoubleSpinBox, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QCheckBox,
    QApplication,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush, QIcon

from core.data import QUALITY_NAMES
from core.calculator import distribute, calculate_with_recycling, total_chance_from_modules
from ui.style import (
    COLOR_BG, COLOR_ACCENT, COLOR_YELLOW, COLOR_RED,
    COLOR_PANEL, COLOR_TEXT, COLOR_ACCENT_LIGHT, COLOR_ACCENT_DARK, COLOR_ROW_ALT,
    LABEL_SECONDARY, LABEL_INFO, LABEL_GREEN,
    SUCCESS_BUTTON_QSS, DANGER_BUTTON_QSS,
    build_stylesheet,
)
from ui.widgets.panel import FactorioPanel
from ui.widgets.module_row import ModuleRow
from ui.assets import QUALITY_ICONS, ARROW_UP, ARROW_DOWN, quality_icon_size

STYLESHEET = build_stylesheet(ARROW_UP, ARROW_DOWN)


@dataclass
class CalcInputs:
    rate: float
    start: int
    max_unlocked: int
    prod_modules: list
    recycling: bool
    rec_threshold: int
    rec_modules: list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factorio Quality Calculator")
        self.setMinimumSize(1024, 640)
        self.resize(1024, 700)
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(12)

        left = QVBoxLayout()
        left.setSpacing(8)
        self._build_input_panel(left)
        self._build_calculate_button(left)
        left.addStretch()

        right = QVBoxLayout()
        right.setSpacing(8)
        self._build_result_panel(right)

        root.addLayout(left, 0)
        root.addLayout(right, 1)

    def _make_param_row(self, label_text: str, widget, parent: QVBoxLayout):
        row = QHBoxLayout()
        row.setSpacing(8)
        label = QLabel(label_text)
        label.setFixedWidth(150)
        label.setStyleSheet(LABEL_SECONDARY)
        row.addWidget(label)
        row.addWidget(widget, 1)
        parent.addLayout(row)

    def _build_input_panel(self, parent: QVBoxLayout):
        prod_panel = FactorioPanel("ПРОИЗВОДСТВО")
        prod_panel.content_layout.setSpacing(6)

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
            self.start_quality.addItem(QIcon(QUALITY_ICONS[i]), f"{QUALITY_NAMES[i]}", i)

        self.max_quality = QComboBox()
        self.max_quality.setIconSize(quality_icon_size)
        for i in range(1, 6):
            self.max_quality.addItem(QIcon(QUALITY_ICONS[i]), f"{QUALITY_NAMES[i]}", i)
        self.max_quality.setCurrentIndex(4)

        self._make_param_row("Выработка:", rate_widget, prod_panel.content_layout)
        self._make_param_row("Нач. качество входа:", self.start_quality, prod_panel.content_layout)
        self._make_param_row("Макс. открытое качество:", self.max_quality, prod_panel.content_layout)
        parent.addWidget(prod_panel)

        mod_panel = FactorioPanel("МОДУЛИ КАЧЕСТВА")
        self.prod_modules = ModuleRow()
        mod_panel.addWidget(self.prod_modules)
        parent.addWidget(mod_panel)

        rec_panel = FactorioPanel("РЕЦИКЛИНГ")
        self.recycle_check = QCheckBox("Включить рециклинг")
        self.recycle_check.setToolTip("Включить расчёт с циклом переработки")
        self.recycle_check.stateChanged.connect(self._toggle_recycling_fields)

        rec_header = QHBoxLayout()
        rec_header.addWidget(self.recycle_check)
        rec_header.addStretch()
        rec_panel.addLayout(rec_header)

        self.recycle_threshold = QComboBox()
        self.recycle_threshold.setIconSize(quality_icon_size)
        for i in range(1, 5):
            self.recycle_threshold.addItem(QIcon(QUALITY_ICONS[i]), f"{QUALITY_NAMES[i]}", i)
        self.recycle_threshold.setToolTip("Всё, что на этом уровне и ниже, уходит в рециклер")

        self._make_param_row("Порог рециклинга:", self.recycle_threshold, rec_panel.content_layout)

        self.rec_modules = ModuleRow()
        rec_panel.addWidget(self.rec_modules)
        self.rec_modules.setVisible(False)

        self._recycling_widgets = [self.recycle_threshold, self.rec_modules]

        parent.addWidget(rec_panel)

    def _toggle_recycling_fields(self, enabled=None):
        if enabled is None:
            enabled = self.recycle_check.isChecked()
        else:
            enabled = bool(enabled)
        for w in self._recycling_widgets:
            w.setVisible(enabled)

    def _build_calculate_button(self, parent: QVBoxLayout):
        self.calc_button = QPushButton("РАССЧИТАТЬ")
        self.calc_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calc_button.setMinimumHeight(44)
        self.calc_button.clicked.connect(self._on_calculate)
        parent.addWidget(self.calc_button)

    def _build_result_panel(self, parent: QVBoxLayout):
        panel = FactorioPanel("РЕЗУЛЬТАТЫ")
        panel.content_layout.setSpacing(8)

        info_col = QVBoxLayout()
        info_col.setSpacing(2)

        self.total_chance_label = QLabel("Суммарный шанс качества: —")
        self.total_chance_label.setObjectName("infoLabel")
        self.total_chance_label.setStyleSheet(LABEL_INFO)
        self.total_chance_label.setWordWrap(True)
        info_col.addWidget(self.total_chance_label)

        self.max_quality_label = QLabel("Макс. открытое качество: —")
        self.max_quality_label.setObjectName("infoLabel")
        self.max_quality_label.setStyleSheet(LABEL_INFO)
        self.max_quality_label.setWordWrap(True)
        info_col.addWidget(self.max_quality_label)

        self.recycle_info_label = QLabel("")
        self.recycle_info_label.setObjectName("greenLabel")
        self.recycle_info_label.setStyleSheet(LABEL_GREEN)
        self.recycle_info_label.setWordWrap(True)
        info_col.addWidget(self.recycle_info_label)

        panel.addLayout(info_col)

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
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {COLOR_ROW_ALT};
            }}
        """)
        panel.content_layout.addWidget(self.table, 1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.export_btn = QPushButton("Копировать таблицу")
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_btn.setMinimumHeight(32)
        self.export_btn.setStyleSheet(SUCCESS_BUTTON_QSS)
        self.export_btn.clicked.connect(self._on_export)
        btn_row.addWidget(self.export_btn)

        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setMinimumHeight(32)
        self.reset_btn.setStyleSheet(DANGER_BUTTON_QSS)
        self.reset_btn.clicked.connect(self._on_reset)
        btn_row.addWidget(self.reset_btn)

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
        inputs = self._collect_inputs()
        msg = self._validate(inputs)
        if msg:
            self._show_warning(msg)
            return

        prod_chance = total_chance_from_modules(inputs.prod_modules)
        rate = inputs.rate
        display_mult = 1.0 / self._get_rate_multiplier()
        ratio = 1.0

        if inputs.recycling:
            rec_chance = total_chance_from_modules(inputs.rec_modules)
            result_items = calculate_with_recycling(
                base_input=rate, start_level=inputs.start,
                Q_prod=prod_chance, Q_rec=rec_chance,
                recycle_threshold=inputs.rec_threshold,
                max_unlocked_level=inputs.max_unlocked,
            )
            total_out = sum(result_items.values())
            ratio = total_out / rate if rate > 0 else 1.0
            self._render_summary(prod_chance, inputs.max_unlocked,
                                 f"Коэфф. рецикл.: {ratio:.4f}  |  Q_rec: {rec_chance * 100:.2f}%")
            if ratio < 0.05:
                self.recycle_info_label.setText(
                    self.recycle_info_label.text()
                    + "  ⚠ Высокие потери: порог рециклинга близок к максимуму"
                )
        else:
            result_items = dict(distribute(inputs.start, prod_chance, rate, inputs.max_unlocked))
            result_items = {lvl: items for lvl, (_, items) in result_items.items()}
            self._render_summary(prod_chance, inputs.max_unlocked, "")

        self._render_table(result_items, inputs.start, inputs.max_unlocked, display_mult, rate, inputs.recycling)

    def _collect_inputs(self) -> CalcInputs:
        return CalcInputs(
            rate=self.production_rate.value() * self._get_rate_multiplier(),
            start=self.start_quality.currentData(),
            max_unlocked=self.max_quality.currentData(),
            prod_modules=self.prod_modules.get_modules(),
            recycling=self.recycle_check.isChecked(),
            rec_threshold=self.recycle_threshold.currentData() if self.recycle_check.isChecked() else 1,
            rec_modules=self.rec_modules.get_modules() if self.recycle_check.isChecked() else [],
        )

    def _validate(self, inputs: CalcInputs) -> str | None:
        if inputs.start > inputs.max_unlocked:
            return "Начальное качество не может превышать максимально открытое."
        if inputs.recycling:
            if inputs.rec_threshold > inputs.max_unlocked:
                return "Порог рециклинга не может превышать максимально открытое качество."
            if inputs.rec_threshold == inputs.max_unlocked:
                return "Порог рециклинга равен максимальному качеству — весь выход уйдёт в рециклер."
        return None

    def _on_reset(self):
        self.production_rate.setValue(60.0)
        self.rate_unit.setCurrentIndex(1)
        self.start_quality.setCurrentIndex(0)
        self.max_quality.setCurrentIndex(4)
        self.recycle_check.setChecked(False)
        self.recycle_threshold.setCurrentIndex(0)
        self.prod_modules.reset_defaults()
        self.rec_modules.reset_defaults()
        self.table.setRowCount(0)
        self.total_chance_label.setText("Суммарный шанс качества: —")
        self.max_quality_label.setText("Макс. открытое качество: —")
        self.recycle_info_label.setText("")

    def _render_summary(self, chance: float, max_unlocked: int, recycle_text: str):
        self.total_chance_label.setText(
            f"Суммарный шанс качества: {chance * 100:.2f}%"
        )
        self.max_quality_label.setText(
            f"Макс. открытое качество: {QUALITY_NAMES[max_unlocked]}"
        )
        self.recycle_info_label.setStyleSheet(LABEL_GREEN)
        self.recycle_info_label.setText(recycle_text)

    def _render_table(self, result_items: dict[int, float], start: int, max_unlocked: int, display_mult: float, input_rate: float, is_recycling: bool):
        self.table.setRowCount(0)
        total_rate = 0.0
        total_share = 0.0
        input_display = input_rate * display_mult

        def _make_styled_item(text: str, color: QColor) -> QTableWidgetItem:
            item = QTableWidgetItem(text)
            item.setForeground(color)
            item.setFont(bold_font)
            item.setBackground(bg)
            return item

        gold = QColor(COLOR_YELLOW)
        bg = QBrush(QColor(COLOR_BG))
        bold_font = QFont()
        bold_font.setBold(True)
        red = QColor(COLOR_RED)

        if is_recycling:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, _make_styled_item("ВСЕГО НА ВХОДЕ", gold))
            self.table.setItem(row, 1, _make_styled_item("100.00", gold))
            self.table.setItem(row, 2, _make_styled_item(f"{input_display:.2f}", gold))

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
        loss_pct = 100.0 - total_share

        if loss > 1e-9:
            row = self.table.rowCount()
            self.table.insertRow(row)
            loss_label = "ПОТЕРИ (75% рециклинга)" if is_recycling else "ПОТЕРИ"
            for col, text in [(0, loss_label), (1, f"{loss_pct:.2f}"), (2, f"{loss_display:.2f}")]:
                self.table.setItem(row, col, _make_styled_item(text, red))

        row = self.table.rowCount()
        self.table.insertRow(row)
        total_display = total_rate * display_mult
        self.table.setItem(row, 0, _make_styled_item("ИТОГО НА ВЫХОДЕ", gold))
        self.table.setItem(row, 1, _make_styled_item(f"{total_share:.2f}", gold))
        self.table.setItem(row, 2, _make_styled_item(f"{total_display:.2f}", gold))

    def _show_warning(self, message: str):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка валидации")
        msg.setText(message)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLOR_PANEL};
                color: {COLOR_TEXT};
            }}
            QLabel {{
                color: {COLOR_TEXT};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {COLOR_ACCENT};
                color: {COLOR_BG};
                font-weight: bold;
                padding: 6px 20px;
                border-top: 2px solid {COLOR_ACCENT_LIGHT};
                border-left: 2px solid {COLOR_ACCENT_LIGHT};
                border-bottom: 2px solid {COLOR_ACCENT_DARK};
                border-right: 2px solid {COLOR_ACCENT_DARK};
                min-width: 60px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_ACCENT_LIGHT};
            }}
        """)
        msg.exec()
