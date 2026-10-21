import html
import sys
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from aspect_engine import AspectLibrary
from thaum_elements import ASPECTS

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ICON_SIZE = 32


def icon_path(aspect: str) -> Path:
    """Aspect PNGs"""
    return ASSETS_DIR / f"{aspect}.png"


class SolverWindow(QMainWindow):
    def __init__(self, library: AspectLibrary):
        super().__init__()
        self.library = library
        self.setWindowTitle("Thaumcraft Aspect Solver")
        self.setMinimumWidth(460)
        self.setWindowIcon(QIcon("assets/icon.png"))

        aspects = sorted(library.all_aspects())

        self.start_box = self._make_combo(aspects)
        self.target_box = self._make_combo(aspects)
        self.target_box.setCurrentIndex(1)

        self.spaces_box = QSpinBox()
        self.spaces_box.setRange(0, 99)
        self.spaces_box.setValue(3)

        self.find_button = QPushButton("Find path")
        self.find_button.setDefault(True)
        self.find_button.clicked.connect(self.find_path)

        self.result_label = QLabel("")
        self.result_label.setTextFormat(Qt.TextFormat.RichText)
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.result_label.setMinimumHeight(60)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        form = QFormLayout()
        form.addRow("Start", self.start_box)
        form.addRow("Target", self.target_box)
        form.addRow("Spaces between", self.spaces_box)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.find_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _make_combo(self, aspects):
        box = QComboBox()
        box.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        box.setFont(QFont("Segoe UI", 16))
        for aspect in aspects:
            path = icon_path(aspect)
            # Missing PNG -> fall back to text only instead of crashing
            icon = QIcon(str(path)) if path.exists() else QIcon()
            box.addItem(icon, aspect)
        return box

    def find_path(self):
        start = self.start_box.currentText()
        target = self.target_box.currentText()
        spaces = self.spaces_box.value()

        try:
            path = self.library.pathfinding(start, target, min_spaces=spaces)
        except ValueError as exc:
            self.show_result(html.escape(str(exc)), ok=False)
            return

        if path:
            self.show_result(self._path_html(path), ok=True)
        else:
            self.show_result("No path found.", ok=False)

    def _path_html(self, path):
        parts = []
        for aspect in path:
            name = html.escape(aspect)
            img = icon_path(aspect)
            if img.exists():
                parts.append(
                    f'<img src="{img.as_posix()}" width="{ICON_SIZE}" '
                    f'height="{ICON_SIZE}" style="vertical-align: middle;"> '
                    f"{name}"
                )
            else:
                parts.append(name)
        return " &rarr; ".join(parts)

    def show_result(self, content_html: str, ok: bool):
        color = "#2e7d32" if ok else "#c62828"
        self.result_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px; font-family: 'Segoe UI';")
        self.result_label.setText(content_html)


def main():
    app = QApplication(sys.argv)
    window = SolverWindow(AspectLibrary(ASPECTS))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()