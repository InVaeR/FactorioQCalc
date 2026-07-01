from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from ui.style import COLOR_PANEL, COLOR_PANEL_HEADER, COLOR_YELLOW, COLOR_BEVEL_DARK, COLOR_BEVEL_LIGHT


class FactorioPanel(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("factorioPanel")
        self.setStyleSheet(f"""
            #factorioPanel {{
                background-color: {COLOR_PANEL};
                border-top: 3px solid {COLOR_BEVEL_LIGHT};
                border-left: 3px solid {COLOR_BEVEL_LIGHT};
                border-bottom: 3px solid {COLOR_BEVEL_DARK};
                border-right: 3px solid {COLOR_BEVEL_DARK};
            }}
        """)
        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)

        self.header = QLabel(title)
        self.header.setObjectName("panelHeader")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_YELLOW};
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
                background: {COLOR_PANEL_HEADER};
                padding: 6px 10px;
                border-bottom: 3px solid {COLOR_BEVEL_DARK};
            }}
        """)
        self._root_layout.addWidget(self.header)

        self.content = QWidget()
        self.content.setObjectName("panelContent")
        self.content.setStyleSheet(f"background-color: {COLOR_PANEL};")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(14, 12, 14, 12)
        self.content_layout.setSpacing(8)
        self._root_layout.addWidget(self.content)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        self.content_layout.addLayout(layout)
