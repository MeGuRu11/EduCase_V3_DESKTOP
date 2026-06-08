"""Дымовой тест окна Player (pytest-qt)."""
from __future__ import annotations

from educase_player.ui.main_window import MainWindow


def test_player_window_title(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "EduCase Player"
