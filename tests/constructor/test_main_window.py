from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtWidgets import QMessageBox
from pytestqt.qtbot import QtBot

from educase_constructor.ui.main_window import MainWindow
from educase_core.application.cases import load_case


def test_constructor_window_title(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "EduCase Constructor"


def test_save_then_load_round_trip(qtbot: QtBot, tmp_path: Path) -> None:
    """Сквозной цикл Constructor → .educase → back: мета и пациенты совпадают."""
    window = MainWindow()
    qtbot.addWidget(window)

    window.editor.case_id_edit.setText("case-7")
    window.editor.title_edit.setText("Вспышка ОКИ")
    window.editor.add_patient_button.click()
    window.editor.patient_editors[0].id_edit.setText("p1")
    window.editor.patient_editors[0].title_edit.setText("Пациент 1")

    dst = tmp_path / "case.educase"
    assert window.save_case_to_path(dst) is True
    assert dst.exists()

    loaded = load_case(dst)
    assert loaded.case.meta.id == "case-7"
    assert loaded.case.meta.title == "Вспышка ОКИ"
    assert len(loaded.case.patients.patients) == 1
    assert loaded.case.patients.patients[0].id == "p1"


def test_save_empty_id_warns_and_skips(
    qtbot: QtBot, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """Пустой id: предупреждение (заглушено), save_case_to_path → False, файла нет."""
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok
    )

    window = MainWindow()
    qtbot.addWidget(window)

    dst = tmp_path / "case.educase"
    assert window.save_case_to_path(dst) is False
    assert not dst.exists()
