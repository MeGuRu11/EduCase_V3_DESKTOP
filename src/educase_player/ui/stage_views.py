"""Фабрика виджетов-заглушек для рендереров этапов.

Точка расширения (СЕМ): когда появятся реальные рендереры этапов, фабрика
будет возвращать специфичный для типа виджет вместо заглушки.
"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from educase_core.domain.stages import (
    Stage,
    StageClinical,
    StageEnvironment,
    StageFinal,
    StagePatients,
    StageSes,
)
from educase_player.ui.document_widget import DocumentWidget
from educase_player.ui.search_widget import SearchWidget


def build_stage_view(stage: Stage) -> QWidget:
    """Создать виджет для этапа.

    Содержит заголовок (stage.title), опционально intro, виджет поиска (если есть),
    DocumentWidget на каждый DocumentTask (если есть) и строку-заглушку.
    """
    widget = QWidget()
    layout = QVBoxLayout(widget)

    layout.addWidget(QLabel(stage.title))

    if stage.intro:
        intro_label = QLabel(stage.intro)
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

    if (
        isinstance(stage, (StagePatients, StageClinical, StageSes, StageFinal))
        and stage.search is not None
        and stage.search.entries
    ):
        layout.addWidget(SearchWidget(stage.search))

    if isinstance(stage, (StageClinical, StageEnvironment, StageSes)) and stage.documents:
        for task in stage.documents:
            layout.addWidget(DocumentWidget(task))

    layout.addWidget(QLabel("Рендерер этапа в разработке"))
    layout.addStretch()

    return widget
