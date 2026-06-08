from pytestqt.qtbot import QtBot

from educase_player.ui.main_window import MainWindow


def test_player_window_title(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "EduCase Player"