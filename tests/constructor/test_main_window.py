from pytestqt.qtbot import QtBot

from educase_constructor.ui.main_window import MainWindow


def test_constructor_window_title(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "EduCase Constructor"