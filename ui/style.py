COLOR_BG = "#1a1a1a"
COLOR_BG_LIGHT = "#252525"
COLOR_PANEL = "#2b2b2b"
COLOR_PANEL_HEADER = "#3a3a3a"
COLOR_YELLOW = "#ffcc00"
COLOR_ACCENT = "#d97b14"
COLOR_ACCENT_LIGHT = "#f09030"
COLOR_ACCENT_DARK = "#8a4a00"
COLOR_GREEN = "#4a8c1c"
COLOR_GREEN_LIGHT = "#6bb32e"
COLOR_RED = "#cc3333"
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
LABEL_WARNING = (
    f"color: {COLOR_YELLOW}; font-size: 14px; font-weight: bold; background: transparent;"
)

SUCCESS_BUTTON_QSS = f"""
QPushButton {{
    background-color: {COLOR_GREEN};
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px 20px;
    border-top: 2px solid {COLOR_GREEN_LIGHT};
    border-left: 2px solid {COLOR_GREEN_LIGHT};
    border-bottom: 2px solid #2a5a0a;
    border-right: 2px solid #2a5a0a;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: {COLOR_GREEN_LIGHT};
    border-top: 2px solid #7dcc44;
    border-left: 2px solid #7dcc44;
}}
QPushButton:pressed {{
    background-color: #2a5a0a;
    border-top: 2px solid #1a3a00;
    border-left: 2px solid #1a3a00;
    border-bottom: 2px solid {COLOR_GREEN_LIGHT};
    border-right: 2px solid {COLOR_GREEN_LIGHT};
    padding: 12px 20px 8px 20px;
}}
"""

DANGER_BUTTON_QSS = f"""
QPushButton {{
    background-color: {COLOR_RED};
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px 20px;
    border-top: 2px solid #e05555;
    border-left: 2px solid #e05555;
    border-bottom: 2px solid #8a1a1a;
    border-right: 2px solid #8a1a1a;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: #e05555;
    border-top: 2px solid #ff7777;
    border-left: 2px solid #ff7777;
}}
QPushButton:pressed {{
    background-color: #8a1a1a;
    border-top: 2px solid #5a0000;
    border-left: 2px solid #5a0000;
    border-bottom: 2px solid #e05555;
    border-right: 2px solid #e05555;
    padding: 12px 20px 8px 20px;
}}
"""


