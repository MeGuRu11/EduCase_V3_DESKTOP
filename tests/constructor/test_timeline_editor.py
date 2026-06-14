"""Тесты редактора таймлайна Constructor: минимальная высота таблицы и сборка драфта."""
from __future__ import annotations

from pytestqt.qtbot import QtBot

from educase_constructor.ui.timeline_editor import TimelineEditor, TimelineListEditor


def test_timeline_editor_events_table_minimum_height(qtbot: QtBot) -> None:
    """Таблица событий имеет minimumHeight >= 140 — видно несколько строк без скролла."""
    editor = TimelineEditor()
    qtbot.addWidget(editor)
    assert editor.events_table.minimumHeight() >= 140


def test_timeline_editor_add_remove_rows(qtbot: QtBot) -> None:
    """«+ строка» добавляет строку в таблицу, «− строка» удаляет последнюю."""
    editor = TimelineEditor()
    qtbot.addWidget(editor)

    assert editor.events_table.rowCount() == 0
    editor.add_row_button.click()
    editor.add_row_button.click()
    assert editor.events_table.rowCount() == 2
    editor.remove_row_button.click()
    assert editor.events_table.rowCount() == 1
    editor.remove_row_button.click()
    editor.remove_row_button.click()
    assert editor.events_table.rowCount() == 0


def test_timeline_list_editor_add_remove(qtbot: QtBot) -> None:
    """«Добавить таймлайн» и «Удалить последний» управляют списком редакторов."""
    editor = TimelineListEditor()
    qtbot.addWidget(editor)

    assert len(editor.timeline_editors) == 0
    editor.add_timeline_button.click()
    editor.add_timeline_button.click()
    assert len(editor.timeline_editors) == 2
    editor.remove_timeline_button.click()
    assert len(editor.timeline_editors) == 1
