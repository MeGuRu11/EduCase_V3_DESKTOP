"""Точка входа Constructor."""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from educase_constructor.ui.main_window import MainWindow
from educase_core.logging import setup_logging


def main() -> int:
    setup_logging("constructor")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