def build_stylesheet(arrow_up: str, arrow_down: str) -> str:
    return f"""
QMainWindow {{
    background-color: {COLOR_BG};
}}
QWidget {{
    color: {COLOR_TEXT};
    font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}}
QLabel {{
    color: {COLOR_TEXT};
    background: transparent;
}}

QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    font-size: 14px;
    font-weight: bold;
    padding: 4px 8px;
    border: 3px solid {COLOR_BEVEL_DARK};
    border-top: 3px solid {COLOR_PANEL_HEADER};
    border-left: 3px solid {COLOR_PANEL_HEADER};
    min-height: 24px;
}}
QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {{
    background-color: {COLOR_BG_LIGHT};
}}
QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 3px solid {COLOR_ACCENT};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    background-color: {COLOR_PANEL_HEADER};
    border: 1px solid {COLOR_BEVEL_DARK};
    border-top: 1px solid {COLOR_BEVEL_LIGHT};
    border-left: 1px solid {COLOR_BEVEL_LIGHT};
    width: 20px;
    margin: 2px;
    subcontrol-position: top right;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background-color: #505050;
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid {COLOR_BEVEL_DARK};
    border-left: 1px solid {COLOR_BEVEL_DARK};
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url("{arrow_up}");
    width: 14px;
    height: 14px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background-color: {COLOR_PANEL_HEADER};
    border: 1px solid {COLOR_BEVEL_DARK};
    border-top: 1px solid {COLOR_BEVEL_LIGHT};
    border-left: 1px solid {COLOR_BEVEL_LIGHT};
    width: 20px;
    margin: 2px;
    subcontrol-position: bottom right;
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: #505050;
}}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid {COLOR_BEVEL_DARK};
    border-left: 1px solid {COLOR_BEVEL_DARK};
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url("{arrow_down}");
    width: 14px;
    height: 14px;
}}

QComboBox {{
    padding: 4px 28px 4px 8px;
}}
QComboBox::drop-down {{
    background-color: {COLOR_PANEL_HEADER};
    border: 1px solid {COLOR_BEVEL_DARK};
    border-top: 1px solid {COLOR_BEVEL_LIGHT};
    border-left: 1px solid {COLOR_BEVEL_LIGHT};
    width: 24px;
    margin: 2px;
    subcontrol-origin: padding;
}}
QComboBox::drop-down:hover {{
    background-color: #505050;
}}
QComboBox::drop-down:pressed {{
    background-color: #2a2a2a;
    border-top: 1px solid {COLOR_BEVEL_DARK};
    border-left: 1px solid {COLOR_BEVEL_DARK};
}}
QComboBox::down-arrow {{
    image: url("{arrow_down}");
    width: 14px;
    height: 14px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    border: 2px solid {COLOR_BEVEL_DARK};
    selection-background-color: {COLOR_ACCENT};
    selection-color: #000000;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    min-height: 30px;
    padding: 4px 8px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: {COLOR_ACCENT};
    color: #000000;
}}

QPushButton {{
    background-color: {COLOR_ACCENT};
    color: {COLOR_BG};
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px 20px;
    border-top: 2px solid {COLOR_ACCENT_LIGHT};
    border-left: 2px solid {COLOR_ACCENT_LIGHT};
    border-bottom: 2px solid {COLOR_ACCENT_DARK};
    border-right: 2px solid {COLOR_ACCENT_DARK};
    min-height: 20px;
}}
QPushButton:disabled {{
    background-color: #3a3a3a;
    color: #707070;
    border-top: 2px solid #4a4a4a;
    border-left: 2px solid #4a4a4a;
    border-bottom: 2px solid #0a0a0a;
    border-right: 2px solid #0a0a0a;
}}
QPushButton:hover {{
    background-color: {COLOR_ACCENT_LIGHT};
    border-top: 2px solid #f9b060;
    border-left: 2px solid #f9b060;
}}
QPushButton:pressed {{
    background-color: {COLOR_ACCENT_DARK};
    border-top: 2px solid #6a3000;
    border-left: 2px solid #6a3000;
    border-bottom: 2px solid {COLOR_ACCENT_LIGHT};
    border-right: 2px solid {COLOR_ACCENT_LIGHT};
    padding: 12px 20px 8px 20px;
}}


QTableWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    border: 3px solid {COLOR_BEVEL_DARK};
    border-top: 3px solid {COLOR_PANEL_HEADER};
    border-left: 3px solid {COLOR_PANEL_HEADER};
    gridline-color: {COLOR_BEVEL_DARK};
    font-size: 13px;
}}
QTableWidget::item {{
    padding: 6px 10px;
    border-bottom: 1px solid {COLOR_BEVEL_DARK};
}}
QHeaderView::section {{
    background-color: {COLOR_PANEL_HEADER};
    color: {COLOR_YELLOW};
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 6px 10px;
    border-bottom: 2px solid {COLOR_BEVEL_DARK};
    border-right: 1px solid {COLOR_BEVEL_DARK};
}}

QScrollBar:vertical {{
    background-color: {COLOR_BG};
    width: 16px;
    border: 1px solid {COLOR_BEVEL_DARK};
}}
QScrollBar::handle:vertical {{
    background-color: {COLOR_PANEL_HEADER};
    border: 1px solid {COLOR_BEVEL_DARK};
    border-top: 1px solid {COLOR_BEVEL_LIGHT};
    border-left: 1px solid {COLOR_BEVEL_LIGHT};
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: #4a4a4a;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""
