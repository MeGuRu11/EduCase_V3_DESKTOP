"""Точка входа Player."""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from educase_core.logging import setup_logging
from educase_player.ui.main_window import MainWindow


def main() -> int:
    setup_logging("player")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
