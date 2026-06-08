"""Дымовой тест окна Constructor (pytest-qt)."""
from __future__ import annotations

from educase_constructor.ui.main_window import MainWindow


def test_constructor_window_title(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "EduCase Constructor"
