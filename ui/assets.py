import os
from PySide6.QtCore import QSize

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

quality_icon_size = QSize(28, 28)
