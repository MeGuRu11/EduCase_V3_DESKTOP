"""Тесты редакторов документов Constructor: сборка драфтов поля/шаблона/задания."""
from __future__ import annotations

from pytestqt.qtbot import QtBot

from educase_constructor.ui.document_editor import (
    DocumentListEditor,
    DocumentTaskEditor,
)
from educase_constructor.ui.field_editor import FieldEditor


def test_field_editor_text_rule(qtbot: QtBot) -> None:
    """Тип ``text`` → ключевые слова попадают в ``keywords`` драфта."""
    editor = FieldEditor()
    qtbot.addWidget(editor)

    editor.label_edit.setText("Диагноз")
    editor.type_combo.setCurrentText("text")
    editor.keywords_editor.canonical_edit.setText("сальмонеллёз")
    editor.keywords_editor.synonyms_edit.setText("salmonella, сальмонелла ,")

    draft = editor.to_draft()
    assert draft.label == "Диагноз"
    assert draft.field_type == "text"
    assert draft.required is True
    assert draft.keywords.canonical == "сальмонеллёз"
    assert draft.keywords.synonyms == ("salmonella", "сальмонелла")


def test_field_editor_number_rule(qtbot: QtBot) -> None:
    """Тип ``number`` → значение, допуск и знаки округления как сырые строки."""
    editor = FieldEditor()
    qtbot.addWidget(editor)

    editor.label_edit.setText("Температура")
    editor.type_combo.setCurrentText("number")
    editor.required_checkbox.setChecked(False)
    editor.number_value_edit.setText("38,5")
    editor.tolerance_edit.setText("0,2")
    editor.ndigits_edit.setText("1")

    draft = editor.to_draft()
    assert draft.field_type == "number"
    assert draft.required is False
    assert draft.number_value == "38,5"
    assert draft.number_tolerance == "0,2"
    assert draft.number_ndigits == "1"


def test_field_editor_date_rule(qtbot: QtBot) -> None:
    """Тип ``date`` → ISO-дата попадает в ``date_value``."""
    editor = FieldEditor()
    qtbot.addWidget(editor)

    editor.label_edit.setText("Дата заболевания")
    editor.type_combo.setCurrentText("date")
    editor.date_value_edit.setText("2026-06-11")

    draft = editor.to_draft()
    assert draft.field_type == "date"
    assert draft.date_value == "2026-06-11"


def test_field_editor_choice_rule(qtbot: QtBot) -> None:
    """Тип ``choice`` → варианты и верные значения разбиваются по запятой."""
    editor = FieldEditor()
    qtbot.addWidget(editor)

    editor.label_edit.setText("Тяжесть")
    editor.type_combo.setCurrentText("choice")
    editor.options_edit.setText("лёгкая, средняя, тяжёлая")
    editor.correct_edit.setText("средняя, тяжёлая ,")

    draft = editor.to_draft()
    assert draft.field_type == "choice"
    assert draft.choice_options == ("лёгкая", "средняя", "тяжёлая")
    assert draft.choice_correct == ("средняя", "тяжёлая")


def test_field_editor_type_switches_stack(qtbot: QtBot) -> None:
    """Смена типа в комбобоксе переключает страницу стека правил."""
    editor = FieldEditor()
    qtbot.addWidget(editor)

    editor.type_combo.setCurrentText("text")
    assert editor.rule_stack.currentWidget() is editor.keywords_editor
    editor.type_combo.setCurrentText("choice")
    assert editor.rule_stack.currentIndex() == 3


def test_task_editor_add_remove_options(qtbot: QtBot) -> None:
    """«Добавить вариант» увеличивает число редакторов опций, «Удалить» — уменьшает."""
    editor = DocumentTaskEditor()
    qtbot.addWidget(editor)

    assert len(editor.option_editors) == 0
    editor.add_option_button.click()
    editor.add_option_button.click()
    assert len(editor.option_editors) == 2
    editor.remove_option_button.click()
    assert len(editor.option_editors) == 1
    editor.remove_option_button.click()
    editor.remove_option_button.click()
    assert len(editor.option_editors) == 0


def test_list_editor_add_remove_tasks(qtbot: QtBot) -> None:
    """«Добавить задание» увеличивает число редакторов заданий, «Удалить» — уменьшает."""
    editor = DocumentListEditor()
    qtbot.addWidget(editor)

    assert len(editor.task_editors) == 0
    editor.add_task_button.click()
    editor.add_task_button.click()
    assert len(editor.task_editors) == 2
    editor.remove_task_button.click()
    assert len(editor.task_editors) == 1
    editor.remove_task_button.click()
    editor.remove_task_button.click()
    assert len(editor.task_editors) == 0


def test_list_editor_to_draft_correct_and_decoy(qtbot: QtBot) -> None:
    """Задание с верным вариантом (шаблон + поле) и обманкой → корректные драфты."""
    editor = DocumentListEditor()
    qtbot.addWidget(editor)

    editor.add_task_button.click()
    task = editor.task_editors[0]
    task.prompt_edit.setText("Выберите донесение")

    task.add_option_button.click()
    task.add_option_button.click()
    correct, decoy = task.option_editors

    correct.title_edit.setText("Внеочередное донесение")
    correct.correct_checkbox.setChecked(True)
    correct.template_editor.title_edit.setText("ДМ-4")
    correct.template_editor.add_field_button.click()
    field = correct.template_editor.field_editors[0]
    field.label_edit.setText("Дата")
    field.type_combo.setCurrentText("date")
    field.date_value_edit.setText("2026-06-11")

    decoy.title_edit.setText("Обычная справка")

    drafts = editor.to_draft()
    assert len(drafts) == 1
    task_draft = drafts[0]
    assert task_draft.prompt == "Выберите донесение"
    assert len(task_draft.options) == 2

    correct_draft, decoy_draft = task_draft.options
    assert correct_draft.title == "Внеочередное донесение"
    assert correct_draft.is_correct is True
    assert correct_draft.template.title == "ДМ-4"
    assert len(correct_draft.template.fields) == 1
    assert correct_draft.template.fields[0].field_type == "date"
    assert correct_draft.template.fields[0].date_value == "2026-06-11"

    assert decoy_draft.title == "Обычная справка"
    assert decoy_draft.is_correct is False
