"""Тесты фабрики build_stage_view — наличие/отсутствие SearchWidget и DocumentWidget."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from educase_core.domain.documents import DocumentOption, DocumentTask
from educase_core.domain.search import KeywordSearch, SearchEntry, SynonymSet
from educase_core.domain.stages import StageClinical, StageContacts
from educase_player.ui.document_widget import DocumentWidget
from educase_player.ui.search_widget import SearchWidget
from educase_player.ui.stage_views import build_stage_view


def _find_search_widget(widget: QWidget) -> SearchWidget | None:
    children: list[SearchWidget] = widget.findChildren(SearchWidget)
    return children[0] if children else None


def _one_entry_search() -> KeywordSearch:
    return KeywordSearch(
        entries=(
            SearchEntry(
                id="e1",
                triggers=SynonymSet(canonical="тест"),
                reveal_text="Результат поиска.",
            ),
        )
    )


def test_stage_with_search_contains_search_widget(qtbot: QtBot) -> None:
    """Этап с непустым search → SearchWidget присутствует."""
    stage = StageClinical(search=_one_entry_search())
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    assert _find_search_widget(view) is not None


def test_stage_without_search_field_no_widget(qtbot: QtBot) -> None:
    """Этап без атрибута search (StageContacts) → SearchWidget отсутствует."""
    stage = StageContacts()
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    assert _find_search_widget(view) is None


def test_stage_with_none_search_no_widget(qtbot: QtBot) -> None:
    """Этап с search=None → SearchWidget не добавляется."""
    stage = StageClinical(search=None)
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    assert _find_search_widget(view) is None


def test_stage_with_empty_entries_no_widget(qtbot: QtBot) -> None:
    """Этап с search.entries=() → SearchWidget не добавляется."""
    stage = StageClinical(search=KeywordSearch(entries=()))
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    assert _find_search_widget(view) is None


def test_stage_with_documents_contains_document_widget(qtbot: QtBot) -> None:
    """Этап с непустым documents → DocumentWidget присутствует для каждого DocumentTask."""
    task = DocumentTask(
        id="t1",
        prompt="Выберите документ",
        options=(DocumentOption(id="opt1", title="Документ А"),),
    )
    stage = StageClinical(documents=(task,))
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    widgets: list[DocumentWidget] = view.findChildren(DocumentWidget)
    assert len(widgets) == 1


def test_stage_without_documents_no_document_widget(qtbot: QtBot) -> None:
    """Этап без documents → DocumentWidget отсутствует."""
    stage = StageClinical(documents=())
    view = build_stage_view(stage)
    qtbot.addWidget(view)

    widgets: list[DocumentWidget] = view.findChildren(DocumentWidget)
    assert len(widgets) == 0
