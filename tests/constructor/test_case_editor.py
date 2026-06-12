"""Тесты CaseEditor: сборка ``CaseDraft`` из меты и редакторов пациентов."""
from __future__ import annotations

from PySide6.QtWidgets import QTableWidgetItem, QTabWidget
from pytestqt.qtbot import QtBot

from educase_constructor.ui.case_editor import CaseEditor
from educase_constructor.ui.patient_editor import PatientEditor


def test_editor_has_six_titled_tabs(qtbot: QtBot) -> None:
    """Компоновка: шесть вкладок в ожидаемом порядке внутри ``self.tabs``."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    assert isinstance(editor.tabs, QTabWidget)
    assert editor.tabs.count() == 6
    titles = [editor.tabs.tabText(i) for i in range(editor.tabs.count())]
    assert titles == [
        "Кейс и пациенты",
        "Клинический",
        "Контакты",
        "Среда",
        "СЭС",
        "Финал",
    ]


def test_add_patient_still_appends_patient_editor(qtbot: QtBot) -> None:
    """После переверстки add_patient по-прежнему кладёт ``PatientEditor`` в список."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    editor.add_patient()
    assert len(editor.patient_editors) == 1
    assert isinstance(editor.patient_editors[0], PatientEditor)


def test_empty_editor_to_draft_carries_id(qtbot: QtBot) -> None:
    """Пустой редактор с введённым id → ``CaseDraft`` с этим id и без пациентов."""
    editor = CaseEditor()
    qtbot.addWidget(editor)
    editor.case_id_edit.setText("case-1")

    draft = editor.to_draft()
    assert draft.case_id == "case-1"
    assert draft.patients == ()


def test_add_and_remove_patient(qtbot: QtBot) -> None:
    """«Добавить пациента» увеличивает число редакторов, «Удалить последнего» — уменьшает."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    assert len(editor.patient_editors) == 0
    editor.add_patient_button.click()
    editor.add_patient_button.click()
    assert len(editor.patient_editors) == 2
    editor.remove_patient_button.click()
    assert len(editor.patient_editors) == 1
    # Удаление при пустом списке не падает.
    editor.remove_patient_button.click()
    editor.remove_patient_button.click()
    assert len(editor.patient_editors) == 0


def test_filled_editor_to_draft(qtbot: QtBot) -> None:
    """Заполненные поля меты и пациента → корректный ``CaseDraft``."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    editor.case_id_edit.setText("case-7")
    editor.title_edit.setText("Вспышка ОКИ")
    editor.author_edit.setText("Иванов")
    editor.nosology_edit.setText("Сальмонеллёз")
    editor.unit_personnel_edit.setText("150")

    editor.add_patient_button.click()
    patient = editor.patient_editors[0]
    patient.id_edit.setText("p1")
    patient.title_edit.setText("Пациент 1")
    patient.add_row_button.click()
    patient.fields_table.setItem(0, 0, QTableWidgetItem("Возраст"))
    patient.fields_table.setItem(0, 1, QTableWidgetItem("25 лет"))
    patient.assets_edit.setText("img_01, img_02 ,")  # пустые куски отбрасываются

    draft = editor.to_draft()
    assert draft.case_id == "case-7"
    assert draft.title == "Вспышка ОКИ"
    assert draft.author == "Иванов"
    assert draft.nosology == "Сальмонеллёз"
    assert draft.unit_personnel == 150
    assert len(draft.patients) == 1
    assert draft.patients[0].id == "p1"
    assert draft.patients[0].fields == (("Возраст", "25 лет"),)
    assert draft.patients[0].assets == ("img_01", "img_02")


def test_unit_personnel_parsing(qtbot: QtBot) -> None:
    """unit_personnel: «150»→150, «»→None, «abc»→None (без падения)."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    editor.unit_personnel_edit.setText("150")
    assert editor.to_draft().unit_personnel == 150
    editor.unit_personnel_edit.setText("")
    assert editor.to_draft().unit_personnel is None
    editor.unit_personnel_edit.setText("abc")
    assert editor.to_draft().unit_personnel is None


def test_unit_personnel_invalid_formats_are_none(qtbot: QtBot) -> None:
    """Пиннинг (W5): «3.5», «1 000», «150abc» молча дают None (контракт не меняем)."""
    editor = CaseEditor()
    qtbot.addWidget(editor)

    for text in ("3.5", "1 000", "150abc"):
        editor.unit_personnel_edit.setText(text)
        assert editor.to_draft().unit_personnel is None
